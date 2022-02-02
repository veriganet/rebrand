#!/usr/bin/env python3

import os
import logging
import subprocess
import pnrw


def cwd():
    directory = os.getcwd()
    logging.debug(directory)
    return directory


def get_env_variable(env, default):
    if not os.environ.get(env, default):
        return logging.warning("%s is not defined!" % env)
    else:
        logging.debug("%s properly set." % env)
        return os.environ.get(env, default)


abbreviation = "tst0"


def wallet_list():
    lines = []
    proc = subprocess.Popen(['%s/%s_node' % (cwd(), abbreviation), '--wallet_list'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode().replace('Wallet ID: ', '')
        if not line:
            break
        lines.append(str(line.rstrip()))

    return lines


def wallet_id_list():
    lines = []
    proc = subprocess.Popen(['./%s_node' % abbreviation, '--wallet_list'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode()
        if not line:
            break
        if "Wallet ID" in line:
            lines.append(str(line.rstrip()).replace('Wallet ID: ', ''))

    return lines


# pnrw
node_ip = get_env_variable('BOOTSTRAP_NODE_IP', '[::1]')
logging.debug(f" node_ip: {node_ip}")
node_port = get_env_variable('BOOTSTRAP_NODE_PORT', 7076)
node_url_suffix = get_env_variable('BOOTSTRAP_URL_SUFFIX', '/api')
node_url = f"{node_ip}:{node_port}{node_url_suffix}"
dont_use_https = get_env_variable('BOOTSTRAP_DONT_USE_HTTPS', 'True')
headers = get_env_variable('BOOTSTRAP_HEADERS', [])
banano = get_env_variable('BOOTSTRAP_BANANO', 'False')

# make node connection
try:
    node = pnrw.Node(node_url, dontUseHTTPS=dont_use_https, headers=headers, banano=banano)
    logging.info('Node connection established')
    logging.debug(f"node uptime: {node.uptime()}")
except pnrw.exceptions as node:
    logging.error(node)

max_supply = 340282366920938463463374607431768211455
divided_supply = max_supply / 7
print(f"divided_supply_raw: {divided_supply}")


def percentage(percent, whole):
  return (percent * whole) / 100.0


print(percentage(14, max_supply))

