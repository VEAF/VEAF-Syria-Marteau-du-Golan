local found = {}
for _, g in ipairs(coalition.getGroups(2, Group.Category.AIRPLANE)) do
  local u = g:getUnit(1)
  if u and u:isActive() then
    local p = u:getPoint()
    local c = g:getController()
    found[#found+1] = string.format("%s [%s] n=%d @%.0f,%.0f alt=%.0f", g:getName(), u:getTypeName(), g:getSize(), p.x, p.z, p.y)
  end
end
local act = veafCombatMission.listActiveMissions and "" or ""
return table.concat(found, " ; ")
