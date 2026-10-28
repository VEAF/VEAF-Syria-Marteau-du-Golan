local out = {}
for _, g in ipairs(coalition.getGroups(1, Group.Category.GROUND)) do
  if g:getName():find("ContreAttaque", 1, true) then
    local u = g:getUnit(1); local p = u:getPoint(); local v = u:getVelocity()
    out[#out+1] = string.format("%s n=%d @%.0f,%.0f v=%.1f m/s", g:getName(), g:getSize(), p.x, p.z, math.sqrt(v.x^2 + v.z^2))
  end
end
return table.concat(out, " | ")
