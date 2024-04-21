import re
from collections import Counter
import geoip2.database


def parse_log_file(file_path):
    ip_counts = Counter()
    ip_pattern = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b):[0-9]+')

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(ip_pattern, line)

            if match:
                ip_counts[match.group(1)] += 1

    return ip_counts


# usage example
result = parse_log_file('./3proxy_example.log')

sorted_ips = result.most_common()
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')

for ip, count in sorted_ips:
    country = reader.country(ip).country.name
    print(f"IP: {ip}, Country: {country}, Count: {count}")
