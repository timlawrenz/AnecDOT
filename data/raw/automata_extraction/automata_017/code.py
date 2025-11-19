empty = DFA(
            states={"q0"},
            input_symbols={"0", "1"},
            transitions={"q0": {"0": "q0", "1": "q0"}},
            initial_state="q0",
            final_states=set(),
        )