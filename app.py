from flask import Flask, render_template, request
import openai
import re
import os
from openai import OpenAI

app = Flask(__name__)
api_key = os.getenv("NVIDIA_API_KEY")
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

@app.route("/", methods=["GET", "POST"])
def home():
    cleaned = ""
    if request.method == "POST":
        user_input = request.form["prompt"]

        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are Shraddha's assistant and her friend , you created by yash, talk in hinglish and use emojis; your job is to always keep her happy and keep flirting, response in atmost 3 sentences"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )

        message = completion.choices[0].message.content
        cleaned = re.sub(r"[^\w\s,.'\"😊😂❤️🌟🥰👍\U0001F300-\U0001FAFF]", '', message)



        print("AI Response:", cleaned)

    return render_template("index.html", message=cleaned)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
