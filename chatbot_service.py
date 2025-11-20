# chatbot_service.py
from rag_system import RAGSystem
from analysis_service import AnalysisService
from database_manager import DatabaseManager
from knowledge_graph_service import KnowledgeGraphService
import networkx as nx

class ChatbotService:
    def __init__(self, users_collection,chat_collection,analysis_service):
        self.rag_system = RAGSystem()
        self.analysis_service = analysis_service
        self.db_manager = DatabaseManager(users_collection=users_collection,chat_collection=chat_collection)
        #self.knowledge_graph_service = KnowledgeGraphService()
        #self.knowledge_graph_service.graph = nx.Graph() 
        
    def handle_chat_request(self, user_id, message):
        # 1. Detect original language
        original_lang = self.analysis_service.detect_language(message)
        print("original_lang:",original_lang)
        # 2. Translate to English if needed for processing
        english_message = message
        if original_lang in ["hindi", "hinglish"]:
            english_message = self.rag_system.translate_text(message, target_language="English")
        # 3. Get user data and determine disease/topic
        user_doc = self.db_manager.get_user_by_id(user_id)
        print(user_doc)
        disease = user_doc.get("topic") if user_doc else None

        # 4. Detect emotion from the English message
        emotion = self.analysis_service.detect_emotion(english_message)
        print("english_message:", english_message, emotion)
        print(disease)
        # 5. Summarize message for knowledge graph/future use (optional)
        summary = self.rag_system.summarize_for_knowledge(english_message)
        # You can now store this 'summary' in a separate collection or knowledge graph
        print(f"Knowledge Summary for {user_id}: {summary}")
        if disease is None or not disease:
            print("dieases.............")
            message_history = self.db_manager.get_recent_user_messages(user_id, limit=10) or []
            print("messages 🔹")
            # Phase 1: RAG screening phase for new user
            if len(message_history) < 5:
                topic = "initial-screening"  # Force topic
                bot_response = self.rag_system.generate_final_response(
                    english_message,topic,original_lang)
                self.db_manager.save_chat_history(user_id, message, bot_response, emotion)
                return {"reply": bot_response,"emotion": emotion}
            else:
                combined_text = " ".join(message_history)
                disease = self.analysis_service.detect_disease(combined_text)
                self.db_manager.create_or_update_user_disease(user_id, disease)


        # 6. Generate the RAG response in the original language
        bot_response = self.rag_system.generate_final_response(english_message, disease, original_lang)

        # 7. Save the conversation to the database
        self.db_manager.save_chat_history(user_id, message, bot_response, emotion)

        # 8. Add to knowledge graph
        '''
        self.knowledge_graph_service.add_user_chat(
            user_id=user_id,
            message=english_message,
            emotion=emotion,
            disease=disease,
            topic=disease
        )
        '''
        # 8. Return the final payload
        print(emotion)
        return {
            "reply": bot_response,
            "disease": disease,
            "emotion": emotion
        }