"""
Rule-Based NLP Grammar Checker
-------------------------------
A transparent, rule-based natural language processing engine that detects
and corrects common grammatical errors in English sentences without
relying on black-box machine learning models.

Error Categories Covered:
1. Capitalization & Punctuation (sentence starts, terminal marks, spacing, standalone 'I')
2. Repeated Words (accidental double tokens like 'the the', 'to to')
3. Indefinite Articles ('a' vs 'an' including phonetic exceptions)
4. Subject-Verb Agreement (singular vs plural pronouns/nouns with appropriate verb forms)
5. Incorrect Verb Usage (modal verbs, auxiliary 'do/did', perfect tense 'has/have/had', infinitive 'to')
"""

import re
from typing import List, Dict, Any, Tuple


class RuleBasedGrammarChecker:
    def __init__(self):
        # Base form to 3rd-person singular present, past, and past participle
        # Format: base: (3rd_singular, past, past_participle)
        self.irregular_verbs: Dict[str, Tuple[str, str, str]] = {
            "go": ("goes", "went", "gone"),
            "do": ("does", "did", "done"),
            "have": ("has", "had", "had"),
            "run": ("runs", "ran", "run"),
            "eat": ("eats", "ate", "eaten"),
            "write": ("writes", "wrote", "written"),
            "see": ("sees", "saw", "seen"),
            "take": ("takes", "took", "taken"),
            "make": ("makes", "made", "made"),
            "come": ("comes", "came", "come"),
            "give": ("gives", "gave", "given"),
            "speak": ("speaks", "spoke", "spoken"),
            "read": ("reads", "read", "read"),
            "sleep": ("sleeps", "slept", "slept"),
            "sing": ("sings", "sang", "sung"),
            "swim": ("swims", "swam", "swum"),
            "drive": ("drives", "drove", "driven"),
            "buy": ("buys", "bought", "bought"),
            "bring": ("brings", "brought", "brought"),
            "know": ("knows", "knew", "known"),
            "think": ("thinks", "thought", "thought"),
            "play": ("plays", "played", "played"),
            "walk": ("walks", "walked", "walked"),
            "work": ("works", "worked", "worked"),
            "like": ("likes", "liked", "liked"),
            "love": ("loves", "loved", "loved"),
            "want": ("wants", "wanted", "wanted"),
            "need": ("needs", "needed", "needed"),
            "help": ("helps", "helped", "helped"),
            "watch": ("watches", "watched", "watched"),
            "teach": ("teaches", "taught", "taught"),
            "study": ("studies", "studied", "studied"),
            "fly": ("flies", "flew", "flown"),
            "cry": ("cries", "cried", "cried"),
            "say": ("says", "said", "said"),
            "tell": ("tells", "told", "told"),
            "find": ("finds", "found", "found"),
            "leave": ("leaves", "left", "left"),
            "feel": ("feels", "felt", "felt"),
            "hear": ("hears", "heard", "heard"),
        }

        # Reverse lookup maps for fast morphological identification
        self.past_to_base: Dict[str, str] = {}
        self.participle_to_base: Dict[str, str] = {}
        self.singular_to_base: Dict[str, str] = {}

        for base, (s_form, p_form, pp_form) in self.irregular_verbs.items():
            self.singular_to_base[s_form] = base
            self.past_to_base[p_form] = base
            self.participle_to_base[pp_form] = base

        # Modal verbs must be followed by bare infinitive (base form)
        self.modal_verbs = {
            "can", "could", "will", "would", "shall", "should", "may", "might", "must"
        }

        # Articles phonetic rules
        # Words starting with silent 'h' taking 'an'
        self.silent_h_words = {"hour", "hours", "honest", "honor", "honour", "heir", "heirs"}

        # Words starting with vowels sounding like consonants (/j/ or /w/) taking 'a'
        self.consonant_vowel_words = {
            "university", "universities", "unicorn", "uniform", "unique", "unit",
            "united", "union", "user", "useful", "useless", "utensil", "european",
            "eucalyptus", "one", "one-time", "oneself"
        }

        # Common regular verb list for morphology checks
        self.common_regular_verbs = {
            "walk", "talk", "play", "clean", "cook", "watch", "call", "open",
            "close", "start", "finish", "wait", "visit", "learn", "jump", "look",
            "listen", "live", "love", "like", "use", "need", "seem", "ask", "move"
        }

    # -------------------------------------------------------------
    # Helper: Verb Morphology
    # -------------------------------------------------------------
    def get_base_verb(self, word: str) -> str:
        """Attempt to convert an inflected verb back to its base form."""
        w = word.lower()
        if w in self.irregular_verbs:
            return w
        if w in self.past_to_base:
            return self.past_to_base[w]
        if w in self.singular_to_base:
            return self.singular_to_base[w]
        if w in self.participle_to_base:
            return self.participle_to_base[w]

        # Regular past / participle ending with -ed
        if w.endswith("ied") and len(w) > 4:
            return w[:-3] + "y"
        if w.endswith("ed") and len(w) > 3:
            candidate = w[:-2]
            if candidate.endswith("e"):
                return candidate
            if candidate in self.common_regular_verbs:
                return candidate
            if (candidate + "e") in self.common_regular_verbs:
                return candidate + "e"
            return candidate

        # Regular 3rd singular ending with -s or -es
        if w.endswith("ies") and len(w) > 4:
            return w[:-3] + "y"
        if w.endswith("es") and len(w) > 3:
            for suffix in ["s", "sh", "ch", "x", "z", "o"]:
                if w[:-2].endswith(suffix):
                    return w[:-2]
            return w[:-1]
        if w.endswith("s") and len(w) > 2 and not w.endswith("ss"):
            return w[:-1]

        return w

    def get_third_person_singular(self, base_verb: str) -> str:
        """Convert a base verb to its 3rd-person singular present form."""
        w = base_verb.lower()
        if w in self.irregular_verbs:
            return self.irregular_verbs[w][0]
        if w.endswith(("s", "sh", "ch", "x", "z", "o")):
            return w + "es"
        if w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
            return w[:-1] + "ies"
        return w + "s"

    def is_verb(self, word: str) -> bool:
        """Check if a word is recognized as a verb or verb form."""
        w = word.lower()
        if w in self.irregular_verbs or w in self.common_regular_verbs:
            return True
        if w in self.past_to_base or w in self.singular_to_base or w in self.participle_to_base:
            return True
        if w.endswith("ed") or (w.endswith("s") and not w.endswith("ss")):
            base = self.get_base_verb(w)
            return base in self.common_regular_verbs or base in self.irregular_verbs
        return False

    # -------------------------------------------------------------
    # Tokenizer
    # -------------------------------------------------------------
    def tokenize(self, sentence: str) -> List[Tuple[str, int, int]]:
        """
        Tokenizes the sentence into (word, start_index, end_index).
        Punctuation is preserved separately or tokenized.
        """
        tokens = []
        for match in re.finditer(r"\b[\w'-]+\b", sentence):
            tokens.append((match.group(), match.start(), match.end()))
        return tokens

    # -------------------------------------------------------------
    # Rule 1: Capitalization & Basic Punctuation
    # -------------------------------------------------------------
    def check_punctuation_and_capitalization(self, text: str) -> List[Dict[str, Any]]:
        errors = []
        clean = text.strip()
        if not clean:
            return errors

        # 1. Starting letter capitalization
        first_letter_match = re.search(r"[a-zA-Z]", clean)
        first_char_pos = -1
        if first_letter_match:
            first_char = first_letter_match.group()
            first_char_pos = first_letter_match.start()
            # If the first word is a standalone 'i', let the standalone 'I' rule handle it to avoid duplicate messages
            is_standalone_i = (first_char.lower() == 'i' and (len(clean) == 1 or not clean[1].isalpha()))
            if first_char.islower() and not is_standalone_i:
                errors.append({
                    "rule": "Capitalization",
                    "found": first_char,
                    "replacement": first_char.upper(),
                    "explanation": f"Sentences should begin with an uppercase letter. Change '{first_char}' to '{first_char.upper()}'.",
                    "span": (first_char_pos, first_char_pos + 1)
                })

        # 2. Terminal punctuation
        if clean and clean[-1] not in ".?!":
            errors.append({
                "rule": "Terminal Punctuation",
                "found": clean[-1],
                "replacement": clean[-1] + ".",
                "explanation": "Sentences must end with an appropriate terminal punctuation mark (period, question mark, or exclamation point).",
                "span": (len(clean) - 1, len(clean))
            })

        # 3. Standalone lowercase 'i'
        for match in re.finditer(r"\b(i)\b", text):
            errors.append({
                "rule": "Pronoun Capitalization",
                "found": "i",
                "replacement": "I",
                "explanation": "The first-person pronoun 'I' must always be capitalized.",
                "span": (match.start(), match.end())
            })

        # 4. Spacing before punctuation like 'hello , world' or 'end .'
        for match in re.finditer(r"\s+([,.;:?!])", text):
            errors.append({
                "rule": "Punctuation Spacing",
                "found": match.group(),
                "replacement": match.group(1),
                "explanation": f"No space should precede punctuation mark '{match.group(1)}'.",
                "span": (match.start(), match.end())
            })

        # 5. Consecutive duplicate punctuation marks like ',,' or ';;'
        for match in re.finditer(r"([,;:?!]){2,}", text):
            errors.append({
                "rule": "Repeated Punctuation",
                "found": match.group(),
                "replacement": match.group()[0],
                "explanation": f"Repeated punctuation marks '{match.group()}' should be replaced with a single mark.",
                "span": (match.start(), match.end())
            })

        return errors

    # -------------------------------------------------------------
    # Rule 2: Repeated Words (Duplication)
    # -------------------------------------------------------------
    def check_repeated_words(self, text: str) -> List[Dict[str, Any]]:
        errors = []
        tokens = self.tokenize(text)

        for i in range(len(tokens) - 1):
            curr_word, c_start, _ = tokens[i]
            next_word, _, n_end = tokens[i + 1]

            # Check consecutive identical words (ignoring case)
            if curr_word.lower() == next_word.lower():
                errors.append({
                    "rule": "Repeated Word",
                    "found": f"{curr_word} {next_word}",
                    "replacement": curr_word,
                    "explanation": f"The word '{curr_word}' is repeated consecutively by mistake. Keep only one instance.",
                    "span": (c_start, n_end)
                })

        return errors

    # -------------------------------------------------------------
    # Rule 3: Articles ('a' vs 'an' vs 'the')
    # -------------------------------------------------------------
    def check_articles(self, text: str) -> List[Dict[str, Any]]:
        errors = []
        tokens = self.tokenize(text)

        for i in range(len(tokens) - 1):
            word, start, end = tokens[i]
            lower_word = word.lower()

            if lower_word not in ("a", "an"):
                continue

            next_word, n_start, n_end = tokens[i + 1]
            lower_next = next_word.lower()

            # Determine whether next word phonetically starts with vowel sound
            has_vowel_sound = False

            if lower_next in self.silent_h_words:
                has_vowel_sound = True
            elif lower_next in self.consonant_vowel_words:
                has_vowel_sound = False
            elif lower_next[0] in "aeiou":
                has_vowel_sound = True
            else:
                has_vowel_sound = False

            # Check rule violations
            if lower_word == "a" and has_vowel_sound:
                replacement = "An" if word.istitle() else "an"
                errors.append({
                    "rule": "Article Usage",
                    "found": f"{word} {next_word}",
                    "replacement": f"{replacement} {next_word}",
                    "explanation": f"Use '{replacement}' instead of '{word}' before words starting with a vowel sound ('{next_word}').",
                    "span": (start, n_end)
                })
            elif lower_word == "an" and not has_vowel_sound:
                replacement = "A" if word.istitle() else "a"
                errors.append({
                    "rule": "Article Usage",
                    "found": f"{word} {next_word}",
                    "replacement": f"{replacement} {next_word}",
                    "explanation": f"Use '{replacement}' instead of '{word}' before words starting with a consonant sound ('{next_word}').",
                    "span": (start, n_end)
                })

        return errors

    # -------------------------------------------------------------
    # Rule 4: Subject-Verb Agreement (SVA)
    # -------------------------------------------------------------
    def check_subject_verb_agreement(self, text: str) -> List[Dict[str, Any]]:
        errors = []
        tokens = self.tokenize(text)
        n = len(tokens)

        # Pronoun groupings
        singular_3rd_pronouns = {"he", "she", "it", "this", "that"}
        plural_pronouns = {"they", "we", "you", "these", "those"}
        first_person_singular = {"i"}

        for i in range(n - 1):
            subj_token, s_start, s_end = tokens[i]
            verb_token, v_start, v_end = tokens[i + 1]

            subj_lower = subj_token.lower()
            verb_lower = verb_token.lower()

            # -----------------------------------------
            # 1. First-Person Singular 'I'
            # -----------------------------------------
            if subj_lower in first_person_singular:
                # 'I is' or 'I are' -> 'I am'
                if verb_lower in ("is", "are"):
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} am",
                        "explanation": f"The pronoun 'I' pairs with 'am' in the present tense, not '{verb_lower}'.",
                        "span": (s_start, v_end)
                    })
                # 'I has' -> 'I have'
                elif verb_lower == "has":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} have",
                        "explanation": f"The pronoun 'I' takes 'have', not 'has'.",
                        "span": (s_start, v_end)
                    })
                # 'I does' -> 'I do'
                elif verb_lower == "does":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} do",
                        "explanation": f"The pronoun 'I' takes 'do', not 'does'.",
                        "span": (s_start, v_end)
                    })
                # 'I goes' / 'I plays' (3rd person singular verb with 'I')
                elif verb_lower in self.singular_to_base and verb_lower not in ("was", "is", "has", "does"):
                    base = self.singular_to_base[verb_lower]
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} {base}",
                        "explanation": f"The pronoun 'I' requires the base verb form '{base}', not the third-person '{verb_lower}'.",
                        "span": (s_start, v_end)
                    })

            # -----------------------------------------
            # 2. Singular 3rd-Person Pronouns ('he', 'she', 'it', 'this', 'that')
            # -----------------------------------------
            elif subj_lower in singular_3rd_pronouns:
                # 'He are' -> 'He is'
                if verb_lower == "are":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} is",
                        "explanation": f"Singular third-person subject '{subj_token}' requires the singular verb 'is', not 'are'.",
                        "span": (s_start, v_end)
                    })
                # 'He were' -> 'He was'
                elif verb_lower == "were":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} was",
                        "explanation": f"Singular subject '{subj_token}' takes 'was' in standard past tense, not 'were'.",
                        "span": (s_start, v_end)
                    })
                # 'He have' -> 'He has'
                elif verb_lower == "have":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} has",
                        "explanation": f"Singular subject '{subj_token}' requires 'has', not 'have'.",
                        "span": (s_start, v_end)
                    })
                # 'He do' -> 'He does'
                elif verb_lower == "do":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} does",
                        "explanation": f"Singular subject '{subj_token}' takes 'does', not 'do'.",
                        "span": (s_start, v_end)
                    })
                # Base verb instead of 3rd person singular (e.g., 'He go' -> 'He goes', 'She run' -> 'She runs')
                elif (verb_lower in self.irregular_verbs or verb_lower in self.common_regular_verbs):
                    s_verb = self.get_third_person_singular(verb_lower)
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} {s_verb}",
                        "explanation": f"Singular subject '{subj_token}' requires the 3rd-person singular present form '{s_verb}', not '{verb_lower}'.",
                        "span": (s_start, v_end)
                    })

            # -----------------------------------------
            # 3. Plural Pronouns ('they', 'we', 'you', 'these', 'those')
            # -----------------------------------------
            elif subj_lower in plural_pronouns:
                # 'They is' -> 'They are'
                if verb_lower == "is":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} are",
                        "explanation": f"Plural subject '{subj_token}' takes 'are', not 'is'.",
                        "span": (s_start, v_end)
                    })
                # 'They was' -> 'They were'
                elif verb_lower == "was":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} were",
                        "explanation": f"Plural subject '{subj_token}' takes 'were', not 'was'.",
                        "span": (s_start, v_end)
                    })
                # 'They has' -> 'They have'
                elif verb_lower == "has":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} have",
                        "explanation": f"Plural subject '{subj_token}' takes 'have', not 'has'.",
                        "span": (s_start, v_end)
                    })
                # 'They does' -> 'They do'
                elif verb_lower == "does":
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} do",
                        "explanation": f"Plural subject '{subj_token}' takes 'do', not 'does'.",
                        "span": (s_start, v_end)
                    })
                # 'They goes' / 'They runs' (singular verb with plural pronoun)
                elif verb_lower in self.singular_to_base and verb_lower not in ("is", "was", "has", "does"):
                    base = self.singular_to_base[verb_lower]
                    errors.append({
                        "rule": "Subject-Verb Agreement",
                        "found": f"{subj_token} {verb_token}",
                        "replacement": f"{subj_token} {base}",
                        "explanation": f"Plural subject '{subj_token}' requires the base plural verb form '{base}', not '{verb_lower}'.",
                        "span": (s_start, v_end)
                    })

        # -----------------------------------------
        # 4. Noun Phrase Agreement (e.g. 'The boy run' vs 'The boys runs')
        # -----------------------------------------
        for i in range(n - 2):
            det_token, d_start, _ = tokens[i]
            noun_token, n_start, n_end = tokens[i + 1]
            verb_token, v_start, v_end = tokens[i + 2]

            det_lower = det_token.lower()
            noun_lower = noun_token.lower()
            verb_lower = verb_token.lower()

            if det_lower in ("the", "a", "an", "this", "that", "my", "your", "his", "her", "our", "their"):
                # Case A: Singular noun with plural verb (e.g., 'The boy are here' or 'The boy run fast')
                is_plural_noun = noun_lower.endswith("s") and not noun_lower.endswith("ss") and noun_lower not in ("bus", "glass", "class")

                if not is_plural_noun:
                    # Singular noun + 'are'
                    if verb_lower == "are":
                        errors.append({
                            "rule": "Subject-Verb Agreement",
                            "found": f"{noun_token} {verb_token}",
                            "replacement": f"{noun_token} is",
                            "explanation": f"Singular noun '{noun_token}' takes 'is', not 'are'.",
                            "span": (n_start, v_end)
                        })
                    # Singular noun + base verb ('The boy run' -> 'The boy runs')
                    elif verb_lower in self.irregular_verbs or verb_lower in self.common_regular_verbs:
                        s_verb = self.get_third_person_singular(verb_lower)
                        errors.append({
                            "rule": "Subject-Verb Agreement",
                            "found": f"{noun_token} {verb_token}",
                            "replacement": f"{noun_token} {s_verb}",
                            "explanation": f"Singular noun '{noun_token}' requires singular verb '{s_verb}', not '{verb_lower}'.",
                            "span": (n_start, v_end)
                        })

                # Case B: Plural noun with singular verb (e.g., 'The boys is here' or 'The boys runs fast')
                else:
                    if verb_lower == "is":
                        errors.append({
                            "rule": "Subject-Verb Agreement",
                            "found": f"{noun_token} {verb_token}",
                            "replacement": f"{noun_token} are",
                            "explanation": f"Plural noun '{noun_token}' takes 'are', not 'is'.",
                            "span": (n_start, v_end)
                        })
                    elif verb_lower in self.singular_to_base and verb_lower not in ("is", "was", "has", "does"):
                        base = self.singular_to_base[verb_lower]
                        errors.append({
                            "rule": "Subject-Verb Agreement",
                            "found": f"{noun_token} {verb_token}",
                            "replacement": f"{noun_token} {base}",
                            "explanation": f"Plural noun '{noun_token}' takes plural verb '{base}', not singular '{verb_lower}'.",
                            "span": (n_start, v_end)
                        })

        return errors

    # -------------------------------------------------------------
    # Rule 5: Incorrect Verb Usage
    # -------------------------------------------------------------
    def check_incorrect_verbs(self, text: str) -> List[Dict[str, Any]]:
        errors = []
        tokens = self.tokenize(text)
        n = len(tokens)

        for i in range(n - 1):
            curr_token, c_start, _ = tokens[i]
            next_token, n_start, n_end = tokens[i + 1]

            curr_lower = curr_token.lower()
            next_lower = next_token.lower()

            # Handle optional 'not' (e.g. 'did not went', 'can not played')
            actual_verb_token = next_token
            actual_verb_lower = next_lower
            target_start = c_start
            target_end = n_end
            has_negation = False

            if curr_lower in ("not", "n't"):
                continue

            if next_lower in ("not", "n't") and (i + 2 < n):
                has_negation = True
                actual_verb_token = tokens[i + 2][0]
                actual_verb_lower = actual_verb_token.lower()
                target_end = tokens[i + 2][2]

            # -----------------------------------------
            # 1. Modal verbs followed by non-base verb
            # e.g., 'can played' -> 'can play', 'will went' -> 'will go', 'must comes' -> 'must come'
            # -----------------------------------------
            if curr_lower in self.modal_verbs:
                base = None
                if actual_verb_lower in self.past_to_base:
                    base = self.past_to_base[actual_verb_lower]
                elif actual_verb_lower in self.singular_to_base:
                    base = self.singular_to_base[actual_verb_lower]
                elif actual_verb_lower.endswith("ed"):
                    base = self.get_base_verb(actual_verb_lower)

                if base and base != actual_verb_lower:
                    replacement = f"{curr_token} not {base}" if has_negation else f"{curr_token} {base}"
                    found_phrase = f"{curr_token} not {actual_verb_token}" if has_negation else f"{curr_token} {actual_verb_token}"
                    errors.append({
                        "rule": "Incorrect Verb Usage",
                        "found": found_phrase,
                        "replacement": replacement,
                        "explanation": f"Modal verb '{curr_token}' must be followed by base form '{base}', not '{actual_verb_token}'.",
                        "span": (target_start, target_end)
                    })

            # -----------------------------------------
            # 2. Auxiliary 'do', 'does', 'did' + past/inflected verb
            # e.g., 'did went' -> 'did go', 'did saw' -> 'did see', 'does likes' -> 'does like'
            # -----------------------------------------
            if curr_lower in ("do", "does", "did"):
                base = None
                if actual_verb_lower in self.past_to_base:
                    base = self.past_to_base[actual_verb_lower]
                elif actual_verb_lower in self.singular_to_base:
                    base = self.singular_to_base[actual_verb_lower]
                elif actual_verb_lower.endswith("ed"):
                    base = self.get_base_verb(actual_verb_lower)

                if base and base != actual_verb_lower:
                    replacement = f"{curr_token} not {base}" if has_negation else f"{curr_token} {base}"
                    found_phrase = f"{curr_token} not {actual_verb_token}" if has_negation else f"{curr_token} {actual_verb_token}"
                    errors.append({
                        "rule": "Incorrect Verb Usage",
                        "found": found_phrase,
                        "replacement": replacement,
                        "explanation": f"Auxiliary '{curr_token}' must be followed by base verb form '{base}', not '{actual_verb_token}'.",
                        "span": (target_start, target_end)
                    })

            # -----------------------------------------
            # 3. Perfect aspect 'has', 'have', 'had' + simple past instead of past participle
            # e.g., 'has went' -> 'has gone', 'have wrote' -> 'have written', 'had ate' -> 'had eaten'
            # -----------------------------------------
            if curr_lower in ("has", "have", "had"):
                if actual_verb_lower in self.past_to_base:
                    base = self.past_to_base[actual_verb_lower]
                    if base in self.irregular_verbs:
                        correct_participle = self.irregular_verbs[base][2]
                        if actual_verb_lower != correct_participle:
                            replacement = f"{curr_token} not {correct_participle}" if has_negation else f"{curr_token} {correct_participle}"
                            found_phrase = f"{curr_token} not {actual_verb_token}" if has_negation else f"{curr_token} {actual_verb_token}"
                            errors.append({
                                "rule": "Incorrect Verb Usage",
                                "found": found_phrase,
                                "replacement": replacement,
                                "explanation": f"The auxiliary '{curr_token}' requires the past participle '{correct_participle}', not the simple past '{actual_verb_token}'.",
                                "span": (target_start, target_end)
                            })

            # -----------------------------------------
            # 4. Infinitive 'to' + inflected verb
            # e.g., 'to went' -> 'to go', 'to played' -> 'to play', 'to eats' -> 'to eat'
            # -----------------------------------------
            if curr_lower == "to" and not has_negation:
                base = None
                if next_lower in self.past_to_base:
                    base = self.past_to_base[next_lower]
                elif next_lower in self.singular_to_base:
                    base = self.singular_to_base[next_lower]
                elif next_lower.endswith("ed"):
                    base = self.get_base_verb(next_lower)

                if base and base != next_lower:
                    errors.append({
                        "rule": "Incorrect Verb Usage",
                        "found": f"to {next_token}",
                        "replacement": f"to {base}",
                        "explanation": f"The infinitive particle 'to' must be followed by the base verb '{base}', not '{next_token}'.",
                        "span": (c_start, n_end)
                    })

        return errors

    # -------------------------------------------------------------
    # Main Engine: Analyze & Produce Corrected Sentence
    # -------------------------------------------------------------
    def analyze(self, sentence: str) -> Dict[str, Any]:
        """
        Runs all rule checks on the input sentence and produces:
        - original_sentence
        - errors (list of detected errors with details)
        - corrected_sentence
        - total_errors
        """
        if not sentence or not sentence.strip():
            return {
                "success": False,
                "message": "Input is empty. Please enter an English sentence to check.",
                "original_sentence": "",
                "corrected_sentence": "",
                "errors": [],
                "total_errors": 0
            }

        raw_sentence = sentence.strip()

        # Collect errors from all rule modules
        detected_errors: List[Dict[str, Any]] = []
        detected_errors.extend(self.check_repeated_words(raw_sentence))
        detected_errors.extend(self.check_articles(raw_sentence))
        detected_errors.extend(self.check_incorrect_verbs(raw_sentence))
        detected_errors.extend(self.check_subject_verb_agreement(raw_sentence))
        detected_errors.extend(self.check_punctuation_and_capitalization(raw_sentence))

        # Deduplicate overlapping errors by span/found text
        unique_errors = []
        seen_spans = set()
        for err in detected_errors:
            key = (err.get("span"), err.get("rule"), err.get("found").lower())
            if key not in seen_spans:
                seen_spans.add(key)
                unique_errors.append(err)

        # Generate corrected sentence by applying replacements cleanly
        corrected = self._build_corrected_sentence(raw_sentence, unique_errors)

        return {
            "success": True,
            "message": "Grammar check completed successfully.",
            "original_sentence": raw_sentence,
            "corrected_sentence": corrected,
            "errors": [
                {
                    "rule": e["rule"],
                    "found": e["found"],
                    "replacement": e["replacement"],
                    "explanation": e["explanation"]
                }
                for e in unique_errors
            ],
            "total_errors": len(unique_errors)
        }

    def _build_corrected_sentence(self, original: str, errors: List[Dict[str, Any]]) -> str:
        """
        Applies fixes deterministically.
        Sorts errors by starting index descending so indices remain valid during replacement.
        """
        if not errors:
            return original

        # Filter out errors that have spans
        spanned_errors = [e for e in errors if "span" in e and e["span"]]
        # Sort descending by start index to avoid invalidating subsequent indices
        spanned_errors.sort(key=lambda x: x["span"][0], reverse=True)

        res = original
        for err in spanned_errors:
            start, end = err["span"]
            replacement = err["replacement"]
            # Apply replacement within boundaries
            res = res[:start] + replacement + res[end:]

        # Clean up any leftover artifacts
        res = re.sub(r"\s+", " ", res).strip()
        res = re.sub(r"\s+([,.;:?!])", r"\1", res)

        # Ensure sentence has terminal punctuation
        if res and res[-1] not in ".?!":
            res += "."

        # Ensure first character is capitalized
        if res and res[0].islower():
            res = res[0].upper() + res[1:]

        return res
