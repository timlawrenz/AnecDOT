dfa = DFA(
            states={"p0", "p1", "p2"},
            input_symbols={"0", "1"},
            transitions={
                "p0": {"0": "p0", "1": "p1"},
                "p1": {"0": "p0", "1": "p2"},
                "p2": {"0": "p2", "1": "p2"},
            },
            initial_state="p0",
            final_states={"p0", "p1"},
        )