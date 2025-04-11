from example.module.behavioral.state import State

class ConcreteState(State):
    def doThis(self) -> None:
        print("Doing this in ConcreteState")

    def doThat(self) -> None:
        print("Doing that in ConcreteState")