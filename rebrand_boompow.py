#!/usr/bin/env python3
import logging

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

# Default boompow payout address
boompow_payout_address = lib.get_env_variable('BOOMPOW_PAYOUT_ADDRESS')

# Fully qualified domain name
domainsvc = lib.get_env_variable('DOMAINSVC')

work_threshold = lib.get_env_variable('WORK_THRESHOLD')
work_thresholds = work_threshold.split(",")
work_threshold_default = lib.get_env_variable('WORK_THRESHOLD_DEFAULT')

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
    "env_example",
    "node_modules",
    "nanocurrency-js"
]

words = [
    [b"previous, difficulty='fffffff800000000'", b"previous, difficulty='%s'" % str.encode(work_threshold_default)],
    [b"base_difficulty='fffffe0000000000'", b"base_difficulty='%s'" % str.encode(work_thresholds[0])],
    [b"DEFAULT_WORK_DIFFICULTY = 'fffffe0000000000'", b"DEFAULT_WORK_DIFFICULTY = '%s'" % str.encode(work_thresholds[0])],
    [b'"difficulty": "fffffe0000000000"', b'"difficulty": "%s"' % str.encode(work_thresholds[0])],
    [b'default `fffffe0000000000`', b'default `%s`' % str.encode(work_thresholds[0])],
]
lib.replace_all(words, ignore_list, "/NanoRPCProxy")

bananoPublicAddress = "    p = re.compile('^(ban)_[13]{1}[13456789abcdefghijkmnopqrstuwxyz]{59}$')"
bananoPublicAddressReplace = "    p = re.compile('^(%s)_[13]{1}[13456789abcdefghijkmnopqrstuwxyz]{59}$')" % abbreviation
lib.find_and_replace("%sboompow/client/config_parse.py" % lib.cwd(),
                 str.encode(bananoPublicAddress),
                 str.encode(bananoPublicAddressReplace))

payoutAddress = "ban_1boompow14irck1yauquqypt7afqrh8b6bbu5r93pc6hgbqs7z6o99frcuym"
payoutAddressReplace = "%s_123...1234" % abbreviation
lib.find_and_replace("%sboompow/client/run_windows.bat" % lib.cwd(),
                 str.encode(payoutAddress),
                 str.encode(payoutAddressReplace))

notAValidAddress = 'msg = "%r is not a valid BANANO address" % string'
notAValidAddressReplace = 'msg = "%r is not a valid address" % string'
lib.find_and_replace("%sboompow/client/config_parse.py" % lib.cwd(),
                 str.encode(notAValidAddress),
                 str.encode(notAValidAddressReplace))

addressRegex = "address_regex = '(?:ban)(?:_)(?:1|3)(?:[13456789abcdefghijkmnopqrstuwxyz]{59})'"
addressRegexReplace = "address_regex = '(?:%s)(?:_)(?:1|3)(?:[13456789abcdefghijkmnopqrstuwxyz]{59})'" % abbreviation
lib.find_and_replace("%sboompow/server/bpow/validators.py" % lib.cwd(),
                 str.encode(addressRegex),
                 str.encode(addressRegexReplace))

abbreviation_len = len(abbreviation)
address_len = 64

if abbreviation_len == 3:
    address_len = 64
elif abbreviation_len == 4:
    address_len = 65
else:
    logging.error("Wrong abbreviation length!")

validateChecksumxrb1 = "if len(address) == 64 and address[:4] == 'ban_':"
validateChecksumxrb1Replace = "if len(address) == %s and address[:%s] == '%s_':" % (address_len,
                                                                                    str(abbreviation_len+1),
                                                                                    abbreviation)
lib.find_and_replace("%sboompow/server/bpow/validators.py" % lib.cwd(),
                 str.encode(validateChecksumxrb1),
                 str.encode(validateChecksumxrb1Replace))

validateChecksumxrb2 = "acrop_key = address[4:-8]"
validateChecksumxrb2Replace = "acrop_key = address[%s:-8]" % str(abbreviation_len+1)
lib.find_and_replace("%sboompow/server/bpow/validators.py" % lib.cwd(),
                 str.encode(validateChecksumxrb2),
                 str.encode(validateChecksumxrb2Replace))

requirementsSerever = """ujson
uvloop
aiohttp
aioredis
amqtt
websockets
requests
asyncio-throttle
nanolib
bitstring
redis"""
requirementsSereverReplace = """aiohttp==3.7.4.post0
aioredis==1.3.1
amqtt==0.10.0a3
async-timeout==3.0.1
asyncio-throttle==1.0.2
attrs==21.2.0
bitstring==3.1.7
certifi==2021.5.30
chardet==4.0.0
docopt==0.6.2
ed25519-blake2b==1.4
hiredis==2.0.0
idna==2.10
multidict==5.1.0
nanolib==0.4.3
passlib==1.7.4
py-cpuinfo==8.0.0
PyYAML==5.4.1
redis==3.5.3
requests==2.25.1
six==1.16.0
transitions==0.8.8
typing-extensions==3.10.0.0
ujson==4.0.2
urllib3==1.26.5
uvloop==0.15.2
websockets==8.1
yarl==1.6.3"""
lib.find_and_replace("%sboompow/server/requirements.txt" % lib.cwd(),
                     str.encode(requirementsSerever),
                     str.encode(requirementsSereverReplace))
# replace urls
urls = [
    [b"bpow.banano.cc", b"%s-bpow.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
    [b"chat.banano.cc", b"%s-chat.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
    [b"https://banano.cc", b"https://%s.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
]
lib.replace_all(urls, ignore_list, "/boompow")
