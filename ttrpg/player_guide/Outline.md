Here's the complete LaTeX skeleton for your **Fate's Edge Player's Guide** as a modular document. This structure includes:

- A clear **preamble** with required packages and formatting
- A **modular skeleton** that loads chapters via `\input{}`
- A commented-out example of how to organize the modular files
- Design notes for clarity and maintainability

---

### ✅ File: `fates_edge_players_guide.tex`

```latex
% !TeX program = lualatex
% !TeX encoding = UTF-8

\documentclass[11pt,twoside,openany]{book}

% ======================
% Document Setup
% ======================
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{tocloft}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{multicol}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{needspace}

% ======================
% Page Layout
% ======================
\geometry{
  paper=a4paper,
  inner=2.5cm,
  outer=2.5cm,
  top=2.5cm,
  bottom=2.5cm
}

% ======================
% Headers & Footers
% ======================
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\leftmark}
\fancyhead[LO]{\rightmark}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% ======================
% Chapter/Section Styling
% ======================
\titleformat{\chapter}[display]
  {\normalfont\Large\bfseries\centering}
  {\chaptertitlename\ \thechapter}{1pc}
  {\LARGE}

\titleformat{\section}
  {\normalfont\large\bfseries}
  {\thesection}{1em}{}

\titleformat{\subsection}
  {\normalfont\normalsize\bfseries}
  {\thesubsection}{1em}{}

% ======================
% Hyperref Setup
% ======================
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  filecolor=magenta,
  urlcolor=cyan,
  pdftitle={Fate's Edge Player's Guide},
  pdfauthor={Your Name},
  pdfsubject={TTRPG Player's Guide},
  pdfkeywords={TTRPG, Fate's Edge, RPG, Player's Guide}
}

% ======================
% Document Info
% ======================
\title{Fate's Edge Player's Guide}
\author{Modular Lore Team}
\date{\today}

% ======================
% Begin Document
% ======================
\begin{document}

\frontmatter
\maketitle
\tableofcontents

\mainmatter

% ======================
% Modular Chapter Inputs
% ======================

% Core Rules & Mechanics
\input{chapters/chapter_01_intro}
\input{chapters/chapter_02_core_mechanics}
\input{chapters/chapter_03_advancement}
\input{chapters/chapter_04_magic}
\input{chapters/chapter_05_world_interaction}

% Character Creation & Play
\input{chapters/chapter_06_attributes_skills}
\input{chapters/chapter_07_xp_paths}
\input{chapters/chapter_08_talents}
\input{chapters/chapter_09_assets_followers}
\input{chapters/chapter_10_archetypes}

% World & Lore
\input{chapters/chapter_11_world_regions}
\input{chapters/chapter_12_cultures}
\input{chapters/chapter_13_gods_powers}
\input{chapters/chapter_14_languages}
\input{chapters/chapter_15_backgrounds}

% Appendices
\input{chapters/chapter_16_compendium_talents}
\input{chapters/chapter_17_compendium_assets}
\input{chapters/chapter_18_npc_companions}
\input{chapters/chapter_19_deck_generators}
\input{chapters/chapter_20_example_builds}

\end{document}
```

---

### 📁 Suggested Modular File Structure

```
fates_edge_players_guide/
├── fates_edge_players_guide.tex     <-- Main document
├── chapters/
│   ├── chapter_01_intro.tex
│   ├── chapter_02_core_mechanics.tex
│   ├── chapter_03_advancement.tex
│   ├── chapter_04_magic.tex
│   ├── chapter_05_world_interaction.tex
│   ├── chapter_06_attributes_skills.tex
│   ├── chapter_07_xp_paths.tex
│   ├── chapter_08_talents.tex
│   ├── chapter_09_assets_followers.tex
│   ├── chapter_10_archetypes.tex
│   ├── chapter_11_world_regions.tex
│   ├── chapter_12_cultures.tex
│   ├── chapter_13_gods_powers.tex
│   ├── chapter_14_languages.tex
│   ├── chapter_15_backgrounds.tex
│   ├── chapter_16_compendium_talents.tex
│   ├── chapter_17_compendium_assets.tex
│   ├── chapter_18_npc_companions.tex
│   ├── chapter_19_deck_generators.tex
│   └── chapter_20_example_builds.tex
```

---

### ✍️ Notes for Modular Writing

- Each `chapter_xx_*.tex` file should begin with `\chapter{...}` or `\section{...}` as appropriate.
- Use `\needspace{5\baselineskip}` before important sections to prevent widow/orphan lines.
- For tables and lists, prefer `longtable`, `booktabs`, and `enumitem` for clean formatting.
- Keep each file focused: e.g., `chapter_02_core_mechanics.tex` should only cover core resolution, outcome matrix, CP, etc.

