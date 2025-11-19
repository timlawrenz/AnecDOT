"""Example using transitions GraphMachine."""
from transitions.extensions import GraphMachine


states = ['asleep', 'awake', 'working']

transitions = [
    {'trigger': 'wake_up', 'source': 'asleep', 'dest': 'awake'},
    {'trigger': 'start_work', 'source': 'awake', 'dest': 'working'},
    {'trigger': 'sleep', 'source': ['awake', 'working'], 'dest': 'asleep'}
]

class Person:
    pass

person = Person()
machine = GraphMachine(model=person, states=states, transitions=transitions, initial='asleep')
