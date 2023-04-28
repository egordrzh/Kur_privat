import json

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
    return response.text

def get_info_to_str(dict_json):
    params = ['tag', 'coord', 'sex', 'emotion', 'age']
    info = dict_json['body']['objects'][0]['persons']
    result_str = ""
    with open('Kursach.txt', 'r') as fn:
        file_name = fn.read()

    # create name dict
    name_dict = {}
    for line in file_name.splitlines():
        name_dict[(line.split(': '))[0]] = (line.split(': '))[1]

    for per in info:
        if (per[params[0]] != 'undefined'): # if tag != undefined
            true_name = ""
            if per[params[0]] in name_dict.keys():
                true_name = name_dict[per[params[0]]]
            for param in params:
                if (param == "tag"):
                    result_str += str(param) + " - " + str(per[param]) + " " + str(true_name) + '\n'
                else:
                    result_str += str(param) + " - " + str(per[param]) + '\n'
            result_str += "------------------------------\n"
    return result_str

if __name__ == '__main__':
    set_postman()
    text_json = json.loads(recognize_request())
    info = get_info_to_str(text_json)
    print(info)
    f = open('persons_info.txt', 'w')
    f.write(info)
    f.close()
