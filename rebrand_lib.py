import argparse
import os
import logging
import subprocess
import shutil
import re

log_level = os.environ.get('LOGGING', default="INFO")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log_level)

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


def remove_prefix(text, prefix):
    return text[len(prefix):] if text.startswith(prefix) else text


def cwd(directory="./"):
    logging.debug(directory)
    if os.environ.get("CI") == "true" and os.environ.get("DRONE") == "true":
        directory = "/drone/src/"
    return directory


def get_env_variable(env):
    if not os.environ.get(env, None):
        return logging.error("%s is not defined!" % env)
    else:
        logging.debug("%s properly set." % env)
        return os.environ.get(env)


def key_create(a):
    lines = []
    proc = subprocess.Popen(['%snano-node-22.0.0-Linux/bin/nano_node' % cwd(), '--key_create'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        lines.append(str(line.rstrip()))

    private = lines[0].split(": ")[1].rstrip("'")
    public = lines[1].split(": ")[1].rstrip("'")
    account = lines[2].split(": ")[1].rstrip("'").replace("nano_", a)

    return print('''{
    "private": "%s",
    "public": "%s",
    "account": "%s"
}
    ''' % (private, public, account))


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


def replace_all(data, ignore_list, nano_node=""):
    for dirname, dirs, files in os.walk(cwd()+nano_node):
        for file_name in files:
            filepath = os.path.join(dirname, file_name)

            for x in data:
                if is_ignored(filepath, ignore_list):
                    logging.debug("IGNORED %s" % filepath)
                else:
                    find_and_replace(filepath, x[0], x[1])


# rename directories
def rename_dirs(dirs):
    for d in dirs:
        if os.path.exists(d[0]):
            os.rename(d[0], d[1])
