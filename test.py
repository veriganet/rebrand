#!/usr/bin/env python3

import os
import logging
import subprocess


def cwd():
    directory = os.getcwd()
    logging.debug(directory)
    return directory


def wallet_id_list():
    lines = []
    proc = subprocess.Popen(['./%s_node' % "tst0", '--wallet_list'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode()
        if not line:
            break
        if "Wallet ID" in line:
            lines.append(str(line.rstrip()).replace('Wallet ID: ', ''))

    return lines


wallet_id_list = wallet_id_list()

print(wallet_id_list)
