#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys

main_desc = "Script to rebrand nano-node as new block chain." \
            "Example: " \
            "rebrand.py -b kor"

# Initiate the parser
parser = argparse.ArgumentParser(description=main_desc)

# version arg
parser.add_argument("-V", "--version", help="Shows version", action="store_true")

# debug
parser.add_argument("--debug", help="Enable debug", action="store_true")

# abbreviation
parser.add_argument("-a", "--abbreviation", help="Three or four letter abbreviation of new block chain. Example: kor, "
                                                 "nano")

# name
parser.add_argument("-n", "--name", help="Full name of the block chain. Example: KORcoin")

# domain
parser.add_argument("-d", "--domain", help="Fully qualified domain name for official nodes / representatives. "
                                           "Example: korcoin.net")

# Read arguments from the command line
args = parser.parse_args()

# Check for --version or -V
if args.version:
    print("0.0.1")

words = [
    ["nano_pow_server", "kor_pow_server"],
    ["RaiBlocksDev", "KorBlocksDev"],
    ["RaiBlocksBeta", "KorBlocksBeta"],
    ["RaiBlocksTest", "KorBlocksTest"],
    ["Nanocurrency", "Korcurrency"],
    ["nanocurrency", "korcurrency"],
    ["nano_wallet", "kor_wallet"],
    ["nano_node", "kor_node"],
    ["nano_rpc", "kor_rpc"],
    ["NanoDev", "KorDev"],
    ["NanoBeta", "KorBeta"],
    ["NanoTest", "KorTest"],
    ["nanodir", "kordir"],
    [" nano ", " kor "],
    [" Nano ", " Kor "],
    [" NANO ", " KOR "],
    ["Nano", "Kor"],
    ["NANO", "KOR"],
]

urls = [
    ["security\@nano.org", "security\@kor.org"],
    ["info\@nano.org", "info\@kor.org"],
    ["russel\@nano.org", "contact\@kor.org"],
    ["https\:\/\/nano.org", "https\:\/\/kor.org"],
    ["https\:\/\/nano.org/", "https\:\/\/kor.org\/"],
    ["https\:\/\/docs.nano.org", "https\:\/\/docs.kor.org"],
    ["https\:\/\/chat.nano.org", "https\:\/\/chat.kor.org"],
    ["https\:\/\/content.nano.org", "https\:\/\/content.kor.org"],
    ["peering-beta.nano.org", "peering-beta.kor.org"],
    ["peering.nano.org", "peering.kor.org"],
    ["peering-test.nano.org", "peering-test.kor.org"],
    ["repo.nano.org", "repo.kor.org"],
    ["nano.org", "kor.org"],
]

dirs = [
    [".\/nano\/nano_node", ".\/nano\/kor_node"],
    [".\/nano\/nano_rpc", ".\/nano\/kor_rpc"],
    [".\/nano\/nano_wallet", ".\/nano\/kor_wallet"],
]


def command_result(dir_path, old, new):
    return print(subprocess.run("grep -rl "
                                "--exclude-dir={.git,.github,miniupnp,lmdb,crypto,gtest,cpptoml,"
                                "nano-pow-server,flatbuffers,rocksdb,.idea,util,docker,ci,venv} "
                                "--exclude={rebrand.py,.gitmodules,README.md,SECURITY.md} %s . | xargs sed -i "
                                "'s/%s/%s/g'" %
                                (old, old, new),
                                cwd=dir_path,
                                shell=True,
                                text=True))


# replace words
for word in words:
    command_result("./", word[0], word[1])

# replace urls
for url in urls:
    command_result("./", url[0], url[1])

# rename directories
for d in dirs:
    if os.path.exists(d[0]):
        os.rename(d[0], d[1])