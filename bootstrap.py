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


abbreviation = get_env_variable('ABBREVIATION', "")
max_supply = 340282366920938463463374607431768211455


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

# keys
live_genesis_key_seed = get_env_variable('GENESIS_LIVE_KEY_SEED', "")

live_pre_conf_reps_seeds = [
    get_env_variable('LIVE_PRE_CONF_REP_0_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_1_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_2_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_3_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_4_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_5_KEY_SEED', ""),
    get_env_variable('LIVE_PRE_CONF_REP_6_KEY_SEED', "")
]

live_pre_conf_reps_accounts = []

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

# check if any wallets exist
wallet_list = wallet_list()
logging.debug(f"Wallet List: {wallet_list}")

wallet_id_list = wallet_id_list()
logging.debug(f"wallet_id_list: {wallet_id_list}")

if args.boot:
    for wallet in wallet_id_list:
        account_list = node.account_list(wallet)
        logging.debug(f"account_list: {account_list}")

    live_genesis_key = node.deterministic_key(live_genesis_key_seed, 0)
    logging.debug(f"Genesis Account ID: {live_genesis_key['account']}")

    for i, seed in enumerate(live_pre_conf_reps_seeds):
        if seed:
            account = node.deterministic_key(seed, 0)
            live_pre_conf_reps_accounts.append(account['account'])
            logging.debug(f"Representative {i} Account ID: {account['account']}")

    create_genesis_wallet = False
    create_genesis_account = False

    fund_representatives = False

    # define create_[]_wallet variables
    if live_genesis_key['account'] not in wallet_list:
        logging.info("Genesis key DO NOT exist in wallet")
        create_genesis_wallet = True
        logging.debug(f"create_genesis_wallet: {create_genesis_wallet}")
    else:
        logging.info("Genesis key exist in wallet. Skipping...")
        logging.debug(f"create_genesis_wallet: {create_genesis_wallet}")

    # create genesis wallet
    live_genesis_wallet = None
    if create_genesis_wallet:
        try:
            live_genesis_wallet = node.wallet_create()
            logging.info('Creating genesis wallet')
            logging.debug(f"Wallet ID {live_genesis_wallet}")

            # add genesis seed to the wallet
            genesis_wallet_details = node.wallet_change_seed(live_genesis_wallet, live_genesis_key_seed)
            logging.info('Adding genesis seed to wallet')
            logging.debug(f"Genesis Wallet ID: {live_genesis_wallet}")
            logging.debug(f"Genesis Seed: {live_genesis_key_seed}")
            logging.debug(f"Genesis Wallet Details: {genesis_wallet_details}")
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Skipping creating genesis wallet...")
        logging.info("Getting genesis wallet id...")
        for wallet in wallet_id_list:
            account_list = node.account_list(wallet)
            logging.debug(f"Wallet ID: {wallet}")
            logging.debug(f"Accounts in this wallet: {account_list}")
            if live_genesis_key['account'] in account_list:
                logging.info('Genesis wallet id found.')
                live_genesis_wallet = wallet
                logging.debug(f"Genesis Wallet ID: {live_genesis_wallet}")

    # get number of deterministic_key equal to number of representatives
    #live_genesis_accounts = node.account_list(live_genesis_wallet)
    live_genesis_accounts = []
    logging.info(f"Getting {len(live_pre_conf_reps_accounts)} deterministic accounts for genesis account")
    for i in range(len(live_pre_conf_reps_accounts)):
        live_genesis_account = node.deterministic_key(live_genesis_key_seed, i)["account"]
        logging.debug(f"live_genesis_account {i}: {live_genesis_account}")
        live_genesis_accounts.append(live_genesis_account)

    # create genesis accounts for number of representatives
    if len(live_genesis_accounts) < len(live_pre_conf_reps_accounts):
        logging.info("Adding more accounts to genesis wallet.")
        logging.debug("This means there are less accounts in genesis wallet then active representatives.")
        try:
            number_of_accounts = len(live_pre_conf_reps_accounts)
            genesis_account = node.accounts_create(live_genesis_wallet, number_of_accounts)
            logging.info(f"Creating {number_of_accounts} in genesis wallet.")
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Skipping to add accounts to genesis wallet.")
        logging.debug("This means there are enough accounts in genesis wallet.")

    # fund representative accounts
    for i, account in enumerate(live_pre_conf_reps_accounts):
        logging.debug(f"account: {account}")
        account_balance = node.account_balance(account)
        logging.debug(f"Representative {i} account balance: {account_balance}")

        # check if account has any balance and send the funds if not
        if account_balance['balance'] <= 0 and account_balance['pending'] <= 0:
            logging.debug(f"account_balance_balance: {account_balance['balance']}")
            logging.debug(f"account_balance_pending: {account_balance['pending']}")
            logging.info(f"Sending funds to representative {i} ...")
            node.send(live_genesis_wallet, live_genesis_key['account'],
                      account,
                      amount=100000000000000000000000000000)
            logging.debug(f"Representative {i} balance: {account_balance}")
        else:
            logging.info(f"Representative {i} funded! Skipping...")
            logging.debug(f"Representative {i} balance: {account_balance}")

    # fund genesis accounts
    for i, account in enumerate(live_genesis_accounts):
        # get account balance
        account_balance = node.account_balance(account)
        logging.debug(f"genesis account: {account}")
        logging.debug(f"genesis account balance: {account_balance}")

        # check if account has balance. if not fund the account
        if account_balance['balance'] <= 0 and account_balance['pending'] <= 0:
            logging.debug(f"account_balance_balance: {account_balance['balance']}")
            logging.debug(f"account_balance_pending: {account_balance['pending']}")
            logging.info(f"Sending funds to genesis account: {account} ...")
            amount = max_supply/len(live_genesis_accounts)
            node.send(live_genesis_wallet, live_genesis_key['account'],
                      account,
                      amount=amount)
            logging.debug(f"Sent : {amount}")
        else:
            logging.info("Genesis account has been funded. Skipping...")
            logging.debug(f"Account balance: {account_balance}")

    # get representatives walled ids
    live_pre_conf_reps_wallet_ids = []
    for i, wallet in enumerate(wallet_id_list):
        account_list = node.account_list(wallet)
        logging.debug(f"Wallet ID: {wallet}")
        logging.debug(f"Accounts in this wallet: {account_list}")
        if live_pre_conf_reps_accounts in account_list:
            logging.info('Representative account wallet id found.')
            live_pre_conf_reps_wallet_ids.append(wallet)
            logging.debug(f"Genesis Wallet ID: {live_pre_conf_reps_wallet_ids}")

    # change genesis accounts representatives to officials representatives
    logging.info(f"live_genesis_accounts: {live_genesis_accounts}")
    for i, account in enumerate(live_genesis_accounts):
        # get account's representative
        logging.info("Getting genesis account representative...")
        account_representative = node.account_representative(account)
        logging.info(f"Genesis account {i} representative: {account_representative}")
        logging.debug(f"Genesis account_representative: {account_representative}")

        # check if genesis account representative is correct
        logging.debug(f"live_pre_conf_reps_accounts[{i}]: {live_pre_conf_reps_accounts[i]}")
        if account_representative is live_pre_conf_reps_accounts[i]:
            logging.info(f"Genesis account {i} representative is correct")
            logging.info(f"NOT changing the representative!")
            logging.debug(f"account_representative: {account_representative}")
            logging.debug(f"live_pre_conf_reps_accounts[i]: {live_pre_conf_reps_accounts[i]}")
        else:
            logging.info(f"Genesis account {i} representative is NOT correct!")
            logging.info(f"Changing genesis account {i} representative.")
            new_account_representative = live_pre_conf_reps_accounts[i]
            node.account_representative_set(live_genesis_wallet,
                                            account,
                                            new_account_representative)




if args.clean:
    print("""
WARNING! WARNING! WARNING!
Your are about to delete all the wallets from your local node.
Make sure you have backup your local node wallets and wallet data before proceeding.
""")
    confirm_delete = input('Please confirm with `yes` or `no` to delete all wallets from local node? ')

    if confirm_delete == "yes" or confirm_delete == "Yes" or confirm_delete == "YES":
        try:
            for wallet in wallet_id_list:
                logging.info('Removing wallet from local node...')
                node.wallet_destroy(wallet)
        except pnrw.exceptions as error:
            logging.error(error)
    else:
        logging.info("Not deleting wallets...")
        logging.info("You are safe for now.")
