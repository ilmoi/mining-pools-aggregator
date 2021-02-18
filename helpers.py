import os
import re
from datetime import datetime
from pathlib import Path

import requests
import tldextract
from IPy import IP
from requests.exceptions import MissingSchema


def extract_url(filename):
    """
    Extracts url from the 1st line of the file.
    """
    with open(filename) as f:
        try:
            first_line = f.readlines()[0]
            url = re.search("(?P<url>https?://[^\s]+)", first_line).group("url")
            print(f'Extracted url: {url}.')
            return url
        except:
            print(f'ERROR! No url found in {filename}. '
                  f'Make sure url is on the 1st line and starts with http(s). '
                  f'For now skipping this file.')


def extract_full_repo(file_url):
    """
    Takes a raw link and extracts the full repo (github or gitlab style).
    """
    if 'raw.githubusercontent' in file_url:
        file_url = re.sub('raw.githubusercontent', 'github', file_url)
        file_url = '/'.join(file_url.split('/')[:-2])
        return file_url
    elif 'gitlab' in file_url:
        file_url = '/'.join(file_url.split('/')[:-4])
        return file_url
    return


def prep_temp_file(filename, url):
    """
    Prepares a temporary version of the passed filename. Includes headers.
    """
    temp_filename = Path(str(filename).split('.')[-2] + '_temp.txt')
    try:
        contents = requests.get(url, stream=True)
    except MissingSchema:
        return
    with open(temp_filename, 'wb') as f:
        # add header
        repo = extract_full_repo(url)
        header = f"# source: {url}\n" \
                 f"# {'full repo: ' + repo if repo else ''}\n" \
                 f"# pulled: {datetime.now()}\n" \
                 f"# original file starts below the ### line\n" \
                 f"#\n" \
                 f"{'#' * 80}\n\n".encode('utf-8')
        f.write(header)
        # add contents
        for chunk in contents.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
        return temp_filename


def refresh_file_contents(filename):
    """
    Tries to refresh file contents.
    1. Opens file & extracts url from first line
    2. Tries to download the file from url, adds header, saves into a temp copy
    3. If length of temp copy > 0 keeps new (assume success), else keeps old (assume failure)
    """
    url = extract_url(filename)
    temp_filename = prep_temp_file(filename, url)
    if temp_filename:
        os.remove(filename)
        os.rename(temp_filename, filename)
        print(f'Done refreshing {filename}.')


def extract_tld(url):
    """
    Extracts tld from the url.
    """
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"


def process_file(filename):
    """
    Processes a single file. Specifically:
    1. Cleans lines of prefixes / ports / whitespaces
    2. Skips blanks / comments
    3. Extracts TLD
    4. Aggregates into a single list (not deduplicated at this point)
    """
    tlds, urls, ips = [], [], []
    with open(filename, "r") as fp:
        i = 0
        for line in fp.readlines():
            # count
            i += 1
            if i % 5000 == 0:
                print(f'Processed line: {i}')
            # skip comments and breaks
            if line.startswith('#') or line == '':
                continue
            # strip stuff
            line = line.strip()
            line = line.strip('/')
            line = line.strip('0.0.0.0 ')  # to remove hosts file format
            line = line.split(':')[0]  # to remove ports
            line = line.strip('/')  # yes, twice, in case hidden behind port
            line = line.strip('-')  # hyphens allowed but not as 1st char - https://stackoverflow.com/questions/7111881/what-are-the-allowed-characters-in-a-subdomain
            # thought about removing _, but apparently they are legal - https://stackoverflow.com/questions/2180465/can-domain-name-subdomains-have-an-underscore-in-it
            # remove IPs
            try:
                IP(line)  # if doesn't error, then indeed an IP
                ips.append(line)
            except ValueError:
                # extract tld
                tld = extract_tld(line)
                tlds.append(tld)
                # append to list
                urls.append(line)

        print(f'Done processing file {filename}.')
        return tlds, urls, ips


def process_folder(foldername):
    """
    Processes a folder containing 1+ files. Specifically:
    1. Refreshes the file before looking inside of it
    2. Aggregates lines across files into a single list (not deduplicated at this point)
    """
    aggregated_tlds, aggregated_urls, aggregated_ips = [], [], []
    for r, d, f in os.walk(foldername):  # r=root, d=directories, f = files
        for file in f:
            filename = Path(foldername) / file
            refresh_file_contents(filename)
            tlds, urls, ips = process_file(filename)
            aggregated_tlds += tlds
            aggregated_urls += urls
            aggregated_ips += ips
    print(f'Done processing folder {foldername}.')
    return aggregated_tlds, aggregated_urls, aggregated_ips