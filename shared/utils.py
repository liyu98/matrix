import yaml
import os

def read_hosts(override_localhost=False):

    cwd = os.getcwd()
    file = cwd + "/hosts.yml"

    with open(file, 'r') as f:
        hosts = yaml.safe_load(f)
    if override_localhost:
        for x, vals in hosts.items():
            if x != 'dashboard' and x != 'clients':
                hosts[x]['host'] = 'localhost'
            elif x == 'clients':
                for i, client in enumerate(vals):
                    for _, c in client.items():
                        c['host'] = 'localhost'

    return hosts
