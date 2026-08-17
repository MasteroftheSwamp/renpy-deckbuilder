default quests = QuestLog()


init python:
    class Quest:
        def __init__(self, id, title, description):
            self.id = id
            self.title = title
            self.description = description
            self.status = "inactive"  # inactive | active | complete


    class QuestLog:
        def __init__(self):
            self.quests = {
                "fight_arena": Quest(
                    "fight_arena",
                    "Fight in the arena",
                    "Enter the arena and prove yourself in battle.",
                ),
            }
            self.active_id = None


        def clear_active(self):
            self.active_id = None


        def set_active(self, quest_id):
            if quest_id not in self.quests:
                return
            # Only one active quest
            if self.active_id and self.active_id in self.quests:
                if self.quests[self.active_id].status == "active":
                    self.quests[self.active_id].status = "inactive"
            self.active_id = quest_id
            self.quests[quest_id].status = "active"


        def complete(self, quest_id):
            if quest_id in self.quests:
                self.quests[quest_id].status = "complete"
            if self.active_id == quest_id:
                self.active_id = None


        def get_active(self):
            if self.active_id and self.active_id in self.quests:
                q = self.quests[self.active_id]
                if q.status == "active":
                    return q
            return None


        def active_title(self):
            q = self.get_active()
            return q.title if q else "No quests right now"


        def active_description(self):
            q = self.get_active()
            return q.description if q else "You have no active quests."
