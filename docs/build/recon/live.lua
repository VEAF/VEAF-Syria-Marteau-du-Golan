local out = {}
for _, g in ipairs(coalition.getGroups(1)) do
  local sx, sz, n, types = 0, 0, 0, {}
  for _, u in ipairs(g:getUnits()) do
    local p = u:getPoint()
    sx, sz, n = sx + p.x, sz + p.z, n + 1
    local tn = u:getTypeName()
    types[tn] = (types[tn] or 0) + 1
  end
  if n > 0 then
    local t = {}
    for k, v in pairs(types) do t[#t + 1] = v .. "x" .. k end
    local cx, cz = sx / n, sz / n
    out[#out + 1] = string.format("%s;%.0f;%.0f;%.0f;%d;%s", g:getName(), cx, cz, land.getHeight({x = cx, y = cz}), n, table.concat(t, ","))
  end
end
return table.concat(out, "|")
