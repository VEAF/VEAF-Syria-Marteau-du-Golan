local g
for _, gg in ipairs(coalition.getGroups(2, Group.Category.GROUND)) do if gg:getName():find("Poussee", 1, true) then g = gg end end
if not g then return "pas de groupe" end
local p = g:getUnit(1):getPoint()
local function wp(x, y, action, speed) return {x = x, y = y, action = action, speed = speed, type = "Turning Point"} end
local route = {points = {
  wp(p.x, p.z, "Off Road", 8),
  wp(-210166, -13463, "Off Road", 8),
  wp(-203930, -7802, "On Road", 16.4),
  wp(-197693, -2500, "On Road", 16.4),
  wp(-193800, 3500, "On Road", 16.4),
}}
g:getController():setTask({id = "Mission", params = {route = route}})
return "route donnée"
