local function count(prefix, side)
  local n = 0
  for _, g in ipairs(coalition.getGroups(side)) do
    if g:getName():find(prefix, 1, true) then
      for _, u in ipairs(g:getUnits()) do if u:isActive() and u:getLife() > 0 then n = n + 1 end end
    end
  end
  return n
end
local after = count("SA11Kiswah", 1)
local ok2, e2 = pcall(veafCombatZone.ActivateZone, "SA11Kiswah", true)
local ok3, e3 = pcall(veafCombatZone.ActivateZone, "Poussee", true)
return string.format("SA11 après désactivation=%d ; réactivation=%s ; poussée=%s %s", after, tostring(ok2), tostring(ok3), tostring(e3))
