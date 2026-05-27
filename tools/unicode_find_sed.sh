# Run all fixes at once
find . -name "*.tex" -exec sed -i '' 's/≥/$\\geq$/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\xaf/ /g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x94/---/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x93/--/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x98/"/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x99/"/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x9c/"/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\x9d/"/g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xe2\x80\xa6/.../g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\xc2\xa0/ /g' {} \;
find . -name "*.tex" -exec sed -i '' $'s/\"s\ /\'s\ /g' {} \;

# Also fix root .tex files
find . -maxdepth 1 -name "*.tex" -exec sed -i '' 's/≥/$\\geq$/g' {} \;
find . -maxdepth 1 -name "*.tex" -exec sed -i '' $'s/\xe2\x80\xaf/ /g' {} \;

echo "✅ All Unicode replacements complete!"

