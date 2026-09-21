from agent.agent import PhysicalAIAgent


def main():

    agent = PhysicalAIAgent()

    command = input(
        "\nRobot command: "
    )

    agent.run(command)


if __name__ == "__main__":

    main()