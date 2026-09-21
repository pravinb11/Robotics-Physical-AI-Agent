class DetectSkill:
    name = "detect"

    def __init__(self, world=None):
        self.world = world

    def execute(self, object_id):
        print(f"[DETECT] Looking for {object_id}")

        if self.world is None:
            return {
                "status": "FAILED",
                "skill": self.name,
                "reason": "world_state_not_available"
            }

        obj = self.world.get_object(object_id)

        if obj is None:
            return {
                "status": "FAILED",
                "skill": self.name,
                "object_id": object_id,
                "reason": "object_not_found"
            }

        if not obj.visible:
            return {
                "status": "FAILED",
                "skill": self.name,
                "object_id": object_id,
                "reason": "object_not_visible"
            }

        return {
            "status": "SUCCESS",
            "skill": self.name,
            "object_id": object_id,
            "position": obj.position,
            "location": obj.location
        }