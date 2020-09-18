# dork-scanner
dork scanning tool built in python. It scrapes web search engines with dorks you provide in order to find vulnerable urls. This tool supports google, yahoo, bing and baidu search engines

# dork-scanner
This script is an automated tool to parse search engines with provided dorks in order to find vulnerable urls. This tool supports google, bing and baidu.
## Requirements
- Python 3
- Packages in requirements.txt
## Setup
Refer to these steps to install the tool on a linux distribution
```
git clone https://github.com/GuestGuri/dork-scanner.git
pip3 install -r requirements.txt
```
## Usage
``` usage: dork-scanner.py [-h] [-S SEARCH] [-E ENGINE] [-P PAGE] [-Pr PROCESS] ```
-S, --search 
- String to be searched for

-E, --engine

- Search engine to be used (google, bing, baidu)

-P, --page
- Number of pages to search in

-Pr, --process
- Number of parallel processes

## Examples
``` python3 dork-scanner.py --search inurl:php?=id1 --engine google --page 3 --process 3 ```
search for inurl:php?=id1 in 3 pages of google using 3 processes
## Author
- Author: Mohamed Ghassen Gargouri 
- LinkedIn : https://www.linkedin.com/in/mohamed-ghassen-gargouri/
