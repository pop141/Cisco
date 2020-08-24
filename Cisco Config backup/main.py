import PySimpleGUI as sg
from connect import Connect

'''
GUI Scrip to backup cisco device config
usage-
Enter source file with IP address of devices
Enter Dest folder to save output
Enter Device Username
Enter Device Password

sg.Image can be commented out if not required. This would mean all values would be -1 
I.E con.default_save would = value[1] ect

'''

def main():
    con = Connect()
    layout = [
        [sg.Image(filename=r'low.png', size=(400,130))],
        [sg.Text('Open Location', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
        [sg.Text('Save Location', size=(15, 1)), sg.Input(), sg.FolderBrowse()],
        [sg.Text('User Name', size=(15, 1)), sg.InputText("", key='Username')],
        [sg.Text('Password', size=(15, 1)), sg.InputText("", key='Password', password_char='*')],
        [sg.Text('_'  * 100, size=(65, 1))],
        [sg.Checkbox('Debug', size=(12, 1), default=False),],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Cisco SSH Backup Tool', layout)

    while True:  # The Event Loop
        event, values = window.read()
        #print(event, values) #to uncomment debug
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Submit':
            con.default_save = values[2]
            con.default_open = values[1]
            lines = sum(1 for line in open(con.default_open)) # Get number of devices in file
            try:
                con.save_config(con.default_open, con.default_save, values['Username'], values['Password'], lines, values[3])
            except Exception as e:
                sg.popup(e)
                print("Exception")


if __name__ == '__main__':
    main()
