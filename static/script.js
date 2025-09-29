let questions = [];
let answers = [];
let current = 0;

document.getElementById("startBtn").addEventListener("click", async ()=>{
  const name = document.getElementById("name").value.trim();
  const entry = document.getElementById("entry").value.trim();
  const gender = document.getElementById("gender").value;
  if(!name || !entry){ alert("Please provide name and entry number."); return; }
  // fetch questions
  const res = await fetch("/get_questions");
  const data = await res.json();
  questions = data.questions;
  answers = new Array(questions.length).fill("");
  document.getElementById("userinfo").classList.add("hidden");
  document.getElementById("questionArea").classList.remove("hidden");
  document.getElementById("qnum").innerText = 1;
  showQuestion(0);
});

function showQuestion(i){
  current = i;
  const q = questions[i];
  document.getElementById("promptText").innerText = q.prompts || "(no prompt)";
  // if(q.image){
  //   document.getElementById("qimg").src = q.image;
  //   document.getElementById("qimg").style.display = "block";
  // } else {
  //   document.getElementById("qimg").style.display = "none";
  // }

  const imageContainer = document.getElementById("image-container");
const img = document.getElementById("question-image");
const pairDiv = document.getElementById("question-image-pair");

if (q.image) {
    imageContainer.style.display = "block";
    img.style.display = "block";
    img.src = q.image;
    pairDiv.innerHTML = "";
} else if (q.image_pair) {
    imageContainer.style.display = "block";
    img.style.display = "none";
    pairDiv.innerHTML = "";
    q.image_pair.forEach(url => {
        const im = document.createElement("img");
        im.src = url;
        im.style.maxWidth = "300px";
        im.style.border = "2px solid #000";
        pairDiv.appendChild(im);
    });
} else {
    imageContainer.style.display = "none";
}


  document.getElementById("answer").value = answers[i] || "";
  document.getElementById("qnum").innerText = (i+1);
  // toggle buttons
  document.getElementById("prevBtn").disabled = (i===0);
  document.getElementById("nextBtn").disabled = (i===questions.length-1);
  if(i===questions.length-1){
    document.getElementById("submitBtn").classList.remove("hidden");
  } else {
    document.getElementById("submitBtn").classList.add("hidden");
  }
}

document.getElementById("prevBtn").addEventListener("click", ()=>{
  answers[current] = document.getElementById("answer").value;
  if(current>0) showQuestion(current-1);
});
document.getElementById("nextBtn").addEventListener("click", ()=>{
  answers[current] = document.getElementById("answer").value;
  if(current<questions.length-1) showQuestion(current+1);
});
document.getElementById("submitBtn").addEventListener("click", async ()=>{
  answers[current] = document.getElementById("answer").value;
  const payload = {
    name: document.getElementById("name").value.trim(),
    entry_number: document.getElementById("entry").value.trim(),
    gender: document.getElementById("gender").value,
    answers: answers,
    questions: questions
  };
  const res = await fetch("/submit", {
    method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload)
  });
  const r = await res.json();
  document.getElementById("questionArea").classList.add("hidden");
  document.getElementById("thanks").classList.remove("hidden");
  document.getElementById("result").innerText = "Saved as: " + (r.saved || "(unknown)");
});
