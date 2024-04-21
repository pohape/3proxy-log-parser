import re
from collections import Counter
import geoip2.database
import sys


def parse_log_file(file_path):
    ip_counts = Counter()
    ip_pattern = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b):[0-9]+')

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(ip_pattern, line)
            if match:
                ip_counts[match.group(1)] += 1

    return ip_counts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 3proxy_log_parser.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    result = parse_log_file(log_file_path)

    sorted_ips = result.most_common()
    reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')

    for ip, count in sorted_ips:
        country = reader.country(ip).country.name
        print(f"IP: {ip}, Country: {country}, Count: {count}")
