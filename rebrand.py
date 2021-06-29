#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
import logging

log_level = os.environ.get('DEBUG', default="DEBUG")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log_level)


def remove_prefix(text, prefix):
    return text[len(prefix):] if text.startswith(prefix) else text


cwd = "./"
logging.debug(cwd)
if os.environ.get("CI") == "true" and os.environ.get("DRONE") == "true":
    cwd = "/drone/src/"


def get_env_variable(env):
    if not os.environ.get(env, None):
        return logging.error("%s is not defined!" % env)
    else:
        logging.debug("%s properly set." % env)
        return os.environ.get(env)


# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = get_env_variable('ABBREVIATION')

# Visible name of the block chain
block_name = get_env_variable('BLOCK_NAME')

# Public key of canary account for beta environment
canary_beta_public_key = get_env_variable('CANARY_BETA_PUBLIC_KEY')

# Public key of canary account for live environment
canary_live_public_key = get_env_variable('CANARY_LIVE_PUBLIC_KEY')

# Public key of canary account for live environment
canary_test_public_key = get_env_variable('CANARY_TEST_PUBLIC_KEY')

# Fully qualified domain name for official nodes / representatives"
# "Default: [abbreviation].block.veriga.net"
# "Example: korcoin.net"
domain = get_env_variable('DOMAIN')

# Public key of faucet account
faucet_public_key = get_env_variable('FAUCET_PUBLIC_KEY')

# Public key of landing account
landing_public_key = get_env_variable('LANDING_PUBLIC_KEY')

# Genesis public account data for dev environment
genesis_dev_public_key = get_env_variable('GENESIS_DEV_PUBLIC_KEY')
genesis_dev_private_key = get_env_variable('GENESIS_DEV_PRIVATE_KEY')
genesis_dev_account = get_env_variable('GENESIS_DEV_ACCOUNT')
genesis_dev_work = get_env_variable('GENESIS_DEV_WORK')
genesis_dev_signature = get_env_variable('GENESIS_DEV_SIGNATURE')

# Genesis public account data for beta environment
genesis_beta_public_key = get_env_variable('GENESIS_BETA_PUBLIC_KEY')
genesis_beta_account = get_env_variable('GENESIS_BETA_ACCOUNT')
genesis_beta_work = get_env_variable('GENESIS_BETA_WORK')
genesis_beta_signature = get_env_variable('GENESIS_BETA_SIGNATURE')

# Genesis public account data for live environment
genesis_live_public_key = get_env_variable('GENESIS_LIVE_PUBLIC_KEY')
genesis_live_account = get_env_variable('GENESIS_LIVE_ACCOUNT')
genesis_live_work = get_env_variable('GENESIS_LIVE_WORK')
genesis_live_signature = get_env_variable('GENESIS_LIVE_SIGNATURE')

# Genesis public account data for test environment
genesis_test_public_key = get_env_variable('GENESIS_TEST_PUBLIC_KEY')
genesis_test_account = get_env_variable('GENESIS_TEST_ACCOUNT')
genesis_test_work = get_env_variable('GENESIS_TEST_WORK')
genesis_test_signature = get_env_variable('GENESIS_TEST_SIGNATURE')

live_pre_configured_rep0 = get_env_variable('LIVE_PRE_CONFIGURED_REP0')
live_pre_configured_rep1 = get_env_variable('LIVE_PRE_CONFIGURED_REP1')
live_pre_configured_rep2 = get_env_variable('LIVE_PRE_CONFIGURED_REP2')
live_pre_configured_rep3 = get_env_variable('LIVE_PRE_CONFIGURED_REP3')
live_pre_configured_rep4 = get_env_variable('LIVE_PRE_CONFIGURED_REP4')
live_pre_configured_rep5 = get_env_variable('LIVE_PRE_CONFIGURED_REP5')
live_pre_configured_rep6 = get_env_variable('LIVE_PRE_CONFIGURED_REP6')
live_pre_configured_rep7 = get_env_variable('LIVE_PRE_CONFIGURED_REP7')

live_node_peering_port = get_env_variable('LIVE_NODE_PEERING_PORT')
beta_node_peering_port = get_env_variable('BETA_NODE_PEERING_PORT')
test_node_peering_port = get_env_variable('TEST_NODE_PEERING_PORT')

live_rpc_port = get_env_variable('LIVE_RPC_PORT')
beta_rpc_port = get_env_variable('BETA_RPC_PORT')
test_rpc_port = get_env_variable('TEST_RPC_PORT')

main_desc = "Script to rebrand nano-node as new block chain." \
            "Example: " \
            "rebrand.py"

# Initiate the parser
parser = argparse.ArgumentParser(description=main_desc)

# debug
parser.add_argument("--debug", help="Enable debug", action="store_true")

# version arg
parser.add_argument("-V", "--version", help="Shows version", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

# Check for --version or -V
if args.version:
    print("V22.0_0.0.1")

accounts = [
    # nano/core_test/block.cpp .account_address
    [
        b"xrb_15nhh1kzw3x8ohez6s75wy3jr6dqgq65oaede1fzk5hqxk4j8ehz7iqtb3to",
        b"%s_15nhh1kzw3x8ohez6s75wy3jr6dqgq65oaede1fzk5hqxk4j8ehz7iqtb3to" % str.encode(abbreviation)
    ],
    # nano/core_test/block.cpp .representative_address
    [
        b"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
        b"%s_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou" % str.encode(abbreviation)
    ],
    # nano/core_test/block.cpp .account_address burn
    [
        b"xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        b"%s_1111111111111111111111111111111111111111111111111111hifc8npp" % str.encode(abbreviation)
    ],
    [
        b"nano_1111111111111111111111111111111111111111111111111111hifc8npp",
        b"%s_1111111111111111111111111111111111111111111111111111hifc8npp" % str.encode(abbreviation)
    ],
    # nano/core_test/block.cpp
    [
        b"xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        b"%s_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3" % str.encode(abbreviation)
    ],
    # nano/core_test/block.cpp
    [
        b"xrb_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf",
        b"%s_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf" % str.encode(abbreviation)
    ],
    # nano/core_test/block.cpp
    [
        b"xrb_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb",
        b"%s_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb" % str.encode(abbreviation)
    ],
    [
        b"nano_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb",
        b"%s_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb" % str.encode(abbreviation)
    ],
    # nano/core_test/toml.cpp preconfigured_representatives
    [
        b"nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
        b"%s_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4" % str.encode(abbreviation)
    ],
    # nano/node/nodeconfig.cpp offline_representative.decode_account
    [
        b"nano_1defau1t9off1ine9rep99999999999999999999999999999999wgmuzxxy",
        b"%s_1defau1t9off1ine9rep99999999999999999999999999999999wgmuzxxy" % str.encode(abbreviation)
    ]
]

canary_public_keys = [
    # nano/secure/common.cpp
    [
        b'beta_canary_public_key_data = "868C6A9F79D4506E029B378262B91538C5CB26D7C346B63902FFEB365F1C1947"',
        b'beta_canary_public_key_data = "%s"' % str.encode(canary_beta_public_key)
    ],
    [
        b'live_canary_public_key_data = "7CBAF192A3763DAEC9F9BAC1B2CDF665D8369F8400B4BC5AB4BA31C00BAA4404"',
        b'live_canary_public_key_data = "%s"' % str.encode(canary_live_public_key)
    ],
    [
        b'test_canary_public_key_data = nano::get_env_or_default ("NANO_TEST_CANARY_PUB", '
        b'"3BAD2C554ACE05F5E528FBBCE79D51E552C55FA765CCFD89B289C4835DE5F04A")',
        b'test_canary_public_key_data = nano::get_env_or_default ("NANO_TEST_CANARY_PUB", '
        b'"%s")' % str.encode(canary_test_public_key)
    ]
]

dirs = [
    ["%snano/nano_node" % cwd, "%snano/%s_node" % (cwd, abbreviation)],
    ["%snano/nano_rpc" % cwd, "%snano/%s_rpc" % (cwd, abbreviation)],
    ["%snano/nano_wallet" % cwd, "%snano/%s_wallet" % (cwd, abbreviation)],
]

landing_faucet_keys = [
    # nano/node/json_handler.cpp landing_balance
    [
        b"059F68AAB29DE0D3A27443625C7EA9CDDB6517A8B76FE37727EF6A4D76832AD5",
        b"%s" % str.encode(landing_public_key)
    ],
    # nano/node/json_handler.cpp faucet_balance
    [
        b"8E319CE6F3025E5B2DF66DA7AB1467FE48F1679C13DD43BFDB29FA2E9FC40D3B",
        b"%s" % str.encode(faucet_public_key)
    ]
]

ignore_list = [
    "build",
    "git",
    "github",
    "miniupnp",
    "crypto",
    "lmd",
    "gtest",
    "cpptoml",
    "flatbuffers",
    "rocksd",
    "idea",
    "docker",
    "venv",
    "cmake-build-debug",
    "rebrand.py",
    "gitmodules",
    "gitignore",
    "README.md",
    "SECURITY.md",
    "rep_weights_beta",
    "rep_weights_live",
    "clang-format",
    "env_local",
    "env_example"
]

genesis_keys = [
    [
        b'dev_private_key_data = "34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4"',
        b'dev_private_key_data = "%s"' % str.encode(genesis_dev_private_key)
    ],
    [
        b'dev_public_key_data = "B0311EA55708D6A53C75CDBF88300259C6D018522FE3D4D0A242E431F9E8B6D0"',
        b'dev_public_key_data = "%s"' % str.encode(genesis_dev_public_key)
    ],
    [
        b'beta_public_key_data = "259A43ABDB779E97452E188BA3EB951B41C961D3318CA6B925380F4D99F0577A"',
        b'beta_public_key_data = "%s"' % str.encode(genesis_beta_public_key)
    ],
    [
        b'live_public_key_data = "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA"',
        b'live_public_key_data = "%s"' % str.encode(genesis_live_public_key)
    ],
    [
        b'test_public_key_data = nano::get_env_or_default ("NANO_TEST_GENESIS_PUB", '
        b'"45C6FF9D1706D61F0821327752671BDA9F9ED2DA40326B01935AB566FB9E08ED")',
        b'test_public_key_data = nano::get_env_or_default ("NANO_TEST_GENESIS_PUB", '
        b'"%s")' % str.encode(genesis_test_public_key)
    ]
]

genesis_dev_data = [
    [b"B0311EA55708D6A53C75CDBF88300259C6D018522FE3D4D0A242E431F9E8B6D0", b"%s" % str.encode(genesis_dev_public_key)],
    [b"xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo", b"%s" % str.encode(genesis_dev_account)],
    [b"7b42a00ee91d5810", b"%s" % str.encode(genesis_dev_work)],
    [b"ECDA914373A2F0CA1296475BAEE40500A7F0A7AD72A5A80C81D7FAB7F6C802B2CC7DB50F5DD0FB25B2EF11761FA7344A158DD5A700B21BD47DE5BD0F63153A02",
     b"%s" % str.encode(genesis_dev_signature)]
]

genesis_beta_data = [
    [b"259A43ABDB779E97452E188BA3EB951B41C961D3318CA6B925380F4D99F0577A", b"%s" % str.encode(genesis_beta_public_key)],
    [b"nano_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1", b"%s" % str.encode(genesis_beta_account)],
    [b"79d4e27dc873c6f2", b"%s" % str.encode(genesis_beta_work)],
    [b"4BD7F96F9ED2721BCEE5EAED400EA50AD00524C629AE55E9AFF11220D2C1B00C3D4B3BB770BF67D4F8658023B677F91110193B6C101C2666931F57046A6DB806",
     b"%s" % str.encode(genesis_beta_signature)]
]

genesis_live_data = [
    [b"E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA", b"%s" % str.encode(genesis_live_public_key)],
    [b"xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3", b"%s" % str.encode(genesis_live_account)],
    [b"62f05417dd3fb691", b"%s" % str.encode(genesis_live_work)],
    [b"9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02",
     b"%s" % str.encode(genesis_live_signature)]
]

genesis_test_data = [
    [b"45C6FF9D1706D61F0821327752671BDA9F9ED2DA40326B01935AB566FB9E08ED", b"%s" % str.encode(genesis_live_public_key)],
    [b"nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j", b"%s" % str.encode(genesis_live_account)],
    [b"bc1ef279c1a34eb1", b"%s" % str.encode(genesis_live_work)],
    [b"15049467CAEE3EC768639E8E35792399B6078DA763DA4EBA8ECAD33B0EDC4AF2E7403893A5A602EB89B978DABEF1D6606BB00F3C0EE11449232B143B6E07170E",
     b"%s" % str.encode(genesis_live_signature)]
]

live_preconf_reps = [
    [
        b"A30E0A32ED41C8607AA9212843392E853FCBCB4E7CB194E35C94F07F91DE59EF",
        b"%s" % str.encode(live_pre_configured_rep0)
    ],
    [
        b"67556D31DDFC2A440BF6147501449B4CB9572278D034EE686A6BEE29851681DF",
        b"%s" % str.encode(live_pre_configured_rep1)
    ],
    [
        b"5C2FBB148E006A8E8BA7A75DD86C9FE00C83F5FFDBFD76EAA09531071436B6AF",
        b"%s" % str.encode(live_pre_configured_rep2)
    ],
    [
        b"AE7AC63990DAAAF2A69BF11C913B928844BF5012355456F2F164166464024B29",
        b"%s" % str.encode(live_pre_configured_rep3)
    ],
    [
        b"BD6267D6ECD8038327D2BCC0850BDF8F56EC0414912207E81BCF90DFAC8A4AAA",
        b"%s" % str.encode(live_pre_configured_rep4)
    ],
    [
        b"2399A083C600AA0572F5E36247D978FCFC840405F8D4B6D33161C0066A55F431",
        b"%s" % str.encode(live_pre_configured_rep5)
    ],
    [
        b"2298FAB7C61058E77EA554CB93EDEEDA0692CBFCC540AB213B2836B29029E23A",
        b"%s" % str.encode(live_pre_configured_rep6)
    ],
    [
        b"3FE80B4BC842E82C1C18ABFEEC47EA989E63953BC82AC411F304D13833D52A56",
        b"%s" % str.encode(live_pre_configured_rep7)
    ]
]

urls = [
    [b"security\@nano.org", b"security\@%s" % str.encode(domain)],
    [b"info\@nano.org", b"info\@%s" % str.encode(domain)],
    [b"russel\@nano.org", b"contact\@%s" % str.encode(domain)],
    [b"https\:\/\/nano.org", b"https\:\/\/%s" % str.encode(domain)],
    [b"https\:\/\/nano.org/", b"https\:\/\/%s\/" % str.encode(domain)],
    [b"https\:\/\/docs.nano.org", b"https\:\/\/docs.%s" % str.encode(domain)],
    [b"https\:\/\/chat.nano.org", b"https\:\/\/chat.%s" % str.encode(domain)],
    [b"https\:\/\/content.nano.org", b"https\:\/\/content.%s" % str.encode(domain)],
    [b"peering-beta.nano.org", b"peering-beta.%s" % str.encode(domain)],
    [b"peering.nano.org", b"peering.%s" % str.encode(domain)],
    [b"peering-test.nano.org", b"peering-test.%s" % str.encode(domain)],
    [b"repo.nano.org", b"repo.%s" % str.encode(domain)],
    [b"nano.org", b"%s" % str.encode(domain)],
]

words = [
    [b"nano_pow_server", b"%s_pow_server" % str.encode(abbreviation)],
    [b"RaiBlocksDev", b"%sBlocksDev" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"RaiBlocksBeta", b"%sBlocksBeta" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"RaiBlocksTest", b"%sBlocksTest" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"Nanocurrency", b"%scurrency" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"nanocurrency", b"%scurrency" % str.encode(abbreviation)],
    [b"nano_wallet", b"%s_wallet" % str.encode(abbreviation)],
    [b"nano_node", b"%s_node" % str.encode(abbreviation)],
    [b"nano_rpc", b"%s_rpc" % str.encode(abbreviation)],
    [b"nano-node", b"%s-node" % str.encode(abbreviation)],
    [b"NanoDev", b"%sDev" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"NanoBeta", b"%sBeta" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"NanoTest", b"%sTest" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"nanodir", b"%sdir" % str.encode(abbreviation)],
    [b" Nano ", b" %s " % str.encode(abbreviation[0].upper() + abbreviation[1:])],
    [b"Nano", b"%s" % str.encode(abbreviation[0].upper() + abbreviation[1:])],
]


def key_create(a):
    lines = []
    proc = subprocess.Popen(['%snano-node-22.0.0-Linux/bin/nano_node' % cwd, '--key_create'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        lines.append(str(line.rstrip()))

    private = lines[0].split(": ")[1].rstrip("'")
    public = lines[1].split(": ")[1].rstrip("'")
    account = lines[2].split(": ")[1].rstrip("'").replace("nano_", a)

    return print('''{
    "private": "%s",
    "public": "%s",
    "account": "%s"
}
    ''' % (private, public, account))


def is_ignored(f, w_list):
    if args.debug:
        print("f: %s" % f)
        print("Ignored words: %s" % w_list)

    if w_list is not None:
        if re.compile('|'.join(w_list)).search(f):
            return True
        else:
            return False
    else:
        return False


def find_and_replace(filename, find, replace):
    with open(filename, "rb") as orig_file_obj:
        with open("%s.tmp" % filename, "wb") as new_file_obj:
            orig_text = orig_file_obj.read()
            new_text = orig_text.replace(find, replace)
            new_file_obj.write(new_text)

    shutil.copyfile("%s.tmp" % filename, filename)
    os.remove("%s.tmp" % filename)


def replace_all(data):
    for dirname, dirs, files in os.walk(cwd):
        for file_name in files:
            filepath = os.path.join(dirname, file_name)

            for x in data:
                if is_ignored(filepath, ignore_list):
                    logging.debug("IGNORED %s" % filepath)
                else:
                    find_and_replace(filepath, x[0], x[1])


# rename directories
for d in dirs:
    if os.path.exists(d[0]):
        os.rename(d[0], d[1])

# replace word
replace_all(words)

# replace urls
replace_all(urls)

# replace dev_genesis_data
for data in genesis_dev_data:
    find_and_replace("%snano/secure/common.cpp" % cwd, data[0], data[1])
    logging.debug("Found %s" % data[0])
    logging.debug("Replaced %s" % data[1])

# replace beta_genesis_data
for data in genesis_beta_data:
    find_and_replace("%snano/secure/common.cpp" % cwd, data[0], data[1])
    logging.debug("Found %s" % data[0])
    logging.debug("Replaced %s" % data[1])

# replace live_genesis_data
for data in genesis_live_data:
    find_and_replace("%snano/secure/common.cpp" % cwd, data[0], data[1])
    logging.debug("Found %s" % data[0])
    logging.debug("Replaced %s" % data[1])

# replace test_genesis_data
for data in genesis_test_data:
    find_and_replace("%snano/secure/common.cpp" % cwd, data[0], data[1])
    logging.debug("Found %s" % data[0])
    logging.debug("Replaced %s" % data[1])

# replace accounts
replace_all(accounts)

# replace landing / faucet account
for key in landing_faucet_keys:
    find_and_replace("%snano/node/json_handler.cpp" % cwd, key[0], key[1])

# replace live preconfigured representative
for rep in live_preconf_reps:
    find_and_replace("%snano/node/nodeconfig.cpp" % cwd, rep[0], rep[1])

# replace canary public keys
for key in canary_public_keys:
    find_and_replace("%snano/secure/common.cpp" % cwd, key[0], key[1])

list_abbreviation = list(abbreviation)

# replace _onan
find_and_replace("%snano/lib/numbers.cpp" % cwd,
                 b'destination_a.append ("_onan"); // nano_',
                 b'destination_a.append ("_%s"); // %s_' % (str.encode(''.join(list_abbreviation[::-1])),
                                                            str.encode(abbreviation))
                 )

# replace xrb_ prefix
find_and_replace("%snano/lib/numbers.cpp" % cwd,
                 b"auto xrb_prefix (source_a[0] == 'x' && source_a[1] == 'r' && source_a[2] == 'b' && (source_a[3] == "
                 b"'_' || source_a[3] == '-'));",
                 b"auto xrb_prefix (source_a[0] == '%s' && source_a[1] == '%s' && source_a[2] == '%s' && (source_a[3] "
                 b"== '_' || source_a[3] == '-'));" % (str.encode(list_abbreviation[0]),
                                                       str.encode(list_abbreviation[1]),
                                                       str.encode(list_abbreviation[2]))
                 )

if len(list_abbreviation) == 3:
    # replace nano_ prefix
    find_and_replace("%snano/lib/numbers.cpp" % cwd,
                     b"auto nano_prefix (source_a[0] == 'n' && source_a[1] == 'a' && source_a[2] == 'n' && source_a[3] == "
                     b"'o' && (source_a[4] == '_' || source_a[4] == '-'));",
                     b"auto nano_prefix (source_a[0] == '%s' && source_a[1] == '%s' && source_a[2] == '%s' && source_a[3] "
                     b"== 'c' && (source_a[4] == '_' || source_a[4] == '-'));" % (str.encode(list_abbreviation[0]),
                                                                                  str.encode(list_abbreviation[1]),
                                                                                  str.encode(list_abbreviation[2]))
                     )
else:
    # replace nano_ prefix
    find_and_replace("%snano/lib/numbers.cpp" % cwd,
                     b"auto nano_prefix (source_a[0] == 'n' && source_a[1] == 'a' && source_a[2] == 'n' && source_a[3] == "
                     b"'o' && (source_a[4] == '_' || source_a[4] == '-'));",
                     b"auto nano_prefix (source_a[0] == '%s' && source_a[1] == '%s' && source_a[2] == '%s' && source_a[3] "
                     b"== '%s' && (source_a[4] == '_' || source_a[4] == '-'));" % (str.encode(list_abbreviation[0]),
                                                                                   str.encode(list_abbreviation[1]),
                                                                                   str.encode(list_abbreviation[2]),
                                                                                   str.encode(list_abbreviation[3]))
                     )

# build.sh
find_and_replace("%sdocker/node/entry.sh" % cwd, b"nano-node", b"%s-node" % str.encode(abbreviation))

# Dockerfile
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"make nano_node", b"make %s_node" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"make nano_rpc", b"make %s_rpc" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"make nano_pow_server", b"make %s_pow_server" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd,
                 b"RUN groupadd --gid 1000 nanocurrency",
                 b"RUN groupadd --gid 1000 %scurrency" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd,
                 b"useradd --uid 1000 --gid nanocurrency",
                 b"useradd --uid 1000 --gid %scurrency" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd,
                 b"useradd --uid 1000 --gid nanocurrency --shell /bin/bash --create-home nanocurrency",
                 b"useradd --uid 1000 --gid nanocurrency --shell /bin/bash --create-home %scurrency" %
                 str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"/tmp/build/nano_", b"/tmp/build/%s_" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"/usr/bin/nano_node", b"/usr/bin/%s_node" % str.encode(abbreviation))
find_and_replace("%sdocker/node/Dockerfile" % cwd, b"\"nano_node\"", b"\"%s_node\"" % str.encode(abbreviation))

# entry.sh
find_and_replace("%sdocker/node/entry.sh" % cwd, b"nano_node", b"%s_node" % str.encode(abbreviation))
find_and_replace("%sdocker/node/entry.sh" % cwd, b"/Nano", b"/%s" % str.encode(abbreviation[0].upper() + abbreviation[1:]))

# rename nano_pow_server.cpp
if os.path.exists("%snano-pow-server/src/entry/nano_pow_server.cpp" % cwd):
    os.rename("%snano-pow-server/src/entry/nano_pow_server.cpp" % cwd, "%snano-pow-server/src/entry/kor_pow_server.cpp" % cwd)

# replace ports
# node
find_and_replace("%snano/core_test/toml.cpp" % cwd, b"7075", b"%s" % str.encode(live_node_peering_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"7075", b"%s" % str.encode(live_node_peering_port))
find_and_replace("%snano/lib/config.hpp" % cwd, b"7075", b"%s" % str.encode(live_node_peering_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"54000", b"%s" % str.encode(beta_node_peering_port))
find_and_replace("%snano/lib/config.hpp" % cwd, b"54000", b"%s" % str.encode(beta_node_peering_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"44000", b"%s" % str.encode(test_node_peering_port))
find_and_replace("%snano/lib/config.hpp" % cwd, b"44000", b"%s" % str.encode(test_node_peering_port))
find_and_replace("%snano/qt/qt.cpp" % cwd, b"7075", b"%s" % str.encode(live_node_peering_port))

#rpc
find_and_replace("%snano/lib/config.cpp" % cwd, b"7076", b"%s" % str.encode(live_rpc_port))
find_and_replace("%sci/record_rep_weights.py" % cwd, b"7076", b"%s" % str.encode(live_rpc_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"17076", b"1%s" % str.encode(live_rpc_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"55000", b"%s" % str.encode(beta_rpc_port))
find_and_replace("%snano/lib/config.cpp" % cwd, b"45000", b"%s" % str.encode(test_rpc_port))
