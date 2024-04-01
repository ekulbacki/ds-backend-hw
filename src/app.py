import logging
import requests

from io import BytesIO
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
from exceptions import *

IMAGE_PATH = 'http://178.154.220.122:7777/images'
VALID_IDS = {10022, 9965}

app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


def plate_number_from_image(image: bytes):
    try:
        result = plate_reader.read_text(image)
    except InvalidImage:
        raise InvalidImageError()

    return {
        'plate_number': result
    }


def download_image(image_id, image_path=IMAGE_PATH):
    if not isinstance(image_id, int):
        try:
            image_id = int(image_id)
        except:
            raise InvalidImageIdError()
    
    if image_id not in VALID_IDS:
        raise InvalidImageIdError()
    
    image_url = f'{image_path}/{image_id}'
    
    try:
        response = requests.get(image_url, timeout=5)
    except requests.exceptions.Timeout:
        raise DownloadTimeoutError()
        
    if response.status_code == 404:
        raise ImageNotFoundError()
    elif response.status_code != 200:
        raise ServiceUnavailableError()
    
    image = BytesIO(response.content)
    return image


# <url>:8080/read_plate_number : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/read_plate_number', methods=['POST'])
def read_plate_number():
    try:
        image = request.get_data()
        image = BytesIO(image)
        result = plate_number_from_image(image)
    except Exception as e:
        return {'error': e.message}, e.status_code
    return result


# <url>:8080/read_plate_number/<int:image_id>
# {"plate_number": "c180mv ..."}
@app.route('/read_plate_number/<int:image_id>', methods=['GET'])
def read_plate_number_by_id(image_id):
    try:
        image = download_image(image_id)
        result = plate_number_from_image(image)
    except Exception as e:
        return {'error': e.message}, e.status_code
    return result


# <url>:8080/read_plate_number/ids=<int:image_id>,<int:image_id>
# {"plate_number": "c180mv ..."}
@app.route('/read_plate_number', methods=['GET'])
def read_plate_number_by_ids():
    image_ids = request.args.get('ids')
    if not image_ids:
        e = NoIdsProvidedError()
        return {'error': e.message}, e.status_code
    image_ids = image_ids.split(',')
    results = []
    for image_id in image_ids:
        try:
            image = download_image(image_id)
            result = plate_number_from_image(image)
            results.append({image_id: result})
        except Exception as e:
            results.append({image_id: {'error': e.message}})
            
    return results   


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
