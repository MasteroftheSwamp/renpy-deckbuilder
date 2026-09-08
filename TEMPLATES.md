# Designer template pack

Copy one template file, fill the marked fields, and you have a new level.
Assets (backgrounds, sprites, audio) stay under `game/images/` / `game/audio/` — not in the templates folder.

Jump **Templates** on the debug HUD (bottom-left) → `template_index`.

Branch for this pack: `level-templates` (playtest content stays on `vespera`).

| Kind | Template file | Jump | Live example |
| --- | --- | --- | --- |
| Standard Ren'Py dialogue | `game/scripts/templates/vn_scene.rpy` | `template_vn` | `game/scripts/story/jail.rpy`, intro in `start.rpy` |
| RF — single image | `game/scripts/templates/rf_single.rpy` | `template_rf_single` | `rooftop_a_1` in `game/RF/rooftop_a_levels.rpy` |
| RF — chain of images | `game/scripts/templates/rf_chain.rpy` | `template_rf_chain` | `rooftop_a_1` / `_2` / `_3` |
| Single battle | `game/scripts/templates/battle_single.rpy` | `template_battle_single` | `promoter_bout` in `game/scripts/data/fights.rpy` |
| Battle arena | `game/scripts/templates/battle_arena.rpy` | `template_battle_arena` | `game/scripts/data/levels.json` + `battle.rpy` |

Compatibility aliases (old names still jump):

| Old file / label | Now |
| --- | --- |
| `rf_level.rpy` / `template_rf` | → `template_rf_single` |
| `fight_instance.rpy` / `template_fight` | → `template_battle_single` |
| `arena_fight.rpy` / `template_arena` | → `template_battle_arena` |

Extras still on the hub: cover lane, city map, Vespera patrol.

## Engines you do not copy

- **RF engine** — `game/RF/follower_controller.rpy`. Register bg / route / points; jump `rf_play`.
- **Battle loop** — `game/scripts/battle/*.rpy`.
- **Shop** — `game/scripts/shop/shop.rpy`.
- **Life-sim** — `game/scripts/life_sim/` (hunger is not a battle stat).

## Rules (AGENTS.md)

- Functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Smart quotes in dialogue (`What’s up?`, not `What's up?`).
- Never name an init-python loop variable `_p` (shadows Ren'Py `_p()` / `gui.about`). Use `_pt` or `_point`.
- Never put `background` on a `viewport`.
- Do not add another `label start`.
