from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


class GetVLAN:
    def __init__(self):
        self.show_int = "show interface "
        self.op_mode = " switchport | inc Operational Mode:"
        self.access = " switchport | inc Access Mode VLAN:"
        self.name = " switchport | inc Name:"
        self.voice = " switchport | inc Voice VLAN:"
        self.trunk = " switchport | inc Trunking VLANs Enabled:"

    def dev_connect(self, ip, username, pwd):
        try:
            net_connect = ConnectHandler(device_type="cisco_ios",
                                         host=ip,
                                         username=username,
                                         password=pwd
                                         )

        except AuthenticationException as e:
            raise ValueError(f"Error incorrect username or password {e}")

        except NetMikoTimeoutException as e:
            raise ValueError(f"Connection Timeout to {device['host']} {e}")

        except SSHException as e:
            raise ValueError(f"Error ssh on {device['host']} may not be enabled {e}")

        return net_connect

    def interface_VLAN(self, ip, username, pwd, port):

        net_connect = self.dev_connect(ip, username, pwd)

        mode = net_connect.send_command(self.show_int + port + self.op_mode)
        access = net_connect.send_command(self.show_int + port + self.access)
        if_name = net_connect.send_command(self.show_int + port + self.name)
        ip_phone = net_connect.send_command(self.show_int + port + self.voice)
        trunk = net_connect.send_command(self.show_int + port + self.trunk)

        if "access" in mode:

            if "none" in ip_phone:
                data = f"{if_name}\n{mode}\n{access}"
                return data
            else:
                data = f"{if_name}\n{mode}\n{ip_phone}\n{access}"
                return data

        elif "down" in mode:
            data = f"{if_name}\n{mode}\n{access}"
            return data

        elif "trunk" in mode:
            data = f"{if_name}\n{mode}\n{trunk}"
            return data
