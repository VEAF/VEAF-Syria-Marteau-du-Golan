local out = {}
local list = veafCombatMission.missionsList or veafCombatMission.missions or {}
local k = {}
for kk, v in pairs(veafCombatMission) do if type(v) == "table" then k[#k+1] = kk end end
out[#out+1] = "tables: " .. table.concat(k, ",")
for _, m in pairs(list) do
  local n = m.getName and m:getName() or m.name
  out[#out+1] = "mission: " .. tostring(n) .. " friendly=" .. tostring(m.getFriendlyName and m:getFriendlyName() or m.friendlyName) .. " active=" .. tostring(m.isActive and m:isActive() or m.active)
end
local info = veafCombatMission.GetInformationOnMission and select(2, pcall(veafCombatMission.GetInformationOnMission, {missionName = "CAP-Alliee-Masada"})) or "?"
out[#out+1] = "info: " .. tostring(info)
return table.concat(out, " | ")
