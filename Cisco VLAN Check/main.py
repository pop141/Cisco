import PySimpleGUI as sg
from get_vlan import GetVLAN


def main():

    vl = GetVLAN()

    layout = [
        [sg.Text('Device IP', size=(15, 1)), sg.InputText("", key='IP')],
        [sg.Text('Interface', size=(15, 1)), sg.InputText("", key='Port')],
        [sg.Text('UserName', size=(15, 1)), sg.InputText("", key='Username')],
        [sg.Text('Password', size=(15, 1)), sg.InputText("", key='Password', password_char='*')],
        [sg.Text('_' * 100, size=(65, 1))],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Cisco VLAN Check', layout)

    while True:  # The Event Loop
        event, values = window.read()
        # print(event, values) #to uncomment debug
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Submit':

            try:
                data = vl.interface_VLAN( values['IP'], values['Username'], values['Password'], values['Port'])
                sg.popup(data)

            except Exception as e:
                sg.popup(e)


if __name__ == '__main__':
    main()
