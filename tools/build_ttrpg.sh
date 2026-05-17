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
 echo "Building Quickstart Guide"
 cd $git_root/ttrpg/quickstart
 ../../tools/compile_latex.sh -f quickstart.tex -n "Fate's Edge - Quickstart Guide.pdf" > /dev/null 2>&1|| echo "Quickstart Guide did not build"

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
	../../../tools/compile_latex.sh -f city-of-forgetting.tex -n "Fate's Edge - The City Of Forgetting.pdf" > /dev/null 2>&1|| echo "#31. Did not build"
	../../../tools/compile_latex.sh -f clockwork-cathedral.tex -n "Fate's Edge - The Clockwork Cathedral.pdf" > /dev/null 2>&1|| echo "#32. Did not build"
	../../../tools/compile_latex.sh -f shifting-city-of-chantelune.tex -n "Fate's Edge - The Shifting City of Chantelune.pdf" > /dev/null 2>&1|| echo "#33. Did not build"
	../../../tools/compile_latex.sh -f silent-court.tex -n "Fate's Edge - The Silent Court.pdf" > /dev/null 2>&1|| echo "#34. Did not build"
	../../../tools/compile_latex.sh -f forge-of-souls.tex -n "Fate's Edge - The Forge of Souls.pdf" > /dev/null 2>&1|| echo "#35. Did not build"
	../../../tools/compile_latex.sh -f last-light-of-everflame.tex -n "Fate's Edge - The Last Light of the Everflame, The Lampers vs. The Temple of Light.pdf" > /dev/null 2>&1|| echo "#36. Did not build"
	../../../tools/compile_latex.sh -f truth-that-cannot-be-told.tex -n "Fate's Edge - The Truth That Cannot Be Told.pdf" > /dev/null 2>&1|| echo "#37. Did not build"
	../../../tools/compile_latex.sh -f iron-crucible.tex -n "Fate's Edge - The Iron Crucible.pdf" > /dev/null 2>&1|| echo "#38. Did not build"
	../../../tools/compile_latex.sh -f gilded-chain.tex -n "Fate's Edge - The Gilded Chain.pdf" > /dev/null 2>&1|| echo "#39. Did not build"
        ../../../tools/compile_latex.sh -f beyond-millhaven.tex -n "Fate's Edge - Blood and Silk II, Beyond Millhaven.pdf" 2>&1|| echo "#40. Did not build"
	../../../tools/compile_latex.sh -f brass_gate_milhavenIII.tex -n "Fate's Edge - Blood and Silk III, The Brass Gate.pdf" > /dev/null 2>&1|| echo "#41. Did not build"
	../../../tools/compile_latex.sh -f grumbling_vault.tex -n "Fate's Edge - The Grumbling Vault.pdf" > /dev/null 2>&1|| echo "#42. Did not build"
	../../../tools/compile_latex.sh -f tithe_forgotten_faces.tex -n "Fate's Edge - The Tithe of Forgotten Faces.pdf" > /dev/null 2>&1|| echo "#43. Did not build"
	../../../tools/compile_latex.sh -f vow_of_broken_glass.tex -n "Fate's Edge - The Vow of Broken Glass.pdf" > /dev/null 2>&1|| echo "#44. Did not build"

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
	../../../tools/compile_latex.sh -f  assets-allies-advesaries.tex -n "Fate's Edge Expansion - Assets, Allies, and Adversaries.pdf" > /dev/null 2>&1|| echo "#10. Did not build"
	../../../tools/compile_latex.sh -f  caravans-way-of-silk.tex -n "Fate's Edge Expansion - Caravans, The Way of Silk.pdf" > /dev/null 2>&1|| echo "#11. Did not build"
	../../../tools/compile_latex.sh -f  wilds-hinterlands-hearthfires.tex -n "Fate's Edge Expansion - Wilds, Hinterlands and Hearthfires.pdf" > /dev/null 2>&1|| echo "#12. Did not build"
	../../../tools/compile_latex.sh -f  linns-mists-iron.tex -n "Fate's Edge Expansion - Linns, Mists and Iron.pdf" > /dev/null 2>&1|| echo "#13. Did not build"
	../../../tools/compile_latex.sh -f  sands-of-moon-and-brass.tex -n "Fate's Edge Expansion - Sands of Moon and Brass.pdf" > /dev/null 2>&1|| echo "#14. Did not build"
	../../../tools/compile_latex.sh -f  shadows-and-steel.tex -n "Fate's Edge Expansion - Shadows and Steel.pdf" > /dev/null 2>&1|| echo "#15. Did not build"
	../../../tools/compile_latex.sh -f  iron-and-blood.tex -n "Fate's Edge Expansion - Ykrul, Iron & Blood.pdf" > /dev/null 2>&1|| echo "#17. Did not build"
	../../../tools/compile_latex.sh -f  black-banners-condotta-and-crowns.tex -n "Fate's Edge Expansion - Black Banners, Condotta & Crowns.pdf" > /dev/null 2>&1|| echo "#19. Did not build"
	../../../tools/compile_latex.sh -f  roads-beneath-the-world.tex -n "Fate's Edge Expansion - Under Realms, Roads Beneath the World.pdf" > /dev/null 2>&1|| echo "#20. Did not build"
	../../../tools/compile_latex.sh -f  witches-of-fates-edge.tex -n "Fate's Edge Expansion - Witches of Fate's Edge, Large Cords, Curses, and the Quiet Work of Names.pdf" > /dev/null 2>&1|| echo "#21. Did not build"
	../../../tools/compile_latex.sh -f  book-of-talents.tex -n "Fate's Edge Expansion - The Book of Talents.pdf" > /dev/null 2>&1|| echo "#22. Did not build"
	../../../tools/compile_latex.sh -f  peoples-and-cultures.tex -n "Fate's Edge Expansion - Peoples and Cultures.pdf" > /dev/null 2>&1|| echo "#23. Did not build"
	../../../tools/compile_latex.sh -f  advanced-campaigns.tex -n "Fate's Edge Expansion - Campaigns, Advanced Tools and Reference.pdf" > /dev/null 2>&1|| echo "#24. Did not build"
	../../../tools/compile_latex.sh -f  book-of-shadows.tex -n "Fate's Edge Expansion - The Lantern War of Shadows.pdf" > /dev/null 2>&1|| echo "#25. Did not build"
	../../../tools/compile_latex.sh -f  witchcraft.tex -n "Fate's Edge Expansion - The Book of Shadows.pdf" > /dev/null 2>&1|| echo "#26. Did not build"
	../../../tools/compile_latex.sh -f tactics.tex -n "Fate's Edge Expansion - Advanced Tactics and Grid Combat.pdf" > /dev/null 2>&1|| echo "#27. Did not build"
	../../../tools/compile_latex.sh -f wandering_ledger.tex -n "Fate's Edge Expansion - The Wandering Ledger.pdf" > /dev/null 2>&1|| echo "#28. Did not build"
	../../../tools/compile_latex.sh -f salt_ledger.tex -n "Fate's Edge Expansion - The Salt Ledger.pdf" > /dev/null 2>&1|| echo "#28. Did not build"
	../../../tools/compile_latex.sh -f whisper_ledger.tex -n "Fate's Edge Expansion - The Whisper Ledger.pdf" > /dev/null 2>&1|| echo "#29. Did not build"
	../../../tools/compile_latex.sh -f hearth_ledger.tex -n "Fate's Edge Expansion - The Hearth Ledger.pdf" > /dev/null 2>&1|| echo "#30. Did not build"
	../../../tools/compile_latex.sh -f unbroken-cord.tex -n "Fate's Edge Expansion - The Daughters of the Unbroken Cord.pdf" > /dev/null 2>&1|| echo "#31. Did not build"
	../../../tools/compile_latex.sh -f malachai.tex -n "Fate's Edge Expansion - Malachai, The Unchained Angel.pdf" > /dev/null 2>&1|| echo "#31. Did not build"
	../../../tools/compile_latex.sh -f velvet_touch.tex -n "Fate's Edge Expansion - The Velvet Touch, A Thief's Guide to Silk and Shadow.pdf" > /dev/null 2>&1|| echo "#33. Did not build"
	../../../tools/compile_latex.sh -f dhahara.tex -n "Fate's Edge Expansion - Dhahara, Kingdom of Brass.pdf" > /dev/null 2>&1|| echo "#34. Did not build"
	../../../tools/compile_latex.sh -f eastern_realms.tex -n "Fate's Edge Expansion - The Eastern Realms.pdf" > /dev/null 2>&1|| echo "#36. Did not build"
	../../../tools/compile_latex.sh -f road_beast.tex -n "Fate's Edge Expansion - The Road Bestiary.pdf" > /dev/null 2>&1|| echo "#37. Did not build"
	../../../tools/compile_latex.sh -f saikou_compendium.tex -n "Fate's Edge Expansion - The Road Bestiary.pdf" > /dev/null 2>&1|| echo "#38. Did not build"
	../../../tools/compile_latex.sh -f grey_wanderers_grimoire.tex -n "Fate's Edge Expansion - The Grey Wanderer's Grimoire.pdf" > /dev/null 2>&1|| echo "#39. Did not build"
../../../tools/compile_latex.sh -f way_of_warrior.tex -n "Fate's Edge Expansion - The Way Of The Warrior.pdf" > /dev/null 2>&1|| echo "#40. Did not build"
../../../tools/compile_latex.sh -f frost_ledger.tex -n "Fate's Edge Expansion - The Frost Ledger.pdf" > /dev/null 2>&1|| echo "#41. Did not build"
../../../tools/compile_latex.sh -f akilan.tex -n "Fate's Edge Expansion - Akilan, The Southern Realms.pdf" > /dev/null 2>&1|| echo "#42. Did not build"
../../../tools/compile_latex.sh -f bitter_root.tex -n "Fate's Edge Expansion - The Bitter Root.pdf" > /dev/null 2>&1|| echo "#43. Did not build"
../../../tools/compile_latex.sh -f house_fenwood_i_exile_road.tex -n "Fate's Edge Chronicles - The Fenwoods, Exhile Road.pdf" > /dev/null 2>&1|| echo "#44. Did not build"
../../../tools/compile_latex.sh -f house_fenwood_ii_reckoning_bridge.tex -n "Fate's Edge Chronicles - The Fenwoods, The Reckoning Bridge.pdf" > /dev/null 2>&1|| echo "#45. Did not build"
../../../tools/compile_latex.sh -f house_fenwood_iii_old_dukes_wars.tex -n "Fate's Edge Chronicles - The Fenwoods, The Old Duke's Wars.pdf" > /dev/null 2>&1|| echo "#46. Did not build"
../../../tools/compile_latex.sh -f knaves_regret.tex -n "Fate's Edge Expansion - Vhasia, The Knave's Regret.pdf" > /dev/null 2>&1|| echo "#47. Did not build"
../../../tools/compile_latex.sh -f justicars-judgement.tex -n "Fate's Edge Expansion - Viterra, The Knight's Confession.pdf" > /dev/null 2>&1|| echo "#48. Did not build"
../../../tools/compile_latex.sh -f knights_tale.tex -n "Fate's Edge Expansion - Viterra, The Knight's Confession.pdf" > /dev/null 2>&1|| echo "#49. Did not build"

../../../tools/compile_latex.sh -f air_mist_alder_thorn_mirror.tex -n "Fate's Edge Expansion - The Book of Air, Mist, Alder, Thorn, and Mirror.pdf" > /dev/null 2>&1|| echo "#50. Did not build"
 ../../../tools/compile_latex.sh -f tam_moira_wilds.tex -n "Fate's Edge Expansion - Moira's Journels of the Wilds.pdf" > /dev/null 2>&1|| echo "#51. Did not build"
 ../../../tools/compile_latex.sh -f mistlands.tex -n "Fate's Edge Expansion - Into the Mistlands.pdf" > /dev/null 2>&1|| echo "#51. Did not build"
cd saikou_compendium/
../../../../tools/compile_latex.sh -f main.tex -n "Fate's Edge Expansion - Saikou Ira's Compendium of the Veil.pdf" > /dev/null 2>&1|| echo "#52. Did not build"
cd -
cd threadweavers_spellbook/
../../../../tools/compile_latex.sh -f threadweavers_spellbook.tex -n "Fate's Edge Expansion - The Threadweavers Spellbook.pdf" > /dev/null 2>&1 || echo "#53. Did not build"
cd -

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
