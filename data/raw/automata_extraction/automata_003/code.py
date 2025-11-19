no_reachable_final_dfa = DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q1", "1": "q2"},
            "q2": {"0": "q0", "1": "q1"},
            "q3": {"0": "q2", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q3"},
    )