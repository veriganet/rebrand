from nanolib import generate_seed, generate_account_id, generate_account_key_pair, \
    get_account_id, AccountIDPrefix, Block

# create key pair and account
#seed = generate_seed()
seed = "e1552b5c4ca6328df504b6eb84901de4dad6213f1090dcfaae0c819da8af08f0"
key_pair = generate_account_key_pair(seed, 0)
account = get_account_id(public_key=key_pair.public, prefix=AccountIDPrefix.NANO.value)
account_replace = account.replace('nano_', 'kor_')

# create open block
work = "348a772019c867a9"
signature = ""

print("Seed: %s" % seed)
print("Private: %s" % key_pair.private)
print("Public: %s" % key_pair.public)
print("Account: %s" % account_replace)

# create open block
block = Block(
    block_type="open",
    source=key_pair.public,
    representative=account,
    account=account,
    difficulty="fffffe0000000000"
)
block.solve_work()
block.sign(key_pair.private)

print(block.json())

