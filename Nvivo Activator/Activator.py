from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import xml.etree.ElementTree as ET
from tempfile import mkstemp
import PySimpleGUI as sg      
import subprocess   
import base64   
import os

#Global Variables
DEFAULT_NVIVO = r'C:\Program Files\QSR\NVivo 12\nvivo.exe'
KEY = "9aSa-nUrp21l7I0FQcBHrtinmaiB56G7-ZXzJTNpjj8="
COUNTRIES = []

with open("AcceptedCountryFormat.txt","r") as cf:
    COUNTRIES = cf.readlines()

#Methods     
def ExecuteCommandSubprocess(command, *args):
    print(" ".join((command,)+args))
    try:      
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
        out, err = sp.communicate()    
        if out:      
            print(out.decode("utf-8"))      
        if err:      
            print(err.decode("utf-8"))      
    except:      
        pass     

def decrypt(token):
    f = Fernet(KEY.encode())
    msg = f.decrypt(token.encode()).decode()
    return msg

def createXML(fields=None,data=None):
    tree = ET.ElementTree(ET.Element('Activation'))
    root = tree.getroot()
    pointer = ET.SubElement(root,'Request')
    for f in fields:
        f_key = f[0]
        child = ET.SubElement(pointer,f_key)
        child.text = data[f_key]
    return tree
   
fields_list =  (( 'FirstName','First Name*','bold'),
                ( 'LastName','Last Name*','bold'),
                ( 'Email','Email*','bold'),
                ( 'Phone','Phone',''),
                ( 'Fax','Fax',''),
                ( 'JobTitle','Job Title',''),
                ( 'Sector','Sector',''),
                ( 'Industry','Industry',''),
                ( 'Role','Role',''),
                ( 'Department','Department',''),
                ( 'Organization','Organization',''),
                ( 'City','City',''),
                ( 'Country','Country*','bold'),
                ( 'State','State','') )

#UI
sg.theme('Dark Blue 3')

tabA,tabB,tabC,tabI,tabS, tabL =  [] , [] , [], [], [], []

#Info
tabI.extend([
    [sg.Text(   'Use this app to manage your Nvivo Liscense.')],
    [sg.Text(   'In the tab "Replace", you can actually install a '+
                'license key or replace the current one.')],
    [sg.Text(   'Use the tab "Activate" to fill with your personal info and '+
                'activate the product.')],
    [sg.Text(   'In the tab "Deactivate", you can deactivate the current '+
                'activated license to use it in another PC.')],
])

#Replace license key
tabA.extend([
    [sg.Text('Please enter your license:')],
    [sg.Multiline(key='serial',size=(80, 1))],
    [sg.Button("Replace",key="replaceBtn")]
])

#Activation Data
afields = []
for i in range(len(fields_list)):
    if(fields_list[i][0]=='Country'):
        afields.append([
            sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
            sg.Combo(COUNTRIES,key=fields_list[i][0],size=(25, 1))
        ])
        continue
    afields.append([
        sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
        sg.Input(key=fields_list[i][0],size=(25, 1))
    ])

x = len(afields)
tabB.append([sg.Text('Insert activation data:')])
tabB.extend([
    [sg.Column(afields[:int(x/2)]),sg.Column(afields[int(x/2):])],
    [sg.Button("Activate",key="activateBtn")]
])

#Deactivate current license
tabC.extend([
    [sg.Text('Click on the button to deactivate the current license.')],
    [sg.Button('Deactivate',key="deactivateBtn")]
])

#Log
tabL.extend([
    [sg.Output(size=(70,15))]
])

# Settings
tabS.extend([
    [sg.T("Nvivo Executable Path:")],
    [sg.Text('Nvivo Path', size=(10, 1)), sg.Input(DEFAULT_NVIVO,key="file_path",size=(50,1)), sg.FileBrowse(key="file")],
    [sg.T("Proxy Settings")],
    [sg.Checkbox("Enable Proxy:",default=False, key="proxyT")],
    [sg.T("Username:",size=(10,1)),sg.I(size=(50,1),key="proxyU")],
    [sg.T("Password:",size=(10,1)),sg.I(size=(50,1),key="proxyP")],
    [sg.T("Domain:",size=(10,1)),sg.I(size=(50,1),key="proxyD")],
])

# Merge all settings
layout = [  [sg.TabGroup([
                [   sg.Tab('Info', tabI), 
                    sg.Tab('Replace', tabA), 
                    sg.Tab('Activate', tabB),
                    sg.Tab('Deactivate', tabC),
                    sg.Tab('Settings', tabS),
                    sg.Tab('Log', tabL)  ]
            ])],
            [sg.Button('Exit',key='exitBtn'),sg.B("print")]]


#sg.Print('Nvivo Activator', do_not_reroute_stdout=False)

window = sg.Window('NVIVO Activation', layout)         


# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
    (event, values) = window.read()
    nvivo_path = values["file_path"]

    proxy_settings = []

    if values["proxyT"]:
        proxy_settings.extend(["-u",values["proxyU"]])
        if values["proxyP"].replace(" ", "")!="":
            proxy_settings.extend(["-p",values["proxyP"]])
        if values["proxyD"].replace(" ", "")!="":
            proxy_settings.extend(["-d",values["proxyD"]])

    if event == 'exitBtn'  or event is None:      
        break # exit button clicked    

    if event == 'print':
        print(nvivo_path)
        print(proxy_settings)

    if event == 'replaceBtn':
        lic = decrypt(values["serial"])
        #lic = values["serial"]
        cmd = [nvivo_path,"-i",lic]
        ExecuteCommandSubprocess(nvivo_path,*cmd)

    elif event == 'activateBtn':
        xml = createXML(fields=fields_list,data=values)
        tempf, fname = mkstemp(text=True)
        os.close(tempf)

        with open(fname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
            xml.write(f, xml_declaration=False, encoding='utf-8')

        cmd = ["-a",fname] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)
        os.remove(fname)

    elif event == 'deactivateBtn':
        cmd = ["-deactivate"] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)