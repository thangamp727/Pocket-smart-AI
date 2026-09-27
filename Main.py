# Pocket-Smart-AI - Google Gemini Powered Assistant
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Gemini API Key - .env la irunthu edukkum
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Simple Frontend HTML
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Pocket Smart AI</title>
<style>
body{font-family:Arial;background:#f5f5f5;padding:20px}
.container{max-width:600px;margin:auto;background:white;padding:20px;border-radius:10px;box-shadow:0 0 10px #ccc}
input{width:80%;padding:10px} button{padding:10px;background:#4CAF50;color:white;border:none;cursor:pointer}
#ans{margin-top:20px;white-space:pre-wrap}
</style>
</head>
<body>
<div class="container">
<h2>🤖 Pocket Smart AI</h2>
<input id="q" placeholder="Enna kekanum ketu parunga...">
<button onclick="ask()">Ask</button>
<div id="ans"></div>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value;
 document.getElementById('ans').innerText='Thinking...';
 let res=await fetch('/ask?q='+encodeURIComponent(q));
 let data=await res.json();
 document.getElementById('ans').innerText=data.answer;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/ask")
def ask_ai():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"answer": "Question kudunga thanga!"})
    try:
        prompt = f"You are Pocket Smart AI, a helpful assistant. Answer clearly: {query}"
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)} Check API Key"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
