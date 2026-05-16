#!/bin/bash

# Fix epic_tier.tex: Correct story-beats reference
sed -i '' 's/\\ref{sec:story-beats-gm}/\\ref{sec:outcome-sb}/g' epic_tier.tex

# Fix gm-currency-free.tex: Correct multiple references
sed -i '' 's/\\ref{sec:boons}/\\ref{sec:boons-gm}/g' gm-currency-free.tex
sed -i '' 's/\\ref{sec:story-beats}/\\ref{sec:outcome-sb}/g' gm-currency-free.tex
sed -i '' 's/\\ref{sec:forming-trust}/\\ref{subsec:helping-trust}/g' gm-currency-free.tex

echo "Label/reference fixes applied successfully!"
