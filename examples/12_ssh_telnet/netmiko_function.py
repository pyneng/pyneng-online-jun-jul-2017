from netmiko import ConnectHandler
import sys
import yaml

#COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))

def connect_ssh(device_dict, commands):

    print("Connection to device {}".format( device_dict['ip'] ))

    ssh = ConnectHandler(**device_dict)
    ssh.enable()

    result = ssh.send_config_set(commands)
    print(result)

commands_to_send = ['logg 10.1.12.3', 'ip access-li ext TESST2', 'permit ip any any']

for router in devices['routers']:
    connect_ssh(router, commands_to_send)
