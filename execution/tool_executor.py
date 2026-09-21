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

        if tool_name in ["detect", "grasp"]:

            object_id = arguments.get("object_id")

            if object_id not in self.world.objects:

                return {
                    "valid": False,
                    "reason": (
                        f"Unknown object: {object_id}"
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