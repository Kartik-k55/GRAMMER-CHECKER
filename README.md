# Grammar Error Detection Using Rule-Based NLP

A lightweight, transparent web application for detecting and correcting English grammatical errors using **Rule-Based Natural Language Processing (NLP)** built with **Python Flask**, **HTML5**, **CSS3**, and **JavaScript**.

---

## 📌 Project Overview

Unlike modern black-box machine learning or deep learning models that require heavy GPU resources and offer little explainability, this project utilizes **deterministic rule-based linguistic algorithms**. Every detected error corresponds to explicit grammatical rules, providing the learner with clear, human-readable explanations of *why* an error occurred and *how* to correct it.

---

## 🎯 Supported Grammar Rules

| Rule Category | Description | Incorrect Input Example | Correction |
|---|---|---|---|
| **Subject-Verb Agreement** | Ensures singular subjects take 3rd-person singular verbs and plurals take plural verbs. | *"He go to school."*<br>*"They is happy."*<br>*"The boys runs fast."* | *"He goes to school."*<br>*"They are happy."*<br>*"The boys run fast."* |
| **Incorrect Verb Usage** | Enforces bare infinitives following modal verbs & auxiliary *do/did*, and past participles following *has/have/had*. | *"He can played football."*<br>*"She did went home."*<br>*"They has went there."* | *"He can play football."*<br>*"She did go home."*<br>*"They have gone there."* |
| **Articles (`a`, `an`)** | Phonetic vowel sound checks, including silent *h* and consonant-vowel exceptions. | *"I ate a apple."*<br>*"She bought an car."*<br>*"We waited for a hour."* | *"I ate an apple."*<br>*"She bought a car."*<br>*"We waited for an hour."* |
| **Repeated Words** | Identifies accidental consecutive word duplicates. | *"We went to to the library."* | *"We went to the library."* |
| **Punctuation & Capitalization** | Checks starting letter capitalization, terminal punctuation (`. ? !`), spacing, and lowercase pronoun `i`. | *"he is a student , and i like him"* | *"He is a student, and I like him."* |

---

## 📂 Project Structure

```text
NLP2/
├── app.py                     # Flask web server and API endpoints
├── grammar_checker.py         # Rule-based NLP Grammar Checking Engine
├── requirements.txt           # Python dependencies (Flask, Flask-CORS)
├── test_grammar.py            # Automated test suite covering all rules
├── README.md                  # Project documentation & instructions
├── templates/
│   └── index.html             # Frontend HTML template
└── static/
    ├── css/
    │   └── style.css          # Modern dark/light UI styling & design tokens
    └── js/
        └── script.js          # Interactive frontend logic & API client
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8 or newer installed on your machine.
- Verify your Python version in your terminal:
  ```bash
  python --version
  ```

### 2. Install Required Dependencies
In the project directory, run:
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

### 1. Start the Flask Server
Run the following command in your terminal:
```bash
python app.py
```

You will see output similar to:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## 🌐 Deploying the Project

### Option A: Deploy to Netlify (100% Free & Instant)
This repository is configured for direct deployment on **Netlify**:
1. Go to [Netlify Drop](https://app.netlify.com/drop).
2. Drag and drop the `NLP2` folder (or push this repo to GitHub and connect to Netlify).
3. The project includes:
   - Root `index.html`
   - `_redirects` and `netlify.toml`
   - Automatic in-browser Rule-Based NLP engine fallback in `script.js` so it runs seamlessly on Netlify without needing an external Python server!

### Option B: Deploy with Live Python Flask Backend (Render / Railway)
If you want the Python backend running live in the cloud:
1. Push your repository to GitHub.
2. Go to [Render.com](https://render.com) and create a new **Web Service**.
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py` (or `gunicorn app:app`)
4. Your Flask backend and web interface will be live online!

---

## 🧪 Running Automated Tests

A dedicated test suite is included in `test_grammar.py` to verify each grammar rule category:
```bash
python test_grammar.py
```

---

## 💡 Key Design & Educational Highlights
- **100% Rule-Based NLP:** Uses deterministic linguistic patterns, tokenization, regular expressions, and morphological inflection dictionaries.
- **Explainable Feedback:** Every error clearly explains the grammatical principle being violated.
- **Robust Error Handling:** Validates empty input and congratulates the user when a sentence is 100% grammatically correct.
- **Responsive & Modern Design:** Dark and light theme toggle, smooth micro-animations, and clean cards.
