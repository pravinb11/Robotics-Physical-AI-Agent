import os

from google import genai
from google.genai import types


class LLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.5-flash-lite"

    def create_chat(self, world, tools):

        system_instruction = """
You are the high-level intelligence of a Physical AI robot.

You control a robot through tools.

IMPORTANT RULES:

1. The WORLD STATE is the source of truth.
2. Never invent objects.
3. Never substitute one object for another.
4. Only use object_id values that exist in WORLD STATE.
5. Never invent locations.
6. Never claim an action succeeded unless the tool reports SUCCESS.
7. Use the minimum number of tool calls necessary.
8. After a tool succeeds, use its result to decide the next action.
9. Do not repeat a successful tool call unless necessary.
10. Complete the user's task.
"""

        function_declarations = []

        for tool in tools:

            properties = {}

            for name, prop in tool["parameters"]["properties"].items():

                properties[name] = types.Schema(
                    type=prop["type"],
                    description=prop.get("description", "")
                )

            function_declarations.append(
                types.FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=types.Schema(
                        type="OBJECT",
                        properties=properties,
                        required=tool["parameters"].get("required", [])
                    )
                )
            )

        gemini_tools = [
            types.Tool(
                function_declarations=function_declarations
            )
        ]

        return self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=gemini_tools
            )
        )

    def send(self, chat, message):

        return chat.send_message(message)

    def send_tool_result(
        self,
        chat,
        function_call,
        result
    ):

        function_response = types.Part.from_function_response(
            name=function_call.name,
            response=result
        )

        return chat.send_message(function_response)