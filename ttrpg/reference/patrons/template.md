# Patron Template Standard for Fate's Edge

Below is the **authoritative template** for creating a new Patron entry. It standardises format, terminology, and costs across all patrons.

---

# Patron Template Specification

```latex
% ============================================================================
% PATRON ENTRY TEMPLATE
% ============================================================================

\subsection{Patron Name — Title (Domain \& Domain)}

\subsubsection*{Lore}
[One to two paragraphs establishing the patron's nature, origin, and role in the world. The voice should be evocative and grounded. Include at least one quote in a quote environment.]

\begin{quote}
"Memorable quote that captures the patron's philosophy and tone."
\end{quote}

\subsubsection*{Domain Focus}
\begin{itemize}
  \item \textbf{First Domain:} brief description
  \item \textbf{Second Domain:} brief description
  \item \textbf{Third Domain:} brief description
  \item \textbf{Fourth Domain:} brief description
\end{itemize}

\subsubsection*{Thiasos and Codex (Runekeeper Options)}

A Runekeeper sworn to [Patron] does not bind [brief description of what they do bind]. Their \textbf{Thiasos} is [specific creature or object, with 2-3 examples and a clear upkeep requirement].

The \textbf{Codex} of [Patron] is never [a normal book]. It may be [3-4 examples]. Because [reason], the Codex requires upkeep: [specific upkeep action]. If neglected, it becomes \textit{Compromised} [specific mechanical penalty].

\subsubsection*{Patron's Gift (Imbuement)}

Once per scene as an action, a Runekeeper of [Patron] may touch a held item (weapon, tool, or garment) and whisper a word of [theme]. For the rest of the scene, the item grants \textbf{+1 die} to [Skill 1] or [Skill 2], and the first time each scene [trigger condition], [beneficial effect]. After the scene, the user marks \textbf{+1 Obligation} to [Patron].

\subsubsection*{Rites of [Patron]}

\paragraph{Rite Name} (Tier, XP Cost) \hfill \\
\emph{Time; Range; Resist?} \\
\textbf{Tags:} \texttt{[TAG1]}, \texttt{[TAG2]}, \texttt{[TAG3]} \\
\textbf{Materials:} [Specific, requiring components] \\
\textbf{Effect:} [Clear description of what happens on a hit.] \\
\textbf{Push It:} [Enhanced effect.] Cost: Mark +1 Obligation (total X) or Mark +1 Fatigue. \\
\textbf{Cost:} Mark +X Obligation. \\
\textit{Requires:} Familiar / Familiar + Codex / Familiar + Codex + Tier III (\textit{Invoke:} 1 Boon). \\
\textbf{Invoke:} 1 action / Extended action. \\
\textbf{Duration:} Scene / Instant / Timer: X segments.

\subsubsection*{Cantors \& Cults of [Patron]}

\textbf{The Cantor's Song.} [Description of how a Cantor of this patron performs, what their voice does, and where they are typically found.]

\textbf{The Cult of [Name].} [Description of the patron's cult(s): where they gather, what they believe, what their rituals involve, and their creed. Include a brief note on how outsiders are treated.]

\subsubsection*{Witchcraft of [Patron] (Lay / [Domain])}

A witch who walks with [Patron] is a [title] or [title] — one who crafts the tools of [domain]. Their magic works through the materials of [domain]: [3-4 examples of tools and their uses].

\textbf{The Witch's Tool: [Name].} [Description of a signature tool: what it looks like, once-per-session effect, and secondary uses.]

\textbf{A Hedge Gift: [Name] (Basic, 4 XP).} [Description of a minor talent available to any character with the appropriate background.]

\subsubsection*{Corruption of [Patron]}

\begin{tblr}{
  colspec = {Q[c,1cm] X[2.5] X[2.5]},
  rowhead = 1,
  row{odd} = {bg=gray!10},
  row{1} = {bg=gray!30, font=\bfseries},
  hlines,
}
Tier & Benefit & Cost / Quirk \\
1 & [Mechanical benefit] & [Narrative or mechanical cost] \\
2 & [Mechanical benefit] & [Narrative or mechanical cost] \\
3 & [Mechanical benefit] & [Narrative or mechanical cost] \\
4 & [Mechanical benefit] & [Narrative or mechanical cost] \\
5 & [Mechanical benefit] & [Narrative or mechanical cost] \\
6+ & [Mechanical benefit] & [Narrative or mechanical cost] \\
\end{tblr}

\subsection*{Playstyle Notes}
[2-3 paragraphs summarising how this patron plays at the table. What kinds of characters suit them? What are their typical intrusions? What makes them unique? Who is this patron ideal for?]

\noindent\textbf{Emphasizes}
\begin{itemize}
  \item \textbf{First Emphasis:} brief description
  \item \textbf{Second Emphasis:} brief description
  \item \textbf{Third Emphasis:} brief description
  \item \textbf{Fourth Emphasis:} brief description
  \item \textbf{Fifth Emphasis:} brief description
\end{itemize}
```

---

# Monastic Tradition Template

```latex
% ============================================================================
% MONASTIC TRADITION TEMPLATE
% ============================================================================

% Place this after the Playstyle Notes section

\begin{tcolorbox}[colback=black!5,colframe=patronColor!80!black,title=\textbf{Monastic Name (Patron Name)},breakable]
  \emph{Tagline that captures the monastic philosophy.}

  \vspace{2mm}
  \noindent\textbf{Prerequisites:} [Attribute 1] 3+, [Attribute 2] 2+, Rite of [Key Rite] or Cantor of [Patron].

  \vspace{2mm}
  \noindent\textbf{Debt-Resistant Frame.} [Philosophical explanation of why this tradition resists debts.] Monks of the [Tradition] gain \textbf{+1 die} to resist [specific type of magical debt or obligation]. If they succeed, [narrative flourish].

  \vspace{2mm}
  \noindent\textbf{Techniques (purchased as Talents):}

  \begin{tblr}{
    colspec = {X[0.7,l] X[1.8,l] X[1.1,l] X[1.4,l]},
    rowhead = 1,
    row{odd}={bg=gray!10},
    row{1}={bg=gray!30, font=\bfseries},
    hlines,
  }
  Technique & Effect & Cost & Req. \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \textbf{Name} (Tier, XP) & [Effect] & [Cost] & [Requirement] \\
  \end{tblr}

  \vspace{2mm}
  \noindent\textbf{Master Technique (Epic Talent, 12 XP):}
  \textit{Technique Name.} Once per session, [epic effect]. After the scene, you gain a permanent \textbf{[Debt Scar Name]} ([description of the scar]). You may ignore [type of obligation] but [ongoing consequence].
\end{tcolorbox}
```

---

# Cost Standards Table

| Cost Type | Low Rite | Standard Rite | High Rite |
|-----------|----------|---------------|-----------|
| **Learning XP** | 4–5 | 7–9 | 12–14 |
| **Casting Obligation** | +1 | +1 or +2 | +2 or +3 |
| **Push Obligation** | +1 | +1 | +1 |
| **DV Formula** | `max(1 - Spirit, 1)` | `max(Cost - Spirit, 2)` | `max(Cost - Spirit, 3)` |
| **Typical Effect** | +1 die, reroll, minor boon | +2 dice, scene-long effect, moderate boon | Major effect, artifact creation, campaign-scale |

---

# Standardised Tags Library

| Tag | Purpose | Example Rite |
|-----|---------|--------------|
| `[AREA]` | Affects a zone, not a single target | Crushing Dark |
| `[BANISH]` | Sends an Outsider away | Banishment Knot |
| `[BARRIER]` | Creates cover or obstruction | Circle of Denial |
| `[BIND]` | Immobilises or restrains | Binding Vow |
| `[BOND]` | Creates or strengthens a connection | Shared Ember |
| `[BOOST]` | Grants bonus dice or effect | Lucky Coin |
| `[COMMAND]` | Issues a clear order | Unrefusable Offer |
| `[CONSUME]` | Destroys or absorbs | Essence Feast |
| `[CREATE]` | Makes something new | First Spark |
| `[CURSE]` | Inflicts a Condition | Marked Prey |
| `[DEBT]` | Creates an obligation | Unpayable Debt |
| `[DEBUFF]` | Imposes a penalty | Crowd's Distraction |
| `[DECEPTION]` | Involves lying or disguise | Unwritten Petition |
| `[DRAIN]` | Absorbs from a target | Feasting on Fear |
| `[DREAM]` | Affects sleep or vision | Umbral Dream |
| `[ERASURE]` | Removes or destroys | Forgotten Road |
| `[ESCAPE]` | Aids fleeing or evasion | Quick Exit |
| `[FATE]` | Influences destiny or consequence | Ember's Price |
| `[FEAR]` | Causes or uses fear | Thunderous Presence |
| `[FORCE]` | Physical pressure or push | Crushing Grip |
| `[HEAL]` | Restores health or condition | Healing Touch |
| `[LUCK]` | Involves chance or fortune | Lucky Coin |
| `[MARK]` | Tags a target for tracking | Predator's Gaze |
| `[NAVIGATION]` | Aids wayfinding | Road-Sense |
| `[OMEN]` | Gives cryptic warning | Crossroads Raven |
| `[PASSAGE]` | Opens a route | Waymark |
| `[PLANNING]` | Uses preparation | Plan That Never Fails |
| `[PRESSURE]` | Crushing or inexorable force | Crushing Dark |
| `[PROTECT]` | Defends or shields | Sheltered Hearth |
| `[PURIFY]` | Removes taint or corruption | Lay on Hands |
| `[RADIANT]` | Light, fire, or dawn | Radiant Smite |
| `[READ]` | Perceives emotions or thoughts | Weaver's Glance |
| `[RHYTHM]` | Uses timing or pattern | Humming Stone |
| `[RISK]` | Has a dangerous push option | Unseen Hand |
| `[SACRIFICE]` | Requires giving something up | Ember's Price |
| `[SANCTUARY]` | Creates safe space | Sheltered Hearth |
| `[SECRET]` | Reveals hidden information | Unlatched Secret |
| `[SENSE]` | Perceives hidden things | Sensing Current |
| `[SILENCE]` | Muffles or quietens | Gentle Seal |
| `[SOCIAL]` | Involves interaction | Crowd's Distraction |
| `[SPIRIT]` | Affects the soul or dead | Ancestral Consultation |
| `[STEALTH]` | Involves hiding or secrecy | Unseen Hand |
| `[STORM]` | Weather or electricity | Cracking Lightning |
| `[STRANGLE]` | Restrains breathing | Crushing Grip |
| `[STRIKE]` | Deals damage | Radiant Smite |
| `[SUMMON]` | Calls an entity | Unquiet Host |
| `[TRANSFORM]` | Changes form | Riven Fury |
| `[TRICK]` | Involves deception or cunning | Unseen Hand |
| `[TRUTH]` | Reveals or compels truth | Lingering Trace |
| `[UNSEAL]` | Opens what was closed | Silver Key |
| `[VOW]` | Creates a binding promise | Binding Vow |
| `[WARD]` | Blocks specific entities | Sealed Threshold |
| `[WEATHER]` | Affects storms or sky | Shattered Sky |

---

# Standardised Duration & Timer Language

| Term | Meaning | Example |
|------|---------|---------|
| `Duration: Scene.` | Lasts until the scene ends. | Battle Rage |
| `Duration: Instant.` | Resolves immediately, no duration. | Lucky Coin |
| `Duration: Exchange.` | Lasts one exchange (roughly one turn per character). | Crowd's Distraction |
| `Duration: Session.` | Lasts until the end of the session. | Magpie's Hoard |
| `Integrity Timer: X segments.` | An effect that can be broken or damaged. When timer fills, effect ends. | Circle of Denial |
| `Timer: X segments.` | An effect that advances over time. When timer fills, something happens. | Heist Timer, Laundry Timer |
| `Duration: Campaign (once).` | A one-time permanent effect. | Ember's Price |

---

# Standardised Materials Language

Materials should be:

1. **Specific** enough that a GM can say "you don't have that."
2. **Reasonable** enough that a prepared character can have them.
3. **Consumable** unless otherwise stated.

| Material Type | Examples |
|---------------|----------|
| **Consumable** | a coin, a pinch of dust, a drop of blood, a broken lock |
| **Reusable** | a pair of gloves, a tuning fork, a mask, a staff |
| **Sacrificial** | a piece of unfinished work, a stolen item, a personal memory |
| **Locational** | a threshold, a crossroads, a workbench, a grave |

---

# Quick Summary Checklist for New Patrons

```
✅ Patron Name & Title
✅ Lore (1-2 paragraphs + quote)
✅ Domain Focus (4 items)
✅ Thiasos (creature + upkeep)
✅ Codex (format + upkeep)
✅ Patron's Gift (once/scene, +1 Obligation)
✅ 3-4 Low Rites (4-5 XP, +1 Obligation)
✅ 2-3 Standard Rites (7-9 XP, +1 or +2 Obligation)
✅ 1-2 High Rites (12-14 XP, +2 or +3 Obligation)
✅ Push It for each Rite
✅ Cantor's Song description
✅ Cult description
✅ Witch's Tool description
✅ Hedge Gift (4 XP)
✅ Corruption Table (6 tiers)
✅ Playstyle Notes
✅ Emphasizes (4-5 items)
✅ Monastic Tradition (optional, recommended)
✅ Debt-Resistant Frame (for monastic)
✅ 4-6 Techniques (purchased as Talents)
✅ Master Technique (12 XP Epic Talent)
✅ Cross-Expansion Hooks (optional, recommended)
```
