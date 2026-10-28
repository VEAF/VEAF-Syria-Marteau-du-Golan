---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_Syria_MarteauDuGolan"
veaf.config.era = veaf.ERA.MODERN
veaf.silenceAtcOnAllAirbases()

veaf.config.language = "fr"

-- ── Airfield channels of the mission's radio plan (src/presets.yaml, `bases`) ──────
if veafAirbases then
    veafAirbases.MissionChannels = {
        [13] = { alias = "Base-Haifa", title = "Haifa", uhf = 250.2, vhf = 127.8, fm = 38.6 },
        [20] = { alias = "Base-Kiryat Shmona", title = "Kiryat Shmona", uhf = 250.55, vhf = 118.4, fm = 39.0 },
        [24] = { alias = "Base-Megiddo", title = "Megiddo", uhf = 250.95, vhf = 119.9, fm = 39.4 },
        [30] = { alias = "Base-Ramat David", title = "Ramat David / 84X", uhf = 251.3, vhf = 118.6, fm = 39.75 },
        [34] = { alias = "Base-Rosh Pina", title = "Rosh Pina", uhf = 251.5, vhf = 118.45, fm = 39.95 },
    }
end

-- ── CTLD 2 ───────────────────────────────────────────────────────────────────
-- Configuration lives in ctld-config.yaml (edit it with ctld-tools); this only starts it.
veaf.config.manage_airbase_logistics = true
veaf.config.airbase_logistics_radius = 250
veaf.config.airbase_occupation_radius = 2000
veaf.config.airbase_logistics_tick = 30
-- One module's initialisation error must not take the others down (FIX-DEMO-MISSION-FINDINGS 02).
local function veafGuardedInit(name, initialize)
    local ok, err = xpcall(initialize, function(e)
        if debug and debug.traceback then
            return debug.traceback(tostring(e), 2)
        end
        return tostring(e)
    end)
    if not ok then
        veaf.loggers.get(veaf.Id):error("%s init failed: %s", name, err)
    end
end

veafGuardedInit("CTLD", function()
if ctld then
    veaf.ctld_initialize()
end
end)

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

veafGuardedInit("SECURITY", function()
if veafSecurity then
    veafSecurity.initialize()
end
end)

veafGuardedInit("RADIO", function()
if veafRadio then
    veafRadio.initialize(true)
end
end)

veafGuardedInit("SHORTCUTS", function()
if veafShortcuts then
    veafShortcuts.initialize()
end
end)

veafGuardedInit("NAMEDPOINTS", function()
if veafNamedPoints then
    veafNamedPoints.initialize({})
end
end)

veafGuardedInit("SPAWN", function()
if veafSpawn then
    veafSpawn.initialize()
end
end)

-- ── Combat ──

veafGuardedInit("CARRIER", function()
if veafCarrierOperations then
    veafCarrierOperations.initialize(true)
end
end)

veafGuardedInit("CASMISSION", function()
if veafCasMission then
    veafCasMission.initialize()
end
end)

veafGuardedInit("TRANSPORTMISSION", function()
if veafTransportMission then
    veafTransportMission.initialize()
end
end)

veafGuardedInit("COMBATMISSION", function()
if veafCombatMission then
    veafCombatMission.addCapMission("CAP-Alliee-Masada", "CAP alliée (2 F-15C, MASADA)", "Deux F-15C alliés en patrouille au FL250 au-dessus de MASADA, hors de portée du SA-11 : ils engagent les avions ennemis qui approchent.", false, true)
    veafCombatMission.initialize()
end
end)

veafGuardedInit("COMBATZONE", function()
if veafCombatZone then
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("KhanArnabah")
        :setFriendlyName("Front de Khan Arnabah")
        :setBriefing([[Ligne de défense avancée du 1er Corps syrien à Khan Arnabah : chars et BMP retranchés, Shilka, SA-13 et SA-15. Détruire toutes les unités pour ouvrir la route de Quneitra à la poussée alliée.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :addChainedCombatZone("ContreAttaque")
        :setChainedCombatZonesDelay(300)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("Sasa")
        :setFriendlyName("Réserve blindée de Sa'sa'")
        :setBriefing([[Brigade blindée de réserve du 1er Corps, en attente à l'est de Sa'sa' : T-72, BMP-2, couverte par SA-8 et SA-19. Détruire la réserve avant qu'elle ne monte au front.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("SA6Sasa")
        :setFriendlyName("Batterie SA-6 de Sa'sa'")
        :setBriefing([[Batterie SA-6 (2K12 Kub) qui couvre Sa'sa' et la sortie du col de Beit Jinn. Elle doit tomber avant le passage des hélicoptères.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("SA11Kiswah")
        :setFriendlyName("Batterie SA-11 de Kiswah")
        :setBriefing([[Batterie SA-11 (9K37 Buk) qui protège le PC du 1er Corps à Kiswah. La détruire avant la frappe sur le PC.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("Kiswah")
        :setFriendlyName("PC du 1er Corps à Kiswah")
        :setBriefing([[Poste de commandement du 1er Corps syrien à Kiswah : centre de commandement, tour de transmissions et deux bunkers, défendus par de la AAA et couverts par la batterie SA-11. Détruire les quatre bâtiments pour priver le front de son commandement.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("ArtiKanaker")
        :setFriendlyName("Artillerie de Kanaker")
        :setBriefing([[Groupe d'artillerie du 1er Corps près de Kanaker : quatre obusiers 2S1 et trois lance-roquettes BM-21, qui appuient la ligne de Khan Arnabah. Les détruire avant la poussée alliée.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("ContreAttaque")
        :setFriendlyName("Contre-attaque syrienne")
        :setBriefing([[La chute de Khan Arnabah déclenche la contre-attaque : une colonne de T-72, de BMP-2 et un Tunguska quitte Sa'sa' par la route de Quneitra, vers la ligne alliée. La casser avant le contact.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :disableRadioMenu()
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("Poussee")
        :setFriendlyName("Lancer la poussée alliée")
        :setRadioGroupName("Mission Maker")
        :setBriefing([[Groupement d'assaut de la brigade (Merkava, M113, Avenger) : il franchit la ligne à Quneitra, prend Khan Arnabah puis pousse vers Sa'sa' par la route. À déclencher par le Mission Maker, une fois le front dégarni.]])
        :setCompletable(false)
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("EWRTellHara")
        :setFriendlyName("Radar d'alerte de Tell al-Hara")
        :setBriefing([[Radar d'alerte avancée 55G6 sur la colline de Tell al-Hara : il voit le Golan et renseigne tout le réseau sol-air. Le détruire rend les batteries aveugles hors de leur propre radar.]])
        :setShowUnitsList(false)
        :setEnableSmokeAndFlare(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatOperation:new()
        :setMissionEditorZoneName("OpMarteauGolan")
        :setFriendlyName("Opération Marteau du Golan")
        :setBriefing([[Percer le front du 1er Corps syrien sur le Golan : aveugler la défense sol-air, détruire la ligne de Khan Arnabah, la réserve de Sa'sa' et l'artillerie de Kanaker. Objectifs secondaires : le SA-11 et le PC de Kiswah.]])
        :addTaskingOrder(veafCombatZone.GetZone("EWRTellHara"))
        :addTaskingOrder(veafCombatZone.GetZone("KhanArnabah"))
        :addTaskingOrder(veafCombatZone.GetZone("ArtiKanaker"))
        :addTaskingOrder(veafCombatZone.GetZone("Sasa"))
        :initialize()
    )
    veafCombatZone.initialize()
    veafCombatZone.ActivateZone("SA6Sasa", true)
    veafCombatZone.ActivateZone("SA11Kiswah", true)
    veafCombatZone.ActivateZone("Kiswah", true)
    veafCombatZone.ActivateZone("OpMarteauGolan", true)
end
end)

veafGuardedInit("QRA", function()
if veafQraManager then
    veafQraManager.initialize()
    local QRA_Mezzeh = VeafQRA:new()
        :setName("QRA Mezzeh")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Mezzeh")
        :setGroupsToDeployByEnemyQuantity(1, {"QRA-Mezzeh-MiG29-1"})
        :setGroupsToDeployByEnemyQuantity(4, {"QRA-Mezzeh-MiG29-1", "QRA-Mezzeh-MiG29-2"})
        :setDelayBeforeActivating(900)
        :start()
    local QRA_Khalkhalah = VeafQRA:new()
        :setName("QRA Khalkhalah")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Khalkhalah")
        :setGroupsToDeployByEnemyQuantity(1, {"QRA-Khalkhalah-MiG23-1"})
        :setDelayBeforeActivating(900)
        :start()
end
end)

-- ── Features ──

veafGuardedInit("GRASS", function()
if veafGrass then
    veafGrass.initialize()
end
end)

veafGuardedInit("ASSETS", function()
if veafAssets then
    veafAssets.Assets = {
        {sort = 1, name = "Magic 1", description = "Magic (E-3A, AWACS)", information = "U282.20 (Ch. 7)"},
        {sort = 2, name = "Texaco 1", description = "Texaco-1 (KC-135MPRS, panier)", information = [[Tacan 60Y
U290.10 (Ch. 8)
FL180]]},
        {sort = 3, name = "Arco 1", description = "Arco-1 (KC-135, perche)", information = [[Tacan 64Y
U290.50 (Ch. 9)
FL220]]},
        {sort = 4, name = "JTAC-AbuNada", description = "JTAC Abu Nada (Hummer, Tel Abu Nada)", information = [[Laser 1511
FM 35.55]], jtac = 1511, freq = 35.55, mod = "FM"},
    }
    veafAssets.initialize()
end
end)

veafGuardedInit("MOVE", function()
if veafMove then
    veafMove.initialize()
end
end)

veafGuardedInit("WEATHER", function()
if veafWeather then
    veafWeather.initialize()
end
end)

veafGuardedInit("REMOTE", function()
if veafRemote then
    veafRemote.initialize()
end
end)

veafGuardedInit("AIRBASES", function()
if veafAirbases then
    veafAirbases.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("MARKERS", function()
if veafMarkers then
    veafMarkers.initialize()
end
end)

veafGuardedInit("TIME", function()
if veafTime then
    veafTime.initialize()
end
end)

veafGuardedInit("UNITS", function()
if veafUnits then
    veafUnits.initialize()
end
end)

veafGuardedInit("CACHE", function()
if veafCacheManager then
    veafCacheManager.initialize()
end
end)

veafGuardedInit("EVENTS", function()
if veafEventHandler then
    veafEventHandler.initialize()
end
end)

-- ── Core ──

veafGuardedInit("GROUNDAI", function()
if veafGroundAI then
    veafGroundAI.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("COMMANDS", function()
if veafCommands then
    veafCommands.initialize()
end
end)

-- ── Features ──

veafGuardedInit("INTERPRETER", function()
if veafInterpreter then
    veafInterpreter.initialize()
end
end)

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("tum", "enable", false)

-- ── Skynet-IADS ──────────────────────────────────────────────────────────────
veafGuardedInit("SKYNET", function()
if veafSkynet then
    veafSkynet.initialize(false, false, false, false)
end
end)

-- ── CSAR configuration ───────────────────────────────────────────────────────
-- Note: CSAR.lua must be loaded by mission-script.lua before this block.
veafGuardedInit("CSAR", function()
if csar then
    csar.initialize()
end
end)
