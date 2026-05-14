for f in sections/*.tex; do
  open=$(grep -c 'begin{tcolorbox}' "$f" 2>/dev/null || echo 0)
  close=$(grep -c 'end{tcolorbox}' "$f" 2>/dev/null || echo 0)
  if [ "$open" != "$close" ]; then
    echo "❌ $f: $open open, $close close"
  else
    echo "✅ $f: $open open, $close close"
  fi
done

