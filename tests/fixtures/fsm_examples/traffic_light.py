"""Example using python-statemachine library."""
from statemachine import StateMachine, State


class TrafficLightMachine(StateMachine):
    """A simple traffic light state machine."""
    
    green = State('Green', initial=True)
    yellow = State('Yellow')
    red = State('Red')
    
    cycle = green.to(yellow) | yellow.to(red) | red.to(green)
