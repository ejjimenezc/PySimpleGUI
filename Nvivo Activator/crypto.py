from cryptography.fernet import Fernet
import PySimpleGUI as sg     
import base64
import os

DEFAULT_DIRNAME = "./"
DEFAULT_FILENAME = "nvivolicense"
DEFAULT_FERNET_KEY = "O_ZYxyl433xKrZwCG3y7tUEEouZyLJeZmzITsLJ8rzU="
DEFAULT_SERIAL = '11111-22222-33333-44444-55555'

COL1 = 13
COL2 = 50

def savefile(file_path,encrypted_data):
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

layout = [
    [sg.Text("Serial",size=(COL1,1)),sg.In(DEFAULT_SERIAL,size=(COL2,1),key="serial")],
    [sg.Checkbox('Generate license file', key='check', default=False)],
    [sg.Text("License Folder",size=(COL1,1)),sg.Input(DEFAULT_DIRNAME,key="folder_path",size=(COL2-14,1)), sg.FolderBrowse(key="folder",size=(10,1))],
    [sg.Text("License Filename",size=(COL1,1)),sg.In(DEFAULT_FILENAME,key="file_name",size=(COL2,1))],
    [sg.Button("New key",key="gkey",size=(COL1,1)),sg.Input(DEFAULT_FERNET_KEY,key="keyOutput",size=(COL2,1))],
    [sg.Text("Encrypted Serial",size=(COL1,1)),sg.Input(key="encSerial",size=(COL2,1))],
    [sg.Button("Generate",key="generateBtn"),sg.Button("Exit")]
]

sg.theme('Dark Blue 3')
window = sg.Window('Encrypt License Key',layout)
while True:      
    (event, values) = window.read()
    folder_path = values["folder_path"]
    file_name = values["file_name"]
    serial = values["serial"]
    keyOutput = values["keyOutput"]

    if event == 'Exit'  or event is None:      
        break # exit button clicked   
    if event == "generateBtn":
        path = folder_path+"/"+file_name+'.lic'
        print(keyOutput)
        print(path)
        fernet = Fernet(keyOutput.encode())
        encrypted = fernet.encrypt(serial.encode())
        window['encSerial'].update(encrypted.decode())
        if values['check']:
            savefile(path,encrypted)
    if event == "gkey":
        new_key = Fernet.generate_key().decode()
        window['keyOutput'].update(new_key)
