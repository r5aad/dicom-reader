# DICOM Reader

## Features

* Accept and upload a dicom file
* Extract and return a header based on a dicom tag
* Converts dicom to PNG

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

### APIs

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

## Developement

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
