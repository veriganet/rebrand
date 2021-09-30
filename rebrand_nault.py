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


# serverOptions
find_and_replace("%sNault/src/app/services/app-settings.service.ts" % cwd,
                 str.encode(serverOptions), str.encode(serverOptionsReplace))
