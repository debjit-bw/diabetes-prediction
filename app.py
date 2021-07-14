import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keys/FbAdminConfig.json"

from flask import Flask, request, render_template
from flask_firebase_admin import FirebaseAdmin

from database.manager import db_manager
from controller.main import driver
drivobj = driver()

db = db_manager()

app = Flask(__name__)
app.config["FIREBASE_ADMIN_RAISE_IF_APP_EXISTS"] = False

firebase = FirebaseAdmin(app)  # uses GOOGLE_APPLICATION_CREDENTIALS

# Routing here
@app.route("/")
def unprotected():
    return render_template("418.html"), 418


@app.route("/questionnaires")
@firebase.jwt_required  # This route now requires authorization via firebase jwt
def protected():

    # parse
    content = request.get_json()
    # /

    # chat_id fallback
    if "chat_id" not in content:
        content["chat_id"] = None
    # /

    # db query [GET]
    (user_doc, chat_doc) = db.getdata(
        request.jwt_payload["user_id"], content["chat_id"]
    )
    print(request.jwt_payload["user_id"])
    # /

    # Error redirection
    if type(user_doc) == int:
        return chat_doc, user_doc
    # /

    else:
        if "msg" in content:
            try:
                resp = drivobj.main(content["msg"], chat_doc, user_doc)
                resp["chat_id"] = chat_doc["id"]
                return resp
            finally:
                db.commit(user_doc, chat_doc)
        else:
            return {
                "msg": "msg parameter not found"
            }, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
