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

tab1,tab2,tab3,tab4 =  [] , [] , [], []

tab1.extend([
    [sg.Text('Please enter your license:')],
    [sg.Multiline(key='serial',size=(40, 5))]
])

tab2.append([sg.Text('Insert activation data:')])

col1 = [[   
        sg.Text(field[1],size=(10, 1),font=('Helvetica', 10, field[2])), 
        sg.Input(key=field[0],size=(25, 1))
    ] for field in fields_list[:int(len(fields_list)/2)]]
col2 = [[   
        sg.Text(field[1],size=(10, 1),font=('Helvetica', 10, field[2])), 
        sg.Input(key=field[0],size=(25, 1))
    ] for field in fields_list[int(len(fields_list)/2):]]
tab2.extend([
    [sg.Column(col1),sg.Column(col2)],
    [sg.Button("Activate")]
])

tab3.extend([
    [sg.Text('Click on the button to deactivate the current license.')],
    [sg.Button('Deactivate',key="deactivateBtn")]
])

layout = [  [sg.TabGroup([
                [   sg.Tab('Replace', tab1), 
                    sg.Tab('Activate', tab2),
                    sg.Tab('Deactivate', tab3),
                    sg.Tab('Settings', tab4)  ]
            ])],
            [sg.Button('Exit',key='exitBtn')]]

window = sg.Window('NVIVO Activation', layout)      

# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
  (event, values) = window.read()
  print(event)
  if event == 'exitBtn'  or event is None:      
      break # exit button clicked    
      
  if event == 'Replace':
    #lic = decrypt(values["serial"])
    lic = values["serial"]
    ExecuteCommandSubprocess(NVIVO,"-i",lic)
    
  elif event == 'Activate':
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