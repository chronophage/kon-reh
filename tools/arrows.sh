sed -i '' 's/→/\\rightarrow/g' *.tex

# Optional: Handle other common Unicode arrows if needed
sed -i '' 's/←/\\leftarrow/g' *.tex   # LEFTWARDS ARROW
sed -i '' 's/↔/\\leftrightarrow/g' *.tex # LEFT RIGHT ARROW
sed -i '' 's/⇒/\\Rightarrow/g' *.tex   # RIGHTWARDS DOUBLE ARROW
sed -i '' 's/⇐/\\Leftarrow/g' *.tex   # LEFTWARDS DOUBLE ARROW
sed -i '' 's/⇔/\\Leftrightarrow/g' *.tex # L
