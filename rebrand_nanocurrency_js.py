#!/usr/bin/env python3

import rebrand_lib as lib


# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')


main_desc = "Script to rebrand nanocurrency-js node js module" \
            "Example: " \
            "rebrand-nanocurrency-js"


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
    "node_modules"
]


words = [
    [b"let prefix = 'xrb_'",
     b"""let prefix = '%s_'
     params.useNanoPrefix = true"""
     % str.encode(abbreviation)],
]
lib.replace_all(words, ignore_list)
