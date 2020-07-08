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

domain_list = {
    "Corporación Universitaria Minuto de Dios - UNIMINUTO":["uniminuto.edu","uniminuto.edu.co"],
    "Universidad Tecnológica de Bolivar - UTB":["utb.edu.co"],
    "Fundación Universitaria Konrad Lorenz":["konradlorenz.edu.co","fukl.edu.co"],
    "Universidad Libre de Colombia - UNILIBRE":["unilibre.edu.co","unilibrebaq.edu.co","unilibrebog.edu.co","unilibrecali.edu.co"],
    "Universidad de Boyacá":["uniboyaca.edu.co"],
    "Universidad del Atlántico - UNIATLANTICO":["uniatlantico.edu.co","dcc.uniatlantico.edu.co","mail.uniatlantico.edu.co"],
    "Universidad Autónoma de Bucaramanga - UNAB":["unab.edu.co"],
    "Universidad Simón Bolivar - USB":["unisimonbolivar.edu.co"],
    "Universidad Pontificia Bolivariana - UPB":["upb.edu.co","upbmonteria.edu.co","alfa.upb.edu.co","upbbga.edu.co"],
    "Universidad Tecnológica de Chile - INACAP":["inacap.cl"],
    "Universidad Peruana de Ciencias Aplicadas - UPC":["upc.pe","upc.edu.pe"],
    "Universidad Diego Portales - UDP ":["udp.cl","mail.udp.cl"],
    "Pontificia Universidad Javeriana":["javeriana.edu.co","puj.edu.co","ujaveriana.edu.co","javercol.javeriana.edu.co","javerianacali.edu.co"],
    "Universidad Santo Tomás de Chile - UST":["santotomas.cl"],
    "Universidad del Pacífico de Perú - UP":["up.edu.pe"],
    "Universidad Externado de Colombia":["uexternado.edu.co","externado.edu.co","est.uexternado.edu.co"],
    "Universidad Nacional de San Agustín de Arequipa - UNSA":["unsa.edu.pe"],
    "Universidad Manuela Beltrán - UMB":["umb.edu.co"],
    "Universidad Nacional de Educación - UNAE":["unae.edu.ec"],
    "Universidad Católica de Santa María - UCSM":["ucsm.edu.pe"],
    "Universidad de Costa Rica - UCR":["ucr.ac.cr","fcs.ucr.ac.cr","cariari.ucr.ac.cr"],
    "Universidad del Rosario":["urosario.edu.co","ur.edu.co"],
    "Universidad Tecnológica de Bolivar - UTB":["utb.edu.co"],
    "Universidad Anáhuac":["anahuac.mx","unimayab.edu.mx"],
    "Universidad de Chile - UCHILE":["uchile.cl","redclinicauchile.cl","facso.cl","derecho.uahurtado.cl","clinicalascondes.cl","veterinaria.uchile.cl","ug.uchile.cl","postgradouchile.cl","dgf.uchile.cl","dii.uchile.cl","ciae.uchile.cl","med.uchile.cl","inta.uchile.cl","uchilefau.cl","ing.uchile.cl","iap.uchile.cl","fe"],
    "Universidad de los Andes - UNIANDES":["uniandes.edu.co","adm.uniandes.edu.co"]
}


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
            sg.popup(out.decode("utf-8"),title="Mensaje",keep_on_top=True)   
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
                ( 'Phone','Teléfono',''),
                ( 'Organization','Organización',''),
                ( 'Country','País*','bold') )

def validation(**data):
    if "nvivopath" in data:
        return os.path.exists(NVIVO_PATH)
    if "path" in data:
        return os.path.exists(data["path"])
    if "data" in data:
        check = True
        errors = []
        values = data["data"]

        if not values["FirstName"]:
            check = False
            errors.append("- La casilla de Nombre no puede estar vacía.")
        if not values["LastName"]:
            check = False
            errors.append("- La casilla de Apellido no puede estar vacía.")
        if not re.match("^(.+)@(.+)$",values["Email"]):
            check = False
            errors.append("- El correo es invalido.")
        if not re.match("^[0-9]*$",values["Phone"]):
            check = False
            errors.append("- El teléfono ingresado es invalido.")
        if values["Country"] not in COUNTRIES:
            check = False
            errors.append("- El país ingresado es invalido.")
        return {"check":check,"errors":errors}
    if "email" in data:
        check = True
        errors = []
        org = data["email"]["Organization"]
        ema = []
        if org in domain_list:
            ema += domain_list[org]
        if not org in domain_list:
            check = False
            errors.append("- Escoga una organización valida.")
        domval = [re.match("^(.+)@"+dom+"$",data["email"]["Email"]) for dom in ema]
        if not any(domval):
            check = False
            errors.append("- El correo ingresado no es valido para realizar la activación.")
        return {"check":check,"errors":errors}
    return True
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
            sg.Combo(COUNTRIES,key=fields_list[i][0],size=(54, 1))
        ])
        continue
    elif(fields_list[i][0]=='Organization'):
        afields.append([
            sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
            sg.Combo(list(domain_list.keys()),key=fields_list[i][0],size=(54, 1))
        ])
        continue
    afields.append([
        sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
        sg.Input(key=fields_list[i][0],size=(56, 1))
    ])


x = len(afields)
tabA.append([sg.Text('Ingrese los siguientes datos, necesarios para la activación:')])
tabA.extend(afields)
tabA.append([sg.Text('Presione el siguiente botón para realizar la activación')])
tabA.append([sg.Button("Activar Nvivo",key="activateBtn",size=(40,1))])

# Settings

settings_frame = [
    [sg.T("Seleccione la ubicación del ejecutable de Nvivo:")],
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
    [sg.Frame('Configuración de Proxy', proxy_frame)],
    [sg.Frame('Extra', buttons_frame)]
])

tabL = [
    #[sg.Output(key='-OUTPUT-',size=(70,13))]
]

# Merge all settings

layout = [  [sg.TabGroup([
                [   sg.Tab('Activación', tabA, element_justification="center"),
                    sg.Tab('Configuración', tabS, element_justification="left"),
                    sg.Tab('Log de Acciones', tabL, element_justification="left") ]
])],
            [sg.Button('Cerrar aplicación',key='exitBtn',size=(15,1))]]#,sg.Button('Print',key='test',size=(15,1))]]

def gui():
    window = sg.Window('Activador de NVIVO', layout)         

    while True:      
        (event, values) = window.read(timeout=100)
        nvivo_path = values["file_path"]
        license_path = values["licensepath"]
        proxy_settings = []

        
        emailValidation = validation(email=values)

        if event in (sg.WIN_CLOSED, 'exitBtn'):      
            break # exit button clicked  

        if values["proxyT"]:
            proxy_settings.extend(["-u",values["proxyU"]])
            if values["proxyP"].replace(" ", "")!="":
                proxy_settings.extend(["-p",values["proxyP"]])
            if values["proxyD"].replace(" ", "")!="":
                proxy_settings.extend(["-d",values["proxyD"]])  

        if event == 'installLic':

            valida = validation(data=values)
            emailCheck = validation(email=values)
            if not os.path.exists(nvivo_path):
                sg.popup('No se encuentra el ejecutable de Nvivo.',
                'Seleccione la ubicacion desde Configuracion.',title="Error")
            elif not os.path.exists(license_path):
                sg.popup('Seleccione el archivo de licencia.',title="Error",
                keep_on_top=True)
            elif not valida["check"]:
                sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
                title="Error",
                keep_on_top=True)
            elif not emailCheck["check"]:
                sg.popup("Se encontraron los siguientes errores:",*emailCheck["errors"],
                title="Error",
                keep_on_top=True)
            else:
                print("- Instalando licencia.")
                lic = decrypt(license_path)
                cmd = ["-i",lic]
                ExecuteCommandSubprocess(nvivo_path,*cmd)

        if event == 'activateLic':
            valida = validation(data=values)
            emailCheck = validation(email=values)
            if not os.path.exists(nvivo_path):
                sg.popup('No se encuentra el ejecutable de Nvivo.',
                'Seleccione la ubicacion desde Configuracion.',title="Error")
            elif not os.path.exists(license_path):
                sg.popup('Seleccione el archivo de licencia.',title="Error",
                keep_on_top=True)
            elif not valida["check"]:
                sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
                title="Error",
                keep_on_top=True)
            elif not emailCheck["check"]:
                sg.popup("Se encontraron los siguientes errores:",*emailCheck["errors"],
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
            emailCheck = validation(email=values)
            if not os.path.exists(nvivo_path):
                sg.popup('No se encuentra el ejecutable de Nvivo.',
                'Seleccione la ubicacion desde Configuracion.',title="Error")
            elif not os.path.exists(license_path):
                sg.popup('Seleccione el archivo de licencia.',title="Error",
                keep_on_top=True)
            elif not valida["check"]:
                sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
                title="Error",
                keep_on_top=True)
            elif not emailCheck["check"]:
                sg.popup("Se encontraron los siguientes errores:",*emailCheck["errors"],
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
            valida = validation(data=values)
            emailCheck = validation(email=values)
            if not os.path.exists(nvivo_path):
                sg.popup('No se encuentra el ejecutable de Nvivo.',
                'Seleccione la ubicacion desde Configuracion.',title="Error")
            elif not os.path.exists(license_path):
                sg.popup('Seleccione el archivo de licencia.',title="Error",
                keep_on_top=True)
            elif not valida["check"]:
                sg.popup("Se encontraron los siguientes errores:",*valida["errors"],
                title="Error",
                keep_on_top=True)
            elif not emailCheck["check"]:
                sg.popup("Se encontraron los siguientes errores:",*emailCheck["errors"],
                title="Error",
                keep_on_top=True)
            else:
                print("- Desactivando licencia.")
                cmd = ["-deactivate"] + proxy_settings
                ExecuteCommandSubprocess(nvivo_path,*cmd)

        if event == 'test':
            validation(data=values)
    window.close()

if __name__ == '__main__':
    gui()
    print('Exiting Program')