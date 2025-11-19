from fsm import MealyMachine, State

adder = MealyMachine('Binary addition')

carry = State('carry')
nocarry = State('no carry', initial=True)

nocarry[(1, 0), 1] = nocarry
nocarry[(0, 1), 1] = nocarry
nocarry[(0, 0), 0] = nocarry
nocarry[(1, 1), 0] = carry

carry[(1, 1), 1] = carry
carry[(0, 1), 0] = carry
carry[(1, 0), 0] = carry
carry[(0, 0), 1] = nocarry
