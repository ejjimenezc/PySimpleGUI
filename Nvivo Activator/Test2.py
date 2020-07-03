import PySimpleGUI as sg      
import hashlib      

'''      
        Create a secure login for your scripts without having to include your password    in the program.  Create an SHA1 hash code for your password using the GUI. Paste into variable in final program      
        1. Choose a password      
        2. Generate a hash code for your chosen password by running program and entering 'gui' as the password      
        3. Type password into the GUI      
        4. Copy and paste hash code Window GUI into variable named login_password_hash    
        5. Run program again and test your login!      
'''      
 

# ----------------------------- Paste this code into your program / script -----------------------------      
# determine if a password matches the secret password by comparing SHA1 hash codes      
def PasswordMatches(password, hash):      
    password_utf = password.encode('utf-8')      
    sha1hash = hashlib.sha1()      
    sha1hash.update(password_utf)      
    password_hash = sha1hash.hexdigest()      
    if password_hash == hash:      
        return True      
    else:      
        return False      

login_password_hash = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'      
password = sg.popup_get_text('Password', password_char='*')      
if password == 'gui':                # Remove when pasting into your program      
    HashGeneratorGUI()               # Remove when pasting into your program      
    exit(69)                         # Remove when pasting into your program      
if PasswordMatches(password, login_password_hash):      
    print('Login SUCCESSFUL')      
else:      
    print('Login FAILED!!') 