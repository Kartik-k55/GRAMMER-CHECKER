"""
Flask Application for Rule-Based Grammar Error Detection
Connects the frontend web interface with the rule-based NLP grammar checker.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from grammar_checker import RuleBasedGrammarChecker

app = Flask(__name__)
CORS(app)

# Initialize the rule-based grammar checker engine
checker = RuleBasedGrammarChecker()

# Sample sentences for quick testing
SAMPLE_SENTENCES = [
    {
        "category": "Subject-Verb Agreement",
        "sentence": "He go to school every morning.",
        "description": "Singular 3rd person 'He' with base verb 'go'"
    },
    {
        "category": "Subject-Verb Agreement",
        "sentence": "The boys runs very fast.",
        "description": "Plural subject 'boys' with singular verb 'runs'"
    },
    {
        "category": "Incorrect Verb Usage",
        "sentence": "She can played the guitar nicely.",
        "description": "Modal verb 'can' followed by past tense 'played'"
    },
    {
        "category": "Incorrect Verb Usage",
        "sentence": "They has went to the market.",
        "description": "Auxiliary 'has' with simple past 'went'"
    },
    {
        "category": "Article Error",
        "sentence": "I ate a apple and an car was parked outside.",
        "description": "'a' before vowel sound & 'an' before consonant sound"
    },
    {
        "category": "Repeated Words",
        "sentence": "We went to to the the library.",
        "description": "Accidental consecutive duplicated words"
    },
    {
        "category": "Punctuation & Capitalization",
        "sentence": "he is a good student , and i like him",
        "description": "Missing start capital, spacing before comma, lowercase 'i', missing period"
    },
    {
        "category": "Combined Errors",
        "sentence": "she can played with a apple in the the morning",
        "description": "Multiple grammar rules violated simultaneously"
    },
    {
        "category": "Error-Free Sentence",
        "sentence": "The diligent student writes clear notes every day.",
        "description": "Grammatically correct sentence test"
    }
]


@app.route("/")
def home():
    """Renders the main grammar checker web page."""
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_grammar():
    """
    API endpoint: Receives text input, performs rule-based NLP analysis,
    and returns detected errors, explanations, and corrected sentence.
    """
    try:
        data = request.get_json(silent=True) or request.form
        sentence = data.get("sentence", "").strip()

        if not sentence:
            return jsonify({
                "success": False,
                "message": "Please enter an English sentence to check.",
                "original_sentence": "",
                "corrected_sentence": "",
                "errors": [],
                "total_errors": 0
            }), 400

        result = checker.analyze(sentence)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred while analyzing the sentence: {str(e)}",
            "original_sentence": "",
            "corrected_sentence": "",
            "errors": [],
            "total_errors": 0
        }), 500


@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns curated example sentences for one-click testing in the UI."""
    return jsonify({"success": True, "samples": SAMPLE_SENTENCES}), 200


if __name__ == "__main__":
    print("Starting Rule-Based Grammar Checker on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
