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

NVIVO = r'C:\Program Files\QSR\NVivo 12\nvivo'
KEY = "9aSa-nUrp21l7I0FQcBHrtinmaiB56G7-ZXzJTNpjj8="

# Please check Demo programs for better examples of launchers      
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
    
fields_list =  (( 'FirstName','First Name*',True),
                ( 'LastName','Last Name*',True),
                ( 'Email','Email*',False),
                ( 'Phone','Phone',False),
                ( 'Fax','Fax',False),
                ( 'JobTitle','Job Title',False),
                ( 'Sector','Sector',False),
                ( 'Industry','Industry',False),
                ( 'Role','Role',False),
                ( 'Department','Department',False),
                ( 'Organization','Organization',False),
                ( 'City','City',False),
                ( 'Country','Country',True),
                ( 'State','State',False) )


layout = []
layout.append( [sg.Text('Please enter your Activation Data')] )
layout.extend( [ [ sg.Text(field[1],size=(15, 1)), sg.InputText(key=field[0])] for field in fields_list ] )
layout.append( [sg.Text('Serial data',size=(15, 1)),sg.InputText(key='serial')] )
layout.extend( [ [sg.Output(size=(88, 10))],      
                 [sg.Button('Replace'),sg.Button('Activate'), sg.Button('Deactivate'), sg.Button('Exit')] ] )

window = sg.Window('NVIVO Activation', layout)      

# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
  (event, values) = window.read()
  if event == 'Exit'  or event is None:      
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
    
  elif event == 'Deactivate':
    ExecuteCommandSubprocess(NVIVO,"-deactivate")