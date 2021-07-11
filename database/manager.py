import random, string
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "yoboshu-datasc-trial01",
    },
)

db = firestore.client()


def randomalnum(n):
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits,
            k=n,
        )
    )


class db_manager:
    def __init__(self) -> None:
        pass

    def getdata(self, user_id, chat_id=None):
        if chat_id != None:
            chat_doc = db.collection("questionnaires_chats").document(chat_id).get()
            if chat_doc.exists:
                chat_doc = chat_doc.to_dict()
                if chat_doc["user_id"] == user_id:
                    user_doc = (
                        db.collection("questionnaires_users").document(user_id).get()
                    )
                    if user_doc.exists:
                        user_doc = user_doc.to_dict()
                        return (user_doc, chat_doc)
                    else:
                        return (404, {"messege": "User not found for given chat"})
                else:
                    return (400, {"messege": "Chat and User mismatch"})
            else:
                return (404, {"messege": "Chat not found for given id"})
        else:
            user_doc = db.collection("questionnaires_users").document(user_id).get()
            if user_doc.exists:
                user_doc = user_doc.to_dict()
                chat_id = randomalnum(20)
                user_doc["chats"].append(chat_id)
                chat_doc = {
                    "id": chat_id,
                    "user_id": user_id,
                    "logs": [],
                    "meta": {"quest": None, "vars": {}, "now_at": None, "ended": False},
                }
                return (user_doc, chat_doc)
            else:
                user_id = user_id
                chat_id = randomalnum(20)
                user_doc = {"id": user_id, "chats": [chat_id], "answers": {}}
                chat_doc = {
                    "id": chat_id,
                    "user_id": user_id,
                    "logs": [],
                    "meta": {"quest": None, "vars": {}, "now_at": None, "ended": False},
                }
                return (user_doc, chat_doc)

    def commit(self, user_doc, chat_doc):
        batch = db.batch()

        user_ref = db.collection("questionnaires_users").document(user_doc["id"])
        batch.set(user_ref, user_doc)

        chat_ref = db.collection("questionnaires_chats").document(chat_doc["id"])
        batch.set(chat_ref, chat_doc)

        batch.commit()
