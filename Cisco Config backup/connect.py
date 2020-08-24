import paramiko
import os
import time
from datetime import date
import tempfile
import PySimpleGUI as sg


class Connect:
    def __init__(self):

        self._default_save = "C:/" if os.path.exists("C:/") else tempfile.gettempdir()
        self._default_open = "C:/" if os.path.exists("C:/") else tempfile.gettempdir()
        self.today = date.today()
        self.date = self.today.strftime("%d-%b-%Y")
        self.i = 0

    @property
    def default_save(self):
        return self._default_save

    @default_save.setter
    def default_save(self, value):
        if os.path.exists(value):
            self._default_save = value
        else:
            raise ValueError('Path not found')

    @property
    def default_open(self):
        return self._default_open

    @default_open.setter
    def default_open(self, value):
        if os.path.exists(value):
            self._default_open = value
        else:
            raise ValueError('Path not found')

    def connect_ssh(self, user, pwd, ip):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=22, username=user, password=pwd, timeout=5, look_for_keys=False)
        except paramiko.ssh_exception.AuthenticationException as e:
            raise ValueError(f"Error incorrect username or password {e}")
        except paramiko.ssh_exception.socket.timeout as e:
            raise ValueError(f"connection {e} please check IPaddress {ip} is avaiable")
        return ssh

    def save_config(self, filename, save, user, pwd, lines, debug):
        with open(filename, "r") as f0:
            if debug == False:
                for ip in f0.readlines():
                    ip = ip.strip()
                    ssh = self.connect_ssh(user, pwd, ip)
                   
                    sg.OneLineProgressMeter('Device Progress', self.i+1, lines , 'meter')

                    terminal = ssh.invoke_shell()
                    time.sleep(2)
                    terminal.send('term len 0\n')
                    time.sleep(1)
                    terminal.send('write memory\n')
                    time.sleep(2)
                    terminal.send('sh run\n')
                    time.sleep(20)
                    output = terminal.recv(999999)
                    os.chdir(save)
                    file_name = "%s_%s" % (ip, self.date) + ".txt"
                    with open(file_name, 'a') as backup:
                        backup.write(output.decode("utf-8"))
                    
                    self.i += 1
                    ssh.close()

            elif debug == True:
                for ip in f0.readlines():
                    ip = ip.strip()
                    ssh = self.connect_ssh(user, pwd, ip)

                    terminal = ssh.invoke_shell()
                    time.sleep(2)
                    terminal.send('term len 0\n')
                    time.sleep(1)
                    sg.Print("Saving Config to device")
                    terminal.send('write memory\n')
                    time.sleep(2)
                    sg.Print("Config Saved")
                    sg.Print(f"backing up config for {ip}")
                    terminal.send('sh run\n')
                    time.sleep(20)
                    output = terminal.recv(999999)
                    os.chdir(save)
                    file_name = "%s_%s" % (ip, self.date) + ".txt"
                    with open(file_name, 'a') as backup:
                        backup.write(output.decode("utf-8"))
                    
                    sg.Print(f"Config saved to {file_name} in location {os.getcwd()} \n")
                    self.i += 1
                    ssh.close()

