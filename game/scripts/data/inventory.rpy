default inventory = Inventory()


init python:
    class ItemDef:
        def __init__(self, id, name, description, icon, consumable=True):
            self.id = id
            self.name = name
            self.description = description
            self.icon = icon
            self.consumable = consumable


    # Registry of known items — add new quest items here
    ITEM_DEFS = {
        "key": ItemDef(
            "key", "Key", "A plain metal key. Might open something.",
            "items/key.png", consumable=True,
        ),
        "access_pass": ItemDef(
            "access_pass", "Access Pass", "Authorises entry to restricted areas.",
            "items/access_pass.png", consumable=True,
        ),
        "swipe_card": ItemDef(
            "swipe_card", "Swipe Card", "A magnetic card for electronic locks.",
            "items/swipe_card.png", consumable=True,
        ),
    }


    class Inventory:
        def __init__(self):
            # id -> count
            self.items = {}


        def clear(self):
            self.items.clear()


        def add(self, item_id, count=1):
            if item_id not in ITEM_DEFS:
                return
            self.items[item_id] = self.items.get(item_id, 0) + count


        def remove(self, item_id, count=1):
            if item_id not in self.items:
                return False
            self.items[item_id] -= count
            if self.items[item_id] <= 0:
                del self.items[item_id]
            return True


        def has(self, item_id, count=1):
            return self.items.get(item_id, 0) >= count


        def count(self, item_id):
            return self.items.get(item_id, 0)


        def list_entries(self):
            """Return list of (ItemDef, count) for UI."""
            result = []
            for item_id, count in self.items.items():
                if count > 0 and item_id in ITEM_DEFS:
                    result.append((ITEM_DEFS[item_id], count))
            return result
