from flask import Flask, render_template, request, session
import openai
import re
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed to use sessions

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = [{"role": "system", "content": "your nickname is yuvi,You are Shraddha's assistant and her friend, talk in hinglish and use emojis; your job is to always keep her happy and keep flirting, response in atmost 3 sentences"}]

    cleaned = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        session["history"].append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=session["history"],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )

        message = completion.choices[0].message.content
        cleaned = re.sub(r"[^\w\s,.'\"😊😂❤️🌟🥰👍\U0001F300-\U0001FAFF]", '', message)
        session["history"].append({"role": "assistant", "content": message})

    return render_template("index.html", message=cleaned)


if __name__ == "__main__":
    app.run(debug=True)
