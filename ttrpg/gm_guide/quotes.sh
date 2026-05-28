find . -name "*.tex" -type f -exec  sed -i '' -e 's/“/``/g' -e 's/”/''/g; -e 's/‘/`/g; -e ;s/’/'/g' {} +
