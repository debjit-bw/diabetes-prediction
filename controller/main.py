from core.routes.diabetes.main import diabetes

class driver:

    def __init__(self) -> None:
        self.quest_dict = {
            "diabetes_prediction": diabetes()
        }

    def main(self, msg, chat_doc, user_doc):
        if chat_doc["meta"]["ended"] == True:
            return {
                "msg": [
                    "Hey looks like this is an old window. Why don't you close this and start over?"
                ],
                "type": None
            }
        else:
            if chat_doc["meta"]["quest"] == None:
                if msg == None:
                    return {
                        "msg": [
                            "Hey! Here are the models currently available?",
                            "Choose one of these."
                        ],
                        "options": [
                            "Diabetes Prediction"
                        ]
                    }
                else:
                    if "diabetes prediction" in msg.lower():
                        chat_doc["meta"]["quest"] = "diabetes_prediction"
                        return self.quest_dict[chat_doc["meta"]["quest"]].main(msg, chat_doc, user_doc)
            else:
                if chat_doc["meta"]["quest"] in self.quest_dict:
                    return self.quest_dict[chat_doc["meta"]["quest"]].main(msg, chat_doc, user_doc)
                else:
                    return {
                        "msg": [
                            "Oops, something weird happened in the server. Try reloading."
                        ]
                    }