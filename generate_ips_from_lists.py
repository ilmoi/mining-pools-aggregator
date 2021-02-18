import concurrent.futures
import socket
import time
from pathlib import Path


def get_ip(line, i):
    # count
    if i % 10 == 0:
        print(f'Processed line: {i}')
    # prep the line
    line = line.strip('.')  # in case using the tld file
    line = line.strip('\n')  # IMPORTANT
    # get ip address
    try:
        return socket.gethostbyname(line)
    except:  # many domains don't exist anymore, so no IP addresses are available
        pass


def get_ips(filename):
    """
    Tries to get IP addresses for all domains in output_url.txt.
    CAUTION: SLOW. Even with multithreading. Someone smarter than me needs to rewrite in C/Go/Rust etc.
    """
    ips = []
    with open(Path('lists') / f"{filename}.txt", "r") as f:
        lines = f.readlines()

        # took 50 from here - https://edmundmartin.com/optimal-number-of-threads-in-python/
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = [executor.submit(get_ip, line, i) for i, line in enumerate(lines)]
            for future in concurrent.futures.as_completed(results):
                if future.result():
                    ips.append(future.result())

    final_ips = list(set(ips))
    final_ips.sort()

    with open(f'blacklists/ips_from_{filename}.txt', 'w') as f:
        f.write("\n".join(final_ips))


if __name__ == '__main__':
    t1 = time.perf_counter()
    get_ips('tlds')
    t2 = time.perf_counter()
    get_ips('urls')
    t3 = time.perf_counter()
    print(f"DONE. Getting IPs for TLDs took {t2-t1}, and for URLs {t3-t2}.")
