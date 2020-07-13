from cryptography.fernet import Fernet
import PySimpleGUI as sg     
import base64
import os

DEFAULT_FILENAME = "nvivolicense"
DEFAULT_FERNET_KEY = "O_ZYxyl433xKrZwCG3y7tUEEouZyLJeZmzITsLJ8rzU="
DEFAULT_SERIAL = 'MVD12-LZ000-BH020-1RE87-DF87G'

COL1 = 14
COL2 = 40

def savefile(file_path,encrypted_data):
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

tab_encryption = [
    [sg.Text("Licencia",size=(COL1,1)),sg.In(DEFAULT_SERIAL,size=(COL2,1),key="serial")],
    [sg.Button("Nueva llave",key="gkey",size=(COL1,1)),sg.Input(DEFAULT_FERNET_KEY,key="keyOutput",size=(COL2,1))],
    [sg.Text("Licencia encriptada",size=(COL1,1)),sg.Input(key="encSerial",size=(COL2,1))],
    [sg.Checkbox('Generar archivo de licencia', key='check', default=False)],
    [sg.Text("Archivo",size=(COL1,1)),sg.Input(disabled=True,key="filepath",size=(COL2-14,1)), sg.FileSaveAs("Guardar",key="savefile",size=(10,1),disabled=True,file_types=(('ALL Files', '*.*'),("Licencia de Nvivo",'*.lic')))],
    [sg.Button("Encriptar licencia",key="generateBtn",size=(20,1))]
]

tab_desencryption = [
    [sg.Text("Texto Encriptado:",size=(COL1,1)),sg.In(size=(COL2,1),key="cipher")],
    [sg.Text("Llave:",size=(COL1,1)),sg.In(size=(COL2,1),key="cipherkey")],
    [sg.Checkbox('Usar archivo de licencia', key='cipherfilecheck', default=False)],
    [sg.Text("Archivo encriptado",size=(COL1,1)),sg.Input(key="cipherfile",size=(COL2-14,1)), sg.FileBrowse("Buscar",key="cipherfilebtn",size=(10,1))],
    [sg.Text("Texto plano:",size=(COL1,1)),sg.In(size=(COL2,1),key="plaintext")],
    [sg.Button("Mostrar texto original",key="decryptBtn",size=(20,1))]
]

layout = [
    [
        sg.TabGroup([
            [
                sg.Tab('Encriptar', tab_encryption, element_justification="center"),
                sg.Tab('Desencriptar', tab_desencryption, element_justification="center")
            ]
        ])
    ],
    [sg.Button("Salir",key='Exit',size=(20,1))]
]

window = sg.Window('Encriptar licencia',layout)
while True:      
    (event, values) = window.read(timeout=100)
    file_path = values["filepath"]
    serial = values["serial"]
    keyOutput = values["keyOutput"]
    cipher = values["cipher"]
    cipherkey = values["cipherkey"]
    cipherfile = values["cipherfile"]
    
    if values["check"]:
        window['filepath'].update(disabled=False)
        window['savefile'].update(disabled=False)
    else:
        window['filepath'].update(disabled=True)
        window['savefile'].update(disabled=True)

    if values["cipherfilecheck"]:
        window['cipherfile'].update(disabled=False)
        window['cipherfilebtn'].update(disabled=False)
    else:
        window['cipherfile'].update(disabled=True)
        window['cipherfilebtn'].update(disabled=True)

    if event == 'Exit'  or event is None:      
        break # exit button clicked   
    if event == "generateBtn":
        fernet = Fernet(keyOutput.encode())
        encrypted = fernet.encrypt(serial.encode())
        window['encSerial'].update(encrypted.decode())
        if values['check']:
            savefile(file_path,encrypted)
    if event == "decryptBtn":
        if values['cipherfilecheck']:
            f = open(cipherfile, "r")
            cipher = f.readline()
            f.close()
        fernet = Fernet(cipherkey.encode())
        decrypted = fernet.decrypt(cipher.encode())
        window['plaintext'].update(decrypted.decode())
    if event == "gkey":
        new_key = Fernet.generate_key().decode()
        window['keyOutput'].update(new_key)
