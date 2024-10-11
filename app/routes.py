from flask import Blueprint, jsonify, request
from app.response import GetAllVideosResponse
from app.use_case import (
    build_embed_url,
    calculate_offset,
    calculate_total_of_pages,
    extract_video_id_from_url,
    get_next_page,
    get_previous_page,
    youtube_url_is_valid,
)
from db.session import Media, Session
from sqlalchemy import select, text
from http import HTTPStatus


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
def check_database_connection():
    with Session() as session:
        try:
            session.execute(text("SELECT 1"))
            return jsonify({"message": "Running"}), HTTPStatus.OK
        except Exception as exc:
            return (
                jsonify({"error": f"Database error: {exc}"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )


@api.route("/videos", methods=["GET"])
def get_all_videos():
    query_params: dict = {
        "itemsPerPage": request.args.get("itemsPerPage", 10),
        "page": request.args.get("page", 1),
        "prev": request.args.get("prev", None),
        "next": request.args.get("next", None),
    }
    limit = int(query_params.get("itemsPerPage"))
    page = int(query_params.get("page"))
    offset = calculate_offset(page=page, items_per_page=limit)
    total_of_items = 0
    with Session() as session:
        items = session.scalars(
            select(Media).limit(limit).offset(offset).order_by(Media.media_id)
        )
        all_items = [
            {
                "id": item.media_id,
                "title": item.title,
                "url": build_embed_url(video_id=item.url),
            }
            for item in items
        ]
        total_of_items = session.query(Media).count()

    total_of_pages = calculate_total_of_pages(
        total_of_items=total_of_items, items_per_page=limit
    )

    response = GetAllVideosResponse(
        items=all_items,
        items_per_page=limit,
        total_of_pages=total_of_pages,
        page=page,
        prev_page=get_previous_page(page),
        next_page=get_next_page(current_page=page, total_of_pages=total_of_pages),
    )
    return jsonify({"success": response.get_response()}), HTTPStatus.OK


@api.route("/videos/<int:media_id>", methods=["GET"])
def get_one_video(media_id):
    with Session() as session:
        video = session.scalar(select(Media).where(Media.media_id == media_id))
        if not video:
            return (
                jsonify({"error": f"Vídeo de id {media_id} não encontrado!"}),
                HTTPStatus.NOT_FOUND,
            )
        item = {
            "id": video.media_id,
            "title": video.title,
            "url": build_embed_url(video_id=video.url),
        }

    return jsonify({"success": item}), HTTPStatus.OK


@api.route("/videos", methods=["POST"])
def save_new_video():
    data = request.get_json()
    if not data["title"] or not data["url"]:
        return (
            jsonify({"error": "Titulo ou URL do video não encontrados!"}),
            HTTPStatus.BAD_REQUEST,
        )

    url = data["url"]
    url_is_valid = youtube_url_is_valid(link=url)
    if not url_is_valid:
        return (
            jsonify({"error": "A URL do video não é válida!"}),
            HTTPStatus.BAD_REQUEST,
        )

    video_id = extract_video_id_from_url(url=url)
    if not video_id:
        return (
            jsonify({"error": "Erro interno ao extrair o ID do vídeo"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    with Session() as session:
        video = session.scalar(select(Media.url).where(Media.url == video_id))

    video_already_exists = video is not None

    if video_already_exists:
        return (
            jsonify({"error": "O vídeo especificado já existe na base de dados"}),
            400,
        )

    with Session() as session:
        media = Media(title=data["title"], url=video_id)
        session.add(media)
        session.commit()

    return jsonify({}), HTTPStatus.CREATED


@api.route("/videos/<int:media_id>", methods=["PUT"])
def edit_video(media_id):
    with Session() as session:
        video = session.scalar(select(Media).where(Media.media_id == media_id))
    if not video:
        return (
            jsonify(
                {
                    "error": f"Não foi possível editar, pois um vídeo com o id {media_id} não foi encontrado na base de dados!"
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()

    title = data.get("title") or video.title
    video_id = video.url
    if data.get("url"):
        url = data["url"]
        url_is_valid = youtube_url_is_valid(link=url)
        if not url_is_valid:
            return jsonify({"error": "A URL do video não é válida!"}), 400

        video_id = extract_video_id_from_url(url=url)
        if not video_id:
            return jsonify({"error": "Erro interno ao extrair o ID do vídeo"}), 500

    with Session() as session:
        another_video = session.scalar(
            select(Media.url).where(Media.url == video_id, Media.media_id != media_id)
        )

    url_already_exists = another_video is not None

    if url_already_exists:
        return (
            jsonify(
                {
                    "error": "O vídeo especificado já existe em outro registro da base de dados. Escolha uma URL diferente"
                }
            ),
            400,
        )

    with Session() as session:
        video.title = title
        video.url = video_id
        session.add(video)
        session.commit()

    return jsonify({"success": f"Video {media_id} atualizado com sucesso!"}), 200


@api.route("/videos/<int:media_id>", methods=["DELETE"])
def remove_video(media_id):
    with Session() as session:
        video = session.scalar(select(Media).where(Media.media_id == media_id))
    if not video:
        return (
            jsonify(
                {
                    "error": f"Não foi possível deletar o vídeo, pois um vídeo com o id {media_id} não foi encontrado na base de dados!"
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    with Session() as session:
        session.delete(video)
        session.commit()

    return (
        jsonify({"success": f"Video {media_id} deletado com sucesso!"}),
        HTTPStatus.OK,
    )


@api.route("/videos", methods=["DELETE"])
def remove_all_videos():
    with Session() as session:
        videos = session.scalars(select(Media))
    if not videos:
        return (
            jsonify({"error": f"Nenhum vídeo foi encontrado na base de dados!"}),
            HTTPStatus.BAD_REQUEST,
        )

    with Session() as session:
        videos = session.scalars(select(Media))
        for video in videos:
            session.delete(video)
        session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT
