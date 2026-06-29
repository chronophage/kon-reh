// Update Fatigue max when Body changes
on("change:attr_body", function() {
  getAttrs(["attr_body"], function(v) {
    setAttrs({
      "attr_fatigue_max": Math.max(1, parseInt(v.attr_body) || 1)
    });
  });
});

// Enforce Boon max (5) and auto-trim to 2 at scene end (manual trigger)
on("change:attr_boons", function() {
  getAttrs(["attr_boons"], function(v) {
    let boons = parseInt(v.attr_boons) || 0;
    if (boons > 5) {
      setAttrs({ "attr_boons": 5 });
      sendChat("System", "/w gm Boons capped at 5! Excess lost.");
    }
  });
});

// Auto-clear Bond used flag at session start (GM triggers via button)
on("clicked:reset_bonds", function() {
  setAttrs({ "attr_bond_used": 0 });
});

// Update Fatigue max display
on("change:attr_body change:attr_fatigue", function() {
  getAttrs(["attr_body", "attr_fatigue"], function(v) {
    let body = parseInt(v.attr_body) || 1;
    let fatigue = parseInt(v.attr_fatigue) || 0;
    setAttrs({
      "attr_fatigue_display": `${fatigue} / ${body}`
    });
  });
});

