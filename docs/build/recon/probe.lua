local out = {}
out[#out+1] = "time=" .. tostring(timer.getTime())
for _, n in ipairs({"veaf", "veafCombatMission", "veafCombatZone", "veafRadio", "veafSecurity", "veafGroundAI"}) do
  out[#out+1] = n .. "=" .. type(_G[n])
end
local fn = {}
for k, v in pairs(veafCombatMission or {}) do if type(v) == "function" and (k:lower():find("activ") or k:lower():find("get")) then fn[#fn+1] = k end end
out[#out+1] = "CM:" .. table.concat(fn, ",")
fn = {}
for k, v in pairs(veafCombatZone or {}) do if type(v) == "function" and (k:lower():find("activ") or k:lower():find("get")) then fn[#fn+1] = k end end
out[#out+1] = "CZ:" .. table.concat(fn, ",")
return table.concat(out, " | ")
