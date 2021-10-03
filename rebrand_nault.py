#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
import logging

log_level = os.environ.get('LOGGING', default="INFO")
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

# Fully qualified domain name
domainsvc = get_env_variable('DOMAINSVC')

rep0 = get_env_variable('LIVE_REP0')
rep1 = get_env_variable('LIVE_REP1')

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
    "rebrand_nault.py",
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
    for dirname, dirs, files in os.walk(cwd+"/nault"):
        for file_name in files:
            filepath = os.path.join(dirname, file_name)

            for x in data:
                if is_ignored(filepath, ignore_list):
                    logging.debug("IGNORED %s" % filepath)
                else:
                    find_and_replace(filepath, x[0], x[1])


words = [
    [b"'nano_'", b"'%s_'" % str.encode(abbreviation)],
    [b"nano_abc...123", b"%s_abc...123" % str.encode(abbreviation)],
    [b"nano_1abc...", b"%s_abc..." % str.encode(abbreviation)],
    [b"nano_abc123", b"%s_abc123" % str.encode(abbreviation)],
    [b"xrb_ or nano_'", b"%s_'" % str.encode(abbreviation)],
    [b"nano_3niceeeyiaa86k58zhaeygxfkuzgffjtwju9ep33z9c8qekmr3iuc95jbqc8", b"%s_" % str.encode(abbreviation)],
    [b" NANO", b" %s" % str.encode(abbreviation.capitalize())],
    [b">NANO<", b">%s<" % str.encode(abbreviation.capitalize())],
    [b"NANO ", b"%s " % str.encode(abbreviation.capitalize())],
]
replace_all(words)

serverOptions = """  serverOptions = [
    {
      name: 'Random',
      value: 'random',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    },
    {
      name: 'My Nano Ninja',
      value: 'ninja',
      api: 'https://mynano.ninja/api/node',
      ws: 'wss://ws.mynano.ninja',
      auth: null,
      shouldRandom: true,
    },
    {
      name: 'Nanos.cc',
      value: 'nanos',
      api: 'https://nault.nanos.cc/proxy',
      ws: 'wss://nault-ws.nanos.cc',
      auth: null,
      shouldRandom: true,
    },
    {
      name: 'PowerNode',
      value: 'powernode',
      api: 'https://proxy.powernode.cc/proxy',
      ws: 'wss://ws.powernode.cc',
      auth: null,
      shouldRandom: true,
    },
    {
      name: 'Rainstorm City',
      value: 'rainstorm',
      api: 'https://rainstorm.city/api',
      ws: 'wss://rainstorm.city/websocket',
      auth: null,
      shouldRandom: true,
    },
    {
      name: 'Nanex.cc',
      value: 'nanex',
      api: 'https://api.nanex.cc',
      ws: null,
      auth: null,
      shouldRandom: false,
    },
    {
      name: 'NanoCrawler',
      value: 'nanocrawler',
      api: 'https://vault.nanocrawler.cc/api/node-api',
      ws: null,
      auth: null,
      shouldRandom: false,
    },
    {
      name: 'Custom',
      value: 'custom',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    },
    {
      name: 'Offline Mode',
      value: 'offline',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    }
  ];"""

serverOptionsReplace = """  serverOptions = [
    {{
      name: 'Random',
      value: 'random',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    }},
    {{
      name: 'RPC 1',
      value: 'rpc1',
      api: 'https://{abr}-rpc.{dsvc}/proxy',
      ws: 'wss://{abr}-ws.{dsvc}',
      auth: null,
      shouldRandom: true,
    }},
    {{
      name: 'Custom',
      value: 'custom',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    }},
    {{
      name: 'Offline Mode',
      value: 'offline',
      api: null,
      ws: null,
      auth: null,
      shouldRandom: false,
    }}
  ];""".format(abr=abbreviation, dsvc=domainsvc)
# serverOptions
find_and_replace("%sNault/src/app/services/app-settings.service.ts" % cwd,
                 str.encode(serverOptions), str.encode(serverOptionsReplace))

# nano_
find_and_replace(
    "%sNault/src/app/components/helpers/nano-account-id/nano-account-id.component.html" % cwd,
    b"nano_", str.encode(abbreviation))

# representativeAccounts
representativeAccounts = """  representativeAccounts = [
    'nano_1x7biz69cem95oo7gxkrw6kzhfywq4x5dupw4z1bdzkb74dk9kpxwzjbdhhs', // NanoCrawler
    'nano_1zuksmn4e8tjw1ch8m8fbrwy5459bx8645o9euj699rs13qy6ysjhrewioey', // Nanowallets.guide
    'nano_3chartsi6ja8ay1qq9xg3xegqnbg1qx76nouw6jedyb8wx3r4wu94rxap7hg', // Nano Charts
    'nano_1ninja7rh37ehfp9utkor5ixmxyg8kme8fnzc4zty145ibch8kf5jwpnzr3r', // My Nano Ninja
    'nano_1iuz18n4g4wfp9gf7p1s8qkygxw7wx9qfjq6a9aq68uyrdnningdcjontgar', // NanoTicker / Json
    'nano_3power3gwb43rs7u9ky3rsjp6fojftejceexfkf845sfczyue4q3r1hfpr3o', // PowerNode
  ];"""

representativeAccountsReplace = """  representativeAccounts = [
    '{rep0}',
    '{rep1}',
  ];""".format(rep0=rep0, rep1=rep1)
find_and_replace("%sNault/src/app/services/nano-block.service.ts" % cwd,
                 str.encode(representativeAccounts),
                 str.encode(representativeAccountsReplace))

# defaultRepresentatives
defaultRepresentatives = """  defaultRepresentatives = [
    {
      id: 'nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4',
      name: 'Nano Foundation #1',
      warn: true,
    },
    {
      id: 'nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou',
      name: 'Nano Foundation #2',
      warn: true,
    },
    {
      id: 'nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p',
      name: 'Nano Foundation #3',
      warn: true,
    },
    {
      id: 'nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m',
      name: 'Nano Foundation #4',
      warn: true,
    },
    {
      id: 'nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k',
      name: 'Nano Foundation #5',
      warn: true,
    },
    {
      id: 'nano_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy',
      name: 'Nano Foundation #6',
      warn: true,
    },
    {
      id: 'nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs',
      name: 'Nano Foundation #7',
      warn: true,
    },
    {
      id: 'nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1',
      name: 'Nano Foundation #8',
      warn: true,
    },
  ];"""

defaultRepresentativesReplace = """  defaultRepresentatives = [
    {{
      id: '{rep0}',
      name: 'Official Representative #1',
      warn: false,
    }},
    {{
      id: '{rep1}',
      name: 'Official Representative #1',
      warn: false,
    }},
  ];""".format(rep0=rep0, rep1=rep1)
find_and_replace("%sNault/src/app/services/representative.service.ts" % cwd,
                 str.encode(defaultRepresentatives),
                 str.encode(defaultRepresentativesReplace))
