from skills.navigate import NavigateSkill
from skills.detect import DetectSkill
from skills.grasp import GraspSkill
from skills.place import PlaceSkill


class ToolExecutor:

    def __init__(self, world):

        self.world = world

        self.tools = {
            "navigate": NavigateSkill(),
            "detect": DetectSkill(world),
            "grasp": GraspSkill(world),
            "place": PlaceSkill()
        }

    # -------------------------------------------------
    # Validate tool arguments
    # -------------------------------------------------

    def validate(self, tool_name, arguments):

        if tool_name in ["detect", "grasp", "place"]:

            object_id = arguments.get("object_id")

            if object_id not in self.world.objects:

                return {
                    "valid": False,
                    "reason": (
                        f"Unknown object: {object_id}"
                    )
                }

        # Detect validation
        if tool_name == "detect":

            object_id = arguments["object_id"]

            obj = self.world.get_object(object_id)

            if not obj.visible:
                return {
                    "valid": False,
                    "reason": f"{object_id} is not visible"
                }

            if obj.location != self.world.robot["location"]:
                return {
                    "valid": False,
                    "reason": (
                        f"Robot is in {self.world.robot['location']} "
                        f"but {object_id} is in {obj.location}"
                    )
                }

        # Grasp validation
    # --------------------------------

        if tool_name == "grasp":

            object_id = arguments["object_id"]

            obj = self.world.get_object(object_id)

            if not obj.visible:
                return {
                    "valid": False,
                    "reason": f"{object_id} is not visible"
                }

            if not obj.graspable:
                return {
                    "valid": False,
                    "reason": f"{object_id} is not graspable"
                }

            if obj.location != self.world.robot["location"]:
                return {
                    "valid": False,
                    "reason": (
                        f"Robot is in {self.world.robot['location']} "
                        f"but {object_id} is in {obj.location}"
                    )
                }

            if self.world.robot["holding"] is not None:
                return {
                    "valid": False,
                    "reason": (
                        f"Robot is already holding "
                        f"{self.world.robot['holding']}"
                    )
                }

        # --------------------------------
        # Place validation
        # --------------------------------

        if tool_name == "place":

            object_id = arguments["object_id"]
            destination = arguments["location"]

            if self.world.robot["holding"] != object_id:
                return {
                    "valid": False,
                    "reason": (
                        f"Robot is not holding {object_id}"
                    )
                }

            if self.world.robot["location"] != destination:
                return {
                    "valid": False,
                    "reason": (
                        f"Robot is in {self.world.robot['location']} "
                        f"but destination is {destination}"
                    )
                }

        return {
            "valid": True
        }

    # -------------------------------------------------
    # Execute tool
    # -------------------------------------------------

    def execute(self, tool_name, arguments):

        if tool_name not in self.tools:

            return {
                "status": "FAILED",
                "tool": tool_name,
                "reason": "Unknown tool"
            }

        validation = self.validate(
            tool_name,
            arguments
        )

        if not validation["valid"]:

            return {
                "status": "FAILED",
                "tool": tool_name,
                "reason": validation["reason"]
            }

        try:

            tool = self.tools[tool_name]

            result = tool.execute(
                **arguments
            )

            return result

        except Exception as e:

            return {
                "status": "FAILED",
                "tool": tool_name,
                "reason": str(e)
            }

    # -------------------------------------------------
    # Gemini function declarations
    # -------------------------------------------------

    def get_tool_declarations(self):

        return [

            {
                "name": "navigate",

                "description":
                    "Navigate the robot to a location.",

                "parameters": {
                    "type": "OBJECT",

                    "properties": {
                        "target": {
                            "type": "STRING",
                            "description":
                                "Destination location."
                        }
                    },

                    "required": ["target"]
                }
            },

            {
                "name": "detect",

                "description":
                    "Detect an object that exists in "
                    "the current world state.",

                "parameters": {
                    "type": "OBJECT",

                    "properties": {
                        "object_id": {
                            "type": "STRING",
                            "description":
                                "ID of an existing object."
                        }
                    },

                    "required": ["object_id"]
                }
            },

            {
                "name": "grasp",

                "description":
                    "Grasp an existing graspable object.",

                "parameters": {
                    "type": "OBJECT",

                    "properties": {
                        "object_id": {
                            "type": "STRING",
                            "description":
                                "ID of an existing object."
                        }
                    },

                    "required": ["object_id"]
                }
            },

            {
                "name": "place",

                "description":
                    "Place a held object at a location.",

                "parameters": {
                    "type": "OBJECT",

                    "properties": {
                        "object_id": {
                            "type": "STRING"
                        },

                        "location": {
                            "type": "STRING"
                        }
                    },

                    "required": [
                        "object_id",
                        "location"
                    ]
                }
            }
        ]