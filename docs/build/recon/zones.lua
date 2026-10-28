local function count(prefix, side)
  local n = 0
  for _, g in ipairs(coalition.getGroups(side)) do
    if g:getName():find(prefix, 1, true) then
      for _, u in ipairs(g:getUnits()) do if u:isActive() and u:getLife() > 0 then n = n + 1 end end
    end
  end
  return n
end
local before = count("SA11Kiswah", 1)
local ok1, e1 = pcall(veafCombatZone.DesactivateZone, "SA11Kiswah", true)
return string.format("SA11 avant=%d désactivation=%s %s", before, tostring(ok1), tostring(e1))
