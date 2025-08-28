import pypandoc

# download pandoc if not available
pypandoc.download_pandoc()

# now convert
pypandoc.convert_text(
    open("output_math_ocr.md").read(),
    "docx",
    format="md",
    outputfile="out.docx",
    extra_args=['--standalone']
)
