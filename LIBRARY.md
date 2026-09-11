# Content library (buildalpha)

Catalog of **stable IDs** a story bot (or human) can assemble into a playthrough.

| Layer | Role |
| --- | --- |
| `library/manifest.json` | Master list of characters, RF rooms, chains, fights, VN beats |
| `library/**/*.json` | Per-id docs pointing at live engine data / image paths |
| `game/RF/library_loader.rpy` | Runtime: `RF_ROOMS`, `RF_CHAINS`, `rf_load_room`, `rf_enter_chain` |
| `game/scripts/templates/` | Grammar for *new* pieces (not the library itself) |
| `game/images/` | Actual art |

## Story bot flow

1. Read `library/manifest.json` — only use listed ids.
2. Spine example:
   - `jump rooftop_a` (chain entry) **or** `jump vespera_patrol`
   - interact → `$ start_fight("vespera_ambush")`
   - `on_lose` → `vespera_capture` (VN)
   - `on_win` → back to room label
3. Room swap inside a chain: `$ rf_chain_exit("rooftop_a_2")`
4. Need a new room/fight? Copy a template, register with `rf_register_room` / `FIGHTS[...]`, add a manifest entry.

## RF API

```renpy
$ rf_load_room("rooftop_a_1")     # or jump rooftop_a_1 / rf_play
$ rf_enter_chain("rooftop_a")     # sets chain + jumps rf_play at entry
$ rf_chain_exit("rooftop_a_2")    # swap room, stay in chain
$ print(rf_current_bg())          # bg path for current room
```

Registered today: `rooftop_a_1`, `rooftop_a_2`, `rooftop_a_3`, `vespera_patrol`.  
Chain: `rooftop_a` → enter label `rooftop_a`.

## Hale dialogue art

Abridged supporting-cast set under `game/images/hale/` (bust + full):

`neutral`, `smug`, `clinical`, `angry`, `surprised`, `pleased`, `frustrated`

- Side / say-box: `dr_hale smug "…"` (`Character` uses `image="hale"`)
- Central: `show hale smug`
- Battle poses remain under `game/images/enemies/hale/` (`hale idle`, `hale attack`, …)

