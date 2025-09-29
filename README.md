Minimal Questionnaire Website
============================

What this is
- A minimal Flask-based website that shows a 30-question questionnaire.
- Questions are grouped by domain (30 directories). For each domain the prompt text
  is read from domain/prompt/*.txt and one image is chosen randomly from domain/data/*.
- No login. The user supplies name, entry number, and gender and then answers 30 questions.
- Submissions are saved in `submissions/` as json files and appended to submissions.csv.

How to run
1. Create a Python 3.9+ virtualenv and install requirements:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the app (comment or uncomment for debug or production mode and change that in app.py as well):
   ```bash
   ./run.sh
   ```
3. Open http://127.0.0.1:5000 in your browser.

Replacing with your question bank
- Replace the `sample_questions` directory with your own directory that uses the same layout:
  - sample_questions/<domain_i>/prompts/*.txt
  - sample_questions/<domain_i>/data/*.png (or .jpg/.jpeg/.gif)
- The app will read domains automatically.
