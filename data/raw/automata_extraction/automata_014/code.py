at_least_one_symbol = DFA(
            states={"q0", "q1"},
            input_symbols={"0", "1"},
            transitions={
                "q0": {"0": "q1", "1": "q1"},
                "q1": {"0": "q1", "1": "q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )