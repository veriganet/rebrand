#!/usr/bin/env python3

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

# Fully qualified domain name
domainsvc = lib.get_env_variable('DOMAINSVC')

rep0 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP0')
rep1 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP1')

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
    #[b"'nano_'", b"'%s_'" % str.encode(abbreviation)],
    [b"nano_abc...123", b"%s_abc...123" % str.encode(abbreviation)],
    [b"nano_abc..123", b"%s_abc...123" % str.encode(abbreviation)],
    [b"nano_1abc...", b"%s_abc..." % str.encode(abbreviation)],
    [b"nano_abc123", b"%s_abc123" % str.encode(abbreviation)],
    [b"xrb_ or nano_'", b"%s_'" % str.encode(abbreviation)],
    [b"nano_3niceeeyiaa86k58zhaeygxfkuzgffjtwju9ep33z9c8qekmr3iuc95jbqc8", b"%s_" % str.encode(abbreviation)],
    [b" NANO", b" %s" % str.encode(abbreviation.upper())],
    [b">NANO<", b">%s<" % str.encode(abbreviation.upper())],
    [b"NANO ", b"%s " % str.encode(abbreviation.upper())],
    [b" XNO", b" %s" % str.encode(abbreviation.upper())],
    [b">XNO<", b">%s<" % str.encode(abbreviation.upper())],
    [b">XNO ", b">%s " % str.encode(abbreviation.upper())],
    [b"XNO ", b"%s " % str.encode(abbreviation.upper())],
    [b"replace('xrb_', 'nano_')", b"replace('nano_', '%s_')" % str.encode(abbreviation)],
    [b"replace('nano_', 'xrb_')", b"replace('nano_', '%s_')" % str.encode(abbreviation)],
    [b"replace('xrb', 'nano')", b"replace('xrb', '%s')" % str.encode(abbreviation)],
    [b"Wrong nano address", b"Wrong %s address" % str.encode(abbreviation)],
    [b"Invalid nano address", b"Invalid %s address" % str.encode(abbreviation)],
]
lib.replace_all(words, ignore_list, "/Nault")

urls = [
    [b"mynano.ninja", b"%s-ninja.%s" % (str.encode(abbreviation), str.encode(domainsvc))],
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
      api: 'https://{abr}-rpc1.{dsvc}/proxy',
      ws: 'wss://{abr}-ws1.{dsvc}',
      auth: null,
      shouldRandom: true,
    }},
    {{
      name: 'RPC 2',
      value: 'rpc2',
      api: 'https://{abr}-rpc2.{dsvc}/proxy',
      ws: 'wss://{abr}-ws2.{dsvc}',
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
lib.find_and_replace("%sNault/src/app/services/app-settings.service.ts" % lib.cwd(),
                 str.encode(serverOptions), str.encode(serverOptionsReplace))

# nano_
lib.find_and_replace(
    "%sNault/src/app/components/helpers/nano-account-id/nano-account-id.component.html" % lib.cwd(),
    b"nano_", b"%s_" % str.encode(abbreviation))

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
lib.find_and_replace("%sNault/src/app/services/nano-block.service.ts" % lib.cwd(),
                 str.encode(representativeAccounts),
                 str.encode(representativeAccountsReplace))

# defaultRepresentatives
defaultRepresentatives = """  defaultRepresentatives = [];"""

defaultRepresentativesReplace = """  defaultRepresentatives = [
    {{
      id: '{rep0}',
      name: 'Official Representative #1',
      warn: false,
    }},
    {{
      id: '{rep1}',
      name: 'Official Representative #2',
      warn: false,
    }},
  ];""".format(rep0=rep0, rep1=rep1)
lib.find_and_replace("%sNault/src/app/services/representative.service.ts" % lib.cwd(),
                 str.encode(defaultRepresentatives),
                 str.encode(defaultRepresentativesReplace))

amounts = """  amounts = [
    { name: 'NANO', shortName: 'NANO', value: 'mnano' },
    { name: 'knano', shortName: 'knano', value: 'knano' },
    { name: 'nano', shortName: 'nano', value: 'nano' },
  ];"""
amountsReplace = """  amounts = [
    {{ name: '{abr_cap}', shortName: '{abr_cap}', value: 'mnano' }},
    {{ name: 'k{abr}', shortName: 'knano', value: 'knano' }},
    {{ name: '{abr}', shortName: 'nano', value: 'nano' }},
  ];""".format(abr=abbreviation, abr_cap=abbreviation.upper())
lib.find_and_replace(
    "%sNault/src/app/components/account-details/account-details.component.ts" % lib.cwd(),
    str.encode(amounts),
    str.encode(amountsReplace))
lib.find_and_replace(
    "%sNault/src/app/components/send/send.component.ts" % lib.cwd(),
    str.encode(amounts),
    str.encode(amountsReplace))

isValidNanoAccount = "        ( searchData.startsWith('xrb_') || searchData.startsWith('nano_') )"
isValidNanoAccountReplace = "        ( searchData.startsWith('{abr}_') )".format(abr=abbreviation)
lib.find_and_replace(
    "%sNault/src/app/app.component.ts" % lib.cwd(),
    str.encode(isValidNanoAccount),
    str.encode(isValidNanoAccountReplace))


nanoAccountID = "replace('nano_', '')"
nanoAccountIDReplace = "replace('nano_', '').replace('{abr}_', '')".format(abr=abbreviation)
lib.find_and_replace("%sNault/src/app/components/helpers/nano-account-id/nano-account-id.component.ts" % lib.cwd(),
                 str.encode(nanoAccountID),
                 str.encode(nanoAccountIDReplace))


musigService = "!address.startsWith('xrb_') && !address.startsWith('nano_')"
musigServiceReplace = "!address.startsWith('{abr}_')".format(abr=abbreviation)
lib.find_and_replace("%sNault/src/app/services/musig.service.ts" % lib.cwd(),
                 str.encode(musigService),
                 str.encode(musigServiceReplace))

musigService2 = "const fullAddressFinal = 'nano_' + base32.encode(fullAddress);"
musigService2Replace = "const fullAddressFinal = '{abr}_' + base32.encode(fullAddress);"\
                        .format(abr=abbreviation)
lib.find_and_replace("%sNault/src/app/services/musig.service.ts" % lib.cwd(),
                 str.encode(musigService2),
                 str.encode(musigService2Replace))

getPublicAccountID = "function getPublicAccountID(accountPublicKeyBytes, prefix = 'nano')"
getPublicAccountIDReplace = "function getPublicAccountID(accountPublicKeyBytes, prefix = '%s')"\
    % abbreviation
lib.find_and_replace("%sNault/src/app/services/util.service.ts" % lib.cwd(),
                 str.encode(getPublicAccountID),
                 str.encode(getPublicAccountIDReplace))

utilIsValidAccount = "if (!isValidAccount(account)) {"
utilIsValidAccountReplace = "if (account !== 'None' && !isValidAccount(account)) {"
lib.find_and_replace("%sNault/src/app/services/util.service.ts" % lib.cwd(),
                 str.encode(utilIsValidAccount),
                 str.encode(utilIsValidAccountReplace))

addWorkToCash = "this.workPool.addWorkToCache(hash, 1 / 64);"
addWorkToCashReplace = "this.workPool.addWorkToCache(hash);"
lib.find_and_replace("%sNault/src/app/services/wallet.service.ts" % lib.cwd(),
                 str.encode(addWorkToCash),
                 str.encode(addWorkToCashReplace))

# replace urls
lib.replace_all(urls, ignore_list, "/Nault")
