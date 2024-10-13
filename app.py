from flask import Flask, render_template, request, jsonify,redirect, url_for
from openai import OpenAI
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():

    print("Chat API called")
    # Retrieve the JSON data from the request
    data = request.get_json()
    user_message = data.get('prompt')

    if not user_message:
        return jsonify({'error': 'Message is required!'}), 400

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Call the OpenAI API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="gpt-3.5-turbo",
        )


        chat_response = response.choices[0].message.content.strip()
        print(chat_response)
        
        # Parse the response into a structured format
        recommendations = json.loads(chat_response)

        print(recommendations)

        # Render the response template with recommendations
        return jsonify(recommendations)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        mood = request.form['mood']
        recommendations = request.form['recommendations']
        return render_template('results.html', mood=mood, recommendations=json.loads(recommendations))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
