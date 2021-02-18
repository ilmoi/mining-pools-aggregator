from helpers import process_folder


def generate_lists():
    """
    Creates lists to be used in a firewall. Specifically:
    1. Aggregates overall blacklist and whitelist
    2. Subtracts latter from former
    3. Deduplicates output so only unique lines remain
    """
    blacklisted_tlds, blacklisted_urls, blacklisted_ips = process_folder('blacklists')
    whitelisted_tlds, whitelisted_urls, whitelisted_ips = process_folder('whitelists')
    final_tlds = list(set(blacklisted_tlds) - set(whitelisted_tlds))
    final_urls = list(set(blacklisted_urls) - set(whitelisted_urls))
    final_ips = list(set(blacklisted_ips) - set(whitelisted_ips))
    final_tlds.sort()
    final_urls.sort()
    final_ips.sort()
    with open("lists/tlds.txt", "w") as f:
        f.write("\n".join(final_tlds))
    with open("lists/urls.txt", "w") as f:
        f.write("\n".join(final_urls))
    with open("lists/ips.txt", "w") as f:
        f.write("\n".join(final_ips))
    print(f'> DONE. Lists generated and contain {len(final_tlds)} TLDs, '
          f'{len(final_urls)} URLs and {len(final_ips)} IPs.')


if __name__ == '__main__':
    generate_lists()
