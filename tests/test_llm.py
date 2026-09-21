import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.llm import LLM


def main():

    llm = LLM()

    command = "Bring me the red bottle."

    task = llm.understand_task(command)

    print("\nUser command:")
    print(command)

    print("\nLLM output:")
    print(task)


if __name__ == "__main__":
    main()