import subprocess

IP_LIST = [
    "1.56.98.184",
    "116.162.168.167",
    "116.169.183.220",
    "175.43.23.215",
    "211.95.142.138",
    "221.204.15.51",
    "221.204.209.225",
    "42.56.64.131",
    "42.56.81.77",
    "60.13.97.57",
    "172.64.80.1",
    "8.133.135.83",
    "104.21.30.139",
    "172.67.172.248",
    "106.15.148.44",
]

def block_ip(ip):
    rule_name = f"BLOCK_{ip.replace('.', '_')}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip} enable=yes'
    subprocess.run(cmd, shell=True)

def main():
    for ip in IP_LIST:
        block_ip(ip)
    print(f"[+] Bloqueio concluído para {len(IP_LIST)} IPs.")

if __name__ == "__main__":
    main()
