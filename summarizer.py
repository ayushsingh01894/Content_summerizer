from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=api_key)

# Summary Function
def summarize_text(text, summary_type):

    prompt = f"""
    Summarize the following content.

    Summary Type: {summary_type}

    Content:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# Key Points Function
def extract_keypoints(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Extract the 5 most important key points from:

                {text}
                """
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def extract_keywords(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Extract the top 10 important keywords from the following content.

                Return only keywords in bullet points.

                Content:
                {text}
                """
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def translate_summary(text, language):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Summarize the following content in {language} language.

                Content:
                {text}
                """
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def chat_with_document(document_text, question):

    prompt = f"""
    You are an AI assistant.

    Use ONLY the document content below
    to answer the question.

    DOCUMENT:
    {document_text}

    QUESTION:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def analyze_resume(text):

    prompt = f"""
    Analyze this resume.

    Give:

    1. Resume Score out of 100
    2. Technical Skills
    3. Strengths
    4. Missing Skills
    5. Improvement Suggestions

    Resume:

    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content