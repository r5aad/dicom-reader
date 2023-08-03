import os
import pydicom
from PIL import Image

from app.models.models import Asset

class LocalFileStore:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.store_bucket = os.path.join(os.getcwd(), bucket_name)
        os.makedirs(self.store_bucket, exist_ok=True)

    def upload(self, file, file_name):
        file_path = os.path.join(self.store_bucket, file_name)
        file.save(file_path)
        return file_path

    def get_base_dir(self):
        return self.store_bucket

file_store = LocalFileStore(bucket_name='file_store')
png_store = LocalFileStore(bucket_name='png_store')

def store(file):
    base_dir = file_store.get_base_dir()
    new_asset = Asset(base_dir, file.filename)
    file_store.upload(file, new_asset.id)
    new_asset.save()
    return new_asset

def read_dicom_header(dicom_file_path):
    dicom_data = pydicom.dcmread(dicom_file_path)
    return dicom_data

def transform_to_hex(tag_str):
    group_str, element_str = tag_str.split(',')
    group_number = int(group_str, 16)
    element_number = int(element_str, 16)
    return (group_number, element_number)

def extract(id, tag):
    asset = get(id)
    if asset is None:
        raise ValueError("No asset found against id: " + str(id))
    dicom_file_path = asset.path
    dicom_data = read_dicom_header(dicom_file_path)
    tag = transform_to_hex(tag)
    if tag not in dicom_data:
        raise ValueError("Invalid DICOM tag: " + str(tag))
    attribute_value = str(dicom_data[tag].value)
    tag_name = pydicom.datadict.keyword_for_tag(tag)
    tag_model = {
        'attribute_value': attribute_value,
        'tag_name': tag_name
    }
    return tag_model

def dicom_to_png(id):
    asset = get(id)
    dicom_file_path = asset.path
    dicom_data = pydicom.dcmread(dicom_file_path)
    if 'PixelData' not in dicom_data:
        raise ValueError("DICOM image has no pixel data")
    pixel_array = dicom_data.pixel_array
    image = Image.fromarray(pixel_array)
    base_dir = png_store.get_base_dir()
    stored_path = png_store.upload(image, asset.name + '.png')
    return {
        'id': asset.id,
        'path': asset.path,
        'name': asset.name,
        'png_path': f"file://{stored_path}"
    }

def list():
    return Asset.query.all()

def get(id):
    return Asset.query.get(id)