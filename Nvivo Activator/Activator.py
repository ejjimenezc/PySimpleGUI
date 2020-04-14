import PySimpleGUI as sg      
import subprocess      
from xml.dom import minidom

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

fields = (  ( 'FirstName','First Name*',True),
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


layout = [
    [sg.Text('Please enter your Activation Data')],
    [sg.Text('First Name*', size=(15, 1)), sg.InputText()],
    [sg.Text('Last Name*', size=(15, 1)), sg.InputText()],
    [sg.Text('Email*', size=(15, 1)), sg.InputText()],
    [sg.Text('Phone', size=(15, 1)), sg.InputText()],
    [sg.Text('Fax', size=(15, 1)), sg.InputText()],
    [sg.Text('Job Title', size=(15, 1)), sg.InputText()],
    [sg.Text('Sector', size=(15, 1)), sg.InputText()],
    [sg.Text('Industry', size=(15, 1)), sg.InputText()],
    [sg.Text('Role', size=(15, 1)), sg.InputText()],
    [sg.Text('Department', size=(15, 1)), sg.InputText()],
    [sg.Text('Organization', size=(15, 1)), sg.InputText()],
    [sg.Text('City', size=(15, 1)), sg.InputText()],
    [sg.Text('Country*', size=(15, 1)), sg.InputText()],
    [sg.Text('State', size=(15, 1)), sg.InputText()],
    [sg.Text('Script output....', size=(20, 1))],      
    [sg.Output(size=(88, 10))],      
    [sg.Button('Activate'), sg.Button('EXIT')],    
        ]      


window = sg.Window('Script launcher', layout)      

# ---===--- Loop taking in user input and using it to call scripts --- #      

while True:      
  (event, values) = window.read()      
  if event == 'EXIT'  or event is None:      
      break # exit button clicked      
  if event == 'Activate':
    print(values)
    text_input = values[0]    
    sg.popup('You entered', text_input)
      #ExecuteCommandSubprocess(NVIVO)   