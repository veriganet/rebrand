#!/usr/bin/env python3
import logging

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

# Fully qualified domain name
domainsvc = lib.get_env_variable('DOMAINSVC')

proxy_price_url = lib.get_env_variable('PROXY_PRICE_URL')
proxy_work_threshold_default = lib.get_env_variable('WORK_THRESHOLD_DEFAULT')

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

price_url = "const price_url = 'https://api.coinpaprika.com/v1/tickers/nano-nano'"
price_url_replace = "const price_url = '%s-wallet.%s/dummy-price/coinpaprika.json'" % (abbreviation, domainsvc)
lib.find_and_replace("%sNanoRPCProxy/src/proxy.ts" % lib.cwd(),
                 str.encode(price_url),
                 str.encode(price_url_replace))

mynano_ninja_url = "const mynano_ninja_url = 'https://mynano.ninja/api/accounts/verified'"
mynano_ninja_url_replace = "const mynano_ninja_url = 'https://%s-ninja.%s/api/accounts/verified'" % (abbreviation, domainsvc)
lib.find_and_replace("%sNanoRPCProxy/src/proxy.ts" % lib.cwd(),
                 str.encode(mynano_ninja_url),
                 str.encode(mynano_ninja_url_replace))

work_threshold_default = "const work_threshold_default: string = 'fffffff800000000'"
work_threshold_default_replace = "const work_threshold_default: string = '%s'" % proxy_work_threshold_default
lib.find_and_replace("%sNanoRPCProxy/src/proxy.ts" % lib.cwd(),
                 str.encode(work_threshold_default),
                 str.encode(work_threshold_default_replace))

bpow_url = "const bpow_url: string = 'https://bpow.banano.cc/service/'"
bpow_url_replace = "const bpow_url: string = 'https://%s-bpow.%s/service/'" % (abbreviation, domainsvc)
lib.find_and_replace("%sNanoRPCProxy/src/proxy.ts" % lib.cwd(),
                 str.encode(bpow_url),
                 str.encode(bpow_url_replace))
