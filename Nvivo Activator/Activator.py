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
NVIVO = r'C:\Program Files\QSR\NVivo 12\nvivo'
KEY = "9aSa-nUrp21l7I0FQcBHrtinmaiB56G7-ZXzJTNpjj8="
COUNTRIES = []

with open("AcceptedCountryFormat.txt","r") as cf:
    COUNTRIES = cf.readlines()

#Methods     
def ExecuteCommandSubprocess(command, *args):      
    try:      
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
        out, err = sp.communicate()    
        print(" ".join(sp.args)) 
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

tabA,tabB,tabC,tabI,tabS =  [] , [] , [], [], []

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

tabA.append([sg.Text('Insert activation data:')])

#Activation Data
afields = []
for i in range(len(fields_list)):
    if(fields_list[i][0]=='Country'):
        afields.append([
            sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
            sg.Combo(COUNTRIES,key=fields_list[i][0],size=(25, 1))
        ])  
    afields.append([
        sg.Text(fields_list[i][1],size=(10, 1),font=('Helvetica', 10, fields_list[i][2])), 
        sg.Input(key=fields_list[i][0],size=(25, 1))
    ])
x = len(afields)
tabB.extend([
    [sg.Column(afields[:int(x/2)]),sg.Column(afields[int(x/2):])],
    [sg.Button("Activate",key="activateBtn")]
])

#Deactivate current license
tabC.extend([
    [sg.Text('Click on the button to deactivate the current license.')],
    [sg.Button('Deactivate',key="deactivateBtn")]
])

layout = [  [sg.TabGroup([
                [   sg.Tab('Info', tabI), 
                    sg.Tab('Replace', tabA), 
                    sg.Tab('Activate', tabB),
                    sg.Tab('Deactivate', tabC),
                    sg.Tab('Settings', tabS)  ]
            ])],
            [sg.Button('Exit',key='exitBtn')]]


sg.Print('Nvivo Activator', do_not_reroute_stdout=False)

window = sg.Window('NVIVO Activation', layout)      

# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
  (event, values) = window.read()
  if event == 'exitBtn'  or event is None:      
      break # exit button clicked    
      
  if event == 'replaceBtn':
    lic = decrypt(values["serial"])
    #lic = values["serial"]
    ExecuteCommandSubprocess(NVIVO,"-i",lic)
    
  elif event == 'activateBtn':
    xml = createXML(fields=fields_list,data=values)
    tempf, fname = mkstemp(text=True)
    os.close(tempf)
    
    with open(fname, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
        xml.write(f, xml_declaration=False, encoding='utf-8')
        
    ExecuteCommandSubprocess(NVIVO,"-a",fname)
    os.remove(fname)
    
  elif event == 'deactivateBtn':
    ExecuteCommandSubprocess(NVIVO,"-deactivate")