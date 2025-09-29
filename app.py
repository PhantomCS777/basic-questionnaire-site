from flask import Flask, render_template, jsonify, request, send_from_directory, abort
import os, random, csv, json, datetime
from pathlib import Path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration: where your question bank is located.
# By default the sample questions live inside "sample_questions" shipped with this project.
QUESTIONS_ROOT = Path(__file__).parent / "sample_questions"
SUBMISSIONS_DIR = Path(__file__).parent / "submissions"
SUBMISSIONS_DIR.mkdir(exist_ok=True)

def list_domains():
    # domains are directories inside QUESTIONS_ROOT
    return sorted([p.name for p in QUESTIONS_ROOT.iterdir() if p.is_dir()])

def choose_for_domain(domain):
    domain_path = QUESTIONS_ROOT / domain
    # pick a random prompt file from domain/prompt/*.txt
    prompt_dir = domain_path / "prompt"
    prompt_files = [p for p in prompt_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"]
    if not prompt_files:
        prompt_text = ""
    else:
        pf = random.choice(prompt_files)
        prompt_text = pf.read_text(encoding="utf-8")
    # pick a random image from domain/data/*
    data_dir = domain_path / "data"
    image_files = [p for p in data_dir.iterdir() if p.is_file() and p.suffix.lower() in [".png",".jpg",".jpeg",".gif"]]
    if not image_files:
        image_url = ""
    else:
        img = random.choice(image_files)
        # we will serve under /questions/<domain>/<filename>
        image_url = f"/questions/{domain}/{img.name}"
    return {"domain": domain, "prompt": prompt_text, "image": image_url}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_questions", methods=["GET"])
def get_questions():
    domains = list_domains()
    # build 30-question list (one per domain). If <30 domains, repeat/domains chosen cyclically.
    # We will keep original ordering of domains but sample images randomly per domain.
    questions = []
    for domain in domains:
        questions.append(choose_for_domain(domain))
    # If there are fewer than 30 domains, repeat domains to reach 30.
    while len(questions) < 30:
        for domain in domains:
            if len(questions) >= 30: break
            questions.append(choose_for_domain(domain))
    # If more than 30 domains, truncate to 30
    questions = questions[:30]
    return jsonify({"questions": questions})

@app.route("/questions/<path:filename>")
def serve_question_file(filename):
    # filename like "<domain>/image.png"
    safe_path = Path(filename)
    if ".." in filename or filename.startswith("/"):
        abort(404)
    parts = filename.split("/", 1)
    domain = parts[0]
    domain_dir = QUESTIONS_ROOT / domain
    if not domain_dir.exists():
        abort(404)
    # Serve from the domain 'data' directory if present
    candidate = domain_dir / "data" / (parts[1] if len(parts) > 1 else "")
    if candidate.exists():
        return send_from_directory(candidate.parent, candidate.name)
    abort(404)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    # expected fields: name, entry_number, gender, answers (list of answers)
    name = data.get("name","").strip()
    entry = data.get("entry_number","").strip()
    gender = data.get("gender","").strip()
    answers = data.get("answers", [])
    questions= data.get("questions", [])
    # print(questions)
    timestamp = datetime.datetime.utcnow().isoformat()
    filename = f"submission_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.json"
    out = {
        "name": name,
        "entry_number": entry,
        "gender": gender,
        "timestamp": timestamp,
        "answers": answers,
        "questions": questions
    }
    (SUBMISSIONS_DIR / filename).write_text(json.dumps(out, indent=2), encoding="utf-8")
    # also append to a CSV log
    csv_path = SUBMISSIONS_DIR / "submissions.csv"
    header = ["timestamp","name","entry_number","gender","answers_json","questions_json"]
    write_header = not csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([timestamp, name, entry, gender, json.dumps(answers, ensure_ascii=False), json.dumps(questions, ensure_ascii=False)])
    return jsonify({"status":"ok", "saved": filename})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
