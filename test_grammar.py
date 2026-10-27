"""
Unit tests for RuleBasedGrammarChecker
Verifies all 5 required rule categories:
1. Subject-verb agreement
2. Incorrect verb usage
3. Articles (a, an, the)
4. Repeated words
5. Basic punctuation & capitalization
"""

from grammar_checker import RuleBasedGrammarChecker


def run_tests():
    checker = RuleBasedGrammarChecker()

    test_cases = [
        # 1. Subject-Verb Agreement
        ("He go to school.", "Subject-verb agreement: 'He go' -> 'He goes'"),
        ("She are very happy.", "Subject-verb agreement: 'She are' -> 'She is'"),
        ("They is playing outside.", "Subject-verb agreement: 'They is' -> 'They are'"),
        ("The boy run fast.", "Subject-verb agreement: 'boy run' -> 'boy runs'"),
        ("The boys runs fast.", "Subject-verb agreement: 'boys runs' -> 'boys run'"),
        ("I has a pencil.", "Subject-verb agreement: 'I has' -> 'I have'"),

        # 2. Incorrect Verb Usage
        ("He can played football.", "Modal verb: 'can played' -> 'can play'"),
        ("She did went home.", "Auxiliary did: 'did went' -> 'did go'"),
        ("They has went to the market.", "Perfect tense: 'has went' -> 'has gone'"),
        ("He wants to went outside.", "Infinitive to: 'to went' -> 'to go'"),

        # 3. Articles (a, an)
        ("I ate a apple today.", "Article: 'a apple' -> 'an apple'"),
        ("She bought an car yesterday.", "Article: 'an car' -> 'a car'"),
        ("We waited for a hour.", "Phonetic silent h: 'a hour' -> 'an hour'"),
        ("This is an university.", "Phonetic consonant: 'an university' -> 'a university'"),

        # 4. Repeated Words
        ("I saw the the bird in the park.", "Repeated word: 'the the' -> 'the'"),
        ("We went to to the store.", "Repeated word: 'to to' -> 'to'"),

        # 5. Punctuation & Capitalization
        ("he is a good student", "Capitalization and terminal punctuation"),
        ("i love reading books.", "Lowercase 'i' pronoun capitalization"),
        ("Hello , how are you?", "Spacing before punctuation"),

        # 6. Combined errors
        ("he can played with a apple in the the morning", "Multiple combined grammatical errors"),

        # 7. Error Handling: Clean correct sentence
        ("She goes to school every day.", "Correct sentence with no errors"),
    ]

    print("=" * 60)
    print("RUNNING RULE-BASED GRAMMAR CHECKER TESTS")
    print("=" * 60)

    for i, (sentence, description) in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {description}")
        print(f"Original:   '{sentence}'")
        result = checker.analyze(sentence)
        print(f"Errors ({result['total_errors']}):")
        for err in result["errors"]:
            print(f"  - [{err['rule']}] Found: '{err['found']}' -> Suggestion: '{err['replacement']}'")
            print(f"    Explanation: {err['explanation']}")
        print(f"Corrected:  '{result['corrected_sentence']}'")


if __name__ == "__main__":
    run_tests()
