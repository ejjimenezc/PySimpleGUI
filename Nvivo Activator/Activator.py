import PySimpleGUI as sg      
import subprocess      
from lxml import etree

NVIVO = r"C:\Program Files\QSR\NVivo 12\nvivo"

# Please check Demo programs for better examples of launchers      
def ExecuteCommandSubprocess(command, *args):      
    try:      
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
        out, err = sp.communicate()      
        if out:      
            print(out.decode("utf-8"))      
        if err:      
            print(err.decode("utf-8"))      
    except:      
        pass      



fields_list = (  ( 'FirstName','First Name*',True),
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
layout.extend( [ [sg.Output(size=(88, 10))],      
                 [sg.Button('Activate'), sg.Button('EXIT')] ] )

window = sg.Window('NVIVO Activation', layout)      

# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
  (event, values) = window.read()      
  if event == 'EXIT'  or event is None:      
      break # exit button clicked      
  if event == 'Activate':
    print(values)
      #ExecuteCommandSubprocess(NVIVO)   