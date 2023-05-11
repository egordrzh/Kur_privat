import json
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import *
def set_postman():
    url = "https://smarty.mail.ru/api/v1/persons/set?oauth_token=2EgmoAre8BLsyaPGbHyRAoze2VwWUYdR1gyupR7eSfoCK96C2D&oauth_provider=mcs"
    payload = {'meta': '{"space": "1", "images": [{"name": "file", "person_id": '+ input_id.get(1.0, "end-1c") + ' }]}'}

    files = [
        (
        'file', (file_path.split('/')[-1], open(file_path, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.json())


def recognize_request():
    url = "https://smarty.mail.ru/api/v1/persons/recognize?oauth_token=2EgmoAre8BLsyaPGbHyRAoze2VwWUYdR1gyupR7eSfoCK96C2D&oauth_provider=mcs"

    payload = {'meta': '{"space": "1", "create_new": false, "images": [{"name": "file"}]}'}
    files = [
        ('file', ('rtf.jpeg', open(file_path, 'rb'), 'image/jpeg'))
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
    with open('db.txt', 'r') as fn:
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


def load_file():
    global file_path
    file_path = filedialog.askopenfilename()

def recognize():
    text_json = json.loads(recognize_request())
    info = get_info_to_str(text_json)
    if info == "":
        info = "Этого человека нет в базе"
    text.delete('1.0', tk.END)
    text.insert(tk.END, info)

def add_to_database():
    if (input_id.get(1.0, "end-1c") == "" or input_name.get(1.0, "end-1c") == ""):
        print("exit")
        text.delete('1.0', tk.END)
        text.insert(tk.END, "Введите все данные о имени и id человека")
        return

    person_write = "person" + input_id.get(1.0, "end-1c")
    name_write = input_name.get(1.0, "end-1c")

    with open('db.txt', 'r') as fn:
        file_name = fn.read()

    if file_name.find(person_write) != -1:
        text.delete('1.0', tk.END)
        text.insert(tk.END, "Человек с таким person id уже есть в базе")
        return

    set_postman()
    text_json = json.loads(recognize_request())

    info = get_info_to_str(text_json)
    person_info = info.split('\n')[0].split('- ')[-1]

    write_str = ""
    if (len(person_info.split()) == 1):
        write_str = person_write + ": " + name_write

    file_name += '\n' + write_str

    with open('db.txt', 'w') as fn:
        fn.write(file_name)


def save_file():
    with open('persons_info.txt', 'w') as f:
        f.write(text.get('1.0', tk.END))


if __name__ == '__main__':
    file_path = ''
    root = tk.Tk()
    root.title("Распознавание лиц")
    root.geometry("400x600")

    # input_id = tk.Label(root, anchor=NW, padx=6, pady=6)


    load_button = tk.Button(root, text="Загрузить фото", command=load_file)
    load_button.pack(pady=10)

    recognize_button = tk.Button(root, text="Распознать", command=recognize)
    recognize_button.pack(pady=10)

    set_button = tk.Button(root, text="Загрузить person_id", command=add_to_database)
    set_button.pack(pady=10)

    save_button = tk.Button(root, text="Сохранить результат", command=save_file)
    save_button.pack(pady=10)



    set_button = tk.Label(root, text="Введите person_id:")
    set_button = tk.Entry(root)

    input_id = tk.Text(root, height=1, width=15)
    input_id.pack()

    input_name = tk.Text(root, height=1, width=15)
    input_name.pack()

    text = tk.Text(root)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()

