#!/usr/bin/env python3

import argparse
import os
import logging
import sys

from nanolib import generate_seed, generate_account_id, generate_account_key_pair, get_account_id, \
    AccountIDPrefix, Block


main_desc = "Script to generate necessary private/public keys to launch blockchain in JSON or environment variables." \
            "Example: " \
            "genkey.py "

# Initiate the parser
parser = argparse.ArgumentParser(description=main_desc)

# debug
parser.add_argument("--debug", help="Enable debug", action="store_true")

# version arg
parser.add_argument("-V", "--version", help="Shows version", action="store_true")

# abr
parser.add_argument("-a", "--abbreviation", required=False, type=str,
                    help="Three or four letter abbreviation of blockchain."
                         "This argument is required for all operations.")

# name
parser.add_argument("-n", "--name", required=False, type=str,
                    help="A user friendly name for the blockchain. Use your imagination. "
                         "Example: TestCOIN, TestCC, TESTcc")

# live network peering port
parser.add_argument("-lnp", "--live-network-peering-port", required=False, type=str,
                    help="Peering port for live network. Ex; 7175")

# key
parser.add_argument("-k", "--key", required=False, type=str, help="Defines the <key> for other commands, hex")

# seed
parser.add_argument("-s", "--seed", required=False, type=str, help="Defines the <seed> for other commands, hex")

# index
parser.add_argument("-i", "--key_index", default=0, required=False,
                    type=int, help="Defines the <index> for private/public key pair, int. Default: 0")
# public_key
parser.add_argument("--public_key", required=False, help="Defines key for getting account id from public key")

# private_key
parser.add_argument("--private_key", required=False, help="Defines key for getting account id from private key")

# generates
parser.add_argument("--generate_key_pair", action="store_true", help="Generates private/public keypair.")

# generate seed
parser.add_argument("--generate_seed", action="store_true", help="Generates private seed")

parser.add_argument("--get_account_id", action="store_true",
                    help="Gets account id/number from private/public key.")

# generate json
parser.add_argument("--output_json", action="store_true",
                    help="Generates all necessary keys & configuration variables in JSON format.")

# Read arguments from the command line
args = parser.parse_args()

if args.debug:
    log_level = os.environ.get('LOGGING', default="DEBUG")
else:
    log_level = os.environ.get('LOGGING', default="INFO")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log_level)

# Check for --version or -V
if args.version:
    print("V22.0_0.0.1")


def cwd():
    directory = os.getcwd()
    logging.debug(directory)
    return directory


def output():
    """
    Generates all necessary keys & configuration variables in JSON format.
    """

    # faucet_keys
    faucet_key_seed = generate_seed()
    faucet_key_pair = generate_account_key_pair(faucet_key_seed, 0)
    faucet_private_key = faucet_key_pair.private
    faucet_public_key = faucet_key_pair.public
    faucet_account_id = get_account_id(public_key=faucet_public_key,
                                        prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)

    # landing_keys
    landing_key_seed = generate_seed()
    landing_key_pair = generate_account_key_pair(landing_key_seed, 0)
    landing_private_key = landing_key_pair.private
    landing_public_key = landing_key_pair.public
    landing_account_id = get_account_id(public_key=landing_public_key,
                                        prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)


    # canary_beta_keys
    canary_beta_key_seed = generate_seed()
    canary_beta_key_pair = generate_account_key_pair(canary_beta_key_seed, 0)
    canary_beta_private_key = canary_beta_key_pair.private
    canary_beta_public_key = canary_beta_key_pair.public
    canary_beta_account_id = get_account_id(public_key=canary_beta_public_key,
                                        prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)

    # canary_live_keys
    canary_live_key_seed = generate_seed()
    canary_live_key_pair = generate_account_key_pair(canary_live_key_seed, 0)
    canary_live_private_key = canary_live_key_pair.private
    canary_live_public_key = canary_live_key_pair.public
    canary_live_account_id = get_account_id(public_key=canary_live_public_key,
                                        prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)

    # canary_test_keys
    canary_test_key_seed = generate_seed()
    canary_test_key_pair = generate_account_key_pair(canary_test_key_seed, 0)
    canary_test_private_key = canary_test_key_pair.private
    canary_test_public_key = canary_test_key_pair.public
    canary_test_account_id = get_account_id(public_key=canary_test_public_key,
                                            prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                       '%s_' % args.abbreviation)

    # genesis_beta_keys
    genesis_beta_key_seed = generate_seed()
    genesis_beta_key_pair = generate_account_key_pair(genesis_beta_key_seed, 0)
    genesis_beta_private_key = genesis_beta_key_pair.private
    genesis_beta_public_key = genesis_beta_key_pair.public
    genesis_beta_account_id = get_account_id(public_key=genesis_beta_public_key,
                                prefix=AccountIDPrefix.NANO.value)
    genesis_beta_account_id_replaced = genesis_beta_account_id.replace('nano_', '%s_' % args.abbreviation)

    # genesis_beta_block
    genesis_beta_block = Block(
        block_type="open",
        source=genesis_beta_public_key.upper(),
        representative=genesis_beta_account_id,
        account=genesis_beta_account_id,
        difficulty="fff3cb0000000000"
    )
    genesis_beta_block.solve_work()
    genesis_beta_block.sign(genesis_beta_private_key)
    genesis_beta_work = genesis_beta_block.work
    genesis_beta_signature = genesis_beta_block.signature

    # genesis_dev_keys
    genesis_dev_key_seed = generate_seed()
    genesis_dev_key_pair = generate_account_key_pair(genesis_dev_key_seed, 0)
    genesis_dev_private_key = genesis_dev_key_pair.private
    genesis_dev_public_key = genesis_dev_key_pair.public
    genesis_dev_account_id = get_account_id(public_key=genesis_dev_public_key,
                                            prefix=AccountIDPrefix.NANO.value)
    genesis_dev_account_id_replaced = genesis_dev_account_id.replace('nano_', '%s_' % args.abbreviation)

    # genesis_dev_block
    genesis_dev_block = Block(
        block_type="open",
        source=genesis_dev_public_key.upper(),
        representative=genesis_dev_account_id,
        account=genesis_dev_account_id,
        difficulty="fff3cb0000000000"
    )
    genesis_dev_block.solve_work()
    genesis_dev_block.sign(genesis_beta_private_key)
    genesis_dev_work = genesis_beta_block.work
    genesis_dev_signature = genesis_beta_block.signature

    # genesis_live_keys
    genesis_live_key_seed = generate_seed()
    genesis_live_key_pair = generate_account_key_pair(genesis_live_key_seed, 0)
    genesis_live_private_key = genesis_live_key_pair.private
    genesis_live_public_key = genesis_live_key_pair.public
    genesis_live_account_id = get_account_id(public_key=genesis_live_public_key,
                                             prefix=AccountIDPrefix.NANO.value)
    genesis_live_account_id_replaced = genesis_live_account_id.replace('nano_', '%s_' % args.abbreviation)

    # genesis_live_block
    genesis_live_block = Block(
        block_type="open",
        source=genesis_live_public_key.upper(),
        representative=genesis_live_account_id,
        account=genesis_live_account_id,
        difficulty="fff3cb0000000000"
    )
    genesis_live_block.solve_work()
    genesis_live_block.sign(genesis_live_private_key)
    genesis_live_work = genesis_live_block.work
    genesis_live_signature = genesis_live_block.signature

    # genesis_test_keys
    genesis_test_key_seed = generate_seed()
    genesis_test_key_pair = generate_account_key_pair(genesis_test_key_seed, 0)
    genesis_test_private_key = genesis_test_key_pair.private
    genesis_test_public_key = genesis_test_key_pair.public
    genesis_test_account_id = get_account_id(public_key=genesis_test_public_key,
                                             prefix=AccountIDPrefix.NANO.value)
    genesis_test_account_id_replaced = genesis_test_account_id.replace('nano_', '%s_' % args.abbreviation)

    # genesis_test_block
    genesis_test_block = Block(
        block_type="open",
        source=genesis_test_public_key.upper(),
        representative=genesis_test_account_id,
        account=genesis_test_account_id,
        difficulty="fff3cb0000000000"
    )
    genesis_test_block.solve_work()
    genesis_test_block.sign(genesis_live_private_key)
    genesis_test_work = genesis_live_block.work
    genesis_test_signature = genesis_test_block.signature

    # beta_representative_0
    beta_pre_conf_rep_0_key_seed = generate_seed()
    beta_pre_conf_rep_0_key_pair = generate_account_key_pair(beta_pre_conf_rep_0_key_seed, 0)
    beta_pre_conf_rep_0_private_key = beta_pre_conf_rep_0_key_pair.private
    beta_pre_conf_rep_0_public_key = beta_pre_conf_rep_0_key_pair.public
    beta_pre_conf_rep_public_key_0 = beta_pre_conf_rep_0_public_key
    beta_pre_conf_rep_account_0 = get_account_id(public_key=beta_pre_conf_rep_0_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # beta_representative_1
    beta_pre_conf_rep_1_key_seed = generate_seed()
    beta_pre_conf_rep_1_key_pair = generate_account_key_pair(beta_pre_conf_rep_1_key_seed, 0)
    beta_pre_conf_rep_1_private_key = beta_pre_conf_rep_1_key_pair.private
    beta_pre_conf_rep_1_public_key = beta_pre_conf_rep_1_key_pair.public
    beta_pre_conf_rep_public_key_1 = beta_pre_conf_rep_1_public_key
    beta_pre_conf_rep_account_1 = get_account_id(public_key=beta_pre_conf_rep_1_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_0
    live_pre_conf_rep_0_key_seed = generate_seed()
    live_pre_conf_rep_0_key_pair = generate_account_key_pair(live_pre_conf_rep_0_key_seed, 0)
    live_pre_conf_rep_0_private_key = live_pre_conf_rep_0_key_pair.private
    live_pre_conf_rep_0_public_key = live_pre_conf_rep_0_key_pair.public
    live_pre_conf_rep_account_0 = get_account_id(public_key=live_pre_conf_rep_0_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_1
    live_pre_conf_rep_1_key_seed = generate_seed()
    live_pre_conf_rep_1_key_pair = generate_account_key_pair(live_pre_conf_rep_1_key_seed, 0)
    live_pre_conf_rep_1_private_key = live_pre_conf_rep_1_key_pair.private
    live_pre_conf_rep_1_public_key = live_pre_conf_rep_1_key_pair.public
    live_pre_conf_rep_account_1 = get_account_id(public_key=live_pre_conf_rep_1_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_2
    live_pre_conf_rep_2_key_seed = generate_seed()
    live_pre_conf_rep_2_key_pair = generate_account_key_pair(live_pre_conf_rep_2_key_seed, 0)
    live_pre_conf_rep_2_private_key = live_pre_conf_rep_2_key_pair.private
    live_pre_conf_rep_2_public_key = live_pre_conf_rep_2_key_pair.public
    live_pre_conf_rep_account_2 = get_account_id(public_key=live_pre_conf_rep_2_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_3
    live_pre_conf_rep_3_key_seed = generate_seed()
    live_pre_conf_rep_3_key_pair = generate_account_key_pair(live_pre_conf_rep_3_key_seed, 0)
    live_pre_conf_rep_3_private_key = live_pre_conf_rep_3_key_pair.private
    live_pre_conf_rep_3_public_key = live_pre_conf_rep_3_key_pair.public
    live_pre_conf_rep_account_3 = get_account_id(public_key=live_pre_conf_rep_3_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_4
    live_pre_conf_rep_4_key_seed = generate_seed()
    live_pre_conf_rep_4_key_pair = generate_account_key_pair(live_pre_conf_rep_4_key_seed, 0)
    live_pre_conf_rep_4_private_key = live_pre_conf_rep_4_key_pair.private
    live_pre_conf_rep_4_public_key = live_pre_conf_rep_4_key_pair.public
    live_pre_conf_rep_account_4 = get_account_id(public_key=live_pre_conf_rep_4_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_5
    live_pre_conf_rep_5_key_seed = generate_seed()
    live_pre_conf_rep_5_key_pair = generate_account_key_pair(live_pre_conf_rep_5_key_seed, 0)
    live_pre_conf_rep_5_private_key = live_pre_conf_rep_5_key_pair.private
    live_pre_conf_rep_5_public_key = live_pre_conf_rep_5_key_pair.public
    live_pre_conf_rep_account_5 = get_account_id(public_key=live_pre_conf_rep_5_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_6
    live_pre_conf_rep_6_key_seed = generate_seed()
    live_pre_conf_rep_6_key_pair = generate_account_key_pair(live_pre_conf_rep_6_key_seed, 0)
    live_pre_conf_rep_6_private_key = live_pre_conf_rep_6_key_pair.private
    live_pre_conf_rep_6_public_key = live_pre_conf_rep_6_key_pair.public
    live_pre_conf_rep_account_6 = get_account_id(public_key=live_pre_conf_rep_6_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    # live_representative_7
    live_pre_conf_rep_7_key_seed = generate_seed()
    live_pre_conf_rep_7_key_pair = generate_account_key_pair(live_pre_conf_rep_7_key_seed, 0)
    live_pre_conf_rep_7_private_key = live_pre_conf_rep_7_key_pair.private
    live_pre_conf_rep_7_public_key = live_pre_conf_rep_7_key_pair.public
    live_pre_conf_rep_account_7 = get_account_id(public_key=live_pre_conf_rep_7_public_key,
                                                 prefix=AccountIDPrefix.NANO.value).replace('nano_',
                                                                                            '%s_' % args.abbreviation)

    keys_output = f'''faucet_key_seed: {faucet_key_seed.upper()}
faucet_private_key: {faucet_private_key.upper()}
faucet_public_key: {faucet_public_key.upper()}
faucet_account_id: {faucet_account_id}

landing_key_seed: {landing_key_seed.upper()}
landing_private_key: {landing_private_key.upper()}
landing_public_key: {landing_public_key.upper()}
landing_account_id: {landing_account_id}

canary_beta_key_seed: {canary_beta_key_seed.upper()}
canary_beta_private_key: {canary_beta_private_key.upper()}
canary_beta_public_key: {canary_beta_public_key.upper()}
canary_beta_account_id: {canary_beta_account_id}

canary_live_key_seed: {canary_live_key_seed.upper()}
canary_live_private_key: {canary_live_private_key.upper()}
canary_live_public_key: {canary_live_public_key.upper()}
canary_live_account_id: {canary_live_account_id}

canary_test_key_seed: {canary_test_key_seed.upper()}
canary_test_private_key: {canary_test_private_key.upper()}
canary_test_public_key: {canary_test_public_key.upper()}
canary_test_account_id: {canary_test_account_id}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
genesis_beta_key_seed: {genesis_beta_key_seed.upper()}
genesis_beta_private_key: {genesis_beta_private_key.upper()}
genesis_beta_public_key: {genesis_beta_public_key.upper()}
genesis_beta_account_id: {genesis_beta_account_id}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
genesis_live_key_seed: {genesis_live_key_seed.upper()}
genesis_live_private_key: {genesis_live_private_key.upper()}
genesis_live_public_key: {genesis_live_public_key.upper()}
genesis_live_account_id: {genesis_live_account_id}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
genesis_dev_key_seed: {genesis_dev_key_seed.upper()}
genesis_dev_private_key: {genesis_dev_private_key.upper()}
genesis_dev_public_key: {genesis_dev_public_key.upper()}
genesis_dev_account_id: {genesis_dev_account_id}

genesis_test_key_seed: {genesis_test_key_seed.upper()}
genesis_test_private_key: {genesis_test_private_key.upper()}
genesis_test_public_key: {genesis_test_public_key.upper()}
genesis_test_account_id: {genesis_test_account_id}

beta_pre_conf_rep_0_key_seed: {beta_pre_conf_rep_0_key_seed.upper()}
beta_pre_conf_rep_0_private_key: {beta_pre_conf_rep_0_private_key.upper()}
beta_pre_conf_rep_0_public_key: {beta_pre_conf_rep_0_public_key.upper()}
beta_pre_conf_rep_account_0: {beta_pre_conf_rep_account_0}

beta_pre_conf_rep_1_key_seed: {beta_pre_conf_rep_1_key_seed.upper()}
beta_pre_conf_rep_1_private_key: {beta_pre_conf_rep_1_private_key.upper()}
beta_pre_conf_rep_1_public_key: {beta_pre_conf_rep_1_public_key.upper()}
beta_pre_conf_rep_account_1: {beta_pre_conf_rep_account_1.upper()}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_0_key_seed: {live_pre_conf_rep_0_key_seed.upper()}
live_pre_conf_rep_0_private_key: {live_pre_conf_rep_0_private_key.upper()}
live_pre_conf_rep_0_public_key: {live_pre_conf_rep_0_public_key.upper()}
live_pre_conf_rep_account_0: {live_pre_conf_rep_account_0}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_1_key_seed: {live_pre_conf_rep_1_key_seed.upper()}
live_pre_conf_rep_1_private_key: {live_pre_conf_rep_1_private_key.upper()}
live_pre_conf_rep_1_public_key: {live_pre_conf_rep_1_public_key.upper()}
live_pre_conf_rep_account_1: {live_pre_conf_rep_account_1}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_2_key_seed: {live_pre_conf_rep_2_key_seed.upper()}
live_pre_conf_rep_2_private_key: {live_pre_conf_rep_2_private_key.upper()}
live_pre_conf_rep_2_public_key: {live_pre_conf_rep_2_public_key.upper()}
live_pre_conf_rep_account_2: {live_pre_conf_rep_account_2}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_3_key_seed: {live_pre_conf_rep_3_key_seed.upper()}
live_pre_conf_rep_3_private_key: {live_pre_conf_rep_3_private_key.upper()}
live_pre_conf_rep_3_public_key: {live_pre_conf_rep_3_public_key.upper()}
live_pre_conf_rep_account_3: {live_pre_conf_rep_account_3}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_4_key_seed: {live_pre_conf_rep_4_key_seed.upper()}
live_pre_conf_rep_4_private_key: {live_pre_conf_rep_4_private_key.upper()}
live_pre_conf_rep_4_public_key: {live_pre_conf_rep_4_public_key.upper()}
live_pre_conf_rep_account_4: {live_pre_conf_rep_account_4}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_5_key_seed: {live_pre_conf_rep_5_key_seed.upper()}
live_pre_conf_rep_5_private_key: {live_pre_conf_rep_5_private_key.upper()}
live_pre_conf_rep_5_public_key: {live_pre_conf_rep_5_public_key.upper()}
live_pre_conf_rep_account_5: {live_pre_conf_rep_account_5}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_6_key_seed: {live_pre_conf_rep_6_key_seed.upper()}
live_pre_conf_rep_6_private_key: {live_pre_conf_rep_6_private_key.upper()}
live_pre_conf_rep_6_public_key: {live_pre_conf_rep_6_public_key.upper()}
live_pre_conf_rep_account_6: {live_pre_conf_rep_account_6}

#!!! IMPORTANT - KEEP THIS KEYS VERY SECURE !!!#
live_pre_conf_rep_7_key_seed: {live_pre_conf_rep_7_key_seed.upper()}
live_pre_conf_rep_7_private_key: {live_pre_conf_rep_7_private_key.upper()}
live_pre_conf_rep_7_public_key: {live_pre_conf_rep_7_public_key.upper()}
live_pre_conf_rep_account_7: {live_pre_conf_rep_account_7}'''

    abbreviation = args.abbreviation
    name = args.name
    faucet_public_key = faucet_public_key.upper()
    landing_public_key = landing_public_key.upper()
    canary_beta_public_key = canary_beta_public_key.upper()
    canary_live_public_key = canary_live_public_key.upper()
    canary_test_public_key = canary_test_public_key.upper()
    genesis_beta_public_key = genesis_beta_public_key.upper()
    genesis_beta_account = genesis_beta_account_id_replaced
    genesis_beta_work = genesis_beta_work
    genesis_beta_signature = genesis_beta_signature
    genesis_dev_public_key = genesis_dev_public_key
    genesis_dev_private_key = genesis_dev_private_key
    genesis_dev_account = genesis_dev_account_id_replaced
    genesis_dev_work = genesis_dev_work
    genesis_dev_signature = genesis_dev_signature
    genesis_live_public_key = genesis_live_public_key
    genesis_live_account = genesis_live_account_id_replaced
    genesis_live_work = genesis_live_work
    genesis_live_signature = genesis_live_signature
    genesis_test_public_key = genesis_test_public_key
    genesis_test_account = genesis_test_account_id_replaced
    genesis_test_work = genesis_test_work
    genesis_test_signature = genesis_test_signature
    beta_pre_conf_rep_account_0 = beta_pre_conf_rep_account_0
    beta_pre_conf_rep_account_1 = beta_pre_conf_rep_account_1
    beta_pre_conf_rep_public_key_0 = beta_pre_conf_rep_0_public_key
    beta_pre_conf_rep_public_key_1 = beta_pre_conf_rep_1_public_key
    beta_pre_conf_rep_private_key_0 = None
    beta_pre_conf_rep_private_key_1 = None
    live_pre_conf_rep_account_0 = live_pre_conf_rep_account_0
    live_pre_conf_rep_account_1 = live_pre_conf_rep_account_1
    live_pre_conf_rep_account_2 = live_pre_conf_rep_account_2
    live_pre_conf_rep_account_3 = live_pre_conf_rep_account_3
    live_pre_conf_rep_account_4 = live_pre_conf_rep_account_4
    live_pre_conf_rep_account_5 = live_pre_conf_rep_account_5
    live_pre_conf_rep_account_6 = live_pre_conf_rep_account_6
    live_pre_conf_rep_account_7 = live_pre_conf_rep_account_7
    live_pre_conf_rep_public_key_0 = live_pre_conf_rep_0_public_key
    live_pre_conf_rep_public_key_1 = live_pre_conf_rep_1_public_key
    live_pre_conf_rep_public_key_2 = live_pre_conf_rep_2_public_key
    live_pre_conf_rep_public_key_3 = live_pre_conf_rep_3_public_key
    live_pre_conf_rep_public_key_4 = live_pre_conf_rep_4_public_key
    live_pre_conf_rep_public_key_5 = live_pre_conf_rep_5_public_key
    live_pre_conf_rep_public_key_6 = live_pre_conf_rep_6_public_key
    live_pre_conf_rep_public_key_7 = live_pre_conf_rep_7_public_key
    live_node_peering_port = args.live_network_peering_port
    s3_bucket_name = "veriga-%s" % args.abbreviation,
    domain_svc = 'verigasvc.com'
    description = ''
    debug = 'DEBUG'
    enable_custom_domain = "false"
    custom_domain = None
    live_pre_conf_rep_private_key_0 = None
    live_pre_conf_rep_private_key_1 = None
    live_pre_conf_rep_private_key_2 = None
    live_pre_conf_rep_private_key_3 = None
    live_pre_conf_rep_private_key_4 = None
    live_pre_conf_rep_private_key_5 = None
    live_pre_conf_rep_private_key_6 = None
    live_pre_conf_rep_private_key_7 = None
    nano_network = 'live'
    beta_node_peering_port = '54000'
    test_node_peering_port = '44000'
    live_rpc_port = '7076'
    beta_rpc_port = '55000'
    test_rpc_port = '45000'
    logging = 'DEBUG'
    nault_version = '1.5.0'
    ninja_version = '663a5b24e2a8e1d423fc3311a6945cc0d234953e'
    node_version = 'V22.1'
    binary_public = 'false'
    number_of_peers = '2'
    status = 1
    created_by = None
    organization = None
    owner = None
    deleted = 'false'
    created_at = None
    updated_at = None
    deleted_by = None

    json_output = f'''{{
    "abbreviation": "{abbreviation}",
    "name": "{name}",
    "description": "{description}",
    "debug": "{debug}",
    "domain_svc": "{domain_svc}",
    "enable_custom_domain": "{enable_custom_domain}",
    "custom_domain": "{custom_domain}",
    "faucet_public_key": "{faucet_public_key}",
    "landing_public_key": "{landing_public_key}",
    "canary_beta_public_key": "{canary_beta_public_key}",
    "canary_live_public_key": "{canary_live_public_key}",
    "canary_test_public_key": "{canary_test_public_key}",
    "genesis_beta_public_key": "{genesis_beta_public_key}",
    "genesis_beta_account": "{genesis_beta_account}",
    "genesis_beta_work": "{genesis_beta_work}",
    "genesis_beta_signature": "{genesis_beta_signature}",
    "genesis_dev_public_key": "{genesis_dev_public_key}",
    "genesis_dev_private_key": "{genesis_dev_private_key}",
    "genesis_dev_account": "{genesis_dev_account}",
    "genesis_dev_work": "{genesis_dev_work}",
    "genesis_dev_signature": "{genesis_dev_signature}",
    "genesis_live_public_key": "{genesis_live_public_key}",
    "genesis_live_account": "{genesis_live_account}",
    "genesis_live_work": "{genesis_live_work}",
    "genesis_live_signature": "{genesis_live_signature}",
    "genesis_test_public_key": "{genesis_test_public_key}",
    "genesis_test_account": "{genesis_test_account}",
    "genesis_test_work": "{genesis_test_work}",
    "genesis_test_signature": "{genesis_test_signature}",
    "beta_pre_conf_rep_account_0": "{beta_pre_conf_rep_account_0}",
    "beta_pre_conf_rep_account_1": "{beta_pre_conf_rep_account_1}",
    "beta_pre_conf_rep_public_key_0": "{beta_pre_conf_rep_public_key_0}",
    "beta_pre_conf_rep_public_key_1": "{beta_pre_conf_rep_public_key_1}",
    "beta_pre_conf_rep_private_key_0": "{beta_pre_conf_rep_private_key_0}",
    "beta_pre_conf_rep_private_key_1": "{beta_pre_conf_rep_private_key_1}",
    "live_pre_conf_rep_account_0": "{live_pre_conf_rep_account_0}",
    "live_pre_conf_rep_account_1": "{live_pre_conf_rep_account_1}",
    "live_pre_conf_rep_account_2": "{live_pre_conf_rep_account_2}",
    "live_pre_conf_rep_account_3": "{live_pre_conf_rep_account_3}",
    "live_pre_conf_rep_account_4": "{live_pre_conf_rep_account_4}",
    "live_pre_conf_rep_account_5": "{live_pre_conf_rep_account_5}",
    "live_pre_conf_rep_account_6": "{live_pre_conf_rep_account_6}",
    "live_pre_conf_rep_account_7": "{live_pre_conf_rep_account_7}",
    "live_pre_conf_rep_public_key_0": "{live_pre_conf_rep_public_key_0}",
    "live_pre_conf_rep_public_key_1": "{live_pre_conf_rep_public_key_1}",
    "live_pre_conf_rep_public_key_2": "{live_pre_conf_rep_public_key_2}",
    "live_pre_conf_rep_public_key_3": "{live_pre_conf_rep_public_key_3}",
    "live_pre_conf_rep_public_key_4": "{live_pre_conf_rep_public_key_4}",
    "live_pre_conf_rep_public_key_5": "{live_pre_conf_rep_public_key_5}",
    "live_pre_conf_rep_public_key_6": "{live_pre_conf_rep_public_key_6}",
    "live_pre_conf_rep_public_key_7": "{live_pre_conf_rep_public_key_7}",
    "live_pre_conf_rep_private_key_0": "{live_pre_conf_rep_private_key_0}",
    "live_pre_conf_rep_private_key_1": "{live_pre_conf_rep_private_key_1}",
    "live_pre_conf_rep_private_key_2": "{live_pre_conf_rep_private_key_2}",
    "live_pre_conf_rep_private_key_3": "{live_pre_conf_rep_private_key_3}",
    "live_pre_conf_rep_private_key_4": "{live_pre_conf_rep_private_key_4}",
    "live_pre_conf_rep_private_key_5": "{live_pre_conf_rep_private_key_5}",
    "live_pre_conf_rep_private_key_6": "{live_pre_conf_rep_private_key_6}",
    "live_pre_conf_rep_private_key_7": "{live_pre_conf_rep_private_key_7}",
    "nano_network": "{nano_network}",
    "live_node_peering_port": "{live_node_peering_port}",
    "beta_node_peering_port": "{beta_node_peering_port}",
    "test_node_peering_port": "{test_node_peering_port}",
    "live_rpc_port": "{live_rpc_port}",
    "beta_rpc_port": "{beta_rpc_port}",
    "test_rpc_port": "{test_rpc_port}",
    "logging": "{logging}",
    "nault_version": "{nault_version}",
    "ninja_version": "{ninja_version}",
    "node_version": "{node_version}",
    "binary_public": "{binary_public}",
    "s3_bucket_name": "veriga-{abbreviation}",
    "number_of_peers": "{number_of_peers}",
    "status": {status},
    "created_by": "{created_by}",
    "organization": "{organization}",
    "owner": "{owner}",
    "deleted": "{deleted}",
    "created_at": "{created_at}",
    "updated_at": "{updated_at}",
    "deleted_by": "{deleted_by}"
}}'''

    # write keys to file
    fk = open("keys.yaml", "w")
    fk.write(keys_output)
    fk.close()

    # write blockchain create data in JSON
    fj = open("blockchain.json", "w")
    fj.write(json_output)
    fj.close()

    print(keys_output)
    print(json_output)


if args.generate_seed:
    logging.debug("Generating random 64 char hex seed...")
    seed = generate_seed()
    print(seed)

if args.generate_key_pair:
    logging.debug("Generating private/public keypair from seed")

    if not args.seed:
        logging.error("--seed not defined")
        logging.debug(args.seed)
        sys.exit(1)

    if len(str(args.key_index)) < 0:
        logging.error("--key_index not defined")
        logging.debug(len(str(args.key_index)))
        sys.exit(1)

    key_pair = generate_account_key_pair(args.seed, args.key_index)
    print(key_pair)


if args.get_account_id:
    logging.debug("Getting accont id from private/public key")
    accound_id = None

    if not args.abbreviation:
        logging.error("--abbreviation not defined")
        logging.debug(args.abbreviation)
        sys.exit(1)

    if args.public_key and not args.private_key:
        logging.debug("--private_key not defined")
        logging.debug(args.public_key)
        logging.debug("Getting account id from public key")
        accound_id = get_account_id(public_key=args.public_key,
                                    prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)

        print(accound_id)

    if not args.public_key and args.private_key:
        logging.debug("--public_key not defined")
        logging.debug("Getting account id from private key")
        accound_id = get_account_id(private_key=args.private_key,
                                    prefix=AccountIDPrefix.NANO.value).replace('nano_', '%s_' % args.abbreviation)

        print(accound_id)


if args.output_json:
    if not args.abbreviation:
        logging.error("--abbreviation not defined")
        logging.debug(args.abbreviation)
        sys.exit(1)

    output()


