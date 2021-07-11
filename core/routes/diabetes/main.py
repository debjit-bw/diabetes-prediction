from core.base import predictives
from models.diabetes.model import model
import re, json


class diabetes(predictives):
    def __init__(self, retrain = False):
        super().__init__()
        self.name = "diabetes_prediction"
        with open("./core/routes/diabetes/entities.json", mode="r", encoding="utf-8") as jsonfile:
            self.entities =  json.load(jsonfile)

        self.ai = model(retrain)

    def postprocessor(self, now_at, chat_doc, user_doc):
        attr = self.entities[now_at]["postp"]
        if attr == "sex":
            if user_doc["answers"][chat_doc["id"]][now_at] == "Male":
                user_doc["answers"][chat_doc["id"]][now_at] = int(1)
            elif user_doc["answers"][chat_doc["id"]][now_at] == "Female":
                user_doc["answers"][chat_doc["id"]][now_at] = int(0)
            else:
                user_doc["answers"][chat_doc["id"]][now_at] = int(0.5)
        elif attr == "y/n":
            if user_doc["answers"][chat_doc["id"]][now_at] == "Yes":
                user_doc["answers"][chat_doc["id"]][now_at] = int(1)
            else:
                user_doc["answers"][chat_doc["id"]][now_at] = int(0)

    def report(self, msg, chat_doc, user_doc):
        ans_list = [user_doc["answers"][chat_doc["id"]]["start"]]
        for i in range(1, 16):
            ans_list.append(user_doc["answers"][chat_doc["id"]][str(i)])
        result = self.ai.predict(ans_list)[1]

        msg = []
        chance = int((result - 0.3)/(1.0 - 0.3)*100)
        if chance < 0:
            chance = 0

        if chance < 50:
            msg.append("You have an extremely low likelihood for diabetes.")
            msg.append("Eat and stay healthy.")
        elif chance < 70:
            msg.append("You have a low chance of diabetes.")
            msg.append("Eat and stay healthy.")
        elif chance < 80:
            msg.append("You have a moderate chance of diabetes.")
            msg.append("We would recommend getting checked up.")
        elif chance < 90:
            msg.append("You have a moderate to high chance of diabetes.")
            msg.append("We would recommend consulting a doctor.")
        elif chance < 95:
            msg.append("You have a high chance of diabetes.")
            msg.append("We would recommend immediate medical attention.")
        else:
            msg.append("You have a very high chance of diabetes.")
            msg.append("We would recommend immediately getting checked up.")
        
        msg.append("Our's is not medical advice. It is a predictive model.")
        msg.append("In any case, we would always recommend getting help from an actual professional.")

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
