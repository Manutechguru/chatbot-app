import os
import google.generativeai as genai
from flask import current_app

def get_chat_response(chat_history):
    api_key = current_app.config['GEMINI_API_KEY']
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # Create a single prompt from chat history (Gemini doesn't take structured role format)
        prompt = ""
        for msg in chat_history:
            role = msg['role'].capitalize()
            content = msg['content']
            prompt += f"{role}: {content}\n"
        prompt += "Assistant:"

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"





