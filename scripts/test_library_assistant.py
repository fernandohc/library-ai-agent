from src.agents.library_assistant import LibraryAssistant

TEST_CASES = [
    {
        "question": "Find horror books currently available.",
        "expected_agent": "book_search",
    },
    {
        "question": "Recommend five books for user-001.",
        "expected_agent": "recommendation",
    },
    {
        "question": "Which genres have the most books?",
        "expected_agent": "analytics",
    },
    {
        "question": "What are the highest-rated books?",
        "expected_agent": "analytics",
    },
]


def main():
    assistant = LibraryAssistant()

    passed = 0
    failed = 0

    for test_case in TEST_CASES:
        question = test_case["question"]
        expected_agent = test_case["expected_agent"]

        print("\n" + "=" * 70)
        print(f"QUESTION: {question}")
        print(f"EXPECTED AGENT: {expected_agent}")

        try:
            result = assistant.ask(question)

            actual_agent = result["agent"]
            answer = result["answer"]

            routing_ok = actual_agent == expected_agent
            answer_ok = bool(answer and answer.strip())

            print(f"ACTUAL AGENT: {actual_agent}")
            print(f"ROUTING: {'PASS' if routing_ok else 'FAIL'}")
            print(f"ANSWER: {'PASS' if answer_ok else 'FAIL'}")

            if not routing_ok:
                print(f"Expected {expected_agent}, got {actual_agent}")

            if not answer_ok:
                print("The agent returned an empty answer.")

            if routing_ok and answer_ok:
                passed += 1
            else:
                failed += 1

            print(f"\nRESPONSE:\n{answer}")

        except Exception as exc:
            failed += 1
            print(f"ERROR: {type(exc).__name__}: {exc}")

    print("\n" + "=" * 70)
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    print(f"TOTAL: {passed + failed}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
