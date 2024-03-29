#!/usr/bin/env python3

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

# Fully qualified domain name
domainsvc = lib.get_env_variable('DOMAINSVC')

# hid representative hover warning
hide_rep_help = lib.get_env_variable('NAULT_HIDE_REP_HELP')

# deprecate this
rep0 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP0')
rep1 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP1')

reps_from_env = [
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP0'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP1'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP2'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP3'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP4'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP5'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP6'),
    lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP7'),
]

# supply_multiplier
supply_multiplier = lib.get_env_variable('SUPPLY_MULTIPLIER')

nault_store_key = lib.get_env_variable('NAULT_STORE_KEY')
nault_price_url = lib.get_env_variable('NAULT_PRICE_URL')

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
    [b"XNO", b"%s" % str.encode(abbreviation.upper())],
    [b"replace('xrb_', 'nano_')", b"replace('nano_', '%s_')" % str.encode(abbreviation)],
    [b"replace('nano_', 'xrb_')", b"replace('nano_', '%s_')" % str.encode(abbreviation)],
    [b"replace('xrb', 'nano')", b"replace('xrb', '%s')" % str.encode(abbreviation)],
    [b"Wrong nano address", b"Wrong %s address" % str.encode(abbreviation)],
    [b"Invalid nano address", b"Invalid %s address" % str.encode(abbreviation)],
    [b"Send nano", b"Send %s" % str.encode(abbreviation)],
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
reps = ""
for rep in reps_from_env:
    if rep:
        reps = reps + f"    '{rep}',\n"

representativeAccounts = """  representativeAccounts = [
    'nano_1x7biz69cem95oo7gxkrw6kzhfywq4x5dupw4z1bdzkb74dk9kpxwzjbdhhs', // NanoCrawler
    'nano_1zuksmn4e8tjw1ch8m8fbrwy5459bx8645o9euj699rs13qy6ysjhrewioey', // Nanowallets.guide
    'nano_3chartsi6ja8ay1qq9xg3xegqnbg1qx76nouw6jedyb8wx3r4wu94rxap7hg', // Nano Charts
    'nano_1ninja7rh37ehfp9utkor5ixmxyg8kme8fnzc4zty145ibch8kf5jwpnzr3r', // My Nano Ninja
    'nano_1iuz18n4g4wfp9gf7p1s8qkygxw7wx9qfjq6a9aq68uyrdnningdcjontgar', // NanoTicker / Json
    'nano_3power3gwb43rs7u9ky3rsjp6fojftejceexfkf845sfczyue4q3r1hfpr3o', // PowerNode
    'nano_1ookerz3adg5rxc4zwwoshim5yyyihf6dpogjihwwq6ksjpq7ea4fuam5mmc', // Nanolooker.com
  ];"""

representativeAccountsReplace = f"""  representativeAccounts = [
{reps.rstrip()}
  ];""".format(reps=reps)
lib.find_and_replace("%sNault/src/app/services/nano-block.service.ts" % lib.cwd(),
                 str.encode(representativeAccounts),
                 str.encode(representativeAccountsReplace))

# defaultRepresentatives
default_reps = ""
for i, rep in enumerate(reps_from_env):
    if rep:
        default_reps = default_reps + """    {{
      id: '{rep}',
      name: 'Official Representative {i}',
      warn: false,
      trusted: true,
    }},\n""".format(rep=rep, i=i).rstrip()

defaultRepresentatives = """  defaultRepresentatives = [];"""

defaultRepresentativesReplace = """  defaultRepresentatives = [
{default_reps}
  ];""".format(default_reps=default_reps)
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

# nfReps
nf_reps = ""
for i, rep in enumerate(reps_from_env):
    if rep:
        nf_reps = nf_reps + """    {{
      id: '{rep}',
      name: 'Official Representative {i}',
      trusted: true,
    }},\n""".format(rep=rep, i=i).rstrip()
nfReps = """  nfReps = [
    {
      id: 'nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4',
      name: 'Nano Foundation #1',
    },
    {
      id: 'nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou',
      name: 'Nano Foundation #2',
    },
    {
      id: 'nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p',
      name: 'Nano Foundation #3',
    },
    {
      id: 'nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m',
      name: 'Nano Foundation #4',
    },
    {
      id: 'nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k',
      name: 'Nano Foundation #5',
    },
    {
      id: 'nano_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy',
      name: 'Nano Foundation #6',
    },
    {
      id: 'nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs',
      name: 'Nano Foundation #7',
    },
    {
      id: 'nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1',
      name: 'Nano Foundation #8',
    },
  ];"""
nfRepsReplace = """  nfReps = [
{nf_reps}
  ];""".format(nf_reps=nf_reps)
lib.find_and_replace("%sNault/src/app/services/representative.service.ts" % lib.cwd(),
                 str.encode(nfReps),
                 str.encode(nfRepsReplace))

defaultRepresentative = """    displayCurrency: 'USD',
    defaultRepresentative: null,"""
defaultRepresentativeReplace = """    displayCurrency: 'USD',
    defaultRepresentative: '{rep}',""".format(rep=reps_from_env[0])
lib.find_and_replace("%sNault/src/app/services/app-settings.service.ts" % lib.cwd(),
                 str.encode(defaultRepresentative),
                 str.encode(defaultRepresentativeReplace))

apiURL = "  apiUrl = `https://api.coingecko.com/api/v3/coins/nano?localization=false&tickers=false&market_data=true" \
         "&community_data=false&developer_data=false&sparkline=false`;"
if nault_price_url == "None":
    apiURLReplace = "  apiUrl = ``;"
else:
    apiURLReplace = "  apiUrl = `%s`;" % nault_price_url
lib.find_and_replace("%sNault/src/app/services/price.service.ts" % lib.cwd(),
                 str.encode(apiURL),
                 str.encode(apiURLReplace))

storeKey = "  storeKey = `nanovault-price`;"
if nault_store_key == "None":
    storeKeyReplace = "  storeKey = ``;"
else:
    storeKeyReplace = "  storeKey = `%s`;" % nault_store_key
lib.find_and_replace("%sNault/src/app/services/price.service.ts" % lib.cwd(),
                 str.encode(storeKey),
                 str.encode(storeKeyReplace))

getPrice = "    if (!currency) return; // No currency defined, do not refetch"
getPriceReplace = """    if (!this.apiUrl) return; // No API URL defined, do not fetch
    if (!this.storeKey) return this.price.lastPrice = 0; // No Store Key not defined, do not fetch
    if (!currency) return this.price.lastPrice = 0; // No currency defined, do not refetch"""
lib.find_and_replace("%sNault/src/app/services/price.service.ts" % lib.cwd(),
                 str.encode(getPrice),
                 str.encode(getPriceReplace))

baseThreshold = "fffffff800000000"
baseThresholdReplace = "%s" % work_thresholds[1]
lib.find_and_replace("%sNault/src/app/services/pow.service.ts" % lib.cwd(),
                 str.encode(baseThreshold),
                 str.encode(baseThresholdReplace))


gxrb_ratio = supply_multiplier + "000"
mxrb_ratio = supply_multiplier
kxrb_ratio = supply_multiplier[:-3]
xrb_ratio = supply_multiplier[:-6]

rai_pipes = """  mrai = 1000000000000000000000000000000;
  krai = 1000000000000000000000000000;
  rai  = 1000000000000000000000000;"""
rai_pipes_replace = """  mrai = {mxrb_ratio};
  krai = {kxrb_ratio};
  rai  = {xrb_ratio};""".\
    format(mxrb_ratio=mxrb_ratio,
           kxrb_ratio=kxrb_ratio,
           xrb_ratio=xrb_ratio)
lib.find_and_replace("%sNault/src/app/pipes/rai.pipe.ts" % lib.cwd(),
                 str.encode(rai_pipes),
                 str.encode(rai_pipes_replace))

util_service = """const mnano = 1000000000000000000000000000000;
const knano = 1000000000000000000000000000;
const nano  = 1000000000000000000000000;"""
util_service_replace = """const mnano = {mxrb_ratio};
const knano = {kxrb_ratio};
const nano  = {xrb_ratio};""".\
    format(mxrb_ratio=mxrb_ratio,
           kxrb_ratio=kxrb_ratio,
           xrb_ratio=xrb_ratio)
lib.find_and_replace("%sNault/src/app/services/util.service.ts" % lib.cwd(),
                 str.encode(util_service),
                 str.encode(util_service_replace))

if hide_rep_help:
    showRepHelp = "<div [class]=\"[ 'representative-help-tooltip', showRepHelp==rep.id ? 'visible' : 'hidden' ]\">"
    showRepHelpReplace = "<div [class]=\"[ 'representative-help-tooltip', showRepHelp==rep.id ? 'hidden' : 'hidden' ]\">"
    lib.find_and_replace("%sNault/src/app/components/change-rep-widget/change-rep-widget.component.html" % lib.cwd(),
                         str.encode(showRepHelp),
                         str.encode(showRepHelpReplace))
# replace urls
lib.replace_all(urls, ignore_list, "/Nault")
