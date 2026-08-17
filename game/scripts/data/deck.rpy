default deck = Deck()


init python:
    class Deck:
        def __init__(self) -> None:
            self.cards = [
                Card(
                    action={"attack": {"value": 5, "all": True}},
                    cost=2,
                    name="Fireball",
                    anim="cast",
                    special={"title": "FIREBALL", "anim": "cast", "colour": "#ff6622", "sfx": "sound/powerup.ogg"},
                ),
                Card(
                    action={"attack": {"value": 10}},
                    cost=2,
                    name="Finishing Strike",
                    anim="slash",
                    special={"title": "FINISHING STRIKE", "anim": "slash", "colour": "#ffcc00", "sfx": "sound/powerup.ogg"},
                ),
                Card(action={"attack": {"value": 3, "stun": True}}, cost=2, name="Bash", anim="punch"),
                Card(action={"attack": {"value": 3}}, cost=1, name="Punch", anim="punch"),
                Card(action={"attack": {"value": 6}, "draw": {"value": 1}}, cost=2, name="Slash", anim="slash"),
                Card(action={"attack": {"value": 2, "poison": True, "poison_duration": 3, "poison_stacks": 1}}, cost=1, name="Poison Dart", anim="cast"),
                Card(action={"draw": {"value": 2}}, cost=1, name="Book", anim="cast"),
                Card(action={"energy": {"value": 1}}, cost=0, name="Meditate", anim="drink"),
                Card(action={"energy": {"value": 2}}, cost=1, name="Pray", anim="raise_hand"),
                Card(action={"heal": {"value": 3, "times": 2}}, cost=2, name="Heal", anim="raise_hand"),
                Card(action={"heal": {"value": 3, "cleanse": "poisoned"}}, cost=1, name="Antidote", anim="raise_hand"),
                Card(action={"heal": {"value": 2, "cleanse": "stunned"}}, cost=1, name="Shake Off", anim="drink"),
            ]

            self.draw_pile = []
            self.discard_pile = []
            self.hand = []


        def get_card(self, card_id: str) -> Card:
            """
            Get card by id.
            """
            return find(self.cards, {"id": card_id})


        def get_cards(self, count: int, upgrade_card_type="") -> Card:
            """
            Get cards.
            """
            copy = self.cards.copy()
            renpy.random.shuffle(copy)

            if upgrade_card_type in ["all", "stun"]:
                copy = list(filter(lambda card: card.action.get("attack") and not card.action["attack"].get(upgrade_card_type), copy))
            elif upgrade_card_type == "cost":
                copy = list(filter(lambda card: card.cost > 0, copy))
            elif upgrade_card_type == "times":
                copy = list(filter(lambda card: card.action.get("attack") or card.action.get("heal"), copy))
            else:
                copy = list(filter(lambda card: card.action.get(upgrade_card_type), copy))

            cards = []
            for _ in range(count):
                if not len(copy):
                    return cards
                cards.append(copy.pop())
            return cards


        def draw_cards(self, count=3) -> None:
            """
            Add card(s) to hand.
            """
            if not count:
                return

            for _ in range(count):
                if not len(self.draw_pile):
                    self.draw_pile = self.discard_pile.copy()
                    self.discard_pile = []
                    renpy.random.shuffle(self.draw_pile)

                    if not len(self.draw_pile):
                        return

                renpy.sound.queue("sound/draw.ogg")
                self.hand.append(self.draw_pile.pop(0))


        def discard_card(self, card: Card) -> None:
            """
            Discard card.
            """
            self.hand.remove(card)
            self.discard_pile.append(card)


        def discard_hand(self) -> None:
            """
            Discard hand at end of turn.
            """
            while len(self.hand):
                self.discard_pile.append(self.hand.pop(0))


        def shuffle(self) -> None:
            """
            Shuffle draw pile before battle.
            """
            self.draw_pile = self.cards.copy()
            renpy.random.shuffle(self.draw_pile)
            self.discard_pile = []
            self.hand = []
