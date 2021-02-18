from helpers import process_folder


def generate_hosts():
    """
    Creates hosts files to be put into /etc/hosts. Specifically:
    1. Aggregates overall blacklist and whitelist
    2. Subtracts latter from former
    3. Deduplicates output so only unique lines remain
    """
    blacklisted_tlds, blacklisted_urls, blacklisted_ips = process_folder('blacklists')
    whitelisted_tlds, whitelisted_urls, whitelisted_ips = process_folder('whitelists')
    final_tlds = list(set(blacklisted_tlds) - set(whitelisted_tlds))
    final_urls = list(set(blacklisted_urls) - set(whitelisted_urls))
    final_tlds.sort()
    final_urls.sort()
    with open("hosts/hosts", "w") as f:
        f.write("0.0.0.0 ")
        f.write("\n0.0.0.0 ".join(final_tlds))
        f.write("\n0.0.0.0 ".join(final_urls))
    print(f'> DONE. Hosts file contains {len(final_tlds) + len(final_urls)} items.')

if __name__ == '__main__':
    generate_hosts()
