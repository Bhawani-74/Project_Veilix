import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, send_from_directory, request, send_file
from Backend.models import db
from Backend.auth import auth

app = Flask(__name__, static_folder="../frontend", static_url_path="")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veilix.db"
app.config["SECRET_KEY"] = "secret"

db.init_app(app)
app.register_blueprint(auth)

# CREATE DB
with app.app_context():
    db.create_all()

# FRONTEND ROUTES
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# 🔥 PROTECT IMAGE ROUTE
@app.route("/protect", methods=["POST"])
def protect_image():
    if "image" not in request.files:
        return {"error": "No file uploaded"}

    file = request.files["image"]

    input_path = "temp_input.jpg"
    output_path = "temp_output.jpg"

    file.save(input_path)

    # CALL AI PIPELINE
    from Ai_engine.veilix_pipeline import process_veilix
    process_veilix(input_path, output_path)

    return send_file(output_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
