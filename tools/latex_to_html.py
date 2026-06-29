#!/usr/bin/env python3
"""
latex_to_html.py – Convert LaTeX documents to clean, web-ready HTML.

Features:
    - Full LaTeX to HTML conversion
    - Table of Contents generation
    - Section splitting (one HTML per section)
    - Dark mode toggle
    - Client-side search with highlighting
    - Print-optimized styles
    - Mobile-responsive layout
    - MathJax support for equations
    - Custom CSS and templates
    - Navigation between sections
    - Clean, semantic HTML output

Usage:
    python latex_to_html.py input.tex --output output.html
    python latex_to_html.py input.tex --title "My Document" --author "Me"
    python latex_to_html.py input.tex --css custom.css --section --toc
    python latex_to_html.py input.tex --dark --search --mathjax
"""

import sys
import os
import re
import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import OrderedDict
from html import escape

# =============================================================================
# Default CSS Styles
# =============================================================================
DEFAULT_CSS = """
/* Fate's Edge HTML Styles — Light Mode */
:root {
    --primary: #c9a94c;
    --primary-dark: #a8893a;
    --primary-light: #e8d89c;
    --bg-body: #f5f0e8;
    --bg-content: #ffffff;
    --bg-nav: #f0ece4;
    --bg-code: #1a1a1a;
    --text-body: #2a2a2a;
    --text-light: #6a6a6a;
    --text-code: #e8e0d4;
    --border: #d0ccc4;
    --shadow: rgba(0,0,0,0.08);
    --font-serif: 'Georgia', 'Times New Roman', serif;
    --font-sans: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    --font-mono: 'Consolas', 'Monaco', 'Courier New', monospace;
    --radius: 8px;
    --transition: 0.3s ease;
}

/* Dark Mode */
[data-theme="dark"] {
    --bg-body: #1a1a1a;
    --bg-content: #242424;
    --bg-nav: #2a2a2a;
    --text-body: #e8e0d4;
    --text-light: #aaa;
    --border: #444;
    --shadow: rgba(0,0,0,0.4);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: var(--font-serif);
    line-height: 1.7;
    color: var(--text-body);
    background: var(--bg-body);
    transition: background var(--transition), color var(--transition);
}

/* Container */
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
    background: var(--bg-content);
    box-shadow: 0 0 30px var(--shadow);
    transition: background var(--transition);
}

/* Header */
.site-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0 1rem;
    border-bottom: 2px solid var(--border);
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.site-header .title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--primary-dark);
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.header-controls button {
    background: var(--bg-nav);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.3rem 0.7rem;
    cursor: pointer;
    font-size: 0.85rem;
    color: var(--text-body);
    transition: all var(--transition);
}

.header-controls button:hover {
    background: var(--primary);
    color: #fff;
}

/* Search */
.search-container {
    margin: 0.5rem 0 1rem;
    display: none;
}
.search-container.active {
    display: block;
}
.search-input {
    width: 100%;
    padding: 0.6rem 1rem;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    background: var(--bg-content);
    color: var(--text-body);
    font-size: 1rem;
    transition: border var(--transition);
}
.search-input:focus {
    outline: none;
    border-color: var(--primary);
}
.search-results {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-light);
}
.search-highlight {
    background: #ffeb3b;
    color: #000;
    padding: 0.1rem 0.2rem;
    border-radius: 2px;
}
[data-theme="dark"] .search-highlight {
    background: #f0c040;
    color: #1a1a1a;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-sans);
    color: var(--text-body);
    margin-top: 1.8rem;
    margin-bottom: 0.8rem;
    font-weight: 600;
    line-height: 1.3;
    transition: color var(--transition);
}

h1 { font-size: 2.4rem; text-align: center; margin-bottom: 1.5rem; }
h2 { font-size: 1.8rem; border-bottom: 2px solid var(--primary); padding-bottom: 0.3rem; }
h3 { font-size: 1.4rem; color: var(--primary-dark); }
h4 { font-size: 1.2rem; font-weight: 600; }
h5, h6 { font-size: 1.1rem; }

p {
    margin-bottom: 1rem;
}

a {
    color: var(--primary-dark);
    text-decoration: none;
    transition: color var(--transition);
}
a:hover {
    text-decoration: underline;
}

/* Tables */
.table-wrapper {
    overflow-x: auto;
    margin: 1.5rem 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
    min-width: 300px;
}
th, td {
    border: 1px solid var(--border);
    padding: 0.5rem 0.8rem;
    text-align: left;
    transition: border var(--transition);
}
th {
    background: var(--bg-nav);
    color: var(--text-body);
    font-weight: 600;
}
tr:nth-child(even) {
    background: var(--bg-body);
}
tr:hover {
    background: var(--primary-light);
    opacity: 0.5;
}
caption {
    caption-side: bottom;
    font-size: 0.85rem;
    color: var(--text-light);
    padding: 0.5rem 0;
}

/* Code blocks */
pre, code {
    font-family: var(--font-mono);
    font-size: 0.9rem;
}
pre {
    background: var(--bg-code);
    color: var(--text-code);
    padding: 1rem 1.2rem;
    border-radius: var(--radius);
    overflow-x: auto;
    margin: 1rem 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}
code {
    background: var(--bg-nav);
    padding: 0.1rem 0.4rem;
    border-radius: 3px;
    color: var(--text-body);
    font-size: 0.85rem;
}
pre code {
    background: transparent;
    padding: 0;
    color: inherit;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid var(--primary);
    padding: 0.5rem 1.5rem;
    margin: 1.5rem 0;
    background: var(--bg-body);
    font-style: italic;
    transition: background var(--transition);
}
blockquote p:last-child {
    margin-bottom: 0;
}

/* Lists */
ul, ol {
    margin: 0.8rem 0 1.2rem 1.8rem;
}
li {
    margin-bottom: 0.3rem;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5rem auto;
    border-radius: 4px;
}

/* Callouts / Infoboxes */
.callout, .note, .warning, .tip, .gm-box {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    border-radius: var(--radius);
    border-left: 4px solid var(--primary);
    transition: background var(--transition);
}
.callout { background: var(--bg-body); }
.note { background: #e8f0f8; border-color: #4a90a9; }
.warning { background: #f8f0e8; border-color: #c94a4a; }
.tip { background: #e8f8e8; border-color: #4a9a4a; }
.gm-box { background: #1a1a2e; border-color: #c9a94c; color: #e8e0d4; }
[data-theme="dark"] .note { background: #1a2a3a; }
[data-theme="dark"] .warning { background: #3a1a1a; }
[data-theme="dark"] .tip { background: #1a3a1a; }
[data-theme="dark"] .gm-box { background: #2a2a3e; }

/* Table of Contents */
.toc {
    background: var(--bg-body);
    padding: 1.5rem 2rem;
    border-radius: var(--radius);
    margin: 1.5rem 0;
    border: 1px solid var(--border);
    transition: background var(--transition);
}
.toc h2 {
    border-bottom: none;
    margin-top: 0;
    font-size: 1.4rem;
}
.toc ul {
    list-style: none;
    padding-left: 0;
    margin: 0.5rem 0;
}
.toc ul ul {
    padding-left: 1.5rem;
}
.toc li {
    margin-bottom: 0.2rem;
}
.toc a {
    color: var(--text-body);
}
.toc a:hover {
    color: var(--primary-dark);
}
.toc .toc-number {
    color: var(--text-light);
    margin-right: 0.5rem;
}

/* Navigation */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin: 1.5rem 0;
    font-size: 0.9rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.nav a {
    color: var(--text-body);
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    transition: all var(--transition);
}
.nav a:hover {
    background: var(--primary);
    color: #fff;
    text-decoration: none;
}
.nav .nav-center {
    color: var(--text-light);
    font-size: 0.8rem;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.85rem;
    color: var(--text-light);
    border-top: 1px solid var(--border);
    padding-top: 1.5rem;
    margin-top: 2.5rem;
    transition: color var(--transition), border var(--transition);
}
.footer a {
    color: var(--primary-dark);
}

/* Section Navigation (section splitting) */
.section-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.section-nav .section-title {
    font-weight: 600;
}
.section-nav .section-links a {
    margin: 0 0.3rem;
    font-size: 0.85rem;
}

/* Dark mode toggle button */
.theme-toggle {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    transition: background var(--transition);
}
.theme-toggle:hover {
    background: var(--bg-nav);
}

/* Scroll to top */
.scroll-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    font-size: 1.4rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity var(--transition);
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 1000;
}
.scroll-top.visible {
    opacity: 1;
}
.scroll-top:hover {
    background: var(--primary-dark);
}

/* Print styles */
@media print {
    body {
        background: white;
        color: black;
    }
    .container {
        box-shadow: none;
        padding: 0.5in;
        max-width: 100%;
    }
    .nav, .section-nav, .header-controls, .scroll-top,
    .search-container, .theme-toggle, .toc {
        display: none !important;
    }
    .toc {
        display: block !important;
        break-after: avoid;
        border: none;
        padding: 0;
    }
    h1, h2, h3, h4, h5, h6 {
        break-after: avoid;
    }
    table, pre, blockquote {
        break-inside: avoid;
    }
    a {
        color: black;
        text-decoration: underline;
    }
}

/* Mobile responsive */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    h1 { font-size: 1.8rem; }
    h2 { font-size: 1.4rem; }
    h3 { font-size: 1.2rem; }
    .nav {
        flex-direction: column;
        text-align: center;
    }
    .site-header {
        flex-direction: column;
        text-align: center;
    }
    .header-controls {
        justify-content: center;
    }
    .toc ul ul {
        padding-left: 1rem;
    }
    table {
        font-size: 0.85rem;
    }
    th, td {
        padding: 0.3rem 0.5rem;
    }
    .scroll-top {
        bottom: 1rem;
        right: 1rem;
        width: 36px;
        height: 36px;
        font-size: 1rem;
    }
}
"""

# =============================================================================
# HTML Template
# =============================================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="author" content="{author}">
    <meta name="generator" content="latex_to_html.py">
    {favicon}
    {mathjax}
    <style>
    {css}
    </style>
    {custom_css}
</head>
<body>
    {scroll_top}

    <div class="container">
        <!-- Header -->
        <header class="site-header">
            <span class="title">{title}</span>
            <div class="header-controls">
                <button class="toc-toggle" onclick="toggleTOC()">📑 TOC</button>
                <button class="search-toggle" onclick="toggleSearch()">🔍 Search</button>
                <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
                    <span id="theme-icon">🌙</span>
                </button>
            </div>
        </header>

        <!-- Search -->
        <div class="search-container" id="search-container">
            <input type="text" class="search-input" id="search-input"
                   placeholder="Search this document..." oninput="performSearch(this.value)">
            <div class="search-results" id="search-results"></div>
        </div>

        <!-- Table of Contents -->
        <div class="toc" id="toc">
            <h2>Table of Contents</h2>
            {toc}
        </div>

        <!-- Section Navigation (if split) -->
        {section_nav}

        <!-- Content -->
        <main id="content">
            {content}
        </main>

        <!-- Navigation -->
        <nav class="nav">
            {nav_prev}
            <span class="nav-center">{nav_center}</span>
            {nav_next}
        </nav>

        <!-- Footer -->
        <footer class="footer">
            <p>{footer_text}</p>
        </footer>
    </div>

    <script>
    // ============================================================
    // Theme Toggle
    // ============================================================
    function toggleTheme() {{
        const html = document.documentElement;
        const icon = document.getElementById('theme-icon');
        const current = html.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        icon.textContent = next === 'dark' ? '☀️' : '🌙';
        localStorage.setItem('fate-edge-theme', next);
    }}

    // Load saved theme
    (function() {{
        const saved = localStorage.getItem('fate-edge-theme');
        if (saved) {{
            document.documentElement.setAttribute('data-theme', saved);
            const icon = document.getElementById('theme-icon');
            icon.textContent = saved === 'dark' ? '☀️' : '🌙';
        }}
    }})();

    // ============================================================
    // Table of Contents Toggle
    // ============================================================
    function toggleTOC() {{
        const toc = document.getElementById('toc');
        toc.style.display = toc.style.display === 'none' ? 'block' : 'none';
    }}

    // ============================================================
    // Search
    // ============================================================
    function toggleSearch() {{
        const container = document.getElementById('search-container');
        container.classList.toggle('active');
        if (container.classList.contains('active')) {{
            document.getElementById('search-input').focus();
        }}
    }}

    function performSearch(query) {{
        const results = document.getElementById('search-results');
        const content = document.getElementById('content');

        // Remove existing highlights
        content.querySelectorAll('.search-highlight').forEach(el => {{
            el.replaceWith(el.textContent);
        }});

        if (!query || query.length < 2) {{
            results.textContent = '';
            return;
        }}

        const text = content.textContent;
        const matches = text.toLowerCase().split(query.toLowerCase()).length - 1;

        if (matches === 0) {{
            results.textContent = 'No results found.';
            return;
        }}

        results.textContent = `Found ${{matches}} match(es).`;

        // Highlight matches in the content
        const walker = document.createTreeWalker(
            content,
            NodeFilter.SHOW_TEXT,
            {{
                acceptNode: function(node) {{
                    const parent = node.parentElement;
                    if (parent && parent.closest && parent.closest('.search-highlight, .toc, .nav, .footer, .section-nav')) {{
                        return NodeFilter.FILTER_REJECT;
                    }}
                    return NodeFilter.FILTER_ACCEPT;
                }}
            }}
        );

        const nodes = [];
        let node;
        while (node = walker.nextNode()) {{
            if (node.textContent.toLowerCase().includes(query.toLowerCase())) {{
                nodes.push(node);
            }}
        }}

        // Create highlighted spans
        nodes.forEach(node => {{
            const text = node.textContent;
            const parent = node.parentNode;
            const span = document.createElement('span');
            span.innerHTML = text.replace(
                new RegExp(escapeRegex(query), 'gi'),
                match => `<span class="search-highlight">${{match}}</span>`
            );
            parent.replaceChild(span, node);
        }});
    }}

    function escapeRegex(str) {{
        return str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
    }}

    // ============================================================
    // Scroll to Top
    // ============================================================
    const scrollBtn = document.getElementById('scroll-top');
    window.addEventListener('scroll', function() {{
        if (window.scrollY > 300) {{
            scrollBtn.classList.add('visible');
        }} else {{
            scrollBtn.classList.remove('visible');
        }}
    }});

    function scrollToTop() {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
    </script>
</body>
</html>
"""

# =============================================================================
# Main Conversion Class
# =============================================================================
class LaTeXToHTML:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.sections = []
        self.toc_items = []
        self.section_count = 0
        self.subsection_count = 0
        self.table_count = 0
        self.current_section = None
        self.section_files = []

    def log(self, msg):
        if self.verbose:
            print(f"[LaTeX2HTML] {msg}")

    def convert(self, tex_content, title=None, author=None):
        """Convert LaTeX content to HTML."""
        self.log("Starting conversion...")

        # Extract title and author if not provided
        if title is None:
            title_match = re.search(r'\\title\{([^}]*)\}', tex_content)
            if title_match:
                title = title_match.group(1)
            else:
                title = "Untitled Document"

        if author is None:
            author_match = re.search(r'\\author\{([^}]*)\}', tex_content)
            if author_match:
                author = author_match.group(1)
            else:
                author = ""

        # Remove LaTeX preamble
        content = re.sub(r'^.*?\\begin\{document\}', '', tex_content, flags=re.DOTALL)
        content = re.sub(r'\\end\{document\}.*$', '', content, flags=re.DOTALL)

        # Process the content
        html = self.process_content(content)

        self.log(f"Conversion complete. Found {len(self.toc_items)} sections.")

        return html, title, author

    def process_content(self, content):
        """Process LaTeX content into HTML."""
        html = []
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                html.append('')
                i += 1
                continue

            # Skip comments
            if line.startswith('%'):
                i += 1
                continue

            # Check for document structure first
            # Sections
            section_match = re.match(r'\\section\{([^}]*)\}', line)
            if section_match:
                title = section_match.group(1)
                self.section_count += 1
                self.subsection_count = 0
                label = self.extract_label(lines, i)
                item_id = label or f"sec-{self.section_count}"
                self.toc_items.append({
                    'level': 1,
                    'number': self.section_count,
                    'title': title,
                    'label': label,
                    'id': item_id
                })
                html.append(f'<h2 id="{item_id}">{self.section_count}. {title}</h2>')
                i += 1
                continue

            # Subsections
            subsection_match = re.match(r'\\subsection\{([^}]*)\}', line)
            if subsection_match:
                title = subsection_match.group(1)
                self.subsection_count += 1
                label = self.extract_label(lines, i)
                item_id = label or f"subsec-{self.section_count}-{self.subsection_count}"
                self.toc_items.append({
                    'level': 2,
                    'number': f"{self.section_count}.{self.subsection_count}",
                    'title': title,
                    'label': label,
                    'id': item_id
                })
                html.append(f'<h3 id="{item_id}">{self.section_count}.{self.subsection_count} {title}</h3>')
                i += 1
                continue

            # Subsubsections
            subsubsection_match = re.match(r'\\subsubsection\{([^}]*)\}', line)
            if subsubsection_match:
                title = subsubsection_match.group(1)
                label = self.extract_label(lines, i)
                item_id = label or f"subsubsec-{self.section_count}-{self.subsection_count}"
                html.append(f'<h4 id="{item_id}">{title}</h4>')
                i += 1
                continue

            # Paragraphs
            para_match = re.match(r'\\paragraph\{([^}]*)\}', line)
            if para_match:
                title = para_match.group(1)
                html.append(f'<h5>{title}</h5>')
                i += 1
                continue

            # Tables
            if line.startswith('\\begin{table}'):
                table_html, i = self.process_table(lines, i)
                html.append(table_html)
                continue

            # Tabular
            if line.startswith('\\begin{tabular}'):
                table_html, i = self.process_tabular(lines, i)
                html.append(table_html)
                continue

            # Lists
            if line.startswith('\\begin{itemize}'):
                list_html, i = self.process_list(lines, i, 'ul')
                html.append(list_html)
                continue

            if line.startswith('\\begin{enumerate}'):
                list_html, i = self.process_list(lines, i, 'ol')
                html.append(list_html)
                continue

            # Descriptions
            if line.startswith('\\begin{description}'):
                list_html, i = self.process_description(lines, i)
                html.append(list_html)
                continue

            # Blockquotes
            if line.startswith('\\begin{quote}') or line.startswith('\\begin{quotation}'):
                quote_html, i = self.process_quote(lines, i)
                html.append(quote_html)
                continue

            # Verbatim
            if line.startswith('\\begin{verbatim}'):
                code_html, i = self.process_verbatim(lines, i)
                html.append(code_html)
                continue

            # Center
            if line.startswith('\\begin{center}'):
                center_html, i = self.process_center(lines, i)
                html.append(center_html)
                continue

            # Custom environments
            if line.startswith('\\begin{callout}'):
                callout_html, i = self.process_callout(lines, i, 'callout')
                html.append(callout_html)
                continue

            if line.startswith('\\begin{note}'):
                callout_html, i = self.process_callout(lines, i, 'note')
                html.append(callout_html)
                continue

            if line.startswith('\\begin{warning}'):
                callout_html, i = self.process_callout(lines, i, 'warning')
                html.append(callout_html)
                continue

            if line.startswith('\\begin{tip}'):
                callout_html, i = self.process_callout(lines, i, 'tip')
                html.append(callout_html)
                continue

            if line.startswith('\\begin{gm}'):
                callout_html, i = self.process_callout(lines, i, 'gm-box')
                html.append(callout_html)
                continue

            # Inline commands
            line = self.process_inline(line)
            html.append(line)
            i += 1

        return '\n'.join(html)

    def extract_label(self, lines, idx):
        """Extract label from following lines."""
        for j in range(idx, min(idx + 5, len(lines))):
            label_match = re.search(r'\\label\{([^}]*)\}', lines[j])
            if label_match:
                return label_match.group(1)
        return None

    def process_inline(self, text):
        """Process inline LaTeX commands."""
        # Bold
        text = re.sub(r'\\textbf\{([^}]*)\}', r'<strong>\1</strong>', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

        # Italic
        text = re.sub(r'\\textit\{([^}]*)\}', r'<em>\1</em>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

        # Monospace
        text = re.sub(r'\\texttt\{([^}]*)\}', r'<code>\1</code>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

        # Small caps
        text = re.sub(r'\\textsc\{([^}]*)\}', r'<span style="font-variant:small-caps">\1</span>', text)

        # Links
        text = re.sub(r'\\url\{([^}]*)\}', r'<a href="\1">\1</a>', text)
        text = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'<a href="\1">\2</a>', text)

        # Images
        text = re.sub(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}', r'<img src="\1" alt="Image" loading="lazy">', text)

        # Footnotes
        text = re.sub(r'\\footnote\{([^}]*)\}', r'<sup class="footnote">[\1]</sup>', text)

        # Em dashes
        text = text.replace('---', '&mdash;')
        text = text.replace('--', '&ndash;')

        # Quotes
        text = re.sub(r'``([^'']*)''', r'&ldquo;\1&rdquo;', text)
        text = re.sub(r'`([^'']*)''', r'&lsquo;\1&rsquo;', text)

        # Accents (basic)
        text = re.sub(r"\\'\{([^}]*)\}", r'\1', text)
        text = re.sub(r"\\`\{([^}]*)\}", r'\1', text)
        text = re.sub(r"\\^\{([^}]*)\}", r'\1', text)
        text = re.sub(r'\\"\{([^}]*)\}', r'\1', text)

        # Math mode (basic - let MathJax handle it)
        text = re.sub(r'\$\$([^$]+)\$\$', r'\\[\1\\]', text)
        text = re.sub(r'\$([^$]+)\$', r'\\(\1\\)', text)

        # Remove remaining commands
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+', '', text)

        return text

    def process_table(self, lines, idx):
        """Process LaTeX table environment."""
        html = ['<div class="table-wrapper">']

        # Get caption
        caption = ''
        for j in range(idx, min(idx + 15, len(lines))):
            cap_match = re.search(r'\\caption\{([^}]*)\}', lines[j])
            if cap_match:
                caption = self.process_inline(cap_match.group(1))
                break

        # Find tabular content
        tabular_start = None
        for j in range(idx, min(idx + 20, len(lines))):
            if '\\begin{tabular}' in lines[j]:
                tabular_start = j
                break

        if tabular_start is not None:
            html.append('<table>')
            if caption:
                html.append(f'<caption>{caption}</caption>')
            table_html, _ = self.process_tabular(lines, tabular_start, include_table_tags=False)
            html.append(table_html)
            html.append('</table>')

        # Skip to end of table
        end_idx = idx
        for j in range(idx, len(lines)):
            if '\\end{table}' in lines[j]:
                end_idx = j
                break

        html.append('</div>')
        return '\n'.join(html), end_idx

    def process_tabular(self, lines, idx, include_table_tags=True):
        """Process LaTeX tabular environment."""
        html = []

        # Parse column specification
        spec_match = re.search(r'\\begin\{tabular\}\{([^}]*)\}', lines[idx])
        specs = spec_match.group(1) if spec_match else ''

        if include_table_tags:
            html.append('<table>')

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if '\\end{tabular}' in line:
                break

            if '\\hline' in line or '\\midrule' in line or '\\toprule' in line or '\\bottomrule' in line:
                i += 1
                continue

            # Process row
            if '&' in line or '\\\\' in line:
                row = line.replace('\\\\', '')
                cells = row.split('&')

                # Check if header row (contains \\textbf or \\bf)
                is_header = any(r'\\textbf' in cell or '\\bf' in cell for cell in cells)

                tag = 'th' if is_header else 'td'
                html.append('<tr>')
                for cell in cells:
                    cell_content = self.process_inline(cell.strip())
                    # Handle multi-column
                    if '\\multicolumn' in cell_content:
                        # Simple multi-column handling
                        mc_match = re.search(r'\\multicolumn\{(\d+)\}\{([^}]*)\}\{([^}]*)\}', cell_content)
                        if mc_match:
                            colspan = int(mc_match.group(1))
                            content = self.process_inline(mc_match.group(3))
                            html.append(f'<{tag} colspan="{colspan}">{content}</{tag}>')
                            continue
                    html.append(f'<{tag}>{cell_content}</{tag}>')
                html.append('</tr>')

            i += 1

        if include_table_tags:
            html.append('</table>')

        return '\n'.join(html), i

    def process_list(self, lines, idx, list_type):
        """Process LaTeX list environment."""
        html = []
        html.append(f'<{list_type}>')

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('\\end{itemize}') or line.startswith('\\end{enumerate}'):
                break

            if line.startswith('\\item'):
                item_content = re.sub(r'^\\item\s*', '', line)
                # Handle nested lists in item
                if '\\begin{itemize}' in item_content or '\\begin{enumerate}' in item_content:
                    # Complex item - will be handled by recursion if nested
                    pass
                html.append(f'<li>{self.process_inline(item_content)}</li>')

            i += 1

        html.append(f'</{list_type}>')
        return '\n'.join(html), i

    def process_description(self, lines, idx):
        """Process LaTeX description environment."""
        html = ['<dl>']

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if '\\end{description}' in line:
                break

            if line.startswith('\\item'):
                item_match = re.search(r'\\item\[([^\]]*)\]\s*(.*)', line)
                if item_match:
                    term = self.process_inline(item_match.group(1))
                    desc = self.process_inline(item_match.group(2))
                    html.append(f'<dt>{term}</dt>')
                    html.append(f'<dd>{desc}</dd>')
                else:
                    item_content = re.sub(r'^\\item\s*', '', line)
                    html.append(f'<dt>{self.process_inline(item_content)}</dt>')

            i += 1

        html.append('</dl>')
        return '\n'.join(html), i

    def process_quote(self, lines, idx):
        """Process LaTeX quote/quotation environment."""
        html = ['<blockquote>']

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if '\\end{quote}' in line or '\\end{quotation}' in line:
                break

            if line:
                html.append(f'<p>{self.process_inline(line)}</p>')

            i += 1

        html.append('</blockquote>')
        return '\n'.join(html), i

    def process_verbatim(self, lines, idx):
        """Process LaTeX verbatim environment."""
        html = ['<pre>']

        i = idx + 1
        while i < len(lines):
            line = lines[i]

            if '\\end{verbatim}' in line:
                break

            # Escape HTML entities
            line = escape(line)
            html.append(line)

            i += 1

        html.append('</pre>')
        return '\n'.join(html), i

    def process_center(self, lines, idx):
        """Process LaTeX center environment."""
        html = ['<div style="text-align:center;">']

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if '\\end{center}' in line:
                break

            if line:
                html.append(f'<p>{self.process_inline(line)}</p>')

            i += 1

        html.append('</div>')
        return '\n'.join(html), i

    def process_callout(self, lines, idx, class_name):
        """Process custom callout environments."""
        html = [f'<div class="{class_name}">']

        i = idx + 1
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith(f'\\end{{{class_name}}}') or '\\end{callout}' in line or \
               '\\end{note}' in line or '\\end{warning}' in line or '\\end{tip}' in line or \
               '\\end{gm}' in line:
                break

            if line:
                html.append(f'<p>{self.process_inline(line)}</p>')

            i += 1

        html.append('</div>')
        return '\n'.join(html), i

    def generate_toc_html(self):
        """Generate table of contents HTML."""
        if not self.toc_items:
            return '<p>No sections found.</p>'

        html = ['<ul>']
        current_level = 1

        for item in self.toc_items:
            level = item['level']
            number = item.get('number', '')
            title = item['title']
            item_id = item.get('id', '')

            # Close lists
            while level < current_level:
                html.append('</ul>')
                current_level -= 1

            # Open new lists
            while level > current_level:
                html.append('<ul>')
                current_level += 1

            display = f'<span class="toc-number">{number}</span>{title}' if number else title
            href = f'#{item_id}' if item_id else f'#{re.sub(r"[^a-zA-Z0-9]", "-", title.lower())}'
            html.append(f'<li><a href="{href}">{display}</a></li>')

        while current_level > 1:
            html.append('</ul>')
            current_level -= 1

        html.append('</ul>')
        return '\n'.join(html)


# =============================================================================
# Section Splitting
# =============================================================================
def split_sections(html_content, toc_items, title, author, output_dir, base_name,
                   lang='en', template=HTML_TEMPLATE, css=DEFAULT_CSS,
                   custom_css='', favicon='', mathjax=''):
    """Split HTML into separate files per section."""
    section_files = []

    # Extract content between headers
    sections = []
    current_section = None
    lines = html_content.split('\n')
    in_content = False

    for line in lines:
        # Detect section headers
        header_match = re.search(r'<h2 id="([^"]*)">(.*?)</h2>', line)
        if header_match:
            if current_section is not None:
                sections.append(current_section)
            current_section = {
                'id': header_match.group(1),
                'title': header_match.group(2),
                'content': []
            }
            continue

        if current_section is not None:
            current_section['content'].append(line)

    if current_section is not None:
        sections.append(current_section)

    # If no sections, just return the original
    if len(sections) <= 1:
        return [{
            'filename': f'{base_name}.html',
            'title': title,
            'content': html_content
        }]

    # Generate individual section files
    total = len(sections)
    for idx, section in enumerate(sections):
        prev_idx = idx - 1
        next_idx = idx + 1

        nav_prev = f'<a href="{base_name}-{prev_idx+1:02d}.html">← Previous</a>' if prev_idx >= 0 else '<span></span>'
        nav_next = f'<a href="{base_name}-{next_idx+1:02d}.html">Next →</a>' if next_idx < total else '<span></span>'

        section_title = f"{section['title']} — {title}"

        # Build section HTML
        content = '<main id="content">'
        # Add the section header back
        content += f'<h2 id="{section["id"]}">{section["title"]}</h2>'
        content += '\n'.join(section['content'])
        content += '</main>'

        # Build full page
        filename = f'{base_name}-{idx+1:02d}.html'

        # Build TOC for this section (just the current section)
        toc_html = '<ul>'
        for item in toc_items:
            if item['id'] == section['id']:
                toc_html += f'<li><a href="{filename}#{item["id"]}">{item.get("number", "")} {item["title"]}</a></li>'
        toc_html += '</ul>'

        full_html = template.format(
            lang=lang,
            theme='light',
            title=section_title,
            description=f"{section_title} — Section {idx+1} of {total}",
            author=author,
            favicon=favicon,
            mathjax=mathjax,
            css=css,
            custom_css=custom_css,
            toc=toc_html,
            section_nav=f'''<div class="section-nav">
                <span class="section-title">Section {idx+1} of {total}</span>
                <span class="section-links">
                    <a href="{base_name}.html">Full Document</a>
                    {"<a href='" + base_name + "-" + str(prev_idx+1).zfill(2) + ".html'>← Prev</a>" if prev_idx >= 0 else ""}
                    {"<a href='" + base_name + "-" + str(next_idx+1).zfill(2) + ".html'>Next →</a>" if next_idx < total else ""}
                </span>
            </div>''',
            content=content,
            nav_prev=nav_prev,
            nav_next=nav_next,
            nav_center=f'Section {idx+1} of {total}',
            footer_text=f'Generated from LaTeX source on {datetime.now().strftime("%Y-%m-%d")}'
        )

        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        section_files.append({
            'filename': filename,
            'title': section_title,
            'path': output_path
        })

    return section_files


# =============================================================================
# Main Function
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Convert LaTeX documents to clean, web-ready HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python latex_to_html.py mydoc.tex
  python latex_to_html.py mydoc.tex --title "My Document" --author "Me"
  python latex_to_html.py mydoc.tex --section --toc --dark
  python latex_to_html.py mydoc.tex --css custom.css --output index.html
  python latex_to_html.py mydoc.tex --mathjax --search
        """
    )

    parser.add_argument('input', help='Input LaTeX file')
    parser.add_argument('--output', '-o', help='Output HTML file')
    parser.add_argument('--title', help='Document title')
    parser.add_argument('--author', help='Document author')
    parser.add_argument('--css', help='Custom CSS file to include')
    parser.add_argument('--section', action='store_true',
                        help='Split output into separate HTML files per section')
    parser.add_argument('--toc', action='store_true',
                        help='Generate a table of contents')
    parser.add_argument('--no-nav', action='store_true',
                        help='Disable navigation links')
    parser.add_argument('--dark', action='store_true',
                        help='Default to dark mode')
    parser.add_argument('--search', action='store_true',
                        help='Enable search functionality')
    parser.add_argument('--mathjax', action='store_true',
                        help='Enable MathJax for equations')
    parser.add_argument('--favicon', help='Path to favicon file')
    parser.add_argument('--lang', default='en', help='Language code')
    parser.add_argument('--template', help='Custom HTML template file')
    parser.add_argument('--output-dir', '-d', help='Output directory for section files')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output')

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"❌ File not found: {args.input}")

    with open(input_path, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # Determine output filename
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.html')

    base_name = output_path.stem

    # Get title from LaTeX if not provided
    title = args.title
    if title is None:
        title_match = re.search(r'\\title\{([^}]*)\}', tex_content)
        if title_match:
            title = title_match.group(1)
        else:
            title = input_path.stem.replace('_', ' ').title()

    # Get author from LaTeX if not provided
    author = args.author
    if author is None:
        author_match = re.search(r'\\author\{([^}]*)\}', tex_content)
        if author_match:
            author = author_match.group(1)
        else:
            author = ''

    # Read custom CSS
    custom_css = ''
    if args.css:
        css_path = Path(args.css)
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                custom_css = f'<style>\n{f.read()}\n</style>'

    # Read custom template
    template = HTML_TEMPLATE
    if args.template:
        template_path = Path(args.template)
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

    # Favicon
    favicon = ''
    if args.favicon:
        favicon = f'<link rel="icon" type="image/x-icon" href="{args.favicon}">'

    # MathJax
    mathjax = ''
    if args.mathjax:
        mathjax = '''<script>
window.MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\(', '\\)']] },
    svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>'''

    # Theme
    theme = 'dark' if args.dark else 'light'

    # Convert
    converter = LaTeXToHTML(verbose=args.verbose)
    html_content, doc_title, doc_author = converter.convert(
        tex_content, title, author
    )

    # Generate TOC
    toc_html = converter.generate_toc_html() if args.toc else ''

    # Build navigation
    nav_prev = '<span></span>'
    nav_next = '<span></span>'
    nav_center = ''

    if not args.no_nav and not args.section:
        # Add navigation only if not splitting sections
        nav_prev = '<a href="#">← Previous</a>'
        nav_next = '<a href="#">Next →</a>'
        nav_center = ''

    # Determine output directory
    if args.section and args.output_dir:
        output_dir = Path(args.output_dir)
    elif args.section:
        output_dir = input_path.parent / f"{base_name}_sections"
    else:
        output_dir = output_path.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    # If section splitting, generate multiple files
    if args.section:
        print(f"📑 Splitting into sections...")
        section_files = split_sections(
            html_content, converter.toc_items, doc_title, doc_author,
            output_dir, base_name, args.lang, template,
            DEFAULT_CSS, custom_css, favicon, mathjax
        )

        print(f"✅ Generated {len(section_files)} section files in: {output_dir}")
        print(f"   Index: {output_dir / f'{base_name}.html'}")

        # Also generate a master index file
        master_content = f'''<!DOCTYPE html>
<html lang="{args.lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{doc_title} — Index</title>
    <style>
    {DEFAULT_CSS}
    </style>
    {custom_css}
</head>
<body>
    <div class="container">
        <h1>{doc_title}</h1>
        <p style="text-align:center; color:var(--text-light);">Click a section to read</p>
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
'''
        for idx, sf in enumerate(section_files):
            num = idx + 1
            master_content += f'<li><a href="{sf["filename"]}">Section {num:02d}: {sf["title"]}</a></li>\n'

        master_content += f'''</ul>
        </div>
        <div style="text-align:center; margin-top:2rem;">
            <p style="font-size:0.9rem; color:var(--text-light);">
                {len(section_files)} sections total &bull; Generated on {datetime.now().strftime("%Y-%m-%d")}
            </p>
        </div>
        <footer class="footer">
            <p>{doc_author}</p>
        </footer>
    </div>
</body>
</html>'''

        index_path = output_dir / f'{base_name}.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(master_content)

        return

    # Build the full HTML for single file
    scroll_top = '''<button class="scroll-top" id="scroll-top" onclick="scrollToTop()" aria-label="Scroll to top">↑</button>'''

    full_html = template.format(
        lang=args.lang,
        theme=theme,
        title=doc_title,
        description=f"{doc_title} — HTML version",
        author=doc_author,
        favicon=favicon,
        mathjax=mathjax,
        css=DEFAULT_CSS,
        custom_css=custom_css,
        scroll_top=scroll_top,
        toc=toc_html,
        section_nav='',
        content=html_content,
        nav_prev=nav_prev,
        nav_next=nav_next,
        nav_center=nav_center,
        footer_text=f'Generated from {input_path.name} on {datetime.now().strftime("%Y-%m-%d")}'
    )

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ HTML written to: {output_path}")
    if args.toc:
        print(f"📑 Table of contents included")
    if args.dark:
        print(f"🌙 Dark mode enabled by default")
    if args.mathjax:
        print(f"📐 MathJax enabled for equations")
    if args.search:
        print(f"🔍 Search enabled")


if __name__ == '__main__':
    main()
