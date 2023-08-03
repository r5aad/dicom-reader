import os
import pydicom
from PIL import Image

from app.models.models import Asset

class LocalFileStore:

    def __init__(self, bucket_name):
        self.store_bucket = bucket_name

    def upload(self, file, file_path):
        """
        Upload a file to the image store
        """
        file.save(file_path)
        return file_path

    def get_file_path(self, filename):
        upload_folder = os.path.join(os.getcwd(), self.store_bucket)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        return file_path

file_store = LocalFileStore(bucket_name='file_store')
png_store = LocalFileStore(bucket_name='png_store')

def store(file):
    """
    Store a file in the upload folder
    """
    file_path = file_store.get_file_path(file.filename)
    new_asset = Asset(file_path, file.filename)
    file_store.upload(file, new_asset.path)
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
    """
    Extract a DICOM tag from an image
    """
    # upload_folder = os.path.join(os.getcwd(), 'file_store')
    # dicom_file_path = os.path.join(upload_folder, "IM000001")

    # get the file path from the database
    asset = Asset.query.get(id)
    dicom_file_path = asset.path
    dicom_data = read_dicom_header(dicom_file_path)
    tag = transform_to_hex(tag)
    if tag not in dicom_data:
        raise ValueError("Invalid DICOM tag: " + str(tag))
    attribute_value = str(dicom_data[tag].value)
    tag_name = pydicom.datadict.keyword_for_tag(tag)
    tag_model = {
        'tag': tag,
        'attribute_value': attribute_value,
        'tag_name': tag_name
    }
    return tag_model

def dicom_to_png(id):
    asset = Asset.query.get(id)
    dicom_file_path = asset.path
    dicom_data = pydicom.dcmread(dicom_file_path)
    if 'PixelData' not in dicom_data:
        raise ValueError("DICOM image has no pixel data")
    pixel_array = dicom_data.pixel_array
    image = Image.fromarray(pixel_array)

    file_path = png_store.get_file_path(asset.name + '.png')
    png_store.upload(image, file_path)
    return {
        'id': asset.id,
        'path': file_path,
        'name': asset.name,
        'png_path': f"file://{file_path}"
    }
