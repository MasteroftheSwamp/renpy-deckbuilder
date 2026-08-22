# ---------------------------------------------------------------------------
# RF interact-point framework + rooftop_a_1 test points
# Holds the follower still during dialogue (lock_plyr_cntrl + pause), like stop_sign.
# ---------------------------------------------------------------------------

default rf_active_point = None

default rooftop_a_points_1 = [
    {
        "name": "test_npc",
        "point": (1106.7857142857142, 948.2142857142857),
        "label": "rf_npc",
        "active": True,
        "detected": False,
        "once": False,
        "char_name": "Stranger",
        "map_sprite": "rf/placeholders/npc_marker.png",
        "side_image": "rf/placeholders/npc_side.png",
        "lines": [
            "Hey — didn't expect anyone else up here.",
            "If you're heading to the arena, watch your footing.",
        ],
    },
    {
        "name": "test_pickup",
        "point": (578.5714285714286, 954.6428571428571),
        "label": "rf_pickup",
        "active": True,
        "detected": False,
        "once": True,
        "map_sprite": "rf/placeholders/item_marker.png",
        "item_name": "Strange Card",
        "card_id": "placeholder",
    },
    {
        "name": "test_dialogue",
        "point": (828.2142857142857, 999.6428571428571),
        "label": "rf_dialogue",
        "active": True,
        "detected": False,
        "once": False,
        "lines": [
            "A chalk mark is scuffed into the rooftop.",
            "Someone passed through here recently.",
        ],
    },
    {
        "name": "test_show",
        "point": (1247.142857142857, 1053.2142857142858),
        "label": "rf_show",
        "active": True,
        "detected": False,
        "once": False,
        "blur": True,
        "fullscreen_image": "rf/placeholders/show_fullscreen.png",
        "char_name": "Memory",
        "lines": [
            "An old poster flutters in the wind.",
            "The face on it is half torn away.",
        ],
    },
    {
        "name": "fight_promoter",
        "point": (1818.2142857142856, 1047.857142857143),
        "label": "fight_promoter_talk",
        "active": True,
        "detected": False,
        "once": True,
        "char_name": "Fight Promoter",
        "map_sprite": "rf/placeholders/npc_marker.png",
        "side_image": "rf/placeholders/npc_side.png",
    },

]


init python:
    RF_CARD_REWARDS = {
        "placeholder": {
            "name": "Found Card",
            "cost": 1,
            "anim": "slash",
            "action": {"attack": {"value": 4}},
        },
    }

    def rf_followers():
        out = []
        for name in ("rooftop_a_follower", "follower", "test_follower"):
            fdisp = getattr(renpy.store, name, None)
            if fdisp is not None:
                out.append(fdisp)
        return out

    def rf_get_trigger_point():
        for fdisp in rf_followers():
            try:
                pt = fdisp.follower.cur_interact_point
            except Exception:
                pt = None
            if pt:
                return pt
        return renpy.store.rf_active_point

    def rf_pause_walk():
        """Freeze movement and block click-to-move (same idea as stop_sign)."""
        renpy.store.lock_plyr_cntrl = True
        for fdisp in rf_followers():
            try:
                fdisp.pause_follower()
            except Exception:
                try:
                    fdisp.stop_follower()
                except Exception:
                    pass

    def rf_resume_walk():
        """Allow click-to-move again; resume path if pause saved one."""
        for fdisp in rf_followers():
            try:
                fdisp.play_follower()
            except Exception:
                pass
        renpy.store.lock_plyr_cntrl = False

    def rf_mark_once(point):
        if point and point.get("once"):
            point["active"] = False
            point["detected"] = True

    def rf_give_card(card_id="placeholder"):
        spec = RF_CARD_REWARDS.get(card_id) or RF_CARD_REWARDS["placeholder"]
        card = Card(
            action=spec.get("action", {"attack": {"value": 1}}),
            cost=spec.get("cost", 1),
            name=spec.get("name", "Found Card"),
            anim=spec.get("anim", "slash"),
        )
        renpy.store.deck.cards.append(card)
        return card

    def rf_map_markers():
        fdisp = getattr(renpy.store, "rooftop_a_follower", None)
        if fdisp is None:
            return []
        out = []
        try:
            pts = fdisp.follower.interact_points or []
        except Exception:
            pts = []
        for p in pts:
            if not p.get("active", True):
                continue
            spr = p.get("map_sprite")
            if not spr:
                lab = p.get("label", "")
                if lab == "rf_npc":
                    spr = "rf/placeholders/npc_marker.png"
                elif lab == "rf_pickup":
                    spr = "rf/placeholders/item_marker.png"
                else:
                    continue
            out.append((p, spr))
        return out



# Art between map (zorder 0) and say window (high zorder) so dialogue stays readable
screen rf_cinematic(img, dim=0.65, zoom=1.0, side=False):
    # Below say (zorder 200), above rf_map (zorder 0)
    zorder 50
    if dim:
        add Solid("#000000") alpha dim
    if side:
        add img:
            xalign 0.0
            yalign 1.0
            xoffset 40
            yoffset -120
    else:
        # Keep main image in upper/mid area so the textbox stays clear
        add img:
            xalign 0.5
            yalign 0.35
            zoom zoom


label rf_point_begin:
    $ rf_active_point = rf_get_trigger_point()
    $ lock_plyr_cntrl = True
    $ rf_pause_walk()
    return


label rf_point_end:
    $ _pt = rf_active_point
    $ rf_mark_once(_pt)
    $ _jump = (_pt or {}).get("jump_after")
    $ rf_active_point = None
    if _jump:
        $ lock_plyr_cntrl = False
        $ rooftop_a_follower.stop_follower()
        hide screen rf_cinematic
        hide screen rf_map
        jump expression _jump
    # Resume any paused path, then unlock click-to-move
    $ rf_resume_walk()
    $ lock_plyr_cntrl = False
    $ renpy.pause(modal=False, hard=True)


label rf_npc:
    call rf_point_begin
    $ _pt = rf_active_point or {}
    $ _name = _pt.get("char_name", "Stranger")
    $ _side = _pt.get("side_image")
    $ _center = _pt.get("center_image")
    $ _blur = _pt.get("blur", bool(_center))
    $ _dlg = _pt.get("dialogue_label")
    $ _lines = _pt.get("lines") or ["..."]

    if _center:
        show screen rf_cinematic(_center, dim=0.55 if _blur else 0.0, zoom=1.0)
    elif _side:
        show screen rf_cinematic(_side, dim=0.0, side=True)

    if _dlg:
        call expression _dlg
    else:
        $ _who = Character(_name, color="#cceeff")
        python:
            for _line in _lines:
                renpy.say(_who, _line)

    hide screen rf_cinematic
    jump rf_point_end


label rf_pickup:
    call rf_point_begin
    $ _pt = rf_active_point or {}
    $ _item = _pt.get("item_name", "an item")
    $ _card_id = _pt.get("card_id", "placeholder")
    $ _dlg = _pt.get("dialogue_label")
    $ _lines = _pt.get("lines")
    $ _card = rf_give_card(_card_id)

    if _dlg:
        call expression _dlg
    elif _lines:
        python:
            for _line in _lines:
                renpy.say(narrator, _line)
    else:
        narrator "You picked up [_item]."
        narrator "A new card was added to your deck: {color=#ffcc66}[_card.name]{/color}."

    if _pt is not None and "once" not in _pt:
        $ _pt["once"] = True
    jump rf_point_end


label rf_dialogue:
    call rf_point_begin
    $ _pt = rf_active_point or {}
    $ _dlg = _pt.get("dialogue_label")
    $ _lines = _pt.get("lines") or ["..."]
    if _dlg:
        call expression _dlg
    else:
        python:
            for _line in _lines:
                renpy.say(narrator, _line)
    jump rf_point_end


label rf_show:
    call rf_point_begin
    $ _pt = rf_active_point or {}
    $ _img = _pt.get("fullscreen_image") or _pt.get("center_image") or _pt.get("prop_image") or "rf/placeholders/prop_center.png"
    $ _blur = _pt.get("blur", True)
    $ _name = _pt.get("char_name")
    $ _dlg = _pt.get("dialogue_label")
    $ _lines = _pt.get("lines") or ["..."]
    $ _prop = bool(_pt.get("prop_image")) and not _pt.get("fullscreen_image") and not _pt.get("center_image")

    $ _zoom = 0.85 if _prop else 1.0
    $ _dim = 0.65 if _blur else 0.0
    show screen rf_cinematic(_img, dim=_dim, zoom=_zoom)

    if _dlg:
        call expression _dlg
    else:
        if _name:
            $ _who = Character(_name, color="#e8d5ff")
            python:
                for _line in _lines:
                    renpy.say(_who, _line)
        else:
            python:
                for _line in _lines:
                    renpy.say(narrator, _line)

    hide screen rf_cinematic
    jump rf_point_end


# Dedicated arena recruiter — always leaves the map for intro/battle
label fight_promoter_talk:
    $ rf_active_point = rf_get_trigger_point()
    $ lock_plyr_cntrl = True
    $ rf_pause_walk()

    # One-shot promoter
    if rf_active_point is not None:
        $ rf_active_point["once"] = True
        $ rf_mark_once(rf_active_point)

    show screen rf_cinematic("rf/placeholders/npc_side.png", dim=0.0, side=True)

    $ _who = Character("Fight Promoter", color="#cceeff")
    _who "You look like you can handle yourself."
    _who "The arena's waiting — prove it, or get carried out."
    _who "Step inside when you're ready."

    hide screen rf_cinematic
    $ lock_plyr_cntrl = False
    $ rooftop_a_follower.stop_follower()
    hide screen rf_map
    hide screen rf_cinematic

    # Instance fight (not the arena ladder)
    $ battle_mode = "instance"
    $ current_fight_id = "promoter_bout"
    jump battle
