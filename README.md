# Kon’reh

> An original abstract strategy game. This repo hosts the **rules (LaTeX)**, **lore/Concordance**, and a **Python rules engine** suitable for analysis, bots, and tools.

[![CI: Python](https://img.shields.io/github/actions/workflow/status/chronophage/kon-reh/ci-python.yml?label=python%20ci)](#)
[![CI: LaTeX](https://img.shields.io/github/actions/workflow/status/chronophage/kon-reh/ci-latex.yml?label=latex%20pdf)](#)
[![License: MIT + CC BY-NC-SA 4.0](https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY--NC--SA%204.0-blue)](#license)

## What’s here

- **/rules** — the core rulebook (`rulebook.tex`) with diagrams (TikZ).
- **/concordance** — lore expansion: schools, historical documents, meta notes.
- **/engine** — Python game engine (legal movegen, ZoC, Cross timers, Seed, Reforge, Crown Stagger).
- **/examples** — annotated master game, openings, notation samples.

## Quick start (engine)

```bash
cd engine
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .                                   # installs as editable package
pytest
python -c "import konreh, sys; print('Konreh ready')"
