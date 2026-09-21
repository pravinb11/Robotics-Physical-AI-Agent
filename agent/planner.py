class Planner:

    def create_plan(self, task):
        object_id = task["object"]
        destination = task["destination"]

        plan = [

            {
                "tool": "navigate",
                "arguments": {
                    "target": "kitchen"
                }
            },

            {
                "tool": "detect",
                "arguments": {
                    "object_id": object_id
                }
            },

            {
                "tool": "grasp",
                "arguments": {
                    "object_id": object_id
                }
            },

            {
                "tool": "navigate",
                "arguments": {
                    "target": destination
                }
            },

            {
                "tool": "place",
                "arguments": {
                    "object_id": object_id,
                    "location": destination
                }
            }
        ]

        return plan