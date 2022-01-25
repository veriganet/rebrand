#!/usr/bin/env python3

import argparse
import os
import logging
import sys
import subprocess
import pnrw
import json

main_desc = "Script the bootstrap newly launched blockchain." \
            "Example: " \
            "bootstrap.py"

# Initiate the parser
parser = argparse.ArgumentParser(description=main_desc)

# debug
parser.add_argument("--debug", help="Enable debug", action="store_true")

# bootstrap
parser.add_argument("--boot", help="Start bootstrapping", action="store_true")

# cleanup wallets
parser.add_argument("--clean", help="Cleanups all wallets from local node by deleting them", action="store_true")

# version arg
parser.add_argument("-V", "--version", help="Shows version", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

if args.debug:
    log_level = os.environ.get('LOGGING', default="DEBUG")
else:
    log_level = os.environ.get('LOGGING', default="INFO")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log_level)


def get_env_variable(env, default):
    if not os.environ.get(env, default):
        return logging.warning("%s is not defined!" % env)
    else:
        logging.debug("%s properly set." % env)
        return os.environ.get(env, default)


def wallet_list():
    lines = []
    proc = subprocess.Popen(['%s/%s_node' % (cwd(), "tst0"), '--wallet_list'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode().replace('Wallet ID: ', '')
        if not line:
            break
        lines.append(str(line.rstrip()))

    return lines


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


# pnrw
node_ip = get_env_variable('BOOTSTRAP_NODE_IP', '[::1]')
logging.debug(f" node_ip: {node_ip}")
node_port = get_env_variable('BOOTSTRAP_NODE_PORT', 7076)
node_url_suffix = get_env_variable('BOOTSTRAP_URL_SUFFIX', '/api')
node_url = f"{node_ip}:{node_port}{node_url_suffix}"
dont_use_https = get_env_variable('BOOTSTRAP_DONT_USE_HTTPS', 'True')
headers = get_env_variable('BOOTSTRAP_HEADERS', [])
banano = get_env_variable('BOOTSTRAP_BANANO', 'False')

# keys
genesis_live_key_seed = get_env_variable('GENESIS_LIVE_KEY_SEED', "")
landing_key_seed = get_env_variable('LANDING_KEY_SEED', "")
live_pre_conf_rep_0_key_seed = get_env_variable('LIVE_PRE_CONF_REP_0_KEY_SEED', "")
live_pre_conf_rep_1_key_seed = get_env_variable('LIVE_PRE_CONF_REP_1_KEY_SEED', "")
live_pre_conf_rep_2_key_seed = get_env_variable('LIVE_PRE_CONF_REP_2_KEY_SEED', "")
live_pre_conf_rep_3_key_seed = get_env_variable('LIVE_PRE_CONF_REP_3_KEY_SEED', "")
live_pre_conf_rep_4_key_seed = get_env_variable('LIVE_PRE_CONF_REP_4_KEY_SEED', "")
live_pre_conf_rep_5_key_seed = get_env_variable('LIVE_PRE_CONF_REP_5_KEY_SEED', "")
live_pre_conf_rep_6_key_seed = get_env_variable('LIVE_PRE_CONF_REP_6_KEY_SEED', "")

# Check for --version or -V
if args.version:
    print("V22.0_0.0.1")


def cwd():
    directory = os.getcwd()
    logging.debug(directory)
    return directory


# make node connection
try:
    node = pnrw.Node(node_url, dontUseHTTPS=dont_use_https, headers=headers, banano=banano)
    logging.info('Node connection established')
    logging.debug(f"node uptime: {node.uptime()}")
except pnrw.exceptions as node:
    logging.error(node)

if args.boot:
    # check if any wallets exist
    wallet_list = wallet_list()
    logging.debug(f"Wallet List: {wallet_list}")

    genesis_key = node.deterministic_key(genesis_live_key_seed, 0)
    landing_key = node.deterministic_key(landing_key_seed, 0)
    rep0_key = node.deterministic_key(live_pre_conf_rep_0_key_seed, 0)
    rep1_key = node.deterministic_key(live_pre_conf_rep_1_key_seed, 0)
    logging.debug(f"Genesis Account ID: {genesis_key['account']}")
    logging.debug(f"Landing Account ID: {landing_key['account']}")
    logging.debug(f"Representative 0 Account ID: {rep0_key['account']}")
    logging.debug(f"Representative 1 Account ID: {rep1_key['account']}")

    create_genesis_wallet = False
    create_landing_wallet = False
    create_rep0_wallet = False
    create_rep1_wallet = False

    # define create_[]_wallet variables
    if genesis_key['account'] not in wallet_list:
        logging.info("Genesis key DO NOT exist in wallet")
        create_genesis_wallet = True
        logging.debug(f"create_genesis_wallet: {create_genesis_wallet}")
    else:
        logging.info("Genesis key exist in wallet. Skipping...")
        logging.debug(f"create_genesis_wallet: {create_genesis_wallet}")

    if landing_key['account'] not in wallet_list:
        logging.info("Landing key DO NOT exist in wallet")
        create_landing_wallet = True
        logging.debug(f"create_landing_wallet: {create_landing_wallet}")
    else:
        logging.info("Landing key exist in wallet. Skipping...")
        logging.debug(f"create_landing_wallet: {create_landing_wallet}")

    if rep0_key['account'] not in wallet_list:
        logging.info("Representative 0 key DO NOT exist in wallet")
        create_rep0_wallet = True
        logging.debug(f"create_rep0_wallet: {create_rep0_wallet}")
    else:
        logging.info("Representative 0 key exist in wallet. Skipping...")
        logging.debug(f"create_rep0_wallet: {create_rep0_wallet}")

    if rep1_key['account'] not in wallet_list:
        logging.info("Representative 0 key DO NOT exist in wallet")
        create_rep1_wallet = True
        logging.debug(f"create_rep0_wallet: {create_rep1_wallet}")
    else:
        logging.info("Representative 1 key exist in wallet. Skipping...")
        logging.debug(f"create_rep1_wallet: {create_rep1_wallet}")

    # create genesis wallet
    genesis_wallet = None
    if create_genesis_wallet:
        try:
            genesis_wallet = node.wallet_create()
            logging.info('Creating genesis wallet')
            logging.debug(f"Wallet ID {genesis_wallet}")

            # add genesis seed to the wallet
            genesis_wallet_details = node.wallet_change_seed(genesis_wallet, genesis_live_key_seed)
            logging.info('Adding genesis seed to wallet')
            logging.debug(f"Genesis Wallet ID: {genesis_wallet}")
            logging.debug(f"Genesis Seed: {genesis_live_key_seed}")
            logging.debug(f"Genesis Wallet Details: {genesis_wallet_details}")
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Skipping creating genesis wallet...")
        logging.info("Getting genesis wallet id...")
        for wallet in wallet_id_list():
            account_list = node.account_list(wallet)
            logging.debug(f"Wallet ID: {wallet}")
            logging.debug(f"Accounts in this wallet: {account_list}")
            if genesis_key['account'] in account_list:
                logging.info('Genesis wallet id found.')
                genesis_wallet = wallet
                logging.debug(f"Genesis Wallet ID: {genesis_wallet}")

    # fund representative 0
    rep0_account_balance = node.account_balance(rep0_key['account'])
    logging.debug(f"rep0_account_balance: {rep0_account_balance}")
    if rep0_account_balance['balance'] <= 0 or rep0_account_balance['pending'] <= 0:
        logging.info("Sending funds to representative 0 ...")
        node.send(genesis_wallet, genesis_key['account'],
                  rep0_key['account'],
                  amount=10000000000000000000000000000000)
        logging.debug(f"Representative 0 balance: {rep0_account_balance}")
    else:
        logging.info("Representative 0 funded! Skipping...")
        logging.debug(f"Representative 0 balance: {rep0_account_balance}")

    # fund representative 1
    rep1_account_balance = node.account_balance(rep1_key['account'])
    if rep1_account_balance['balance'] <= 0 or rep1_account_balance['pending'] <= 0:
        logging.info("Sending funds to representative 1 ...")
        node.send(genesis_wallet, genesis_key['account'],
                  rep1_key['account'],
                  amount=10000000000000000000000000000000)
        logging.debug(f"Representative 1 balance: {rep1_account_balance}")
    else:
        logging.info("Representative 1 funded! Skipping...")
        logging.debug(f"Representative 1 balance: {rep1_account_balance}")

    # fund landing account
    landing_account_balance = node.account_balance(landing_key['account'])
    if landing_account_balance['balance'] <= 0 or landing_account_balance['pending'] <= 0:
        logging.info("Sending funds to landing account ...")
        node.send(genesis_wallet, genesis_key['account'],
                  landing_key['account'],
                  amount=1000000000000000000000000000000000000)
        logging.debug(f"Representative 1 balance: {rep1_account_balance}")
    else:
        logging.info("Landing account funded! Skipping...")
        logging.debug(f"Landing account balance: {landing_account_balance}")

    # create representative 0 wallet
    rep0_wallet = None
    if create_rep0_wallet:
        try:
            rep0_wallet = node.wallet_create()
            logging.info('Creating representative 0 wallet')
            logging.debug(f"Wallet ID {rep0_wallet}")

            # add representative 0 seed to the wallet
            rep0_wallet_details = node.wallet_change_seed(rep0_wallet, live_pre_conf_rep_0_key_seed)
            logging.info('Adding representative 0 seed to wallet')
            logging.debug(f"Genesis Wallet ID: {rep0_wallet}")
            logging.debug(f"Genesis Seed: {live_pre_conf_rep_0_key_seed}")
            logging.debug(f"Genesis Wallet Details: {rep0_wallet_details}")
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Skipping creating representative 0 wallet...")
        logging.info("Getting representative 0 wallet id...")
        for wallet in wallet_id_list():
            account_list = node.account_list(wallet)
            logging.debug(f"Wallet ID: {wallet}")
            logging.debug(f"Accounts in this wallet: {account_list}")
            if rep0_key['account'] in account_list:
                logging.info('Representative 0 wallet id found.')
                genesis_wallet = wallet
                logging.debug(f"Representative 0 Wallet ID: {rep0_wallet}")

    # create representative 0 wallet
    rep1_wallet = None
    if create_rep1_wallet:
        try:
            rep1_wallet = node.wallet_create()
            logging.info('Creating representative 1 wallet')
            logging.debug(f"Wallet ID {rep1_wallet}")

            # add representative 0 seed to the wallet
            rep1_wallet_details = node.wallet_change_seed(rep1_wallet, live_pre_conf_rep_1_key_seed)
            logging.info('Adding representative 0 seed to wallet')
            logging.debug(f"Genesis Wallet ID: {rep1_wallet}")
            logging.debug(f"Genesis Seed: {live_pre_conf_rep_1_key_seed}")
            logging.debug(f"Genesis Wallet Details: {rep1_wallet_details}")
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Skipping creating representative 1 wallet...")
        logging.info("Getting representative 1 wallet id...")
        for wallet in wallet_id_list():
            account_list = node.account_list(wallet)
            logging.debug(f"Wallet ID: {wallet}")
            logging.debug(f"Accounts in this wallet: {account_list}")
            if rep1_key['account'] in account_list:
                logging.info('Representative 1 wallet id found.')
                genesis_wallet = wallet
                logging.debug(f"Representative 1 Wallet ID: {rep1_wallet}")

    # create landing wallet
#    landing_wallet = None
#    if create_landing_wallet:
#        try:
#            landing_wallet = node.wallet_create()
#            logging.info('Creating landing wallet')
#            logging.debug(f"Wallet ID {landing_wallet}")
#
#            # add representative 0 seed to the wallet
#            landing_wallet_details = node.wallet_change_seed(landing_wallet, landing_key_seed)
#            logging.info('Adding landing seed to wallet')
#            logging.debug(f"Landing Wallet ID: {landing_wallet}")
#            logging.debug(f"Landing Seed: {landing_key_seed}")
#            logging.debug(f"Landing Wallet Details: {landing_wallet}")
#        except pnrw.exceptions as error:
#            logging.error(error)
#    else:
#        logging.info("Skipping creating representative 1 wallet...")
#        logging.info("Getting representative 1 wallet id...")
#        for wallet in wallet_id_list():
#            account_list = node.account_list(wallet)
#            logging.debug(f"Wallet ID: {wallet}")
#            logging.debug(f"Accounts in this wallet: {account_list}")
#            if landing_key['account'] in account_list:
#                logging.info('Landing wallet id found.')
#                landing_wallet = wallet
#                logging.debug(f"Landing Wallet ID: {landing_wallet}")
if args.clean:
    print("""
WARNING! WARNING! WARNING!
Your are about to delete all the wallets from your local node.
Make sure you have backup your local node wallets and wallet data before proceeding.
""")
    confirm_delete = input('Please confirm with `yes` or `no` to delete all wallets from local node? ')

    if confirm_delete == "yes" or confirm_delete == "Yes" or confirm_delete == "YES":
        try:
            for wallet in wallet_id_list():
                logging.info('Removing wallet from local node...')
                node.wallet_destroy(wallet)
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Not deleting wallets...")
        logging.info("You are safe for now.")
