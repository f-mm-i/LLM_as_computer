
class Agent:
    def __init__(self, name: str):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError("Метод run должен быть реализован в дочерних классах")


class SimpleAgent(Agent):
    def __init__(self, name: str = "SimpleAgent"):
        super().__init__(name)

    def run(self, input_text: str) -> str:
        return input_text
