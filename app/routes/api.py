from flask import Blueprint, request, jsonify

import app.services.dicom_service as dicom_service

api_bp = Blueprint('api', __name__, url_prefix='/v1')

@api_bp.route('/assets', methods=['POST'])
def handle_store_request():
    """
    Store a DICOM file in the upload folder
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    stored_asset =dicom_service.store(file)
    response = {
        'id': stored_asset.id,
        'path': stored_asset.path,
        'name': stored_asset.name
    }
    return jsonify(response), 200

@api_bp.route('/assets/<id>/extract', methods=['GET'])
def handle_extract_request(id):
    tag_param = request.args.get('tag')
    tag_model = dicom_service.extract(id, tag_param)
    return jsonify(tag_model)

@api_bp.route('/assets/<id>/convert', methods=['GET'])
def handle_convert_request(id):
    response = dicom_service.dicom_to_png(id)
    return jsonify(response)

@api_bp.route('/health', methods=['GET'])
def handle_health_request():
    response = {
        'status': 'pass'
    }
    return jsonify(response)
