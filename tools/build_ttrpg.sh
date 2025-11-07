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
../../tools/compile_latex.sh -f fates-edge-resource-guide.tex -n "Fate's Edge - Comprehensive Resource Guide.pdf" > /dev/null 2>&1|| echo "Resource Guide did not build"

# Compile the Quickstart Guide
# echo "Building Quickstart Guide"
# cd $git_root/ttrpg/quickstart
# ../../tools/compile_latex.sh -f quickstart.tex -n "Fate's Edge - Quickstart Guide.pdf" > /dev/null 2>&1|| echo "Quickstart Guide did not build"

echo "Building Adventures"
cd $git_root/ttrpg/reference/adventures/
../../../tools/compile_latex.sh -f  ashes_of_infernal_accord.tex -n "Fate's Edge - Ashes of the Infernal Accord.pdf" > /dev/null 2>&1|| echo "#1. Did not build"
../../../tools/compile_latex.sh -f  between-knot-and-gate.tex -n "Fate's Edge - Between Knot & Gate.pdf" > /dev/null 2>&1|| echo "#2. Did not build"
../../../tools/compile_latex.sh -f  blood_and_silk_intro_adv.tex -n "Fate's Edge - Blood & Silk Intro Adventure.pdf" > /dev/null 2>&1|| echo "#3. Did not build"
../../../tools/compile_latex.sh -f  crimson-ledger.tex -n "Fate's Edge - The Crimson Ledger of Ecktoria.pdf" > /dev/null 2>&1|| echo "#4. Did not build"
../../../tools/compile_latex.sh -f  hags_panopticon.tex -n "Fate's Edge - The Hag's Panopticon.pdf" > /dev/null 2>&1|| echo "#5. Did not build"
../../../tools/compile_latex.sh -f  mad-cantor-of-frosthollow.tex -n "Fate's Edge - The Mad Cantor of Frosthollow.pdf" > /dev/null 2>&1|| echo "#6. Did not build"
../../../tools/compile_latex.sh -f  of_ways_between.tex -n "Fate's Edge - Of Ways Between.pdf" > /dev/null 2>&1|| echo "#7. Did not build"
../../../tools/compile_latex.sh -f  shadows_of_broken_memory.tex -n "Fate's Edge - Shadows of Broken Memory.pdf" > /dev/null 2>&1|| echo "#8. Did not build"
../../../tools/compile_latex.sh -f  the_recursive_garden.tex -n "Fate's Edge - The Recursive Garden.pdf" > /dev/null 2>&1|| echo "#9. Did not build"
../../../tools/compile_latex.sh -f  the_serpents_coil.tex -n "Fate's Edge - The Serpent's Coil.pdf" > /dev/null 2>&1|| echo "#10. Did not build"
../../../tools/compile_latex.sh -f  whispers_in_the_stacks.tex -n "Fate's Edge - Whispers in the Stacks.pdf" > /dev/null 2>&1|| echo "#11. Did not build"
../../../tools/compile_latex.sh -f  whispers_in_the_tunnels.tex -n "Fate's Edge - Whispers in the Tunnels.pdf" > /dev/null 2>&1|| echo "#12. Did not build"
../../../tools/compile_latex.sh -f  nameless.tex -n "Fate's Edge - The Nameless.pdf" > /dev/null 2>&1|| echo "#13. Did not build"

echo "Building Expansions"
cd $git_root/ttrpg/reference/expansions/
../../../tools/compile_latex.sh -f  horror_campaigns.tex -n "Fate's Edge Expansion - Horror Campaigns.pdf" > /dev/null 2>&1|| echo "#1. Did not build"
../../../tools/compile_latex.sh -f  modern_noir.tex -n "Fate's Edge Expansion - Modern Noir.pdf" > /dev/null 2>&1|| echo "#2. Did not build"
../../../tools/compile_latex.sh -f  dragons-lair.tex -n "Fate's Edge Expansion - Dragon's Lair.pdf" > /dev/null 2>&1|| echo "#3. Did not build"
../../../tools/compile_latex.sh -f  book-of-seven-bell-court.tex -n "Fate's Edge Expansion - The Book of The Seven Bell Court.pdf" > /dev/null 2>&1|| echo "#4. Did not build"


echo "Committing and pushing to git"
cd $git_root/ttrpg/build/
IFS=$'\n';for i in $(ls *.pdf | sed -e 's/\.pdf//g'); do pdftotext -nopgbrk $i.pdf ~/fe_work/$i.txt
done
cd $git_root/ttrpg/build/adventures/
IFS=$'\n';for i in $(ls *.pdf | sed -e 's/\.pdf//g'); do pdftotext -nopgbrk $i.pdf ~/fe_work/$i.txt
done
cd $git_root/ttrpg/build/expansions/
IFS=$'\n';for i in $(ls *.pdf | sed -e 's/\.pdf//g'); do pdftotext -nopgbrk $i.pdf ~/fe_work/$i.txt
done
git add --all
git commit -a -m "PDF Build $(date)"
git push
cd $git_root
git clean -x -f
exit
