import requests
from behave import *

BASE_URL = "http://localhost:8000"

@when('I send a POST request to "{url}" with a file')
def step_send_post_request(context, url):
    with open("test_file.dcm", "rb") as file:
        files = {"file": file}
        response = requests.post(BASE_URL + url, files=files)
    context.response = response

@then('the response status code should be {status_code:d}')
def step_check_response_status_code(context, status_code):
    assert context.response.status_code == status_code

@then('the response JSON should contain "id"')
def step_check_response_json_contains_key(context):
    assert "id" in context.response.json()
    context.id = context.response.json()["id"]

@then('the response JSON should be a list of assets')
def step_check_response_json_is_list_of_assets(context):
    assert isinstance(context.response.json(), list)

@when(u'I send a GET request to "/v1/assets"')
def step_send_get_request_list(context):
    context.response = requests.get(BASE_URL + "/v1/assets")

@when(u'I send a GET request to "/v1/assets/<id>"')
def step_send_get_request_by_id(context):
    context.response = requests.get(BASE_URL + f"/v1/assets/{context.id}")

@then(u'the response status code should be 200 or 404')
def step_check_response_status_code_200_404(context):
    assert context.response.status_code in [200, 404]

@then(u'the response JSON should contain "id", "path", and "name" or an error message')
def step_check_response_json_contains_id_path_name_or_error(context):
    response_data = context.response.json()
    if context.response.status_code == 200:
        assert "id" in response_data
        assert "path" in response_data
        assert "name" in response_data
    elif context.response.status_code == 404:
        assert "error" in response_data

@when(u'I send a GET request to "/v1/assets/<id>/extract" with query parameter "tag={tag}"')
def step_send_get_request_extract(context, tag):
    context.response = requests.get(BASE_URL + f"/v1/assets/{context.id}/extract?tag={tag}")

@then(u'the response status code should be 200 or 400')
def step_check_response_status_code_200_400(context):
    assert context.response.status_code in [200, 400]

@then(u'the response JSON should contain the extracted tag information')
def step_check_response_json_contains_extracted_tag_or_error(context):
    response_data = context.response.json()
    if context.response.status_code == 200:
        assert "tag_name" in response_data
        assert "attribute_value" in response_data
        assert response_data["tag_name"] == "PatientName"

@when(u'I send a GET request to "/v1/assets/<id>/convert"')
def step_send_get_request_convert(context):
    context.response = requests.get(BASE_URL + f"/v1/assets/{context.id}/convert")

@then(u'the response JSON should contain the converted PNG information')
def step_check_response_json_contains_converted_png(context):
    response_data = context.response.json()
    # Add assertions to check the converted PNG information
    assert "png_path" in response_data

@when(u'I send a GET request to "/v1/health"')
def step_send_get_request_health(context):
    context.response = requests.get(BASE_URL + "/v1/health")

@then(u'the response JSON should show status as passing')
def step_check_response_json_contains_extracted_tag_or_error(context):
    response_data = context.response.json()
    if context.response.status_code == 200:
        assert "status" in response_data
        assert response_data["status"] == "pass"