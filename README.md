# DICOM Reader

## Features

* Accept and Upload a DICOM File: Easily upload your DICOM files to the API for processing and storage.

* Retrieve Single or Multiple Stored Files: You can fetch a single stored file by its unique ID or retrieve a list of all stored files.

* Extract and Return DICOM Header: Extract specific information from the DICOM header by providing a DICOM tag, and receive the corresponding attribute value.

* Convert DICOM to PNG: Seamlessly convert DICOM images to PNG format, making it easier to view and share.

Executable app behaviour: [features](./features/api.feature)

### APIs

[API specs](./api_spec.yml)


Save images:

```bash
curl --request POST \
  --url http://127.0.0.1:8000/v1/assets \
  --header 'Content-Type: multipart/form-data' \
  --form file=@file_path
```

Get image:

```bash
curl --request GET \
  --url http://127.0.0.1:8000/v1/assets/d3a8163b-90c2-438f-b530-e68b58a16170
```

List all images:

```bash
curl --request GET \
  --url http://127.0.0.1:8000/v1/assets
```

Extract tag data:

```bash
curl --request GET \
  --url 'http://127.0.0.1:8000/v1/assets/e5ab5fef-560b-43f2-b0e4-03b8968fd5ac/extract?tag=0010%2C0010' \
  --header 'Content-Type: application/json'
```

Convert to png. Note: If using docker, you would be able to see the png file in the mounted path

```bash
curl --request GET \
  --url http://127.0.0.1:8000/v1/assets/9541961a-c991-4f47-9849-9442d72e93aa/convert \
  --header 'Content-Type: application/json'
```

## Run locally

### Docker

The easiest way to run locally is using the docker container

In the root directory, run

```bash
docker build -t dicom_service .
```

Now run

```bash
docker run -p 8000:8000 -v /your_png_store_path/:/app/png_store/ 
-v /your_image_store_path/:/app/file_store/ 
dicom_service
```

### Pipenv

```bash
pip install pipenv
```

```bash
pipenv shell
```

```bash
gunicorn -b 0.0.0.0:8000 'app:create_app()'
```

## Development

Start by install all the dependencies

```bash
pip install -r requirements.txt 
```

Run code in debug mode

```bash
python run.py
```

Update requirements file.

```bash
pip freeze > requirements.txt
```

### Run tests

```bash
python -m pytest tests
```

For integration tests run:

```bash
behave
```

### Contribution

To contribute to the development of this API, please follow these steps:

* Clone the forked repository to your local machine
* Create a new branch for your changes
* Make your changes and commit them
* Before submitting a pull request, ensure that the code adheres to black coding standards. You can use the following commands to format your code:

```bash
pip freeze > requirements.txt
isort **.py
black **.py
```

* Push the changes to your GitHub repository: