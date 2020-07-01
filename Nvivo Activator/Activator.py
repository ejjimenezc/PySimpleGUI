from cryptography.fernet import Fernet
import xml.etree.ElementTree as ET
from tempfile import mkstemp
import PySimpleGUI as sg      
import subprocess   
import base64
import sys
import os
import re

#Global Variables

EXEPATH = os.path.dirname(sys.executable)

NVIVO_PATH = r'C:\Program Files\QSR\NVivo 12\nvivo.exe'
LICENSE_FILE = r''
KEY = "O_ZYxyl433xKrZwCG3y7tUEEouZyLJeZmzITsLJ8rzU="
COUNTRIES = []

countrypath = ''

if os.path.isfile('./AcceptedCountryFormat.txt'):
    countrypath = './AcceptedCountryFormat.txt'
else:
    EXEPATH+"\AcceptedCountryFormat.txt"

with open(countrypath,"r") as cf:
    COUNTRIES = cf.readlines()

#Methods     
def ExecuteCommandSubprocess(command, *args):
    #print(" ".join((command,)+args))
    try:      
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)      
        out, err = sp.communicate()    
        if out:      
            print(out.decode("utf-8"))      
        if err:      
            print(err.decode("utf-8"))      
    except:      
        pass     

def decrypt(license_path):
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
                ( 'Phone','Telefono',''),
                ( 'Organization','Organizacion',''),
                ( 'Country','Pais*','bold') )

def validation(**data):
    if "path" in data:
        return os.path.exists(data["path"])
    if "data" in data:
        check = True
        errors = []
        values = data["data"]
        if not values["FirstName"]:
            check = False
            errors.append("- La casilla de Nombre no puede estar vacia.")
        if not values["LastName"]:
            check = False
            errors.append("- La casilla de Apellido no puede estar vacia.")
        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",values["Email"]):
            check = False
            errors.append("- La casilla de Correo no puede estar vacia.")
        if not re.match("^[0-9]*$",values["Phone"]):
            check = False
            errors.append("- El telefono ingresado es invalido.")
        if values["Country"] not in COUNTRIES:
            check = False
            errors.append("- El pais ingresado es invalido.")
        return {"check":check,"errors":errors}
    return true
#UI
sg.theme('Dark Blue 3')

tabA,tabS, tabL =  [] , [], []

tabA.extend([
    [sg.Text('Seleccione el archivo de licencia:')],
    [sg.Text('Licencia:', size=(10, 1)), sg.Input(LICENSE_FILE,key="license_path",size=(48,1)), 
    sg.FileBrowse('Buscar',key="licensepath")]
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
    [sg.Text('Ruta:', size=(10, 1)), 
        sg.Input(NVIVO_PATH,key="file_path",size=(48,1)), 
        sg.FileBrowse('Buscar',key="file")]]
    
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

tabL = [
    [sg.Output(key='-OUTPUT-',size=(70,13))]
]

# Merge all settings
layout = [  [sg.TabGroup([
                [   sg.Tab('Activacion', tabA, element_justification="center"),
                    sg.Tab('Configuracion', tabS, element_justification="left"),
                    #sg.Tab('Log de Acciones', tabL, element_justification="left") ]
]])],#])],
            [sg.Button('Cerrar aplicacion',key='exitBtn',size=(15,1)),sg.Button('Print',key='test',size=(15,1))]]


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
        if not os.path.exists(license_path):
            sg.popup('Seleccione el archivo de licencia.',title="Error",
        else:
            print("- Instalando licencia.")
            lic = decrypt(license_path)
            cmd = ["-i",lic]
            ExecuteCommandSubprocess(nvivo_path,*cmd)

    if event == 'activateLic':
        valida = validation(data=values)
        if not os.path.exists(license_path):
            sg.popup('Seleccione el archivo de licencia.',title="Error",
            keep_on_top=True)
        elif not valida["check"]:
            sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
            title="Error",
            keep_on_top=True)
        else:                
            print("- Activando licencia.")
            xml = createXML(fields=fields_list,data=values)
            tempf, fname = mkstemp(text=True)
            os.close(tempf)

            with open(fname, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
                xml.write(f, xml_declaration=False, encoding='utf-8')

            cmd = ["-a",fname] + proxy_settings
            ExecuteCommandSubprocess(nvivo_path,*cmd)
            os.remove(fname)
        
    if event == 'activateBtn':
        valida = validation(data=values)
        if not os.path.exists(license_path):
            sg.popup('Seleccione el archivo de licencia.',title="Error",
            keep_on_top=True)
        elif not valida["check"]:
            sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
            title="Error",
            keep_on_top=True)
        else:
            print("- Activando licencia.")
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

    if event == 'deactivateBtn':
        print("- Desactivando licencia.")
        cmd = ["-deactivate"] + proxy_settings
        ExecuteCommandSubprocess(nvivo_path,*cmd)

    if event == 'test':
        validation(data=values)
