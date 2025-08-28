#!/usr/bin/env python3
"""
Math OCR with OpenAI (Handwritten PDF/Images -> Clean Digital Text/LaTeX)

Features
- Accepts a single PDF/image file OR a folder containing PDFs/images.
- Converts PDFs to page images (via pdf2image) and sends each page to an LLM that can read handwriting.
- Outputs a single Markdown file with per-file and per-page sections.
- Prompts the model to produce both clean text and LaTeX, preserving math where possible.
- Uses Chat Completions "image_url" with base64 data URLs for broad compatibility.
  Falls back to the Responses API automatically if Chat Completions is not available.
Usage
------
1) Install requirements:  pip install -r requirements.txt
   NOTE (Windows): pdf2image needs Poppler. Download Poppler for Windows and add its /bin to PATH.
   Linux/Mac: install poppler-utils via your package manager (apt/brew).
2) Set your environment variable:  export OPENAI_API_KEY=sk-...   (Windows: setx OPENAI_API_KEY ...)
3) Run:
   python ocr_math_llm.py --input /path/to/file_or_folder --out out.md --model gpt-4o-mini
"""

import argparse
import base64
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional

from PIL import Image
from io import BytesIO

# PDF support (requires poppler installed on your system)
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except Exception:
    PDF2IMAGE_AVAILABLE = False

# ---- OpenAI client (new SDK) ----
try:
    from openai import OpenAI
    OPENAI_SDK = "new"
except Exception:
    # Fallback to legacy 'openai' import if needed
    try:
        import openai as openai_legacy
        OPENAI_SDK = "legacy"
    except Exception:
        OPENAI_SDK = None

DEFAULT_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o-mini")

PROMPT_TEMPLATE = """You are a careful OCR assistant for handwritten mathematics.
Goal: Convert the page into clean, editable digital content.

Rules:
- Preserve ALL math faithfully. If confident, render equations in LaTeX.
- Also include a plain-language version if it helps readability.
- Keep original problem numbering & headings.
- Use clear structure and bullet points where helpful.
- If something is ambiguous/illegible, write: [unclear: ...] and move on (do not hallucinate).
- Do not include extraneous commentary—only the extracted content.

Output format (Markdown):
1) **Plain Text (cleaned)**
2) **LaTeX** (use fenced code block: ```latex ... ```)
3) **Notes / Ambiguities** (list any [unclear: ...] items)
"""

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
PDF_EXTS = {".pdf"}

def load_image_bytes(path: Path, max_size: int = 1800) -> Tuple[bytes, str]:
    """
    Load image at 'path', optionally downscale large images to max dimension (px),
    and return (bytes, mime_type).
    """
    img = Image.open(path).convert("RGB")
    # Downscale for token efficiency, keep detail for handwriting
    w, h = img.size
    scale = min(1.0, max_size / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w*scale), int(h*scale)))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), "image/png"

def pdf_to_images(pdf_path: Path, dpi: int = 220) -> List[Image.Image]:
    if not PDF2IMAGE_AVAILABLE:
        raise RuntimeError("pdf2image is not installed or Poppler is missing. See README for installation.")
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    return pages

def pil_image_to_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def as_data_url(img_bytes: bytes, mime: str = "image/png") -> str:
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def call_openai_with_image(prompt: str, img_bytes: bytes, mime: str, model: str, temperature: float = 0.0, max_output_tokens: int = 1800) -> str:
    """
    Primary call path: Chat Completions with 'image_url' (base64 data URL).
    Fallback path: Responses API with input_image if Chat Completions isn't available.
    Returns: text string from the model.
    """
    if OPENAI_SDK is None:
        raise RuntimeError("OpenAI SDK not installed. Please 'pip install openai'.")

    # Initialize clients depending on SDK
    if OPENAI_SDK == "new":
        client = OpenAI()
        # Try Chat Completions first
        data_url = as_data_url(img_bytes, mime)
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_url, "detail": "high"}},
                        ],
                    }
                ],
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to Responses API (if available in your account/region)
            try:
                resp = client.responses.create(
                    model=model,
                    input=[{
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {"type": "input_image", "image_data": base64.b64encode(img_bytes).decode("utf-8"), "mime_type": mime, "detail": "high"}
                        ]
                    }],
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )
                # Prefer the normalized convenience accessor if present
                if hasattr(resp, "output_text") and resp.output_text:
                    return resp.output_text.strip()
                # Else try to dig the text output
                try:
                    return resp.output[0].content[0].text.strip()
                except Exception:
                    return str(resp)
            except Exception as e2:
                raise RuntimeError(f"OpenAI API error. Chat+Responses both failed.\nChat error: {e}\nResponses error: {e2}")
    else:
        # legacy openai library import name
        openai_legacy.api_key = os.environ.get("OPENAI_API_KEY")
        data_url = as_data_url(img_bytes, mime)
        try:
            resp = openai_legacy.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    }
                ],
                temperature=temperature,
            )
            return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI legacy ChatCompletion failed: {e}")

def iter_input_files(root: Path) -> List[Path]:
    if root.is_file():
        return [root]
    files = []
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() in IMAGE_EXTS.union(PDF_EXTS):
            files.append(p)
    return files

def process_file(path: Path, model: str, dpi: int, delay: float) -> List[Tuple[str, str]]:
    """
    Returns list of (page_label, extracted_text)
    """
    ext = path.suffix.lower()
    results = []
    if ext in IMAGE_EXTS:
        img_bytes, mime = load_image_bytes(path)
        text = call_openai_with_image(PROMPT_TEMPLATE, img_bytes, mime, model=model)
        results.append((f"{path.name}", text))
    elif ext in PDF_EXTS:
        pages = pdf_to_images(path, dpi=dpi)
        for i, page in enumerate(pages, start=1):
            img_bytes = pil_image_to_bytes(page)
            text = call_openai_with_image(PROMPT_TEMPLATE, img_bytes, "image/png", model=model)
            results.append((f"{path.name} — page {i}", text))
            if delay > 0:
                time.sleep(delay)
    else:
        print(f"Skipping unsupported: {path}", file=sys.stderr)
    return results

def main():
    ap = argparse.ArgumentParser(description="Handwritten Math OCR via OpenAI Vision")
    ap.add_argument("--input", required=True, help="Path to a PDF/image file or a folder containing PDFs/images")
    ap.add_argument("--out", default="output_math_ocr.md", help="Output markdown file")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI vision-capable model (e.g., gpt-4o-mini, gpt-4o)")
    ap.add_argument("--dpi", type=int, default=220, help="PDF render DPI (higher = more detail, more tokens)")
    ap.add_argument("--delay", type=float, default=0.6, help="Delay (s) between pages to be polite to API/rate limits")
    args = ap.parse_args()

    if "OPENAI_API_KEY" not in os.environ:
        print("ERROR: Please set OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    root = Path(args.input)
    files = iter_input_files(root)
    if not files:
        print("No input PDFs or images found.", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out)
    lines = []
    lines.append(f"# Math OCR Output\n")
    lines.append(f"- Model: `{args.model}`")
    lines.append(f"- Source: `{root}`")
    lines.append("")

    for f in files:
        print(f"Processing: {f}", file=sys.stderr)
        lines.append(f"\n---\n\n## File: {f.name}\n")
        try:
            page_results = process_file(f, model=args.model, dpi=args.dpi, delay=args.delay)
            for page_label, text in page_results:
                lines.append(f"\n### {page_label}\n")
                lines.append(text)
                lines.append("")
        except Exception as e:
            lines.append(f"\n### {f.name}\n**Error:** {e}\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Done. Wrote: {out_path}")

if __name__ == "__main__":
    main()
