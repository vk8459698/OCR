# Math OCR Output

- Model: `gpt-4o-mini`
- Source: `ocr_2.png`


---

## File: ocr_2.png


### ocr_2.png

1) **Plain Text (cleaned)**

**(11)**  
\[
\int \frac{\tan \sqrt{x} \sec^2 \sqrt{x}}{\sqrt{x}} \, dx
\]  
Let \( \tan \sqrt{x} = t \)  
\[
\sec^2 \sqrt{x} \cdot \frac{1}{2\sqrt{x}} \, dx = dt
\]  
\[
\Rightarrow \sec^2 \sqrt{x} \, dx = 2 \, dt
\]

**(15)**  
\[
\int \frac{\sin^{-1} x}{\sqrt{1 - x^4}} \, dx = \int \frac{\sin^{-1} x}{\sqrt{1 - (x^2)^2}} \, dx
\]  
Let \( \sin^{-1} x = t \)  
\[
\frac{1}{\sqrt{1 - \sin^2 t}} \, dx = dt
\]

**(11)**  
\[
\frac{\sqrt{1 - \sin A}}{\sqrt{1 + \sin A}} = \sec A - \tan A
\]  

**Use: Rationalize**  
\[
\frac{\sqrt{1 - \sin A}}{\sqrt{1 + \sin A}} \cdot \frac{\sqrt{1 - \sin A}}{\sqrt{1 - \sin A}} = \frac{1 - \sin A}{(1 - \sin^2 A)} = \frac{1 - \sin A}{\cos^2 A}
\]  
\[
\Rightarrow \frac{1 - \sin A}{\cos^2 A} = \frac{1}{\cos A} - \frac{\sin A}{\cos^2 A}
\]

2) **LaTeX**
```latex
\textbf{(11)}  
\[
\int \frac{\tan \sqrt{x} \sec^2 \sqrt{x}}{\sqrt{x}} \, dx
\]  
Let \( \tan \sqrt{x} = t \)  
\[
\sec^2 \sqrt{x} \cdot \frac{1}{2\sqrt{x}} \, dx = dt
\]  
\[
\Rightarrow \sec^2 \sqrt{x} \, dx = 2 \, dt
\]

\textbf{(15)}  
\[
\int \frac{\sin^{-1} x}{\sqrt{1 - x^4}} \, dx = \int \frac{\sin^{-1} x}{\sqrt{1 - (x^2)^2}} \, dx
\]  
Let \( \sin^{-1} x = t \)  
\[
\frac{1}{\sqrt{1 - \sin^2 t}} \, dx = dt
\]

\textbf{(11)}  
\[
\frac{\sqrt{1 - \sin A}}{\sqrt{1 + \sin A}} = \sec A - \tan A
\]  

\textbf{Use: Rationalize}  
\[
\frac{\sqrt{1 - \sin A}}{\sqrt{1 + \sin A}} \cdot \frac{\sqrt{1 - \sin A}}{\sqrt{1 - \sin A}} = \frac{1 - \sin A}{(1 - \sin^2 A)} = \frac{1 - \sin A}{\cos^2 A}
\]  
\[
\Rightarrow \frac{1 - \sin A}{\cos^2 A} = \frac{1}{\cos A} - \frac{\sin A}{\cos^2 A}
\]
```

3) **Notes / Ambiguities**
- [unclear: ...]
