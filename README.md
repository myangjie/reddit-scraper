# reddit-scraper

## Dependencies

* [pmaw](https://pypi.org/project/pmaw/)
* [langdetect](https://pypi.org/project/langdetect/)

## Getting Started

1. Clone the repository: `git clone https://github.com/myangjie/reddit-scraper`

2. Install the requirements: `cd reddit-scraper && pip3 install -r requirements.txt`

## Reproducing Results

1. Run `python3 src/reddit_scraper.py -a <after> -b <before> -s <subreddit>`.
* The `-s` argument is optional. Default: all. For further help, run `python3 src/reddit_scraper.py -h`.

2. View results in `out` folder.

Example output is included in `sample` folder. (Parameters: `python3 src/reddit_scraper.py -a 20220101 -b 20220501 -s montreal`)

### Important!

Keywords for the search query are located in `data/keywords.csv`.


