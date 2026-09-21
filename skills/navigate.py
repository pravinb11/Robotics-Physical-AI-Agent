class NavigateSkill:

    name = "navigate"

    def execute(self, target):

        print(f"[NAVIGATE] Going to {target}")

        return {
            "status": "SUCCESS",
            "skill": self.name,
            "target": target
        }