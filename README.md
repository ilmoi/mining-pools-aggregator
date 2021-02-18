# Crypto mining pools aggregator (domains + IPs)

## Description
Simple tool that aggregates all the crypto mining pool lists I was able to find online. Includes both domains and IPs.

Outputs:
- Aggregate top level domains list (`lists/tlds.txt`) ~10k lines
- Aggregate domains with subdomains list (`lists/urls.txt`) ~130k lines
- Aggregate IPs list (`lists/ips.txt`) ~10k lines
- Aggregate Hosts file (`hosts/hosts`) ~140k lines
 
## Installation

1. Make sure you have python `3.x` on your system.
2. `pip install pipenv` if you don't have it already.
3. `cd` into the dir and run `pipenv install`.
 
## Usage

#### TL;DR;

You can use the files in `hosts` and `lists` folders as is.

To refresh sources and re-aggregate lists run: 

```
./refresh.sh
```

Give it some time (around 20min on 2018 13" MacBook Pro.) 

Output:
```
> DONE. Lists generated and contain 9885 TLDs, 131566 URLs and 8270 IPs.
> DONE. Hosts file generated and contains 141451 items.
```

#### Under the hood

```
pipenv run python generate_lists.py
```
aggregates all files in blacklists folder into one, subtracts anything from whitelists folder, deduplicates, orders alphabetically. Output saved in `lists` folder. 

```
pipenv run python generate_ips_from_lists.py
```
uses the files generated in previous steps and attempts to find IP addresses for each of the urls in those files. Output saved back into `blacklists` folder under names `ips_from_tlds` and `ips_from_urls`.

```
pipenv run python generate_hosts.py
``` 
aggregates `tlds` and `urls` into a single `hosts` file with `0.0.0.0` prefixed on each line.

`helpers.py` is where most of the logic lives. Functions are commented and should be self-explanatory.

There's a few lists that I found but that didn't make the cut saved into `excluded` dir. Mainly because of formatting issues.

## How to extend?

- Add urls to blacklist into `blacklists/CUSTOM_blacklist.txt`
- Add urls to whitelist into `whitelists/CUSTOM_whitelist.txt`
- To add new sources, create a file in either `blacklists` or `whitelists` folder then either paste your list directly, or if you're pulling from a url paste the url onto the first line. Python will do the rest to pull the contents and populate the file. Be sure to post the raw link (ie without html) - see current files for inspiration.  

 
## Credits

All the credit goes to the folk who put together the original lists. This is merely an aggregator.

Ordered alphabetically:

- [andoniaf/mining-pools-list](https://github.com/andoniaf/mining-pools-list)
- [anudeepND/blacklist](https://github.com/anudeepND/blacklist)
- [codingo/Minesweeper](https://github.com/codingo/Minesweeper/)
- [eladmen](https://www.catonetworks.com/blog/the-crypto-mining-threat)
- [firebog](https://firebog.net/)
- [hoshsadiq/adblock-nocoin-list](https://github.com/hoshsadiq/adblock-nocoin-list)
- [Marfjeh/coinhive-block](https://github.com/Marfjeh/coinhive-block)
- [ZeroDot1/CoinBlockerLists](https://gitlab.com/ZeroDot1/CoinBlockerLists)

## Contributions

Welcome. Just issue a PR.