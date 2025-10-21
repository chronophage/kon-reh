# Kon’reh — Design Tokens & Assets

This package provides color tokens and reference SVGs for pieces (standard + color-blind–safe) and a base board.
Use these in print, web, UI, and LaTeX diagrams.

## Contents
- `tokens.json` — canonical color names/hex for code tools
- `tokens.css` — CSS variables for web
- `tokens.sty` — LaTeX color definitions (xcolor)
- `icons/`
  - `standard/` — R/O/G/B tiles with symbols and patterns
  - `alt-cb/`   — color-blind–safe tiles with patterns + redundant symbols
- `board/`
  - `board_base.svg` — 8×8 diamond board master (SVG)

## Color System (recap)
Standard: Red `#C62828`, Orange `#F57C00`, Green `#2E7D32`, Blue `#1565C0`  
Alt CB-safe: Red→Reddish-Purple `#CC79A7`, Orange→Sky Blue `#56B4E9`, Green→Yellow `#F0E442`, Blue→Teal `#009E73`  
Neutrals: Light `#F4F1EC`, Dark `#7C746A`, Grid `#B8B1A4`

Patterns (20–25% black overprint, inside tile):
- Red = 45° diagonal stripes
- Orange = horizontal lines
- Green = dotted field
- Blue = cross-hatch

Symbols:
- Red = ♦ (nail/diamond)
- Orange = ⬡ (herald hex)
- Green = ▲ (runner triangle)
- Blue = ★ (royal star)

## Usage

### Web / UI
Include `tokens.css` and reference variables:
```css
.tile-red { background: var(--piece-red); color:#fff; }
