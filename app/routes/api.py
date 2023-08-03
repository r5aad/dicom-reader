from flask import Blueprint, jsonify, request

import app.services.dicom_service as dicom_service

api_bp = Blueprint("api", __name__, url_prefix="/v1")


@api_bp.route("/assets", methods=["POST"])
def handle_store_request():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]
    stored_asset = dicom_service.store(file)
    return jsonify(stored_asset.to_dict()), 200


@api_bp.route("/assets", methods=["GET"])
def handle_list_request():
    assets = dicom_service.list()
    assets = [asset.to_dict() for asset in assets]
    return jsonify(assets), 200


@api_bp.route("/assets/<id>", methods=["GET"])
def handle_get_request(id):
    asset = dicom_service.get(id)
    if asset is None:
        return jsonify({"error": f"No asset found against {id}"}), 404
    return jsonify(asset.to_dict()), 200


@api_bp.route("/assets/<id>/extract", methods=["GET"])
def handle_extract_request(id):
    try:
        tag_param = request.args.get("tag")
        tag_model = dicom_service.extract(id, tag_param)
        return jsonify(tag_model)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/assets/<id>/convert", methods=["GET"])
def handle_convert_request(id):
    response = dicom_service.dicom_to_png(id)
    return jsonify(response)


@api_bp.route("/health", methods=["GET"])
def handle_health_request():
    response = {"status": "pass"}
    return jsonify(response)
