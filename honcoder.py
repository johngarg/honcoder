import argparse
import hashlib
import pickle

from xgoogle.search import GoogleSearch

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--search", default=None, help="Search term")
PARSER.add_argument("--n", default=None, help="Number of urls to pull from search")
PARSER.add_argument("--lang", default="en", help="Language for search")
PARSER.add_argument(
    "--engine",
    default="google",
    choices=["google"],
    help="Search engine to use (only google currently supported)",
)
PARSER.add_argument("--perpage", default=10, help="Number of results per page")
ARGS = PARSER.parse_args()


def process_url(url):
    """
    Function to process string into format preferred by honcode.
    """
    if url.startswith("htt"):
        url = url.split("//")[1]
    if url.startswith("www."):
        url = url.split("www.")[1]
    base_url = url.split("/")[0] + "/"
    return base_url


def is_HONcode_certified(url, path="data/"):
    """Function returns Boolean value representing certification status of url.
    The url does not already need to be processed.
    """
    base_url = process_url(url)
    m = hashlib.md5()
    m.update(base_url.encode("utf-8"))
    h = m.hexdigest()

    # load pickled data
    with open(f"{path}honcode.dat", "rb") as dat_file:
        data = pickle.load(dat_file)
    if h in data.keys():
        return True
    else:
        return False


def honcode_map(result):
    """
    Return 1 if HONcode certified, 2 if not.
    """
    return 1 if result else 2


def display_results(url, counter):
    """
    Prints results of search
    """
    print(f"Url number: {counter+1} of {N_URLS}")
    print(f"Whole url: {url}")
    print(f"Processed url: {process_url(url)}")
    print(f"Is certified? {is_HONcode_certified(url)}")
    print(
        "--------------------------------------------------------------------------------"
    )


def results_to_csv(args, url, counter):
    if counter == 0:
        print(
            f"Count, Search engine, Search term, Whole url, Processed url, Language, Tertile, Is certified?, Website"
        )

    tertile = (counter // 50) + 1
    processed_url = process_url(url)

    print(
        f"{counter}, {ARGS.engine}, {ARGS.search}, {url}, {processed_url}, {ARGS.lang}, {tertile}, {honcode_map(is_HONcode_certified(url))}, "
    )


if __name__ == "__main__":

    if ARGS.search is None:
        raise ValueError("You need to input a search term!")
    else:
        SEARCH_TERM = ARGS.search

    if ARGS.n is None:
        print("Number of urls not specified, running on 50...")
        N_URLS = 50
    else:
        N_URLS = int(ARGS.n)

    GS = GoogleSearch(SEARCH_TERM, lang=ARGS.lang)
    GS.results_per_page = int(ARGS.perpage)
    COUNTER = 0
    while COUNTER < int(ARGS.n):
        RESULTS = GS.get_results()
        if not RESULTS:
            raise ValueError("Empty results!")
        for result in RESULTS:
            URL = result.url
            results_to_csv(ARGS, URL, COUNTER)
            COUNTER += 1
