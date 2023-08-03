import json

import pytest
from flask import Flask

import app.services.dicom_service as dicom_service
from app.models.models import Asset
from app.routes.api import api_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app


def test_handle_list_request(app, monkeypatch):
    sample_assets = [
        Asset(base_dir="path/", name="Asset 1"),
        Asset(base_dir="path/", name="Asset 2"),
        Asset(base_dir="path/", name="Asset 3"),
    ]
    monkeypatch.setattr(dicom_service, "list", lambda: sample_assets)
    client = app.test_client()
    response = client.get("/v1/assets")
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == len(sample_assets)
