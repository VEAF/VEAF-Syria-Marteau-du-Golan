local out = {}
local n = 0
for _, g in ipairs(coalition.getGroups(1)) do
  if g:getName():find("SA11Kiswah", 1, true) then for _, u in ipairs(g:getUnits()) do if u:isActive() then n = n + 1 end end end
end
out[#out+1] = "SA11 après réactivation=" .. n
for _, g in ipairs(coalition.getGroups(2, Group.Category.GROUND)) do
  if g:getName():find("Poussee", 1, true) then
    local u = g:getUnit(1); local p = u:getPoint(); local v = u:getVelocity()
    out[#out+1] = string.format("%s n=%d @%.0f,%.0f v=%.1f m/s", g:getName(), g:getSize(), p.x, p.z, math.sqrt(v.x^2 + v.z^2))
  end
end
return table.concat(out, " | ")
