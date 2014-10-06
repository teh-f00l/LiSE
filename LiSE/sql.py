count_all_fmt = "SELECT COUNT(*) FROM {tbl};"
func_store_create_table_fmt = (
    "CREATE TABLE {tbl} ("
    "name TEXT NOT NULL PRIMARY KEY, "
    "code TEXT NOT NULL);"
)
func_table_items_fmt = "SELECT name, code FROM {tbl} ORDER BY name;"
func_table_get_fmt = "SELECT code FROM {tbl} WHERE name=?;"
func_table_ins_fmt = "INSERT INTO {tbl} (name, code) VALUES (?, ?);"
func_table_upd_fmt = "UPDATE {tbl} SET code=? WHERE name=?;"
func_table_del_fmt = "DELETE FROM {tbl} wHERE name=?;"
universal_items = (
    "SELECT lise_globals.key, lise_globals.value "
    "FROM lise_globals JOIN "
    "(SELECT key, branch, MAX(tick) AS tick "
    "FROM lise_globals "
    "WHERE branch=? "
    "AND tick<=? "
    "GROUP BY key, branch) AS hitick "
    "ON lise_globals.key=hitick.key "
    "AND lise_globals.branch=hitick.branch "
    "AND lise_globals.tick=hitick.tick;"
)
universal_get = (
    "SELECT lise_globals.value FROM lise_globals JOIN "
    "(SELECT key, branch, MAX(tick) AS tick "
    "FROM lise_globals "
    "WHERE key=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY key, branch) AS hitick "
    "ON lise_globals.key=hitick.key "
    "AND lise_globals.branch=hitick.branch "
    "AND lise_globals.tick=hitick.tick;"
)
universal_ins = (
    "INSERT INTO lise_globals (key, branch, tick, value) "
    "VALUES (?, ?, ?, ?);"
)
universal_upd = (
    "UPDATE lise_globals SET value=? WHERE "
    "key=? AND "
    "branch=? AND "
    "tick=?;"
)
characters = "SELECT character FROM characters;"
ct_characters = "SELECT COUNT(*) FROM characters;"
ct_character = "SELECT COUNT(*) FROM characters WHERE character=?;"
char_del_fmt = "DELETE FROM {tbl} WHERE character=?;"
poll_rules_fmt = (
    "SELECT "
    "characters.character, "
    "characters.{tbl}_rulebook, "
    "active_rules.rule, "
    "active_rules.active, "
    "handle.handled "
    "FROM characters JOIN active_rules ON "
    "characters.{tbl}_rulebook=active_rules.rulebook "
    "JOIN "
    "(SELECT rulebook, rule, branch, MAX(tick) AS tick "
    "FROM active_rules WHERE "
    "branch=? AND "
    "tick<=? GROUP BY rulebook, rule, branch) AS hitick "
    "ON active_rules.rulebook=hitick.rulebook "
    "AND active_rules.rule=hitick.rule "
    "AND active_rules.branch=hitick.branch "
    "AND active_rules.tick=hitick.tick "
    "LEFT OUTER JOIN rulebooks "
    "ON rulebooks.rulebook=characters.{tbl}_rulebook "
    "AND rulebooks.rule=active_rules.rule "
    "LEFT OUTER JOIN "
    "(SELECT character, rulebook, rule, "
    "1 AS handled FROM {tbl}_rules_handled "
    "WHERE branch=? AND tick=?) "
    "AS handle ON "
    "handle.character=characters.character AND "
    "handle.rulebook=characters.{tbl}_rulebook AND "
    "handle.rule=active_rules.rule "
    "WHERE handle.handled IS NULL"
    ";"
)
handled_rule_fmt = (
    "INSERT INTO {ruletyp}_rules_handled "
    "(character, rulebook, rule, branch, tick) "
    "VALUES (?, ?, ?, ?, ?);"
)
active_rules_fmt = (
    "SELECT active_rules.rule, active_rules.active "
    "FROM active_rules JOIN "
    "(SELECT rulebook, rule, branch, MAX(tick) AS tick "
    "FROM {tbl} WHERE "
    "character=? AND "
    "rulebook=? AND "
    "branch=? AND "
    "tick<=? GROUP BY rulebook, rule, branch) AS hitick "
    "ON active_rules.rulebook=hitick.rulebook "
    "AND active_rules.branch=hitick.branch "
    "AND active_rules.tick=hitick.tick;"
)
active_rule_fmt = (
    "SELECT active_rules.active FROM active_rules JOIN ("
    "SELECT rulebook, rule, branch, MAX(tick) AS tick "
    "FROM {tbl} WHERE "
    "character=? AND "
    "rulebook=? AND "
    "rule=? AND "
    "branch=? AND "
    "tick<=? GROUP BY rulebook, rule, branch) AS hitick "
    "ON active_rules.rulebook=hitick.rulebook "
    "AND active_rules.rule=hitick.rule "
    "AND active_rules.branch=hitick.branch "
    "AND active_rules.tick=hitick.tick;"
)
rule_ins_fmt = (
    "INSERT INTO active_rules "
    "(rulebook, rule, branch, tick, active) "
    "VALUES (?, ?, ?, ?, ?);"
)
rule_upd_fmt = (
    "UPDATE active_rules SET active=? WHERE "
    "rulebook=? AND "
    "rule=? AND "
    "branch=? AND "
    "tick=?;"
)
del_char_things = "DELETE FROM things WHERE graph=?;",
del_char_avatars = "DELETE FROM avatars WHERE character_graph=?;"
node_is_thing = (
    "SELECT location FROM things JOIN ("
    "SELECT character, thing, branch, MAX(tick) AS tick "
    "FROM things WHERE "
    "character=? "
    "AND thing=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, thing, branch) AS hitick "
    "ON things.character=hitick.character "
    "AND things.thing=hitick.thing "
    "AND things.branch=hitick.branch "
    "AND things.tick=hitick.tick;"
)
rulebook_get_fmt = (
    "SELECT {rulemap}_rulebook FROM characters WHERE character=?;"
)
upd_rulebook_fmt = (
    "UPDATE characters SET {rulemap}_ruleboook=? WHERE character=?"
)
avatar_users = (
    "SELECT avatars.avatar_graph FROM avatars JOIN ("
    "SELECT character_graph, avatar_graph, avatar_node, "
    "branch, MAX(tick) AS tick "
    "FROM avatars WHERE "
    "avatar_graph=? AND "
    "avatar_node=? AND "
    "branch=? AND "
    "tick<=? GROUP BY "
    "character_graph, avatar_graph, avatar_node, "
    "branch) AS hitick "
    "ON avatars.character_graph=hitick.character_graph "
    "AND avatars.avatar_graph=hitick.avatar_graph "
    "AND avatars.avatar_node=hitick.avatar_node "
    "AND avatars.branch=hitick.branch "
    "AND avatars.tick=hitick.tick;"
)
arrival_time_get = (
    "SELECT MAX(tick) FROM things "
    "WHERE character=? "
    "AND thing=? "
    "AND location=? "
    "AND branch=? "
    "AND tick<=?;"
)
next_arrival_time_get = (
    "SELECT MIN(tick) FROM things "
    "WHERE character=? "
    "AND thing=? "
    "AND location=? "
    "AND branch=? "
    "AND tick>?;"
)
thing_loc_and_next_get = (
    "SELECT location, next_location FROM things JOIN ("
    "SELECT character, thing, branch, MAX(tick) AS tick "
    "FROM things "
    "WHERE character=? "
    "AND thing=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, thing, branch) AS hitick "
    "ON things.character=hitick.character "
    "AND things.thing=hitick.thing "
    "AND things.branch=hitick.branch "
    "AND things.tick=hitick.tick;"
)
thing_loc_and_next_ins = (
    "INSERT INTO things ("
    "character, "
    "thing, "
    "branch, "
    "tick, "
    "location, "
    "next_location) VALUES ("
    "?, ?, ?, ?, ?, ?);"
)
thing_loc_and_next_upd = (
    "UPDATE things SET location=?, next_location=? "
    "WHERE character=? "
    "AND thing=? "
    "AND branch=? "
    "AND tick=?;"
)
thing_loc_items = (
    "SELECT things.thing, things.location FROM things JOIN ("
    "SELECT character, thing, branch, MAX(tick) AS tick "
    "FROM things "
    "WHERE character=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, thing, branch) AS hitick "
    "ON things.character=hitick.character "
    "AND things.thing=hitick.thing "
    "AND things.branch=hitick.branch "
    "AND things.tick=hitick.tick "
    "LEFT OUTER JOIN "
    "(SELECT nodes.graph, nodes.node, nodes.branch, nodes.rev, "
    "nodes.extant FROM nodes JOIN "
    "(SELECT graph, node, branch, MAX(rev) AS rev FROM nodes "
    "WHERE graph=? "
    "AND branch=? "
    "AND rev<=? GROUP BY graph, node, branch) AS hirev ON "
    "nodes.graph=hirev.graph AND "
    "nodes.node=hirev.node AND "
    "nodes.branch=hirev.branch AND "
    "nodes.rev=hirev.rev) AS existence ON "
    "things.character=existence.graph AND "
    "things.thing=existence.node "
    "WHERE existence.extant;"
)
thing_and_loc = (
    "SELECT things.thing, things.location FROM things JOIN ("
    "SELECT character, thing, branch, MAX(tick) AS tick "
    "FROM things "
    "WHERE character=? "
    "AND thing=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, thing, branch) AS hitick "
    "ON things.character=hitick.character "
    "AND things.thing=hitick.thing "
    "AND things.branch=hitick.branch "
    "AND things.tick=hitick.tick "
    "LEFT OUTER JOIN "
    "(SELECT nodes.graph, nodes.node, nodes.branch, "
    "nodes.rev, nodes.extant "
    "FROM nodes JOIN "
    "(SELECT graph, node, branch, MAX(rev) AS rev "
    "FROM nodes "
    "WHERE graph=? "
    "AND node=? "
    "AND branch=? "
    "AND rev<=? GROUP BY graph, node, branch) AS hirev ON "
    "nodes.graph=hirev.graph AND "
    "nodes.node=hirev.node AND "
    "nodes.branch=hirev.branch AND "
    "nodes.rev=hirev.rev) AS existence ON "
    "things.character=existence.graph AND "
    "things.thing=existence.node "
    "WHERE existence.extant;"
)
character_things_items = (
    "SELECT things.thing, things.location FROM things JOIN ("
    "SELECT character, thing, branch, MAX(tick) AS tick "
    "FROM things "
    "WHERE character=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, thing, branch) AS hitick ON "
    "things.character=hitick.character "
    "AND things.thing=hitick.thing "
    "AND things.branch=hitick.branch "
    "AND things.tick=hitick.tick;"
)
avatarness = (
    "SELECT "
    "avatars.avatar_graph, "
    "avatars.avatar_node, "
    "avatars.is_avatar FROM avatars "
    "JOIN ("
    "SELECT character_graph, avatar_graph, avatar_node, "
    "branch, MAX(tick) AS tick FROM avatars WHERE "
    "character_graph=? AND "
    "branch=? AND "
    "tick<=? GROUP BY character_graph, avatar_graph, "
    "avatar_node, branch) AS hitick ON "
    "avatars.character_graph=hitick.character_graph AND "
    "avatars.avatar_graph=hitick.avatar_graph AND "
    "avatars.avatar_node=hitick.avatar_node AND "
    "avatars.branch=hitick.branch AND "
    "avatars.tick=hitick.tick;"
)
avatars_now = (
    "SELECT avatars.avatar_graph, avatars.avatar_node, is_avatar "
    "FROM avatars JOIN "
    "(SELECT character_graph, avatar_graph, avatar_node, branch, "
    "MAX(tick) AS tick FROM avatars "
    "WHERE character_graph=? "
    "AND branch=? "
    "AND tick<=? GROUP BY "
    "character_graph, avatar_graph, avatar_node, branch) "
    "AS hitick "
    "ON avatars.character_graph=hitick.character_graph "
    "AND avatars.avatar_graph=hitick.avatar_graph "
    "AND avatars.branch=hitick.branch "
    "AND avatars.tick=hitick.tick "
    "LEFT OUTER JOIN "
    "(SELECT nodes.graph, nodes.node, "
    "nodes.branch, nodes.rev, nodes.extant FROM nodes JOIN "
    "(SELECT graph, node, branch, MAX(rev) AS rev "
    "FROM nodes WHERE "
    "branch=? AND "
    "rev<=? GROUP BY graph, node, branch) AS hirev ON "
    "nodes.graph=hirev.graph AND "
    "nodes.node=hirev.node AND "
    "nodes.branch=hirev.branch AND "
    "nodes.rev=hirev.rev) AS existence ON "
    "avatars.avatar_graph=existence.graph AND "
    "avatars.avatar_node=existence.node WHERE "
    "existence.extant;"
)
avatars_ever = (
    "SELECT avatar_graph, avatar_node, branch, tick, is_avatar "
    "FROM avatars WHERE "
    "character_graph=?;"
)
is_avatar_of = (
    "SELECT avatars.is_avatar FROM avatars JOIN ("
    "SELECT character_graph, avatar_graph, avatar_node, "
    "branch, MAX(tick) AS tick FROM avatars "
    "WHERE character_graph=? "
    "AND avatar_graph=? "
    "AND avatar_node=? "
    "AND branch=? "
    "AND tick<=? GROUP BY "
    "character_graph, avatar_graph, avatar_node, "
    "branch) AS hitick ON "
    "avatars.character_graph=hitick.character_graph "
    "AND avatars.avatar_graph=hitick.avatar_graph "
    "AND avatars.avatar_node=hitick.avatar_node "
    "AND avatars.branch=hitick.branch "
    "AND avatars.tick=hitick.tick;"
)
sense_func_get = (
    "SELECT function FROM senses JOIN "
    "(SELECT character, sense, branch, MAX(tick) AS tick "
    "FROM senses WHERE "
    "character=? AND "
    "sense=? AND "
    "branch=? AND "
    "tick<=? GROUP BY character, sense, branch) AS hitick "
    "ON senses.character=hitick.character "
    "AND senses.sense=hitick.sense "
    "AND senses.branch=hitick.branch "
    "AND senses.tick=hitick.tick;"
)
sense_active_items = (
    "SELECT sense, active FROM senses JOIN ("
    "SELECT character, sense, branch, MAX(tick) AS tick "
    "FROM senses WHERE "
    "(character='' OR character=?) "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, sense, branch) AS hitick "
    "ON senses.character=hitick.character "
    "AND senses.sense=hitick.sense "
    "AND senses.branch=hitick.branch "
    "AND senses.tick=hitick.tick;"
)
sense_is_active = (
    "SELECT active FROM senses JOIN ("
    "SELECT character, sense, branch, MAX(tick) AS tick "
    "FROM senses WHERE "
    "character IN ('', ?) "
    "AND sense=? "
    "AND branch=? "
    "AND tick<=? "
    "GROUP BY character, sense, branch) AS hitick "
    "ON senses.character=hitick.character "
    "AND senses.sense=hitick.sense "
    "AND senses.branch=hitick.branch "
    "AND senses.tick=hitick.tick;"
)
sense_fun_ins = (
    "INSERT INTO senses "
    "(character, sense, branch, tick, function, active) "
    "VALUES "
    "(?, ?, ?, ?, ?, ?);"
)
sense_fun_upd = (
    "UPDATE senses SET function=?, active=? "
    "WHERE character=? "
    "AND sense=? "
    "AND branch=? "
    "AND tick=?;"
)
sense_ins = (
    "INSERT INTO senses "
    "(character, sense, branch, tick, active) "
    "VALUES "
    "(?, ?, ?, ?, ?);"
)
sense_upd = (
    "UPDATE senses SET active=? "
    "WHERE character=? "
    "AND sense=? "
    "AND branch=? "
    "AND tick=?;"
)
character_ins = (
    "INSERT INTO characters "
    "(character, "
    "character_rulebook, "
    "avatar_rulebook, "
    "thing_rulebook, "
    "place_rulebook, "
    "portal_rulebook) "
    "VALUES (?, ?, ?, ?, ?, ?);"
)
avatar_ins = (
    "INSERT INTO avatars ("
    "character_graph, avatar_graph, avatar_node, "
    "branch, tick, is_avatar"
    ") VALUES (?, ?, ?, ?, ?, ?);"
)
avatar_upd = (
    "UPDATE avatars SET is_avatar=? WHERE "
    "character_graph=? AND "
    "avatar_graph=? AND "
    "avatar_node=? AND "
    "branch=? AND "
    "tick=?;"
)
rulebook_rules = (
    "SELECT rule FROM rulebooks WHERE rulebook=? ORDER BY idx ASC;"
)
ct_rulebook_rules = "SELECT COUNT(*) FROM rulebooks WHERE rulebook=?;"
rulebook_get = "SELECT rule FROM rulebooks WHERE rulebook=? AND idx=?;"
rulebook_ins = "INSERT INTO rulebooks (rulebook, idx, rule) VALUES (?, ?, ?);"
rulebook_upd = "UPDATE rulebooks SET rule=? WHERE rulebook=? AND idx=?;"
rulebook_inc = "UPDATE rulebooks SET idx=idx+1 WHERE rulebook=? AND idx>=?;"
rulebook_dec = "UPDATE rulebooks SET idx=idx-1 WHERE rulebook=? AND idx>?;"
rulebook_del = "DELETE FROM rulebooks WHERE rulebook=? AND idx=?"
allrules = "SELECT rule FROM rules;"
haverule = "SELECT rule FROM rules WHERE rule=?;"
ctrules = "SELECT COUNT(*) FROM rules;"
ruleins = "INSERT INTO rules (rule) VALUES (?);"
ruledel = "DELETE FROM rules WHERE rule=?;"
avatar_branch_data = (
    "SELECT "
    "avatars.avatar_node, "
    "avatars.is_avatar FROM avatars JOIN ("
    "SELECT character_graph, avatar_graph, avatar_node, "
    "branch, MAX(tick) AS tick FROM avatars "
    "WHERE character_graph=? "
    "AND avatar_graph=? "
    "AND branch=? "
    "AND tick<=? GROUP BY "
    "character_graph, avatar_graph, avatar_node, branch"
    ") AS hitick ON "
    "avatars.character_graph=hitick.character_graph "
    "AND avatars.avatar_graph=hitick.avatar_graph "
    "AND avatars.avatar_node=hitick.avatar_node "
    "AND avatars.branch=hitick.branch "
    "AND avatars.tick=hitick.tick;"
)
thing_locs_data = (
    "SELECT tick, location, next_location FROM things "
    "WHERE character=? "
    "AND thing=? "
    "AND branch=?;"
)
