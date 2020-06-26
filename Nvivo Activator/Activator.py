from cryptography.fernet import Fernet
import xml.etree.ElementTree as ET
from tempfile import mkstemp
import PySimpleGUI as sg      
import subprocess   
import base64   
import os

#Global Variables
NVIVO_PATH = r'C:\Program Files\QSR\NVivo 12\nvivo.exe'
LICENSE_FILE = r'nvivolicense.lic'
KEY = "O_ZYxyl433xKrZwCG3y7tUEEouZyLJeZmzITsLJ8rzU="
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

def decrypt(license_path):
    print(license_path)
    with open(license_path, 'rb') as f:
        data = f.read()
    f = Fernet(KEY.encode())
    decrypted = f.decrypt(data).decode()
    return decrypted

def createXML(fields=None,data=None):
    tree = ET.ElementTree(ET.Element('Activation'))
    root = tree.getroot()
    pointer = ET.SubElement(root,'Request')
    for f in fields:
        f_key = f[0]
        child = ET.SubElement(pointer,f_key)
        child.text = data[f_key]
    return tree
   
fields_list =  (( 'FirstName','Nombre*','bold'),
                ( 'LastName','Apellido*','bold'),
                ( 'Email','Correo*','bold'),
                ( 'Phone','Telefono*',''),
                ( 'Organization','Organizacion',''),
                ( 'Country','Pais*','bold') )

#UI
sg.theme('Dark Blue 3')

tabA,tabS =  [] , []

tabA.extend([
    [sg.Text('Seleccione el archivo de licencia:')],
    [sg.Text('Licencia:', size=(10, 1)), sg.Input(LICENSE_FILE,key="license_path",size=(48,1)), 
    sg.FileBrowse(key="licensepath")]
])

#Activation Data
afields = []
for i in range(len(fields_list)):
    if(fields_list[i][0]=='Country'):
        afields.append([
            sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
            sg.Combo(COUNTRIES,key=fields_list[i][0],size=(18, 1))
        ])
        continue
    afields.append([
        sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
        sg.Input(key=fields_list[i][0],size=(20, 1))
    ])

x = len(afields)
tabA.append([sg.Text('Ingrese los siguientes datos, necesarios para la activacion:')])
tabA.extend([
    [sg.Column(afields[:int(x/2)]),sg.Column(afields[int(x/2):])]
])
tabA.append([sg.Text('Darle click al siguiente boton para realizar la activacion')])
tabA.append([sg.Button("Activar Nvivo",key="activateBtn",size=(40,1))])

# Settings

settings_frame = [
    [sg.T("Seleccione la ubicacion del ejecutable de Nvivo:")],
    [sg.Text('Ruta de Instalacion', size=(10, 1)), 
        sg.Input(NVIVO_PATH,key="file_path",size=(48,1)), 
        sg.FileBrowse(key="file")]]
    
proxy_frame = [
    [sg.Checkbox("Habilitar proxy:",default=False, key="proxyT")],
    [sg.T("Username:",size=(10,1)),sg.I(size=(20,1),key="proxyU"),
        sg.T("Password:",size=(10,1)),sg.I(size=(21,1),key="proxyP")],
    [sg.T("Domain:",size=(10,1)),sg.I(size=(20,1),key="proxyD")]]
    
buttons_frame = [
    [sg.Button('Desactivar licencia',key="deactivateBtn",size=(19,1)),
    sg.Button("Instalar licencia",key="installLic",size=(19,1)),
    sg.Button("Activar licencia",key="activateLic",size=(19,1))]]

tabS.extend([
    [sg.Frame('Ejecutable de Nvivo', settings_frame)],
    [sg.Frame('Configuracion de Proxy', proxy_frame)],
    [sg.Frame('Extra', buttons_frame)]
])

# Merge all settings
layout = [  [sg.TabGroup([
                [   sg.Tab('Activacion', tabA, element_justification="center"),
                    sg.Tab('Configuracion', tabS, element_justification="left") ]
            ])],
            [sg.Button('Exit',key='exitBtn',size=(15,1)),]]


#sg.Print('Nvivo Activator', do_not_reroute_stdout=False)

window = sg.Window('NVIVO Activation', layout)         


# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
    (event, values) = window.read()
    nvivo_path = values["file_path"]
    license_path = values["licensepath"]
    proxy_settings = []

    if event == 'exitBtn'  or event is None:      
        break # exit button clicked  

    if values["proxyT"]:
        proxy_settings.extend(["-u",values["proxyU"]])
        if values["proxyP"].replace(" ", "")!="":
            proxy_settings.extend(["-p",values["proxyP"]])
        if values["proxyD"].replace(" ", "")!="":
            proxy_settings.extend(["-d",values["proxyD"]])  

    if event == 'installLic':
        lic = decrypt(license_path)
        cmd = ["-i",lic]
        ExecuteCommandSubprocess(nvivo_path,*cmd)

    if event == 'activateLic':
        xml = createXML(fields=fields_list,data=values)
        tempf, fname = mkstemp(text=True)
        os.close(tempf)

        with open(fname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
            xml.write(f, xml_declaration=False, encoding='utf-8')

        cmd = ["-a",fname] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)
        os.remove(fname)
        
    elif event == 'activateBtn':
        xml = createXML(fields=fields_list,data=values)
        tempf, fname = mkstemp(text=True)
        os.close(tempf)

        with open(fname, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
            xml.write(f, xml_declaration=False, encoding='utf-8')

        lic = decrypt(license_path)
        cmd = ["-i",lic,"-a",fname] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)
        os.remove(fname)

    elif event == 'deactivateBtn':
        cmd = ["-deactivate"] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)