from world.object import WorldObject


class WorldState:

    def __init__(self):

        self.robot = {
            "location": "living_room",
            "position": [0.0, 0.0, 0.0],
            "holding": None
        }

        self.objects = {}

        self.people = {

            "user": {
                "location": "living_room"
            }

        }

    # -------------------------------------------------
    # Object update
    # -------------------------------------------------

    def update_object(self, obj):

        self.objects[obj.object_id] = obj

    # -------------------------------------------------
    # Tool result update
    # -------------------------------------------------

    def update(self, result):

        skill = result.get("skill")

        # ---------------------------------------------
        # Navigation
        # ---------------------------------------------

        if skill == "navigate":

            self.robot["location"] = (
                result["target"]
            )

        # ---------------------------------------------
        # Grasp
        # ---------------------------------------------

        elif skill == "grasp":

            object_id = result["object_id"]

            self.robot["holding"] = object_id

            if object_id in self.objects:

                self.objects[
                    object_id
                ].visible = False

        # ---------------------------------------------
        # Place
        # ---------------------------------------------

        elif skill == "place":

            object_id = result["object_id"]

            location = result["location"]

            self.robot["holding"] = None

            if object_id in self.objects:

                self.objects[
                    object_id
                ].location = location

                self.objects[
                    object_id
                ].visible = True

    # -------------------------------------------------
    # Get object
    # -------------------------------------------------

    def get_object(self, object_id):

        return self.objects.get(
            object_id
        )

    # -------------------------------------------------
    # Convert to dictionary
    # -------------------------------------------------

    def to_dict(self):

        return {

            "robot": self.robot,

            "objects": {

                object_id: obj.to_dict()

                for object_id, obj
                in self.objects.items()
            },

            "people": self.people
        }

    # -------------------------------------------------
    # Display
    # -------------------------------------------------

    def show(self):

        print(
            "\n========== WORLD STATE =========="
        )

        print(
            self.to_dict()
        )

        print(
            "=================================\n"
        )