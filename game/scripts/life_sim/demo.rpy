# Standalone city hub for the life-sim layer. No Route Finder.
#
# Uses the stock map HUD (screen hud / show_hud) — hunger sits under health
# in that frame, clock is the gold line at the top of the same frame.
# There is no second life-sim HUD.
#
# To try it inside the real game, jump to life_sim_demo (do not replace
# label start). To boot this folder as its own project, uncomment the
# start label at the bottom of this file.

# Tiny stubs so screen hud() does not crash when this boots without RF /
# the real Player / quests. The real game already defines these; init 999
# only fills holes.
init python:
    class _LsStubPlayer:
        def __init__(self):
            self.health = 15
            self.health_max = 15
            self.energy = 3
            self.energy_max = 3

    class _LsStubQuests:
        def __init__(self):
            self.quests = {}
        def active_title(self):
            return "Explore the city"
        def get_active(self):
            return None

    class _LsStubDeck:
        def __init__(self):
            self.cards = []

    class _LsStubInventory:
        def list_entries(self):
            return []

init 999 python:
    _store = renpy.store
    if getattr(_store, "player", None) is None:
        _store.player = _LsStubPlayer()
    if getattr(_store, "quests", None) is None:
        _store.quests = _LsStubQuests()
    if not hasattr(_store, "money"):
        _store.money = 0
    if not hasattr(_store, "wins"):
        _store.wins = 0
    if getattr(_store, "deck", None) is None:
        _store.deck = _LsStubDeck()
    if getattr(_store, "inventory", None) is None:
        _store.inventory = _LsStubInventory()


screen life_sim_city_map():
    tag life_sim_map

    add Solid("#1a1a22")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 10

        text "You are at [life_sim.location_label]." size 28
        text "Walk to a location. Time jumps on arrival." size 18 color "#aaaaaa"

        null height 8

        textbutton "Home" action Return("home") text_size 26
        textbutton "Gym" action Return("gym") text_size 26
        textbutton "Cafe" action Return("cafe") text_size 26
        textbutton "Alley" action Return("alley") text_size 26
        textbutton "Arena" action Return("arena") text_size 26

        null height 12
        textbutton "Reset week" action Return("reset") text_size 20 text_color "#888888" text_hover_color "#ffcc44"


label life_sim_demo:

    $ quick_menu = False
    $ life_sim.reset()
    scene black
    $ show_hud()
    "The city does not tick. Clocks jump when you finish something — a walk, a meal, a fight, a night’s sleep."
    jump life_sim_city


label life_sim_city:

    $ show_hud()
    call screen life_sim_city_map

    $ dest = _return
    if dest == "reset":
        $ life_sim.reset()
        "The week rewinds. Same streets, empty pockets filled again."
        jump life_sim_city

    if dest != life_sim.location:
        $ _walk = life_sim.travel_to(dest)
        $ dest_name = NODE_LABELS.get(dest, dest)
        $ walk_label = format_duration(_walk["minutes"])
        "You walk to [dest_name]. The street takes [walk_label]."

    jump expression "life_sim_loc_" + dest


label life_sim_loc_home:

    menu:
        "Home. The mattress still smells like rain."

        "Sleep until 08:00 tomorrow":
            $ life_sim.sleep()
            "You drop. Hunger ticks slower in the dark. Morning lands on 08:00."
            jump life_sim_loc_home

        "Back to the street":
            jump life_sim_city


label life_sim_loc_gym:

    if life_sim.starving:
        "The attendant takes one look at you. “Eat something. I’m not spotting a ghost.”"
        jump life_sim_city

    menu:
        "Iron, chalk, a radio nobody asked for."

        "Train vitality" if life_sim.stats.can_train("vitality"):
            $ life_sim.train("vitality")
            "Two hours. Your ceiling on health ticks up. It will apply the next time you fight."
            jump life_sim_loc_gym

        "Train stamina" if life_sim.stats.can_train("stamina"):
            $ life_sim.train("stamina")
            "Two hours. More energy in the tank next fight — battle still refills it at the start of your turn."
            jump life_sim_loc_gym

        "Train strength" if life_sim.stats.can_train("strength"):
            $ life_sim.train("strength")
            "Two hours. Your hits will land heavier the next time you step into the ring."
            jump life_sim_loc_gym

        "You’re already at the cap." if not (life_sim.stats.can_train("vitality") or life_sim.stats.can_train("stamina") or life_sim.stats.can_train("strength")):
            jump life_sim_city

        "Back to the street":
            jump life_sim_city


label life_sim_loc_cafe:

    menu:
        "Steam, cheap plates, a chalkboard that never changes."

        "Eat ($[EAT_COST], one hour)" if life_sim.cash >= EAT_COST:
            $ life_sim.eat()
            "Grease and heat. Hunger eases. The till is lighter."
            jump life_sim_loc_cafe

        "You can’t cover the special." if life_sim.cash < EAT_COST:
            jump life_sim_city

        "Back to the street":
            jump life_sim_city


label life_sim_loc_alley:

    menu:
        "The alley keeps its own weather."

        "Play scenario":
            jump life_sim_alley_scene

        "Back to the street":
            jump life_sim_city


label life_sim_alley_scene:

    "A figure blocks the far end. Not hidden. Waiting."
    "They want a fight, or they want you gone. Either way, this will take a while."
    "You talk it down. Bruised pride, no blood. Time to head back."
    $ life_sim.finish_activity("alley")
    "The city takes you back. Three hours have gone, on top of the walk."
    jump life_sim_city


label life_sim_loc_arena:

    menu:
        "Canvas, lights, the same door as always."

        "Start fight":
            python:
                _ls_player = getattr(renpy.store, "player", None)
                _ls_snap = life_sim.apply_to_player(_ls_player)
            "Battle snapshot — HP max [life_sim.stats.health_max], energy max [life_sim.stats.energy_max], ATK × [life_sim.stats.attack_multiplier]."
            "The battle would run as it does now. Cards, energy, turns. Life sim does not touch mid-fight."
            $ life_sim.finish_activity("arena")
            "The bout is over. Two hours, then the street again."
            jump life_sim_city

        "Back to the street":
            jump life_sim_city


# Uncomment to boot this demo as a tiny standalone project:
# label start:
#     jump life_sim_demo
