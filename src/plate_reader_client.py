import requests

HOST = 'http://127.0.0.1:8080'

class PlateReaderClient:
    def __init__(self, host=HOST):
        self.host = host

    def read_plate_number_from_image(self, image: bytes):
        response = requests.post(
            f'{self.host}/read_plate_number',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=image
        )
        return response.json()

    def read_plate_number_from_id(self, image_id: int):
        response = requests.get(
            f'{self.host}/read_plate_number/{image_id}'
        )
        return response.json()

    def read_plate_number_from_ids(self, image_ids: list[int]):
        response = requests.get(
            f'{self.host}/read_plate_number',
            params={'ids': ','.join(map(str, image_ids))}
        )
        return response.json()

if __name__ == '__main__':
    client = PlateReaderClient()
    
    # read_plate_number_from_image
    with open('../images/9965.jpg', 'rb') as image:
        res = client.read_plate_number_from_image(image)
        print(res)
        
    # read_plate_number_from_id
    res = client.read_plate_number_from_id(10022)
    print(res)
    
    # read_plate_number_from_ids
    res = client.read_plate_number_from_ids([10022, 9965, 9965, 9965, 10022])
    print(res)
