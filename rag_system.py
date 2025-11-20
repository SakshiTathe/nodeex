# rag_system.py
import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import torch
import re
import google.generativeai as genai
from config import AVAILABLE_TOPICS
from config import api_key,dialogues_path

class RAGSystem:
    def __init__(self):
        print("🔧 Initializing RAG System...")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        self.encoder_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.rag_contexts = {}
        self._load_dialogues()
        print("✅ RAG System Initialized.")

    def _load_dialogues(self):
        for topic in AVAILABLE_TOPICS:
            filepath = os.path.join(dialogues_path, f"{topic}.csv")
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)

                docs = (df['questionText'].astype(str) + " " + df['answerText'].astype(str)).dropna().tolist()
                embeddings = self.encoder_model.encode(docs, convert_to_tensor=True).cpu().numpy().astype("float32")
                index = faiss.IndexFlatL2(embeddings.shape[1])
                index.add(embeddings)
                
                self.rag_contexts[topic] = {'docs': docs, 'index': index}


    def get_rag_context(self, query, topic, k=2):
        context_data = self.rag_contexts.get(topic, self.rag_contexts.get('counseling-fundamentals'))
        if not context_data:
            return ""
        q_embed = self.encoder_model.encode([query]).astype("float32")
        _, indices = context_data['index'].search(q_embed, k)
        return ' '.join([context_data['docs'][i] for i in indices[0]])
        
    def generate_final_response(self, user_message, topic, lang):
        rag_context_str = self.get_rag_context(user_message, topic)

        lang_instructions = {
            "hinglish": "Respond naturally in Hinglish with empathy.",
            "hindi": "Respond in simple Hindi empathetically.",
            "english": "Respond in English naturally and empathetically."
        }

        prompt = f"""
        You are a compassionate mental health chatbot. The user is talking about '{topic}'.
        Instruction: {lang_instructions.get(lang, lang_instructions['english'])}

        Use these dialogue examples for tone: "{rag_context_str}"
        User's message: "{user_message}"

        Provide a supportive, brief, and natural response.
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()

    def translate_text(self, text, target_language="English"):
        prompt = f"Translate the following text to {target_language}, preserving the emotional tone: \"{text}\". Output only the translation."
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()

    def summarize_for_knowledge(self, user_message):
        prompt = f"""
        Analyze this user's message. Extract the primary mental health concern, key symptoms, and potential triggers.
        Message: "{user_message}"
        Summary:
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text.strip()
