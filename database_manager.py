# database_manager.py
from datetime import datetime
from bson import ObjectId,Binary

class DatabaseManager:
    def __init__(self, users_collection,chat_collection):
        self.users = users_collection
        self.chats = chat_collection

    def get_user(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def create_or_update_user_disease(self, user_id, disease):
        self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"disease": disease}},
            upsert=True
        )
    def get_user_by_id(self, user_id):
        user = self.users.find_one({"_id": ObjectId(user_id)})
        return user
    
    def get_recent_messages(self, user_id, limit=10):
        try:
            user = self.chats.find_one({"userId": ObjectId(user_id)})
            if not user or "conversations" not in user:
                return []
            return user["conversations"][-limit:]
        except Exception as e:
            print(f"Error fetching recent messages: {e}")
            return []
    
    def get_recent_user_messages(self, user_id, limit=10):
        messages = self.get_recent_messages(user_id, limit)
        user_messages = []
        for m in messages:
            user_text = m.get("user")  # safely get user text
            if user_text:
                user_messages.append(user_text)
        return user_messages

    
    def save_chat_history2(self, user_id, user_msg, bot_msg, emotion):
        conversation_record = {
            "user": user_msg,
            "bot": bot_msg,
            "emotion": emotion,
            "timestamp": datetime.utcnow()
        }
        self.chats.update_one(
            {"user_id": ObjectId(user_id)},
            {"$push": {"conversations": conversation_record}},
        )
    
    def save_chat_history(self, user_id, user_msg, bot_msg, emotion):
        conversationRecord = {
            "user": user_msg,
            "bot": bot_msg,
            "emotion": emotion,
            "timestamp": datetime.utcnow()
        }
        mood_History={
            "emotion": emotion,
            "timestamp": datetime.utcnow()
        }
        existing_chat = self.chats.find_one({"userId": ObjectId(user_id)})
        if not existing_chat:
            chat_doc = {
                "userId": ObjectId(user_id),
                "moodHistory": [mood_History],
                "conversations": [conversationRecord],
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
            self.chats.insert_one(chat_doc)
        else:
            self.chats.update_one(
                {"userId": ObjectId(user_id)},
                {"$push": {"conversations": conversationRecord,
                        "moodHistory":mood_History}},
            )











