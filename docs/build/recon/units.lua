local out = {}
for _, g in ipairs(coalition.getGroups(1)) do
  local gn = g:getName()
  if not (gn:find("QRA") or gn:find("Template") or gn:find("veafSpawn") or gn:find("OnDemand")) then
    for _, u in ipairs(g:getUnits()) do
      local p = u:getPoint()
      out[#out + 1] = string.format("%s;%s;%.1f;%.1f;%.1f", gn, u:getTypeName(), p.x, p.z, p.y)
    end
  end
end
return table.concat(out, "|")
