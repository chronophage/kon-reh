#/usr/bin/env bash

set -e

original_path=$(pwd)

# Compile the SRD
echo "Building SRD"
cd ../ttrpg/srd/
../../tools/compile_latex.sh -f fates-edge-srd-main.tex -n "Fate's Edge - SRD.pdf" > /dev/null 2>&1|| echo "SRD did not build"
cd - > /dev/null 2>&1

# Compile the Player's Guide
echo "Building Player's Guide"
cd ../ttrpg/player_guide/
../../tools/compile_latex.sh -f fates_edge_players_guide.tex -n "Fate's Edge - Player's Guide.pdf" > /dev/null 2>&1|| echo "Player's Guide did not build"
cd - > /dev/null 2>&1

# Compile the GM Guide
echo "Building GM Guide"
cd ../ttrpg/gm_guide
../../tools/compile_latex.sh -f gm_guide.tex -n "Fate's Edge - GM Guide.pdf"> /dev/null 2>&1|| echo "GM Guide did not build"
cd - > /dev/null 2>&1

# Compile the Resource Guide
echo "Building Comprehensive Resource Guide"
cd ../ttrpg/reference
../../tools/compile_latex.sh -f fates-edge-resource-guide.tex -n "Fate's Edge - Comprehensive Resource Guide.pdf" > /dev/null 2>&1|| echo "Resource Guide did not build"

echo "done"
cd $original_path
exit
