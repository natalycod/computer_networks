import subprocess
import argparse
import re
import platform

def get_command(ip, sz):
    command = []
    os_now = platform.system().lower()
    if (os_now == 'linux'):
        command =["ping", "-M", "do", "-s", str(sz), "-c", "1", ip]
    elif (os_now == 'windows'):
        command = ["ping", "-M", "do", "-s", str(sz), "-n", "1", ip]
    elif (os_now == 'darwin'):
        command = ["ping", "-D", "-s", str(sz), "-c", "1", ip]
    else:
        print('Sorry, I don\'t know how to work in your OS')
        exit(1)
    return command

def check_ping(ip):
    result = subprocess.run(get_command(ip, 0), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if (result.returncode != 0):
        print("Can\'t ping this host")
        exit(result.stderr)

def check_icmp_enabled():
    result = subprocess.run(
        ["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.stdout == 1:
        print('ICMP is disabled')
        exit(1)

def check_name_valid(ip):
    ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"

    try:
        is_ip = re.compile(ValidIpAddressRegex)
        is_host = re.compile(ValidHostnameRegex)
    except:
        print('Can\'t check that address is correct, so I\'ll just believe you')
        return

    if not is_ip.match(ip) and not is_host.match(ip):
        print(f"{ip} is neither correct ip nor correct host")
        exit(1)

def ping_with_size(ip, sz):
    sz = max(0, sz - 28)
    result = subprocess.run(get_command(ip, sz), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if (not(result.returncode in [0, 1])):
        print("Error during pinging")
        exit(result.stderr)
    return result.returncode == 0

def BinarySearch(ip):
    L = 0
    R = 1
    while (ping_with_size(ip, R)):
        R *= 2
    while (L < R):
        mid = (L + R + 1) // 2
        if (ping_with_size(ip, mid)):
            L = mid
        else:
            R = mid - 1
    return L

def printMTU(ip):
    print("MTU is equal to", BinarySearch(ip))

argparser = argparse.ArgumentParser()
argparser.add_argument(
    '--address',
    required=True,
    help='ip-address of the destination'
)

args = argparser.parse_args()
ip = args.address

check_icmp_enabled()
check_name_valid(ip)
check_ping(ip)

printMTU(ip)