#/usr/bin/env bash

set -e

git_root=$(git rev-parse --show-toplevel)
original_path=$(pwd)

# Compile the SRD
echo "Building SRD"
cd $git_root/ttrpg/srd/
../../tools/compile_latex.sh -f fates-edge-srd-main.tex -n "Fate's Edge - SRD.pdf" > /dev/null 2>&1|| echo "SRD did not build"
cd - > /dev/null 2>&1

# Compile the Player's Guide
echo "Building Player's Guide"
cd $git_root/ttrpg/player_guide
../../tools/compile_latex.sh -f fates_edge_players_guide.tex -n "Fate's Edge - Player's Guide.pdf" > /dev/null 2>&1|| echo "Player's Guide did not build"
cd - > /dev/null 2>&1

# Compile the GM Guide
echo "Building GM Guide"
cd $git_root/ttrpg/gm_guide
../../tools/compile_latex.sh -f gm_guide.tex -n "Fate's Edge - GM Guide.pdf"> /dev/null 2>&1|| echo "GM Guide did not build"
cd - > /dev/null 2>&1

# Compile the Resource Guide
echo "Building Comprehensive Resource Guide"
cd $git_root/ttrpg/reference
../../tools/compile_latex.sh -f quickstart.tex -n "Fate's Edge - Comprehensive Resource Guide.pdf" > /dev/null 2>&1|| echo "Resource Guide did not build"

# Compile the Quickstart Guide
echo "Building Quickstart Guide"
cd $git_root/ttrpg/quickstart
../../tools/compile_latex.sh -f fates-edge-resource-guide.tex -n "Fate's Edge - Quickstart Guide.pdf" > /dev/null 2>&1|| echo "Quickstart Guide did not build"

echo "Committing and pushing to git"
git add --all
git commit -a -m "PDF Build $(date)"
git push
cd $original_path
exit
