import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.tool_executor import ToolExecutor


executor = ToolExecutor()


result = executor.execute(
    "navigate",
    {
        "target": "kitchen"
    }
)

print(result)


result = executor.execute(
    "detect",
    {
        "object_id": "red_bottle"
    }
)

print(result)


result = executor.execute(
    "grasp",
    {
        "object_id": "red_bottle"
    }
)

print(result)