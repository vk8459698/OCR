# Math OCR Output

- Model: `gpt-4o-mini`
- Source: `ocr_1.png`


---

## File: ocr_1.png


### ocr_1.png

1) **Plain Text (cleaned)**

2) Given:
   - \( x = \sqrt{a \sin^2 t} \)
   - \( y = \sqrt{a \cos^2 t} \)

   To prove:
   \[
   \frac{dy}{dx} = -\frac{y}{x}
   \]

   Proof:
   - \( x = \sqrt{a \sin^2 t} \)
   - Using chain rule and differentiating w.r.t. \( t \):
     \[
     \frac{dx}{dt} = \frac{1}{2\sqrt{a \sin^2 t}} \cdot \frac{1}{\sqrt{1 - t^2}} \cdot a \sin^t \log a \quad (1)
     \]
   - Similarly,
     \[
     \frac{dy}{dt} = \frac{1}{2\sqrt{a \cos^2 t}} \cdot \frac{1}{-\sqrt{1 - t^2}} \cdot a \cos^t \log a \quad (2)
     \]

   Dividing (1) & (2) we get:
   \[
   \frac{dy}{dt} = \frac{dy}{dx} \cdot \frac{dx}{dt}
   \]

   Therefore,
   \[
   \frac{dy}{dx} = -\frac{a \cos^t}{2\sqrt{a \cos^2 t} \cdot \sqrt{1 - t^2}} \cdot a \sin^t \log a
   \]

   Simplifying:
   \[
   \frac{dy}{dx} = -\frac{a \cos^t}{\sqrt{a \sin^2 t}} = -\frac{y}{x}
   \]

   Hence proved.

2) **LaTeX**
```latex
\text{Given:}
\begin{align*}
x & = \sqrt{a \sin^2 t} \\
y & = \sqrt{a \cos^2 t}
\end{align*}

\text{To prove:}
\[
\frac{dy}{dx} = -\frac{y}{x}
\]

\text{Proof:}
\begin{align*}
x & = \sqrt{a \sin^2 t} \\
\text{Using chain rule and differentiating w.r.t. } t: \\
\frac{dx}{dt} & = \frac{1}{2\sqrt{a \sin^2 t}} \cdot \frac{1}{\sqrt{1 - t^2}} \cdot a \sin^t \log a \quad (1) \\
\text{Similarly,} \\
\frac{dy}{dt} & = \frac{1}{2\sqrt{a \cos^2 t}} \cdot \frac{1}{-\sqrt{1 - t^2}} \cdot a \cos^t \log a \quad (2)
\end{align*}

\text{Dividing (1) \& (2) we get:}
\[
\frac{dy}{dt} = \frac{dy}{dx} \cdot \frac{dx}{dt}
\]

\text{Therefore,}
\[
\frac{dy}{dx} = -\frac{a \cos^t}{2\sqrt{a \cos^2 t} \cdot \sqrt{1 - t^2}} \cdot a \sin^t \log a
\]

\text{Simplifying:}
\[
\frac{dy}{dx} = -\frac{a \cos^t}{\sqrt{a \sin^2 t}} = -\frac{y}{x}
\]

\text{Hence proved.}
```

3) **Notes / Ambiguities**
- [unclear: "Using chain role and differentiating w.r.t. t;"]
- [unclear: "a sin^t log a"]
- [unclear: "a cos^t log a"]
- [unclear: "a cos^t / 2 sqrt{a cos^2 t} sqrt{1 - t^2}"]
