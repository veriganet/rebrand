#!/usr/bin/env python3
import logging

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

# Fully qualified domain name
domainsvc = lib.get_env_variable('DOMAINSVC')

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

bananoPublicAddress = "    p = re.compile('^(ban)_[13]{1}[13456789abcdefghijkmnopqrstuwxyz]{59}$')"
bananoPublicAddressReplace = "    p = re.compile('^('+os.getenv(\"ABBREVIATION\", \"ban\")+')_[13]{1}[13456789abcdefghijkmnopqrstuwxyz]{59}$')"
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
                                                                                    abbreviation_len,
                                                                                    abbreviation)
lib.find_and_replace("%sboompow/server/bpow/validators.py" % lib.cwd(),
                 str.encode(validateChecksumxrb1),
                 str.encode(validateChecksumxrb1Replace))

validateChecksumxrb2 = "acrop_key = address[4:-8]"
validateChecksumxrb2Replace = "acrop_key = address[%s:-8]" % abbreviation_len
lib.find_and_replace("%sboompow/server/bpow/validators.py" % lib.cwd(),
                 str.encode(validateChecksumxrb2),
                 str.encode(validateChecksumxrb2Replace))

# replace urls
urls = [
    [b"bpow.banano.cc", b"%s-bpow.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
    [b"chat.banano.cc", b"%s-chat.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
    [b"https://banano.cc", b"https://%s.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
]
lib.replace_all(urls, ignore_list, "/boompow")
