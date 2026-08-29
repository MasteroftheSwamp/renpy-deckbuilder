# Designer template pack

Copy one template file, fill in the marked fields, and you have a new VN scene / RF map / fight instance / arena fight. Stats (vitality / stamina / strength → battle) live in one obvious file.

Jump **Templates** on the debug HUD (bottom-left) to try each kind in-game (`template_index`).

| Kind | Live example | Copy this template | Jump |
| --- | --- | --- | --- |
| Visual novel scene | `game/scripts/story/jail.rpy`, intro in `start.rpy` | `game/scripts/templates/vn_scene.rpy` | `template_vn` |
| Route Finder map | `game/RF/rooftop_a_levels.rpy` + `rf_points.rpy` | `game/scripts/templates/rf_level.rpy` | `template_rf` |
| Fight instance (one-off) | `game/scripts/data/fights.rpy` `promoter_bout` | `game/scripts/templates/fight_instance.rpy` | `template_fight` |
| Arena ladder fight | `game/scripts/data/levels.json` + `battle.rpy` | `game/scripts/templates/arena_fight.rpy` | `template_arena` |
| Sneak (windows/doors/cover) | `game/scripts/stealth/cover_lane.rpy` | (already the template) | `cover_lane` |
| City RF map | `game/scripts/rf/city_map.rpy` | (already the example) | `city_map` |
| Stats | `game/scripts/data/stats.rpy` | same | (HUD Stats tab / `life_sim_demo`) |

## Engines you do not copy

- **RF engine** is `game/RF/follower_controller.rpy` — do **not** edit it for a new map. Register the map, route, follower, and interact points; jump `rf_play`.
- **Battle loop** is `game/scripts/battle/*.rpy` (`battle`, `player_turn`, `enemy_turn`, `win`, `lose`, `reward`).
- **Shop** is `game/scripts/shop/shop.rpy`.
- **Life-sim clock / hunger** is `game/scripts/life_sim/` (`clock.rpy`, `needs.rpy`, `bridge.rpy`). Hunger is **not** a battle stat.

## Rules (AGENTS.md)

- Functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Smart quotes in dialogue (`What’s up?`, not `What's up?`).
- Never name an init-python loop variable `_p` (shadows Ren'Py `_p()` / `gui.about`). Use `_pt` or `_point`.
- Never put `background` on a `viewport`.
- Do not add another `label start`.
