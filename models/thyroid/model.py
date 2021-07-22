class model:
    def __init__(self) -> None:
        self.hypo = {
            "Dry skin": 0,
            "Puffy face": 1,
            "Muscle weakness": 2,
            "Elevated blood cholesterol level": 3,
            "Muscle aches, tenderness and stiffness": 4,
            "Pain, stiffness or swelling in your joints": 5,
            "Thinning hair": 6,
            "Depression": 7,
            "Yellowing of the skin and whites of the eyes (jaundice)": 8,
            "A large, protruding tongue.": 9,
            "Difficulty breathing.": 10,
            "Poor muscle tone": 11,
        }

        self.hyper = {
            "Increased appetite": 0,
            "Tremor, usually a fine trembling in your hands and fingers": 1,
            "Sweating": 2,
            "Nervousness, anxiety and irritability": 3,
            "Difficulty sleeping": 4,
            "Skin thinning": 5,
            "Fine, brittle hair": 6,
            "Dry, red or swollen eyes": 7,
            "Excessive tearing or discomfort in one or both eyes": 8,
            "Light sensitivity": 9,
            "Blurry or double vision, inflammation, or reduced eye movement": 10,
            "Protruding eyeballs": 11,
        }

        self.s_ops = {
            "Increased sensitivity to cold": 0,
            "Increased sensitivity to heat": 1,
            "Frequent bowels": 2,
            "Constipation": 3,
            "Unintentional weight loss": 4,
            "Weight Gain": 5,
            "Rapid, irregular heartbeat & pounding of your heart": 6,
            "Slowed heart rate": 7,
        }

        self.hypo_l = [1, 0, 0, 1, 0, 1, 0, 1]
        self.hyper_l = [0, 1, 1, 0, 1, 0, 1, 0]

        self.dot = lambda X, Y: sum(map(lambda x, y: x * y, X, Y))

    def make_preds(self, answers):

        duo = [0] * 8
        for i in range(2, 6):
            if answers[str(i)] != "None":
                duo[self.s_ops[answers[str(i)]]] = 1

        if sum(duo) == 0:
            duo_len = 1
        else:
            duo_len = sum([n ** 2 for n in duo]) ** 0.5
        hypo_dot_2 = self.dot(duo, self.hypo_l) / (2 * duo_len)
        hyper_dot_2 = self.dot(duo, self.hyper_l) / (2 * duo_len)

        hyper_3 = [0] * 11
        for s in answers["hyper"]:
            if s != "None":
                hyper_3[self.hyper[s]] = 1

        hypo_3 = [0] * 11
        for s in answers["hypo"]:
            if s != "None":
                hypo_3[self.hypo[s]] = 1

        if sum(hyper_3) == 0:
            hyper_3_len = 1
        else:
            hyper_3_len = sum([n ** 2 for n in hyper_3]) ** 0.5

        if sum(hypo_3) == 0:
            hypo_3_len = 1
        else:
            hypo_3_len = sum([n ** 2 for n in hypo_3]) ** 0.5

        hyper_dot_3 = self.dot(hyper_3, [1] * 11) / (11 ** 0.5 * hyper_3_len)
        hypo_dot_3 = self.dot(hypo_3, [1] * 11) / (11 ** 0.5 * hypo_3_len)

        msg = []

        if hyper_dot_2 + hypo_dot_2 < 0.4 and hyper_dot_3 + hypo_dot_3 < 0.4:
            msg += [
                "You do not seem to be experiencing much of the symptoms related to hypothyroidism and hyperthyroidism."
            ]
            if answers["start"] == 1:
                msg += [
                    "Since you described that the base of your neck is swollen, we would recommend you to go visit a medical professional."
                ]
            elif answers["1"] == 1:
                msg += [
                    "It is possible that you are not suffering from any thyroidism, and the fatigue is due to stress or some other disease.",
                    "We would advice you to go see a medical professional if you think something is wrong.",
                ]
            else:
                msg += [
                    "We would advice you to go see a medical professional if you think something is wrong.",
                    "Eat healthy and have a great day!",
                ]
        elif hyper_dot_2 >= hypo_dot_2 and hyper_dot_3 >= hypo_dot_3:
            msg += [
                "The symptoms you are describing largely point towards hypothyroidism"
            ]
            if hyper_dot_2 + hyper_dot_3 < 1:
                msg += [
                    "The severity is moderate, and we would recommend you to go see a medical professional."
                ]
            elif hyper_dot_2 + hyper_dot_3 < 1.5:
                msg += [
                    "The severity is on the higher side, and we would recommend immediate medical attention."
                ]
            else:
                msg += [
                    "The severity is high, and we would recommend you to go see a medical professional immediately."
                ]
        elif hypo_dot_2 >= hyper_dot_2 and hypo_dot_3 >= hyper_dot_3:
            msg += [
                "The symptoms you are describing largely point towards hypothyroidism"
            ]
            if hypo_dot_2 + hypo_dot_3 < 1:
                msg += [
                    "The severity is moderate, and we would recommend you to go see a medical professional."
                ]
            elif hypo_dot_2 + hypo_dot_3 < 1.5:
                msg += [
                    "The severity is on the higher side, and we would recommend immediate medical attention."
                ]
            else:
                msg += [
                    "The severity is high, and we would recommend you to go see a medical professional immediately."
                ]
        else:
            msg += [
                "The symptoms appear mixed. While you show some symptoms of hyperthyroidism, you also show some of hypothyroidism.",
                "If you feel something is wrong with your thyroid we would ask you to go see a medical professional",
            ]
            if hypo_dot_2 + hypo_dot_3 > hyper_dot_2 + hyper_dot_3:
                msg += [
                    "Based on our tests, we found an inclination towards hypothyroidism."
                ]
            else:
                msg += [
                    "Based on our tests, we found an inclination towards hyperthyroidism."
                ]
        print(f"Hyper 2: {hyper_dot_2} \t Hyper 3: {hyper_dot_3}")
        print(f"Hypo 2: {hypo_dot_2} \t Hypo 3: {hypo_dot_3}")

        return msg

    def predict(self, inputs):
        return self.make_preds(inputs)
