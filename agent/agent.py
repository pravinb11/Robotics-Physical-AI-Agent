from world.world_state import WorldState
from perception.mock_perception import MockPerception
from execution.tool_executor import ToolExecutor
from agent.llm import LLM


class PhysicalAIAgent:

    def __init__(self):

        self.world = WorldState()

        self.perception = MockPerception()

        for obj in self.perception.detect_objects():
            self.world.update_object(obj)

        self.executor = ToolExecutor(self.world)

        self.llm = LLM()

    def task_completed(self, user_command):

        command = user_command.lower()

        # Current task:
        # "Bring the red bottle"

        if "red bottle" in command:

            obj = self.world.get_object("red_bottle")

            if obj is None:
                return False

            user_location = self.world.people["user"]["location"]

            return (
                obj.location == user_location
                and
                self.world.robot["holding"] is None
            )

        return False

    def run(self, user_command):

        print("\n==============================")
        print("PHYSICAL AI AGENT")
        print("==============================")

        print("\nUSER:")
        print(user_command)

        print("\nINITIAL WORLD STATE:")
        print(self.world.to_dict())

        chat = self.llm.create_chat(
            self.world,
            self.executor.get_tool_declarations()
        )

        message = f"""
CURRENT WORLD STATE:

{self.world.to_dict()}

USER COMMAND:

{user_command}
"""

        response = self.llm.send(chat, message)

        for step in range(12):

            print(f"\nAGENT STEP {step + 1}")

            if not response.function_calls:

                print("\nGEMINI:")
                print(response.text)

                return

            # One tool call per step; the prompt asks for minimal, sequential calls
            function_call = response.function_calls[0]

            tool_name = function_call.name
            arguments = dict(function_call.args)

            print(f"[LLM TOOL CALL] {tool_name}")
            print(f"[ARGUMENTS] {arguments}")

            result = self.executor.execute(tool_name, arguments)

            print(f"[TOOL RESULT] {result}")

            # Update physical world
            self.world.update(result)

            print("\nUPDATED WORLD STATE:")
            print(self.world.to_dict())

            # Check whether the physical goal is actually complete
            if self.task_completed(user_command):

                print("\n==============================")
                print("TASK COMPLETED")
                print("==============================")

                print(self.world.to_dict())

                # Let Gemini see the final result and give its closing message
                response = self.llm.send_tool_result(
                    chat,
                    function_call,
                    result
                )

                if response.text:
                    print("\nGEMINI:")
                    print(response.text)

                return

            # The reply becomes the next thing to process
            response = self.llm.send_tool_result(
                chat,
                function_call,
                result
            )

        print("\nStopped: step limit reached")
