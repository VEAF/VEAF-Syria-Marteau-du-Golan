local keys = {}
for k, v in pairs(veafRadio) do if type(v) ~= "function" then keys[#keys+1] = k .. ":" .. type(v) end end
local out = {"veafRadio keys: " .. table.concat(keys, ",")}
local function walk(m, depth, acc)
  if depth > 4 or type(m) ~= "table" then return end
  local t = m.title or m.name
  if t then acc[#acc+1] = string.rep("  ", depth) .. tostring(t) .. (m.secured and " [S]" or "") end
  for _, sub in ipairs(m.subMenus or {}) do walk(sub, depth + 1, acc) end
  for _, c in ipairs(m.commands or {}) do
    local ct = c.title or c.name
    if ct then acc[#acc+1] = string.rep("  ", depth + 1) .. "> " .. tostring(ct) .. ((c.usage or c.secured) and (" [" .. tostring(c.usage or "S") .. "]") or "") end
  end
end
local root = veafRadio.radioMenu or veafRadio.rootMenu or veafRadio.mainmenu
local acc = {}
walk(root, 0, acc)
out[#out+1] = table.concat(acc, "\n")
return table.concat(out, "\n")
