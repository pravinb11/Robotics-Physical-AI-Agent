class PlaceSkill:

    name = "place"

    def execute(self, object_id, location):

        print(f"[PLACE] Placing {object_id} at {location}")

        return {
            "status": "SUCCESS",
            "skill": self.name,
            "object_id": object_id,
            "location": location
        }