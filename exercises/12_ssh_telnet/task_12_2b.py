# -*- coding: utf-8 -*-

'''
Дополнить функцию send_config_commands из задания 12.2a или 12.2

Добавить проверку на ошибки:
* При выполнении команд, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве.

При этом, параметр output также должен работать, но теперь он отвечает за вывод
только тех команд, которые выполнились корректно.

Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками 

Оба словаря в формате
* ключ - IP устройства
* значение - вывод с выполнением команд

Проверить функцию на команде с ошибкой.
'''

def send_config_commands(device_list, config_commands, output=True):
    errors = ['Invalid input detected','Incomplete command', 'Ambiguous command']
    success_dict = {}
    fail_dict = {}

    for router in device_list:
        success = []
        fail = []
        ip = router['ip']
        #print ('Connect to device with ip {}'.format(ip))
        ssh = netmiko.ConnectHandler(**router)
        ssh.enable()
        for command in config_commands:
            #Так как функция для отправки команд конфигурационного режима,
            # тут лучше использовать ssh.send_config_set
            result = ssh.send_config_set(command)
            #это не обязательно, но можно отрезать лищнюю информацию:
            result = '\n'.join(result.split('\n')[2:-2])
            #Немного другой вариант проверки на ошибки
            if any(err in result for err in errors):
                fail.append(result)
                #По заданию надо было выполнить информацию об ошибках все время
                #Но задание было немного корявое :)
                print('###Following error occured on {} for command "{}"'.format(
                                                                    ip, command))
                print(result)
            else:
                success.append(result)
                if output: print(result)
        success_dict[ip] = success
        fail_dict[ip] = fail
        ssh.disconnect()
    return success_dict, fail_dict

with open('devices.yaml') as f:
    dev_dict = yaml.load(f)
dev_list = dev_dict['routers']

commands = [ 'logging 0255.255.1',
             'logging buffered 20010',
             'logging ' ]


success, fail = send_config_commands(dev_list, commands, output=False)
print(success)
print(fail)
