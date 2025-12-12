flowchart TD
    %% =========================
    %% CORE LOOP
    %% =========================
    CORE((The Core Loop<br/>Declare Action → Set Position/DV<br/>Roll d10s → Count Successes & SB<br/>Apply Outcome → Spend SB))
    class CORE core

    %% =========================
    %% FIRST RING — PRIMARY SYSTEMS
    %% =========================
    SB[Story Beats]
    CLOCKS[Clocks System]
    MODULES[Player-Managed Modules]
    BOONS[Boons]

    CORE --> SB
    CORE --> CLOCKS
    CORE --> MODULES
    CORE --> BOONS

    SB --> CORE
    CLOCKS --> CORE
    MODULES --> CORE
    BOONS --> CORE

    %% =========================
    %% SECOND RING — SPECIALIZED SYSTEMS
    %% =========================
    OBLIGATION[Obligation]
    CORRUPTION[Corruption]
    LEASH[Leash]
    SUPPLY[Supply Clock]
    FATIGUE[Fatigue & Harm]
    RESOURCES[Character Resources]
    MANDATE[Mandate]
    CRISIS[Crisis]

    %% Player-Managed Cluster
    MODULES --> OBLIGATION
    MODULES --> CORRUPTION
    MODULES --> LEASH
    MODULES --> FATIGUE

    %% Clocks Cluster
    CLOCKS --> SUPPLY
    CLOCKS --> MANDATE
    CLOCKS --> CRISIS

    %% Cross-links
    SUPPLY --> FATIGUE
    SUPPLY --> RESOURCES

    RESOURCES --> BOONS
    RESOURCES --> CLOCKS

    OBLIGATION --> MANDATE
    CORRUPTION --> MANDATE

    LEASH --> SB
    CORRUPTION --> SB
    OBLIGATION --> SB

    FATIGUE --> CORE

    CRISIS --> RESOURCES
    CRISIS --> SB

    MANDATE --> SB

    %% =========================
    %% THIRD RING — NARRATIVE CONSEQUENCES
    %% =========================
    NARRATIVE[[Narrative Consequences]]

    CHARACTERS[Character Arcs<br/>Growth · Relationships · Consequences]
    CAMPAIGN[Campaign Evolution<br/>World Change · Factions · Threats]
    AGENCY[Player Agency<br/>Meaningful Choice · World Reacts]

    SB --> NARRATIVE
    CLOCKS --> NARRATIVE
    MODULES --> NARRATIVE
    BOONS --> NARRATIVE

    NARRATIVE --> CHARACTERS
    NARRATIVE --> CAMPAIGN
    NARRATIVE --> AGENCY

    CHARACTERS --> CORE
    CAMPAIGN --> CORE
    AGENCY --> CORE

    %% =========================
    %% STYLING
    %% =========================
    classDef core fill:#2b2b2b,color:#ffffff,stroke:#ffffff,stroke-width:3px
    classDef primary fill:#1f6feb,color:#ffffff
    classDef secondary fill:#4fa3ff,color:#000000
    classDef narrative fill:#e6d8ad,color:#000000,stroke-width:2px

    class SB,CLOCKS,MODULES,BOONS primary
    class OBLIGATION,CORRUPTION,LEASH,SUPPLY,FATIGUE,RESOURCES,MANDATE,CRISIS secondary
    class NARRATIVE,CHARACTERS,CAMPAIGN,AGENCY narrative
