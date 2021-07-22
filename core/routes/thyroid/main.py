from core.base import predictives
from models.thyroid.model import model
import re, json


class thyroid(predictives):
    def __init__(self):
        super().__init__()
        self.name = "thyroid_prediction"
        with open(
            "./core/routes/thyroid/entities.json", mode="r", encoding="utf-8"
        ) as jsonfile:
            self.entities = json.load(jsonfile)

        self.ai = model()

    def postprocessor(self, now_at, chat_doc, user_doc):
        attr = self.entities[now_at]["postp"]
        if attr == "y/n":
            if user_doc["answers"][chat_doc["id"]][now_at] == "Yes":
                user_doc["answers"][chat_doc["id"]][now_at] = int(1)
            else:
                user_doc["answers"][chat_doc["id"]][now_at] = int(0)

    def report(self, msg, chat_doc, user_doc):
        msg  = self.ai.predict(user_doc["answers"][chat_doc["id"]])

        msg += [
            "Our's is not medical advice. It is a predictive model.",
            "In any case, we would always recommend getting help from an actual professional."
        ]

        return msg

    def main(self, msg, chat_doc, user_doc):

        now_at = chat_doc["meta"]["now_at"]

        # Initial text
        if now_at == None:
            entity = {
                k: v
                for k, v in self.entities["start"].items()
                if k in ["msg", "options", "type"]
            }
            chat_doc["meta"]["now_at"] = "start"
            return entity
        # /

        if str(msg).lower() != "previous":

            # Validate the incoming msg
            # /

            # Log the answer
            if now_at == "start":
                user_doc["answers"][chat_doc["id"]] = {"quest": self.name}

            user_doc["answers"][chat_doc["id"]][now_at] = msg
            # /

            # Run post processor
            if self.entities[now_at]["postp"] != None:
                self.postprocessor(now_at, chat_doc, user_doc)
            # /

        # Renew the now_at
        if str(msg).lower() == "previous":
            chat_doc["meta"]["now_at"] = self.entities[now_at]["previous"]
        else:
            chat_doc["meta"]["now_at"] = self.entities[now_at]["next"]
        # /

        entity = {
            k: v
            for k, v in self.entities[chat_doc["meta"]["now_at"]].items()
            if k in ["msg", "options", "type"]
        }

        # Run the pre processor for next msg
        if self.entities[chat_doc["meta"]["now_at"]]["prep"] == "reporting":
            entity["msg"] = self.report(msg, chat_doc, user_doc)
        # /

        # End check
        if self.entities[chat_doc["meta"]["now_at"]]["next"] == None:
            chat_doc["meta"]["ended"] = True
        # /

        return entity
