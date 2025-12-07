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
../../../tools/compile_latex.sh -f  obsidian-convergence.tex -n "Fate's Edge - The Obsidian Convergence.pdf" > /dev/null 2>&1|| echo "#14. Did not build"
../../../tools/compile_latex.sh -f  banner-swap-in-the-wind.tex -n "Fate's Edge - The Banner Swap in the Wind.pdf" > /dev/null 2>&1|| echo "#15. Did not build"
../../../tools/compile_latex.sh -f  crimson-veil.tex -n "Fate's Edge - The Crimson Veil.pdf" > /dev/null 2>&1|| echo "#16. Did not build"
../../../tools/compile_latex.sh -f  silk-and-velvet.tex -n "Fate's Edge - Silk & Velvet.pdf" > /dev/null 2>&1|| echo "#17. Did not build"
../../../tools/compile_latex.sh -f  step-into-sorrow.tex -n "Fate's Edge - Step Into Sorrow.pdf" > /dev/null 2>&1|| echo "#18. Did not build"
../../../tools/compile_latex.sh -f  stone-and-silence.tex -n "Fate's Edge - Stone & Silence.pdf" > /dev/null 2>&1|| echo "#19. Did not build"
../../../tools/compile_latex.sh -f  carnival-of-broken-dreams.tex -n "Fate's Edge - The Carnival of Broken Dreams.pdf" > /dev/null 2>&1|| echo "#20. Did not build"
../../../tools/compile_latex.sh -f memory-merchants-labyrinth.tex -n "Fate's Edge - The Memory Merchant's Labyrinth.pdf" > /dev/null 2>&1|| echo "#21. Did not build"
../../../tools/compile_latex.sh -f gilded-thorn.tex -n "Fate's Edge - The Gilded Thorn.pdf" > /dev/null 2>&1|| echo "#22. Did not build"
../../../tools/compile_latex.sh -f carnival-of-echoes.tex -n "Fate's Edge - The Carnival of Echoes.pdf" > /dev/null 2>&1|| echo "#23. Did not build"
../../../tools/compile_latex.sh -f cursed-caravan.tex -n "Fate's Edge - The Cursed Caravan.pdf" > /dev/null 2>&1|| echo "#23. Did not build"
../../../tools/compile_latex.sh -f dwarven-debt.tex -n "Fate's Edge - The Dwarven Debt.pdf" > /dev/null 2>&1|| echo "#24. Did not build"
../../../tools/compile_latex.sh -f merchant-war.tex -n "Fate's Edge - The Merchant War.pdf" > /dev/null 2>&1|| echo "#25. Did not build"
../../../tools/compile_latex.sh -f mist-walker.tex -n "Fate's Edge - The Mist Walker.pdf" > /dev/null 2>&1|| echo "#26. Did not build"
../../../tools/compile_latex.sh -f usurpers-gambit.tex -n "Fate's Edge - The Usurpers Gambit.pdf" > /dev/null 2>&1|| echo "#27. Did not build"
../../../tools/compile_latex.sh -f into-the-direwood.tex -n "Fate's Edge - Into the Direwood.pdf" > /dev/null 2>&1|| echo "#28. Did not build"
../../../tools/compile_latex.sh -f guest-who-brought-death.tex -n "Fate's Edge - The Guest Who Brought Death.pdf" > /dev/null 2>&1|| echo "#29. Did not build"
../../../tools/compile_latex.sh -f forbidden-library.tex -n "Fate's Edge - The Forbidden Library.pdf" > /dev/null 2>&1|| echo "#30. Did not build"
../../../tools/compile_latex.sh -f ninth-bell.tex -n "Fate's Edge - The Ninth Bell.pdf" > /dev/null 2>&1|| echo "#31. Did not build"


echo "Building Expansions"
cd $git_root/ttrpg/reference/expansions/
../../../tools/compile_latex.sh -f  horror_campaigns.tex -n "Fate's Edge Expansion - Horror Campaigns.pdf" > /dev/null 2>&1|| echo "#1. Did not build"
../../../tools/compile_latex.sh -f  modern_noir.tex -n "Fate's Edge Expansion - Modern Noir.pdf" > /dev/null 2>&1|| echo "#2. Did not build"
../../../tools/compile_latex.sh -f  dragons-lair.tex -n "Fate's Edge Expansion - Dragon's Lair.pdf" > /dev/null 2>&1|| echo "#3. Did not build"
../../../tools/compile_latex.sh -f  book-of-seven-bell-court.tex -n "Fate's Edge Expansion - The Book of The Seven Bell Court.pdf" > /dev/null 2>&1|| echo "#4. Did not build"
../../../tools/compile_latex.sh -f  amaranthine-sea.tex -n "Fate's Edge Expansion - The Amaranthine Sea.pdf" > /dev/null 2>&1|| echo "#5. Did not build"
../../../tools/compile_latex.sh -f  psionics.tex -n "Fate's Edge Expansion - Psionics.pdf" > /dev/null 2>&1|| echo "#6. Did not build"
../../../tools/compile_latex.sh -f  political-intrigue.tex -n "Fate's Edge Expansion - Political Intrigue.pdf" > /dev/null 2>&1|| echo "#7. Did not build"
../../../tools/compile_latex.sh -f  violets-and-stone.tex -n "Fate's Edge Expansion - Violets and Stone.pdf" > /dev/null 2>&1|| echo "#8. Did not build"
# ../../../tools/compile_latex.sh -f  allies-and-adversaries.tex -n "Fate's Edge Expansion - Allies and Adversaries.pdf" > /dev/null 2>&1|| echo "#9. Did not build"
# ../../../tools/compile_latex.sh -f  assets-worldly-patrons.tex -n "Fate's Edge Expansion - Assets and Wordly Patrons.pdf" > /dev/null 2>&1|| echo "#10. Did not build"
../../../tools/compile_latex.sh -f  assets-allies-advesaries.tex -n "Fate's Edge Expansion - Assets, Allies, and Adversaries.pdf" > /dev/null 2>&1|| echo "#10. Did not build"
../../../tools/compile_latex.sh -f  caravans-way-of-silk.tex -n "Fate's Edge Expansion - Caravans: The Way of Silk.pdf" > /dev/null 2>&1|| echo "#11. Did not build"
../../../tools/compile_latex.sh -f  wilds-hinterlands-hearthfires.tex -n "Fate's Edge Expansion - Wilds: Hinterlands and Hearthfires.pdf" > /dev/null 2>&1|| echo "#12. Did not build"
../../../tools/compile_latex.sh -f  linns-mists-iron.tex -n "Fate's Edge Expansion - Linns: Mists and Iron.pdf" > /dev/null 2>&1|| echo "#13. Did not build"
../../../tools/compile_latex.sh -f  sands-of-moon-and-brass.tex -n "Fate's Edge Expansion - Sands of Moon and Brass.pdf" > /dev/null 2>&1|| echo "#14. Did not build"
../../../tools/compile_latex.sh -f  shadows-and-steel.tex -n "Fate's Edge Expansion - Shadows and Steel.pdf" > /dev/null 2>&1|| echo "#15. Did not build"
#../../../tools/compile_latex.sh -f  aeler-stone-breath-ledger.tex -n "Fate's Edge Expansion - Aeler: Stone, Breath, and Ledger.pdf" > /dev/null 2>&1|| echo "#16. Did not build"
../../../tools/compile_latex.sh -f  iron-and-blood.tex -n "Fate's Edge Expansion - Ykrul: Iron & Blood.pdf" > /dev/null 2>&1|| echo "#17. Did not build"
#../../../tools/compile_latex.sh -f  threshold-folk.tex -n "Fate's Edge Expansion - Threshold Folk: Small Peoples & Hidden Realms.pdf" > /dev/null 2>&1|| echo "#18. Did not build"
#../../../tools/compile_latex.sh -f  elves-lethai-root-law-river-courts.tex -n "Fate's Edge Expansion - Lethai: Root-Law and River Courts.pdf" > /dev/null 2>&1|| echo "#18. Did not build"
../../../tools/compile_latex.sh -f  black-banners-condotta-and-crowns.tex -n "Fate's Edge Expansion - Black Banners: Condotta & Crowns.pdf" > /dev/null 2>&1|| echo "#19. Did not build"
../../../tools/compile_latex.sh -f  roads-beneath-the-world.tex -n "Fate's Edge Expansion - Under Realms: Roads Beneath the World.pdf" > /dev/null 2>&1|| echo "#20. Did not build"
../../../tools/compile_latex.sh -f  witches-of-fates-edge.tex -n "Fate's Edge Expansion - Witches of Fate's Edge: Large Cords, Curses, and the Quiet Work of Names.pdf" > /dev/null 2>&1|| echo "#21. Did not build"
../../../tools/compile_latex.sh -f  book-of-talents.tex -n "Fate's Edge Expansion - The Book of Talents.pdf" > /dev/null 2>&1|| echo "#22. Did not build"
../../../tools/compile_latex.sh -f  peoples-and-cultures.tex -n "Fate's Edge Expansion - Peoples and Cultures.pdf" > /dev/null 2>&1|| echo "#23. Did not build"
../../../tools/compile_latex.sh -f  advanced-campaigns.tex -n "Fate's Edge Expansion - Campaigns: Advanced Tools and Reference.pdf" > /dev/null 2>&1|| echo "#23. Did not build"

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
git clean -x -f > /dev/null 2>&1
exit
