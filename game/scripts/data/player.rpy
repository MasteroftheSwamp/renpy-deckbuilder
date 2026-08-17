default player = Player()


init python:
    class Player(RPGCharacter):
        XALIGN = 0.18
        YALIGN = 1.0


        def __init__(self, health=15, energy=3) -> None:
            super().__init__(
                health=health,
                energy=energy,
                name="Player",
                image="player",
            )

            self.draw_cards = 3
            self.moves = 3
            self.moves_max = 3
            self.turns = 0
            self.turns_max = 0

            self.cards_bought = 0
            self.cards_removed = 0
            self.cards_upgraded = 0
            self.rewards_bought = 0
            self.shop_cards = 2

            self.home_xalign = self.XALIGN


        def show(self) -> None:
            self.home_xalign = self.XALIGN
            self.refresh_sprite()
            renpy.with_statement(dissolve)


        def hide(self) -> None:
            self.hide_all_states()
            renpy.transition(dissolve, layer=LAYER_ENEMIES)


        def end_turn(self) -> None:
            """
            End player turn: discard hand, tick statuses, then enemy turn.

            Called from a screen button, so status messages use notify
            (narrator would start a nested interaction and crash).
            """
            self.turns -= 1
            deck.discard_hand()
            renpy.hide_screen("player_end_turn")

            messages = self.tick_statuses("end_turn")
            for msg in messages:
                renpy.notify(msg)

            if self.health <= 0:
                renpy.jump("lose")

            renpy.jump("enemy_turn")
