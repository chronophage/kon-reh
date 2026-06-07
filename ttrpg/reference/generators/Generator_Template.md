## 0. Universal Rules (DO THESE):
 - No editorial comments in the body of the text, the comments are fine. This include the template itself or any diagnostic info. PERIOD.
 - No mentioning of the real-world in ways that could break immersion (proper nouns especially, adjectives or general object names and titles are fine) 
 - American English!!!, 
 - No raw Unicode or Markup, use \textit and \textbf instead of *foobar* or **foobar** 
 - Debt and ledger to be more subtextual. Some regions make more sense to have it more prominent than others. Game terms are fine.

---

## 1. Preamble Code (put in your document preamble)

```latex
\usepackage[dvipsnames]{xcolor}   % for coloured suits
\usepackage{amsfonts, amssymb}    % for suit symbols
\usepackage{tcolorbox}
\tcbuselibrary{skins, breakable}

% ----- Card suit and rank formatting -----
% Define suit colours (hearts/diamonds red, spades/clubs black)
\newcommand{\cardSuit}[1]{%
  \ifnum\pdfstrcmp{#1}{\spadesuit}=0 \textcolor{black}{\spadesuit}%
  \else\ifnum\pdfstrcmp{#1}{\heartsuit}=0 \textcolor{red}{\heartsuit}%
  \else\ifnum\pdfstrcmp{#1}{\diamondsuit}=0 \textcolor{red}{\diamondsuit}%
  \else\ifnum\pdfstrcmp{#1}{\clubsuit}=0 \textcolor{black}{\clubsuit}%
  \else #1\fi\fi\fi\fi
}

% Command to print a full card: \card{♠}{A} or \card{\spadesuit}{10}
\newcommand{\card}[2]{%
  \tcbox[colback=white, colframe=gray!50, sharp corners, boxsep=1pt, left=2pt, right=2pt, top=1pt, bottom=1pt]%
    {\cardSuit{#1}\ \textbf{#2}}%
}

% Optional: shortcut commands for each suit
\newcommand{\spadecard}[1]{\card{\spadesuit}{#1}}
\newcommand{\heartcard}[1]{\card{\heartsuit}{#1}}
\newcommand{\clubcard}[1]{\card{\clubsuit}{#1}}
\newcommand{\diamondcard}[1]{\card{\diamondsuit}{#1}}
```

---

## 2. Region Diagnostic Template (LaTeX formatted)

Copy this section into your document. Fill it out for each weak region.

```latex
\section*{Region Diagnostic Template}

\subsection*{\textbf{\textsf{[Region Name]}}}

\paragraph{Current Hook (one sentence)}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[Write it here. If you can't, that's your first problem.]
\vspace{2mm}
\end{minipage}}

\paragraph{Core Conflict (one sentence)}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[What are the players caught between?]
\vspace{2mm}
\end{minipage}}

\paragraph{The One Thing Only This Region Does}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[Mechanical or narrative unique to this region.]
\vspace{2mm}
\end{minipage}}

\paragraph{Interactive Mechanics (player-facing)}
\begin{itemize}
\item[\card{\spadesuit}{1}] Mechanic 1
\item[\card{\heartsuit}{2}] Mechanic 2
\item[\card{\clubsuit}{3}] Mechanic 3
\item[\card{\diamondsuit}{4}] (optional) Mechanic 4
\end{itemize}

\paragraph{Campaign Timers (GM-facing)}
\begin{itemize}
\item \textbf{[Timer name \& size]} – \textit{Advances when:} [conditions]. \textit{At full:} [consequence].
\item \textbf{[Second timer]} – \textit{Advances when:} ... \textit{At full:} ...
\end{itemize}

\paragraph{Faction Triad}
\begin{tabular}{|p{0.2\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|p{0.2\linewidth}|}
\hline
\textbf{Faction} & \textbf{Goal} & \textbf{Method} & \textbf{Why players care} \\
\hline
A & & & \\
\hline
B & & & \\
\hline
C & & & \\
\hline
\end{tabular}

\paragraph{The Price}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[What do players sacrifice/gamble to gain power here?]
\vspace{2mm}
\end{minipage}}

\paragraph{Geography as Constraint}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[How does the land itself limit or enable choices?]
\vspace{2mm}
\end{minipage}}

\paragraph{The Ninth Taboo manifestation}
\framebox[\linewidth][l]{%
\begin{minipage}{\linewidth}
\vspace{2mm}
[How does “never count to nine” rule appear here?]
\vspace{2mm}
\end{minipage}}

\paragraph{Current Weaknesses (honest self-assessment)}
\begin{itemize}
\item Weakness 1
\item Weakness 2
\item Weakness 3
\end{itemize}

\vspace{1cm}
\hrule
\vspace{0.5cm}
\noindent\emph{Use the Design Guide (below) to address identified gaps.}
```

---

## 3. Example Usage

Here is how the card formatting looks when you write:

```latex
The party draws \card{\spadesuit}{7} (place) and \card{\heartsuit}{Q} (actor).
```

It produces a small, clean box: **♠ 7** and **♥ Q** (with heart in red). You can also write `\spadecard{7}`, `\heartcard{Q}`, etc.

---

## 4. Design Guide Summary (Fast Reference)

After diagnosing a region, apply these fixes:

| Weakness | Fix |
|----------|-----|
| Bland hook | Lead with **conflict**, not lore. Name a specific threat or mystery. |
| No campaign timer | Add a visible 4–10 segment timer that ticks on player actions/GM spends. |
| Binary factions | Introduce a **third faction** with overlapping goals (e.g., traders, exiles, heretics). |
| No price for power | Every reward requires a **gamble**: memory loss, Hollow attention, obligation, corruption. |
| Generic geography | Give each terrain a **mechanical tag** (thin air, bell‑lines, walking paths, etc.). |
| Weak Ninth Taboo | Tie the taboo to a **specific local consequence** (cairns vote, wells dry, bridges loop). |

---

## 5. Notes for Mac Homebrew LaTeX

The code uses only standard packages. Install with:

```bash
tlmgr install tcolorbox xcolor
```

All symbols (`\spadesuit`, `\heartsuit`, `\clubsuit`, `\diamondsuit`) are part of `amsfonts`. The `pdfstrcmp` conditional requires `pdftex` or `luatex` – it works with MacTeX. If you encounter issues, replace `\pdfstrcmp` with `\ifx` (simpler) or use the `xstring` package. A robust fallback:

```latex
\newcommand{\cardSuit}[1]{%
  \def\temp{#1}%
  \ifx\temp\spadesuit\relax\textcolor{black}{\spadesuit}\else
  \ifx\temp\heartsuit\relax\textcolor{red}{\heartsuit}\else
  \ifx\temp\diamondsuit\relax\textcolor{red}{\diamondsuit}\else
  \ifx\temp\clubsuit\relax\textcolor{black}{\clubsuit}\else
  #1\fi\fi\fi\fi
}
```
