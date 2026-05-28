# 1. Fix sec:clocks-fronts → sec:core-resolution-cycle
sed -i '' 's/sec:clocks-fronts/sec:core-resolution-cycle/g' \
  sections/advanced_gm_tools.tex \
  sections/epic_tier.tex \
  sections/preface.tex

# 2. Remove the broken (autoref subsec:three-clock-guideline) from preface
sed -i '' 's/ (\\autoref{subsec:three-clock-guideline})//g' \
  sections/preface.tex

# 3. Remove sec:player-managed-modules-gm references (delete the \ref{...})
sed -i '' 's/ \\ref{sec:player-managed-modules-gm}//g' \
  sections/advanced_gm_tools.tex \
  sections/magic.tex

# 4. Fix subsec:module-thresholds → subsec:corruption-blooms
sed -i '' 's/subsec:module-thresholds/subsec:corruption-blooms/g' \
  sections/magic.tex

# 5. Fix subsec:followers-assets → sec:followers-assets-gm
sed -i '' 's/subsec:followers-assets/sec:followers-assets-gm/g' \
  sections/magic.tex \
  sections/epic_tier.tex

# 6. Remove sec:threat-pool reference
sed -i '' 's/ \\ref{sec:threat-pool}//g' \
  sections/epic_tier.tex

# 7. Fix app:rival-parties → app:rival-generator
sed -i '' 's/app:rival-parties/app:rival-generator/g' \
  sections/campaign_design.tex

# 8. Remove ch:legacy-engine reference (whole phrase)
sed -i '' 's/ (see \\ref{ch:legacy-engine})//g' \
  sections/managing_resources.tex

# 9. Fix sec:obligation-capacity → sec:obligation-corruption-gm
sed -i '' 's/sec:obligation-capacity/sec:obligation-corruption-gm/g' \
  sections/managing_resources.tex

# 10. Remove sec:acts-of-service reference
sed -i '' 's/ (see \\ref{sec:acts-of-service})//g' \
  sections/managing_resources.tex

# 11. Remove sec:player-terrestrial-patrons reference
sed -i '' 's/ \\ref{sec:player-terrestrial-patrons}//g' \
  sections/managing_resources.tex

# 12. Remove subsec:assets-choice reference
sed -i '' 's/ \\ref{subsec:assets-choice}//g' \
  sections/managing_resources.tex

# 13. Remove boring-game and enhanced-gm-play from reading plan
sed -i '' 's/ and \\autoref{sec:boring-game} (in \\autoref{ch:enhanced-gm-play})//g' \
  sections/preface.tex

# 14. Remove any remaining (in \autoref{ch:enhanced-gm-play})
sed -i '' 's/ (in \\autoref{ch:enhanced-gm-play})//g' \
  sections/preface.tex

# 1. In appendix.tex: subsec:module-thresholds → subsec:corruption-blooms
sed -i '' 's/subsec:module-thresholds/subsec:corruption-blooms/g' \
  sections/appendix.tex

# 2. In appendix.tex: subsec:followers-assets → sec:followers-assets-gm
sed -i '' 's/subsec:followers-assets/sec:followers-assets-gm/g' \
  sections/appendix.tex \
  sections/campaign_design.tex

# 3. In appendix.tex: ch:core-mechanics → ch:gm-core
sed -i '' 's/ch:core-mechanics/ch:gm-core/g' \
  sections/appendix.tex

# 4. In appendix.tex: remove broken \autoref{sec:when-to-roll} (replace with ch:gm-core)
sed -i '' 's/\\autoref{sec:when-to-roll}/Chapter~\\ref{ch:gm-core}/g' \
  sections/appendix.tex

# 5. In appendix.tex: sec:harm → Chapter~\ref{ch:gm-core}
sed -i '' 's/\\autoref{sec:harm}/Chapter~\\ref{ch:gm-core}/g' \
  sections/appendix.tex

# 6. In appendix.tex: sec:story-beats → sec:outcome-sb
sed -i '' 's/\\autoref{sec:story-beats}/\\autoref{sec:outcome-sb}/g' \
  sections/appendix.tex

# 7. In appendix.tex: sec:harm-fatigue → sec:fatigue-gm
sed -i '' 's/\\autoref{sec:harm-fatigue}/\\autoref{sec:fatigue-gm}/g' \
  sections/appendix.tex

# 8. In appendix.tex: remove broken \autoref{subsec:threat-pool} (delete the whole parenthetical)
sed -i '' 's/ (see \\autoref{subsec:threat-pool})//g' \
  sections/appendix.tex

# 9. In appendix.tex: sec:advancement → remove the reference entirely
sed -i '' 's/ (\\autoref{sec:advancement})//g' \
  sections/appendix.tex

# 10. In appendix.tex: sec:assets-system → sec:followers-assets-gm
sed -i '' 's/\\autoref{sec:assets-system}/\\autoref{sec:followers-assets-gm}/g' \
  sections/appendix.tex

# 11. In appendix.tex: remove broken \ref{subsec:three-beat-combat} (delete the See sentence)
sed -i '' 's/See \\ref{subsec:three-beat-combat} for complete action economy.//g' \
  sections/appendix.tex
