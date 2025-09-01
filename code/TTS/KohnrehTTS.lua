-- Kon'reh Tabletop Simulator Helper
-- Tracks: turns (incl. opening double move), Blue specials per life, Rooted/Seed, Crown Stagger, Central Four stay/exclusion, Reforge countdown, global Green cap, Crown Buyback (variant).
-- v1.0

-- =========================
-- ====== STATE ============
-- =========================
state = {
  active = "A",                -- "A" (first) or "B" (second)
  moveCountThisTurn = 0,       -- for double move tracking at game start
  openingDoubleAvailableB = true, -- second player gets a 2-move opener
  variant = {
    crownBuyback = false,      -- OFF by default (toggle in UI)
  },
  globals = {
    greenCap = 6,
    greensOnBoard = 2,         -- start: 1 per side on board? If you start with 1 each, set to 2; if 0, set to 0.
  },
  -- Blue per-side data
  A = {
    specials = { hop=false, disp=false }, -- per Blue life
    rooted = false,
    rootedReason = "", -- "Seed", "CrownStagger"
    crossStay = 0,     -- consecutive own turns ended in Central Four
    crossExcluded = 0, -- own-turns remaining you cannot re-enter after exit
    seedLockHomeDepartureUsed = false, -- Mobilization delay already consumed for this Blue life
    sanctumBan = { left=false, right=false }, -- after Reforge-at-Sanctum
    reforge = { active=false, turnsLeft=0 },
    buybackUsedThisLife = false,
  },
  B = {
    specials = { hop=false, disp=false },
    rooted = false,
    rootedReason = "",
    crossStay = 0,
    crossExcluded = 0,
    seedLockHomeDepartureUsed = false,
    sanctumBan = { left=false, right=false },
    reforge = { active=false, turnsLeft=0 },
    buybackUsedThisLife = false,
  }
}

-- Utility: sync UI toggles and labels
function refreshUI()
  UI.setAttribute("activeSide","text","Active: "..state.active)
  UI.setAttribute("turnMoves","text","Moves this turn: "..tostring(state.moveCountThisTurn))
  UI.setAttribute("doubleInfo","text",
    state.openingDoubleAvailableB and "B has opening double-move" or "B opening double consumed")

  for _,side in ipairs({"A","B"}) do
    local s = state[side]
    UI.setAttribute("lbl_"..side.."_hop","text", s.specials.hop and "Hop: USED" or "Hop: ready")
    UI.setAttribute("lbl_"..side.."_disp","text", s.specials.disp and "Displace: USED" or "Displace: ready")
    UI.setAttribute("lbl_"..side.."_rooted","text", s.rooted and ("Rooted ("..s.rootedReason..")") or "Free")
    UI.setAttribute("lbl_"..side.."_cross","text",
      "Cross: stay "..s.crossStay.."/3 | excl "..s.crossExcluded)
    UI.setAttribute("lbl_"..side.."_reforge","text",
      s.reforge.active and ("Reforge: "..s.reforge.turnsLeft.." turns left") or "Reforge: —")
    UI.setAttribute("lbl_"..side.."_mob","text",
      s.seedLockHomeDepartureUsed and "Mobilized" or "Not yet left Home")
    UI.setAttribute("lbl_"..side.."_sanban","text",
      "Sanctum bans: L:"..(s.sanctumBan.left and "X" or "—").." R:"..(s.sanctumBan.right and "X" or "—"))
    UI.setAttribute("lbl_"..side.."_buyback","text",
      state.variant.crownBuyback and (s.buybackUsedThisLife and "Buyback: USED" or "Buyback: ready") or "Buyback: OFF")
  end

  UI.setAttribute("lbl_cap","text","Greens on board: "..state.globals.greensOnBoard.." / "..state.globals.greenCap)
  UI.setAttribute("btn_toggle_buyback","text",
    "Crown Buyback: "..(state.variant.crownBuyback and "ON" or "OFF"))
end

function onLoad()
  refreshUI()
end

-- Active side helper
local function S() return state[state.active] end
local function Opp() return (state.active=="A") and "B" or "A" end

-- =========================
-- ====== TURN FLOW ========
-- =========================
function btn_endMove(_, _)
  -- increment move count; enforce B-opening double logic
  state.moveCountThisTurn = state.moveCountThisTurn + 1

  if state.active=="B" and state.openingDoubleAvailableB then
    if state.moveCountThisTurn < 2 then
      broadcastToAll("B opening double: take another move.", {1,1,0})
      refreshUI()
      return
    else
      state.openingDoubleAvailableB = false
    end
  end

  -- End of side's turn housekeeping:
  -- 1) Cross stay increments only if the Blue ended in Cross (players should click btn_crossStayed if true)
  -- 2) Cross exclusion ticks down at the END of your turn
  local s = S()
  if s.crossExcluded > 0 then s.crossExcluded = s.crossExcluded - 1 end

  -- 3) Rooted clears at the START of your next turn, so it persists through end of this turn.
  -- 4) Reforge countdown ticks only for the side whose Blue was captured (they have N of their *own* turns).
  if s.reforge.active then
    s.reforge.turnsLeft = s.reforge.turnsLeft - 1
    if s.reforge.turnsLeft <= 0 then
      broadcastToAll("⚑ Reforge failed: "..state.active.." loses (no banner planted in time).", {1,0.3,0.3})
      -- Freeze further changes; you can Reset via buttons if desired.
    end
  end

  -- Turn passes
  state.active = Opp()
  state.moveCountThisTurn = 0

  -- Now at the START of new side's turn: clear Rooted for that side if it exists.
  local ns = S()
  if ns.rooted then
    ns.rooted = false
    ns.rootedReason = ""
  end

  refreshUI()
end

function btn_passTurn(_, _)  -- handy for setup/testing
  state.moveCountThisTurn = 99
  btn_endMove()
end

-- =========================
-- ===== BLUE SPECIALS =====
-- =========================
local function maybeCrownStagger(side)
  local s = state[side]
  if s.specials.hop and s.specials.disp and not s.rooted then
    s.rooted = true
    s.rootedReason = "Crown Stagger"
    broadcastToAll("♛ Crown Stagger: "..side.." Blue is Rooted until its next turn begins.", {0.8,0.9,1})
  end
end

function btn_useHop(_, _)
  local s = S()
  if s.specials.hop then
    broadcastToAll("Hop already used this Blue life.", {1,0.7,0.2}); return
  end
  -- Enforce “slide→special only” with a reminder (we can’t see moves, so we warn)
  -- (In Kon'reh: you may slide then special; special→slide is forbidden.)
  s.specials.hop = true
  maybeCrownStagger(state.active)
  refreshUI()
end

function btn_useDisp(_, _)
  local s = S()
  if s.specials.disp then
    broadcastToAll("Displacement already used this Blue life.", {1,0.7,0.2}); return
  end
  s.specials.disp = true
  maybeCrownStagger(state.active)
  refreshUI()
end

function btn_resetSpecialsThisLife(_, _)
  local s = S()
  s.specials.hop = false
  s.specials.disp = false
  s.buybackUsedThisLife = false
  refreshUI()
end

-- =========================
-- ====== BUYBACK ==========
-- =========================
function btn_toggleBuyback(_, _)
  state.variant.crownBuyback = not state.variant.crownBuyback
  refreshUI()
end

function btn_buyback(_, _)
  if not state.variant.crownBuyback then
    broadcastToAll("Crown Buyback variant is OFF.", {1,0.7,0.2}); return
  end
  local s = S()
  if s.buybackUsedThisLife then
    broadcastToAll("Buyback already used this Blue life.", {1,0.7,0.2}); return
  end
  if state.globals.greensOnBoard <= 0 then
    broadcastToAll("No Green available to sacrifice for buyback.", {1,0.7,0.2}); return
  end
  -- We cannot verify “Blue on Home Apex” automatically; trust the players.
  s.specials.hop = false
  s.specials.disp = false
  s.buybackUsedThisLife = true
  state.globals.greensOnBoard = state.globals.greensOnBoard - 1
  broadcastToAll("Crown Buyback: specials refreshed; 1 Green sacrificed; you lose this whole turn.", {0.9,0.9,0.4})
  refreshUI()
end

-- =========================
-- ====== SEED / ROOTED ====
-- =========================
function btn_markLeftHome(_, _)
  local s = S()
  if s.seedLockHomeDepartureUsed then
    broadcastToAll(state.active.." Blue already left Home earlier in this life.", {0.8,0.8,1})
  else
    s.seedLockHomeDepartureUsed = true
    broadcastToAll(state.active.." Blue has departed Home for the first time (Mobilization delay now in effect).", {0.8,0.8,1})
  end
  refreshUI()
end

function btn_seed(_, _)
  local s = S()
  if not s.seedLockHomeDepartureUsed then
    broadcastToAll("Mobilization delay: you cannot Seed on the first departure from Home.", {1,0.6,0.6}); return
  end
  if s.rooted then
    broadcastToAll("This Blue is already Rooted.", {1,0.7,0.2}); return
  end
  if state.globals.greensOnBoard >= state.globals.greenCap then
    broadcastToAll("Global Green cap reached ("..state.globals.greenCap.."). Seed illegal.", {1,0.6,0.6}); return
  end
  -- We can’t check Sanctum occupancy; trust players to comply.
  s.rooted = true
  s.rootedReason = "Seed"
  state.globals.greensOnBoard = state.globals.greensOnBoard + 1
  broadcastToAll(state.active.." Seeds: spawn a Green on the opposite Sanctum; Blue is Rooted until next turn begins.", {0.7,1,0.7})
  refreshUI()
end

-- =========================
-- ===== CENTRAL FOUR ======
-- =========================
function btn_crossStayed(_, _)
  local s = S()
  s.crossStay = math.min(3, s.crossStay + 1)
  if s.crossStay == 3 then
    broadcastToAll(state.active.." has maxed Cross stay (3). Must end **outside** next turn.", {1,0.9,0.5})
  end
  refreshUI()
end

function btn_crossExit(_, _)
  local s = S()
  if s.crossStay > 0 then s.crossStay = 0 end
  s.crossExcluded = 2
  broadcastToAll(state.active.." exited the Central Four: Cross exclusion for next 2 turns.", {0.8,0.9,1})
  refreshUI()
end

-- =========================
-- ====== REFORGE ==========
-- =========================
function btn_captureBlue(_, _)
  -- Opponent’s Blue captured → opponent gets 5 of their turns to plant.
  local opp = Opp()
  state[opp].reforge.active = true
  state[opp].reforge.turnsLeft = 5
  broadcastToAll("♜ Blue captured! "..opp.." now has 5 of THEIR turns to plant a banner.", {1,0.8,0.4})
  -- Captor’s Blue gains a fresh life OR continues same? In Kon’reh, specials refresh on return (Reforge), not on capture.
  refreshUI()
end

function btn_plantBanner(_, _)
  local s = S()
  if not s.reforge.active then
    broadcastToAll("No active Reforge for "..state.active..".", {1,0.7,0.2}); return
  end
  -- Runner removed (manual); choose placement in UI:
  -- We don’t know which option picked; provide three buttons:
end

function btn_reforgeHome(_, _)
  local s = S()
  if not s.reforge.active then return end
  s.reforge.active = false
  s.reforge.turnsLeft = 0
  -- Blue returns at Home Apex; specials refreshed:
  s.specials.hop, s.specials.disp = false,false
  s.buybackUsedThisLife = false
  s.seedLockHomeDepartureUsed = false
  s.sanctumBan.left, s.sanctumBan.right = false,false
  broadcastToAll("Reforge: Blue placed at HOME. Specials refreshed.", {0.7,1,0.7})
  refreshUI()
end

function btn_reforgeSanctumL(_, _) reforgeSanctum("left") end
function btn_reforgeSanctumR(_, _) reforgeSanctum("right") end
function reforgeSanctum(which)
  local s = S()
  if not s.reforge.active then return end
  if s.sanctumBan[which] then
    broadcastToAll("That Sanctum is banned for this Blue life.", {1,0.6,0.6}); return
  end
  s.reforge.active = false
  s.reforge.turnsLeft = 0
  s.specials.hop, s.specials.disp = false,false
  s.buybackUsedThisLife = false
  s.seedLockHomeDepartureUsed = false
  s.sanctumBan[which] = true
  local label = (which=="left") and "LEFT" or "RIGHT"
  broadcastToAll("Reforge: Blue placed at SANCTUM ("..label.."). That Sanctum can’t Seed for this Blue life.", {0.7,1,0.7})
  refreshUI()
end

function btn_reforgeOppApex(_, _)
  local s = S()
  if not s.reforge.active then return end
  if state.globals.greensOnBoard <= 0 then
    broadcastToAll("Opposing-Apex Reforge requires sacrificing a Green.", {1,0.6,0.6}); return
  end
  s.reforge.active = false
  s.reforge.turnsLeft = 0
  s.specials.hop, s.specials.disp = false,false
  s.buybackUsedThisLife = false
  s.seedLockHomeDepartureUsed = false
  state.globals.greensOnBoard = state.globals.greensOnBoard - 1
  broadcastToAll("Reforge: Blue placed at OPPOSING APEX (paid 1 Green). Specials refreshed.", {0.7,1,0.7})
  refreshUI()
end

-- =========================
-- ====== CAP TRACKING =====
-- =========================
function btn_capPlus(_, _)
  if state.globals.greensOnBoard < state.globals.greenCap then
    state.globals.greensOnBoard = state.globals.greensOnBoard + 1
  end
  refreshUI()
end
function btn_capMinus(_, _)
  if state.globals.greensOnBoard > 0 then
    state.globals.greensOnBoard = state.globals.greensOnBoard - 1
  end
  refreshUI()
end

-- =========================
-- ====== UTILITIES ========
-- =========================
function btn_resetAll(_, _)
  local keepBuybackVariant = state.variant.crownBuyback
  state = nil
  state = {
    active="A", moveCountThisTurn=0, openingDoubleAvailableB=true,
    variant = { crownBuyback = keepBuybackVariant },
    globals = { greenCap=6, greensOnBoard=2 },
    A = { specials={hop=false,disp=false}, rooted=false, rootedReason="", crossStay=0, crossExcluded=0,
          seedLockHomeDepartureUsed=false, sanctumBan={left=false,right=false},
          reforge={active=false,turnsLeft=0}, buybackUsedThisLife=false },
    B = { specials={hop=false,disp=false}, rooted=false, rootedReason="", crossStay=0, crossExcluded=0,
          seedLockHomeDepartureUsed=false, sanctumBan={left=false,right=false},
          reforge={active=false,turnsLeft=0}, buybackUsedThisLife=false },
  }
  refreshUI()
end

-- ===== KON'REH SETUP BAGS SPAWNER (add-on) =========================
local BAG_SPOTS = { A = {-16, 1.2, -6}, B = { 16, 1.2, -6} }  -- tweak positions as you like

local COLORS = {
  Blue   = {r=0.20,g=0.55,b=0.95},
  Orange = {r=0.95,g=0.55,b=0.15},
  Red    = {r=0.82,g=0.20,b=0.25},
  Green  = {r=0.25,g=0.72,b=0.35},
}

local COUNTS = { Blue=1, Orange=2, Red=6, Green=1 }

local function spawnToken(kind, side, pos)
  local obj = spawnObject({
    type = "BlockCircle",
    position = {pos[1], pos[2], pos[3]},
    rotation = {0, 0, 0},
    scale = {0.7, 0.25, 0.7},
    sound = false,
    snap_to_grid = false
  })
  obj.setName(kind.." ("..side..")")
  obj.setDescription("Kon'reh piece • side="..side.." • type="..kind)
  obj.setColorTint(COLORS[kind] or {r=0.8,g=0.8,b=0.8})
  obj.setLock(false)
  return obj
end

local function spawnSideBag(side, where)
  local bag = spawnObject({
    type = "Bag",
    position = where,
    rotation = {0, 0, 0},
    scale = {1.1, 1.1, 1.1},
    sound = false
  })
  bag.setName("Pieces — Side "..side)
  bag.setDescription("Kon'reh starter set ("..side..")")
  bag.setColorTint({r=(side=="A" and 0.85 or 0.35), g=0.35, b=(side=="A" and 0.35 or 0.85)})
  bag.lock() bag.unlock()

  -- spawn near the bag, then put them inside
  local drop = {where[1], where[2]+0.5, where[3]+2.0}
  for _,kind in ipairs({"Blue","Orange","Orange","Red","Red","Red","Red","Red","Red","Green"}) do
    local chip = spawnToken(kind, side, drop)
    Wait.frames(function() if bag and chip and bag.putObject then bag.putObject(chip) end end, 2)
  end

  -- optional table aids
  local die = spawnObject({type="Die_6", position={where[1], where[2]+0.5, where[3]-2.2}})
  die.setName("Reforge Countdown (optional)")
  local bead1 = spawnObject({type="Chip", position={where[1]-1.2, where[2]+0.5, where[3]-2.2}})
  local bead2 = spawnObject({type="Chip", position={where[1]+1.2, where[2]+0.5, where[3]-2.2}})
  bead1.setName("Blue Special Marker") bead2.setName("Blue Special Marker")

  return bag
end

function btn_spawnSetupBags(_, _)
  local a = spawnSideBag("A", BAG_SPOTS.A)
  local b = spawnSideBag("B", BAG_SPOTS.B)
  broadcastToAll("Spawned Kon'reh setup bags for Sides A & B. Drag bags where you like; right-click → Search to pull pieces.", {0.8,1,0.8})
end
-- ===================================================================
