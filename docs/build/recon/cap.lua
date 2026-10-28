local ok, err = pcall(veafCombatMission.ActivateMission, "CAP-Alliee-Masada", true)
local found = {}
for _, g in ipairs(coalition.getGroups(2, Group.Category.AIRPLANE)) do
  local n = g:getName()
  if n:find("CAP") or n:find("OnDemand") or n:find("Alliee") then
    local u = g:getUnit(1)
    local p = u and u:getPoint()
    found[#found+1] = string.format("%s n=%d active=%s alt=%s", n, g:getSize(), tostring(u and u:isActive()), p and string.format("%.0f", p.y) or "?")
  end
end
return "activate ok=" .. tostring(ok) .. " " .. tostring(err) .. " | " .. table.concat(found, " ; ")
