import requests

def set_request():
    url = 'https://smarty.mail.ru/api/v1/persons/set'
    oauth_token = '2tbQtCJ6H9g4fjU4eH5jkrZRrw2qmfHVNCGYopbGSmTYoKJpPu'
    oauth_provider = 'mcs'

    headers = {'accept': 'application/json'}

    files = [
        ('file', ('ded1.jpg', open('C:\\Users\\Acer\\Desktop\\kur\\Egor.jpg', 'rb'), 'image/jpeg'))
    ]

    meta1 = {"space": "1", "images": [{"name": "file", "person_id": 1}]}

    data = {"meta": str(meta1)}

    response = requests.post(url, headers=headers, data=data, files=files,
                             params={'oauth_token': oauth_token, 'oauth_provider': oauth_provider})

    print(response.json())


def set_postman():
    url = "https://smarty.mail.ru/api/v1/persons/set?oauth_token=2tbQtCJ6H9g4fjU4eH5jkrZRrw2qmfHVNCGYopbGSmTYoKJpPu&oauth_provider=mcs"

    payload = {'meta': '{"space": "5", "images": [{"name": "file", "person_id": 1}]}'}
    files = [
        (
        'file', ('ded1.jpg', open('C:\\Users\\Acer\\Desktop\\kur\\Egor.jpg', 'rb'), 'image/jpeg'))
    ]
    headers = {
        'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.json())


def recognize_request():
    url = "https://smarty.mail.ru/api/v1/persons/recognize?oauth_token=2tbQtCJ6H9g4fjU4eH5jkrZRrw2qmfHVNCGYopbGSmTYoKJpPu&oauth_provider=mcs"

    payload = {'meta': '{"space": "5", "create_new": false, "images": [{"name": "file"}]}'}
    files = [
        ('file', ('rtf.jpeg', open('C:\\Users\\Acer\\Desktop\\kur\\rtf.jpg', 'rb'), 'image/jpeg'))
    ]
    headers = {
        'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.json())


if __name__ == '__main__':
    set_postman()
    recognize_request()

