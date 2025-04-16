import yaml

NUM_CLIENTS = 50

compose = {
    'version': '3.8',
    'services': {},
    'networks': {
        'client_net': {
            'driver': 'bridge',
            'ipam': {
                'config': [{'subnet': '192.168.10.0/24'}]
            }
        },
        'server_net': {
            'driver': 'bridge',
            'ipam': {
                'config': [{'subnet': '192.168.20.0/24'}]
            }
        }
    }
}

# 기본 gateway + 서버들
compose['services']['gateway'] = {
    'image': 'my-gateway-image',
    'container_name': 'gateway',
    'cap_add': ['NET_ADMIN', 'SYS_ADMIN'],
    'sysctls': {'net.ipv4.ip_forward': '1'},
    'networks': {
        'client_net': {'ipv4_address': '192.168.10.200'},
        'server_net': {'ipv4_address': '192.168.20.200'}
    },
    'tty': True,
    'stdin_open': True
}

for i in range(1, 4):
    compose['services'][f'server{i}'] = {
        'image': 'my-server-image',
        'container_name': f'server{i}',
        'cap_add': ['NET_ADMIN'],
        'environment': [f'SERVER_NAME=server{i}'],
        'networks': {
            'server_net': {'ipv4_address': f'192.168.20.10{i}'}
        }
    }

# client 생성
# for i in range(1, NUM_CLIENTS + 1):
#     client_name = f'client{i}'
#     compose['services'][client_name] = {
#         'image': 'my-client-image',
#         'container_name': client_name,
#         'cap_add': ['NET_ADMIN'],
#         'environment': [f'CLIENT_NAME={client_name}'],
#         'networks': {
#             'client_net': {'ipv4_address': f'192.168.10.{i + 3}'}
#         },
#         'stdin_open': True,
#         'tty': True,
#         'depends_on': ['gateway', 'server1', 'server2', 'server3']
#     }

# 저장
with open('docker-compose.yml', 'w') as f:
    yaml.dump(compose, f, default_flow_style=False)
