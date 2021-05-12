from enum import Enum
from typing import Union
from collections.abc import Callable, Sequence


class Predicate:
    def __init__(self, name, objects):
        """
        Class to handle a predicate and the objects it is applied to.

        Arguments
        ---------
        name : string
            The name of the predicate.
        objects : list
            The list of objects this predicate applies to.
        """
        self.name = name
        self.objects = objects


class Effect(Predicate):
    def __init__(self, name, objects, func, probability=100):
        """
        Class to handle an individual effect of an action.

        Arguments
        ---------
        name : string
            The name of the effect.
        objects : list
            The list of objects this effect applies to.
        func : string
            The name of the function that applies the effect in the corresponding action.
        probability : int
            For non-deterministic problems, the probability that this effect will take place
            (defaults to 100)
        """
        super().__init__(name, objects)
        self.func = func
        self.probability = self.set_prob(probability)

    def set_prob(self, prob):
        """
        Setter function for probability.

        Arguments
        ---------
        prob : int
            The probability to be assigned.

        Returns
        -------
        prob : int
            The probability, after being checked for validity.
        """
        # ensure an integer is given
        try:
            test_int = int(prob)
        except ValueError:
            raise ValueError("Must enter an integer value for probability.")
        # enforce that probability is between 0 and 100 inclusive
        if prob < 0:
            prob = 0
        elif prob > 100:
            prob = 100
        return prob


class Action:
    def __init__(self, name, obj_params):
        """
        Class to handle each action.

        Arguments
        ---------
        name : string
            The name of the action.
        obj_params : list
            The list of objects this action applies to.

        Other Class Attributes
        ---------
        precond : list of Predicates
            The list of preconditions needed for this action.
        effects : list of Effects
            The list of effects this action results in/
        """
        self.name = name
        self.obj_params = obj_params
        self.precond = []
        self.effects = []

    def add_effect(self, name, objects, func, probability=100):
        """
        Creates an effect and adds it to this action.

        Arguments
        ---------
        name : string
            The name of the effect.
        objects : list
            The list of objects this effect applies to.
        func : string
            The name of the function that applies the effect in the corresponding action.
        probability : int
            For non-deterministic problems, the probability that this effect will take place
            (defaults to 100)

        Returns
        -------
        None
        """
        for obj in objects:
            if obj not in self.obj_params:
                raise Exception(
                    "Object must be one of the objects supplied to the action"
                )
        effect = Effect(name, objects, func, probability=100)
        self.effects.append(effect)

    def add_precond(self, name, objects):
        """
        Creates a precondition and adds it to this action.

        Arguments
        ---------
        name : string
            The name of the predicate to be used for the precondition.
        objects : list
            The list of objects this predicate applies to.

        Returns
        -------
        None
        """
        for obj in objects:
            if obj not in self.obj_params:
                raise Exception(
                    "Object must be one of the objects supplied to the action"
                )
        precond = Predicate(name, objects)
        self.precond.append(precond)


class ObservationToken:
    """
    An ObservationToken object implements a `tokenize` function to generate an
    observation token for an action-state pair.
    """

    class token_method(Enum):
        IDENTITY = 1

    def __init__(
        self,
        method: Union[
            token_method, Callable[[Action, Sequence[Predicate]], tuple]
        ] = token_method.IDENTITY,
    ):
        """
        Creates an ObservationToken object. This will store the supplied
        tokenize method to use on action-state pairs.

        Attributes
        ----------
        tokenize : function
            The function to apply to an action-state pair to generate the
            observation token.
        """
        if isinstance(method, self.token_method):
            self.tokenize = self.get_method(method)
        else:
            self.tokenize = method

    def get_method(self, method) -> Callable[[Action, Sequence[Predicate]], tuple]:
        """
        Retrieves a predefined `tokenize` function.

        Arguments
        ---------
        method : Enum
            The enum corresponding to the predefined `tokenize` function.

        Returns
        -------
        tokenize : object
            The `tokenize` function reference.
        """

        tokenize = self.identity
        if method == self.token_method.IDENTITY:
            tokenize = self.identity
        return tokenize

    def identity(self, action: Action, state: Sequence[Predicate]) -> tuple:
        """
        The identity `tokenize` function.

        Arguments
        ---------
        action : Action
            An `Action` object.
        state : list
            An list of fluents representing the state.

        Returns
        -------
        tokenize : function
            The `tokenize` function reference.
        """
        return (action, state)


class Step:
    """
    A Step object stores the action, fluents being acted on, and state prior
    to the action for a step in a trace.
    """

    def __init__(self, action: Action, fluents: list, state: list):
        """
        Creates a Step object. This stores action, fluents being acted on,
        and state prior to the action.

        Attributes
        ----------
        action : Action
            The action taken in this step.
        fluents : list
            A list of fluents being acted on.
        state : list
            A list of fluents representing the state.
        """
        self.action = action
        self.fluents = fluents
        self.state = state


if __name__ == "__main__":
    action = Action("put down", ["block 1", "block 2"])
    # action.add_effect("eff", ["block 1", "block 2"], "func1", 94)
    # action.add_precond("precond", ["block 1", "block 2"])
    # action.add_effect("eff", ["block 1", "block 3"], "func1", 94)

    o = ObservationToken()
    p = Predicate("name", [1])
    state = [p]
    token = o.tokenize(action, state)
    print(token)
