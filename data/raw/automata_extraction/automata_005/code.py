frag = DFA(
            states={0, 1, 2, 3, 4},
            input_symbols={"0", "1"},
            transitions={
                0: {"1": 0, "0": 0},
                1: {"1": 0, "0": 3},
                3: {"1": 1, "0": 4},
                2: {"1": 0, "0": 4},
                4: {"1": 2, "0": 3},
            },
            initial_state=3,
            final_states={1, 4},
        )