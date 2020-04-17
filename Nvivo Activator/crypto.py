from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import PySimpleGUI as sg     
import base64
import os

def gen_key_lic(password,salt,msg):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    token = f.encrypt(msg.encode())
    return key.decode(),token.decode()


layout = [
    [sg.Text("Message",size=(10,1)),sg.In(key="msg")],
    [sg.Text("Password",size=(10,1)),sg.In("nvivo12",key="pass")],
    [sg.Text("Salt",size=(10,1)),sg.In("securesalt",key="salt")],
    [sg.Button("Generate",key="generateBtn"),sg.Button("Exit")],
    [sg.Text("Key",size=(10,1)),sg.Output(key="key",size=(50,1))],
    [sg.Text("License",size=(10,1)),sg.Output(key="output",size=(50,1))]
]

window = sg.Window('Generate Key',layout)
while True:      
    (event, values) = window.read()
    if event == 'Exit'  or event is None:      
        break # exit button clicked   
    if event == "generateBtn":
        nkey,npass = gen_key_lic(values["pass"],values["salt"],values["msg"])
        window['key'].update(nkey)
        window['output'].update(npass)