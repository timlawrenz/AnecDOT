dfa = DFA(
            states={"", "a", "b", "aa", "bb", "ab", "ba"},
            input_symbols={"a", "b"},
            transitions={
                "": {"a": "a", "b": "b"},
                "a": {"b": "ab", "a": "aa"},
                "b": {"b": "bb"},
                "aa": {"a": "aa", "b": "ab"},
                "bb": {"a": "ba"},
                "ab": {"b": "bb"},
                "ba": {"a": "aa"},
            },
            initial_state="",
            final_states={"aa"},
            allow_partial=True,
        )