#!/usr/bin/env python3

import argparse
import os
import re
import mmap
import shutil

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
    "clang-format"
]

words = [
    [b"nano_pow_server", b"kor_pow_server"],
    [b"RaiBlocksDev", b"KorBlocksDev"],
    [b"RaiBlocksBeta", b"KorBlocksBeta"],
    [b"RaiBlocksTest", b"KorBlocksTest"],
    [b"Nanocurrency", b"Korcurrency"],
    [b"nanocurrency", b"korcurrency"],
    [b"nano_wallet", b"kor_wallet"],
    [b"nano_node", b"kor_node"],
    [b"nano_rpc", b"kor_rpc"],
    [b"nano-node", b"kor-node"],
    [b"NanoDev", b"KorDev"],
    [b"NanoBeta", b"KorBeta"],
    [b"NanoTest", b"KorTest"],
    [b"nanodir", b"kordir"],
    [b" Nano ", b" Kor "],
    [b"Nano", b"Kor"],
]

urls = [
    [b"security\@nano.org", b"security\@kor.org"],
    [b"info\@nano.org", b"info\@kor.org"],
    [b"russel\@nano.org", b"contact\@kor.org"],
    [b"https\:\/\/nano.org", b"https\:\/\/kor.org"],
    [b"https\:\/\/nano.org/", b"https\:\/\/kor.org\/"],
    [b"https\:\/\/docs.nano.org", b"https\:\/\/docs.kor.org"],
    [b"https\:\/\/chat.nano.org", b"https\:\/\/chat.kor.org"],
    [b"https\:\/\/content.nano.org", b"https\:\/\/content.kor.org"],
    [b"peering-beta.nano.org", b"peering-beta.kor.org"],
    [b"peering.nano.org", b"peering.kor.org"],
    [b"peering-test.nano.org", b"peering-test.kor.org"],
    [b"repo.nano.org", b"repo.kor.org"],
    [b"nano.org", b"kor.org"],
]

dirs = [
    ["nano/nano_node", "nano/kor_node"],
    ["nano/nano_rpc", "nano/kor_rpc"],
    ["nano/nano_wallet", "nano/kor_wallet"],
]

accounts = [
    # nano/core_test/block.cpp .account_address
    [b"xrb_15nhh1kzw3x8ohez6s75wy3jr6dqgq65oaede1fzk5hqxk4j8ehz7iqtb3to",
     b"kor_15nhh1kzw3x8ohez6s75wy3jr6dqgq65oaede1fzk5hqxk4j8ehz7iqtb3to"],
    # nano/core_test/block.cpp .representative_address
    [b"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
     b"kor_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"],
    # nano/core_test/block.cpp .account_address burn
    [b"xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
     b"kor_1111111111111111111111111111111111111111111111111111hifc8npp"],
    [b"nano_1111111111111111111111111111111111111111111111111111hifc8npp",
     b"kor_1111111111111111111111111111111111111111111111111111hifc8npp"],
    # nano/core_test/block.cpp
    [b"xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
     b"kor_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
    # nano/core_test/block.cpp
    [b"xrb_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf",
     b"kor_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf"],
    # nano/core_test/block.cpp
    [b"xrb_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb",
     b"kor_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb"],
    [b"nano_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb",
     b"kor_1gys8r4crpxhp94n4uho5cshaho81na6454qni5gu9n53gksoyy1wcd4udyb"],
    # nano/core_test/toml.cpp preconfigured_representatives
    [b"nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
     b"kor_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4"],
    # nano/node/nodeconfig.cpp offline_representative.decode_account
    [b"nano_1defau1t9off1ine9rep99999999999999999999999999999999wgmuzxxy",
     b"kor_1defau1t9off1ine9rep99999999999999999999999999999999wgmuzxxy"],
    # genesis accounts
    # dev_public_key_data
    [b"xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo",
     b"kor_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo"],
    # beta_public_key_data
    [b"nano_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1",
     b"kor_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1"],
    # live_public_key_data
    [b"xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
     b"kor_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
    # test_public_key_data
    [b"nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
     b"kor_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j"],
]

genesis_data = [
    # dev_genesis_data
    [
        # old
        b'''"type": "open",
        "source": "B0311EA55708D6A53C75CDBF88300259C6D018522FE3D4D0A242E431F9E8B6D0",
        "representative": "kor_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo",
        "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo",
        "work": "7b42a00ee91d5810",
        "signature": "ECDA914373A2F0CA1296475BAEE40500A7F0A7AD72A5A80C81D7FAB7F6C802B2CC7DB50F5DD0FB25B2EF11761FA7344A158DD5A700B21BD47DE5BD0F63153A02"''',
        # new
        b'''"type": "open",
        "source": "B0311EA55708D6A53C75CDBF88300259C6D018522FE3D4D0A242E431F9E8B6D0",
        "representative": "kor_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo",
        "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpiij4txtdo",
        "work": "7b42a00ee91d5810",
        "signature": "ECDA914373A2F0CA1296475BAEE40500A7F0A7AD72A5A80C81D7FAB7F6C802B2CC7DB50F5DD0FB25B2EF11761FA7344A158DD5A700B21BD47DE5BD0F63153A02"'''
    ],
    # beta_genesis_data
    [  # old
        b'''"type": "open",
        "source": "259A43ABDB779E97452E188BA3EB951B41C961D3318CA6B925380F4D99F0577A",
        "representative": "nano_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1",
        "account": "nano_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1",
        "work": "79d4e27dc873c6f2",
        "signature": "4BD7F96F9ED2721BCEE5EAED400EA50AD00524C629AE55E9AFF11220D2C1B00C3D4B3BB770BF67D4F8658023B677F91110193B6C101C2666931F57046A6DB806"''',
        # new
        b'''"type": "open",
        "source": "259A43ABDB779E97452E188BA3EB951B41C961D3318CA6B925380F4D99F0577A",
        "representative": "kor_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1",
        "account": "kor_1betagoxpxwykx4kw86dnhosc8t3s7ix8eeentwkcg1hbpez1outjrcyg4n1",
        "work": "79d4e27dc873c6f2",
        "signature": "4BD7F96F9ED2721BCEE5EAED400EA50AD00524C629AE55E9AFF11220D2C1B00C3D4B3BB770BF67D4F8658023B677F91110193B6C101C2666931F57046A6DB806"'''
    ],
    # live_genesis_data
    [
        # old
        b'''"type": "open",
        "source": "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA",
        "representative": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        "account": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        "work": "62f05417dd3fb691",
        "signature": "9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02"''',
        # new
        b'''"type": "open",
        "source": "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA",
        "representative": "kor_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        "account": "kor_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        "work": "62f05417dd3fb691",
        "signature": "9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02"'''
    ],
    # test_genesis_data
    [
        # old
        b'''"type": "open",
        "source": "45C6FF9D1706D61F0821327752671BDA9F9ED2DA40326B01935AB566FB9E08ED",
        "representative": "nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
        "account": "nano_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
        "work": "bc1ef279c1a34eb1",
        "signature": "15049467CAEE3EC768639E8E35792399B6078DA763DA4EBA8ECAD33B0EDC4AF2E7403893A5A602EB89B978DABEF1D6606BB00F3C0EE11449232B143B6E07170E"''',
        # new
        b'''"type": "open",
        "source": "45C6FF9D1706D61F0821327752671BDA9F9ED2DA40326B01935AB566FB9E08ED",
        "representative": "kor_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
        "account": "kor_1jg8zygjg3pp5w644emqcbmjqpnzmubfni3kfe1s8pooeuxsw49fdq1mco9j",
        "work": "bc1ef279c1a34eb1",
        "signature": "15049467CAEE3EC768639E8E35792399B6078DA763DA4EBA8ECAD33B0EDC4AF2E7403893A5A602EB89B978DABEF1D6606BB00F3C0EE11449232B143B6E07170E"'''
    ],
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
    for dirname, dirs, files in os.walk(os.getcwd()):
        for file_name in files:
            filepath = os.path.join(dirname, file_name)

            for x in data:
                if is_ignored(filepath, ignore_list):
                    print("File is ignored!")
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
find_and_replace("nano/lib/numbers.cpp", genesis_data[0][0], genesis_data[0][1])


# replace beta_genesis_data
find_and_replace("nano/lib/numbers.cpp", genesis_data[1][0], genesis_data[1][1])


# replace live_genesis_data
find_and_replace("nano/lib/numbers.cpp", genesis_data[2][0], genesis_data[2][1])


# replace test_genesis_data
find_and_replace("nano/lib/numbers.cpp", genesis_data[3][0], genesis_data[3][1])


# replace accounts
replace_all(accounts)


# replace _onan
find_and_replace("nano/lib/numbers.cpp",
                 b'destination_a.append ("_onan"); // nano_',
                 b'destination_a.append ("_rok"); // kor_'
                 )



# replace xrb_ prefix
find_and_replace("nano/lib/numbers.cpp",
                 b"auto xrb_prefix (source_a[0] == 'x' && source_a[1] == 'r' && source_a[2] == 'b' && (source_a[3] == "
                 b"'_' || source_a[3] == '-'));",
                 b"auto xrb_prefix (source_a[0] == 'k' && source_a[1] == 'o' && source_a[2] == 'r' && (source_a[3] == "
                 b"'_' || source_a[3] == '-'));"
                 )


# replace nano_ prefix
find_and_replace("nano/lib/numbers.cpp",
                 b"auto nano_prefix (source_a[0] == 'n' && source_a[1] == 'a' && source_a[2] == 'n' && source_a[3] == "
                 b"'o' && (source_a[4] == '_' || source_a[4] == '-'));",
                 b"auto nano_prefix (source_a[0] == 'k' && source_a[1] == 'o' && source_a[2] == 'r' && source_a[3] == "
                 b"'c' && (source_a[4] == '_' || source_a[4] == '-'));"
                 )
