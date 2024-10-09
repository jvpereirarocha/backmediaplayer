from flask import Blueprint, jsonify, request
from db.session import Session
from sqlalchemy import text


api = Blueprint("media", __name__, url_prefix="/media")


@api.after_request
def set_response_after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Content-Type"] = "application/json"
    response.headers["X-Req-Origin"] = "backend"
    return response


@api.route("/health", methods=["GET"])
def check_database_conneection():
    with Session() as session:
        try:
            session.execute(text("SELECT 1"))
            return jsonify({"message": "Running"}), 200
        except Exception as exc:
            return jsonify({"error": f"Database error: {exc}"}), 500


@api.route("/videos", methods=["GET"])
def get_all_videos():
    items = [
        {"title": "SRE - Fabricio Veronez", "url": "https://www.youtube.com/embed/Juz7afZO8s"},
        {"title": "TNT", "url": "https://www.youtube.com/embed/92MpKa1J8-0"},
        {"title": "SRE - Fabricio Veronez", "url": "https://www.youtube.com/embed/Juz7afZO8s"},
        {"title": "TNT", "url": "https://www.youtube.com/embed/92MpKa1J8-0"},
    ]
    return jsonify({"success": items}), 200


@api.route("/save", methods=["POST"])
def save_new_video():
    data = request.get_json()
    if not data["title"] or not data["url"]:
        return jsonify({"error": "Titulo ou URL do video não encontrados!"}), 400

    return jsonify({}), 201