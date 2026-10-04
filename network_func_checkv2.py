#!/usr/bin/env python3

import argparse
import socket
import sys
import time
import urllib.error
import urllib.request


def check_tcp_dns_server(timeout: float) -> bool:
    """Test raw TCP connectivity to Google's DNS service."""
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=timeout):
            print("[ OK ] TCP connection to 8.8.8.8:53")
            return True
    except OSError as exc:
        print(f"[FAIL] TCP connection to 8.8.8.8:53: {exc}")
        return False


def check_system_dns(hostname: str, timeout: float) -> bool:
    """
    Resolve a hostname using the system resolver.

    This uses the resolver configured through /etc/resolv.conf,
    NetworkManager, or another active NSS resolver.

    Fill the /etc/resolve.conf tables with the script or manually using(also on Kali for some open VPN):
    printf '%$\n' \
            'nameserver 192.168.0.1' \
            'nameserver 1.1.1.1' \
            | sudo tee /etc/resolve.conf
    """
    try:
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)

        results = socket.getaddrinfo(
            hostname,
            443,
            type=socket.SOCK_STREAM,
        )

        socket.setdefaulttimeout(old_timeout)

        addresses = sorted({result[4][0] for result in results})

        if addresses:
            print(f"[ OK ] System DNS resolved {hostname}:")
            for address in addresses:
                print(f"      {address}")
            return True

        print(f"[FAIL] System DNS returned no addresses for {hostname}")
        return False

    except socket.gaierror as exc:
        print(f"[FAIL] System DNS resolution for {hostname}: {exc}")
        return False
    except OSError as exc:
        print(f"[FAIL] System DNS check for {hostname}: {exc}")
        return False


def check_https(url: str, timeout: float) -> bool:
    """Test HTTPS using normal DNS resolution and TLS."""
    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "network-function-check/1.0"},
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            print(f"[ OK ] HTTPS {url} returned HTTP {response.status}")
            return True

    except urllib.error.HTTPError as exc:
        # A response such as 403 still proves DNS, TCP, TLS, and HTTP worked.
        print(f"[ OK ] HTTPS {url} returned HTTP {exc.code}")
        return True

    except urllib.error.URLError as exc:
        print(f"[FAIL] HTTPS {url}: {exc.reason}")
        return False

    except OSError as exc:
        print(f"[FAIL] HTTPS {url}: {exc}")
        return False


def network_check(timeout: float) -> bool:
    print("Running network checks...\n")

    tcp_ok = check_tcp_dns_server(timeout)
    dns_ok = check_system_dns("google.com", timeout)
    https_ok = check_https("https://example.com", timeout)

    print()

    if tcp_ok and dns_ok and https_ok:
        print("Networks all good :)")
        return True

    print("Network problem detected.")
    if tcp_ok and not dns_ok:
        print("Diagnosis: Internet access exists, but system DNS is not working.")
    elif not tcp_ok:
        print("Diagnosis: Basic outbound TCP connectivity is failing.")
    elif dns_ok and not https_ok:
        print("Diagnosis: DNS works, but HTTPS connectivity failed.")

    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TCP connectivity, system DNS, and HTTPS."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Timeout in seconds for each test; default: 5",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Repeat every five seconds until all checks pass",
    )

    args = parser.parse_args()

    if args.wait:
        while not network_check(args.timeout):
            print("\nRetrying in 5 seconds...\n")
            time.sleep(5)
        return 0

    return 0 if network_check(args.timeout) else 1


if __name__ == "__main__":
    sys.exit(main())
