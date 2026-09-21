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

        for step in range(8):

            print(f"\nAGENT STEP {step + 1}")

            response = self.llm.send(
                chat,
                message
            )

            if response.function_calls:

                for function_call in response.function_calls:

                    tool_name = function_call.name
                    arguments = dict(function_call.args)

                    print(f"[LLM TOOL CALL] {tool_name}")
                    print(f"[ARGUMENTS] {arguments}")

                    result = self.executor.execute(
                        tool_name,
                        arguments
                    )

                    print(f"[TOOL RESULT] {result}")

                    # Update physical world
                    self.world.update(result)

                    print("\nUPDATED WORLD STATE:")
                    print(self.world.to_dict())

                    # Send actual FunctionResponse to Gemini
                    response = self.llm.send_tool_result(
                        chat,
                        function_call,
                        result
                    )

                    # If Gemini immediately asks for another tool,
                    # process it in the next agent step.
                    if response.function_calls:
                        continue

                    if response.text:
                        print("\nGEMINI:")
                        print(response.text)

                    return

            else:

                print("\nGEMINI:")
                print(response.text)

                return