import hashlib
import pickle
import pprint
import googlesearch
import argparse
from xgoogle.search import GoogleSearch

parser = argparse.ArgumentParser()
parser.add_argument('--search', default=None, help='Search term')
parser.add_argument('--n', default=None, help='Number of urls to pull from search')
parser.add_argument('--lang', default='en', help='Language for search')
parser.add_argument('--engine', default='google', choices=['google'],
                    help='Search engine to use (only google currently supported)')
parser.add_argument('--perpage', default=10, help='Number of results per page')
args = parser.parse_args()

def process_url(url):
    """Function to process string into format preferred by honcode."""
    if url.startswith('htt'):
        url = url.split('//')[1]
    if url.startswith('www.'):
        url = url.split('www.')[1]
    base_url = url.split('/')[0] + '/'
    return base_url

def is_HONcode_certified(url, path='data/'):
    """Function returns Boolean value representing certification status of url.
    The url does not already need to be processed.
    """
    base_url = process_url(url)
    m = hashlib.md5()
    m.update(base_url.encode('utf-8'))
    h = m.hexdigest()

    # load pickled data
    with open(f'{path}honcode.dat', 'rb') as dat_file:
        data = pickle.load(dat_file)
    if h in data.keys():
        return True
    else:
        return False

def honcode_map(result):
    """Return 1 if HONcode certified, 2 if not."""
    return 1 if result else 2

def display_results(url, counter):
    """Prints results of search"""
    print(f'Url number: {counter+1} of {n_urls}')
    print(f'Whole url: {url}')
    print(f'Processed url: {process_url(url)}')
    print(f'Is certified? {is_HONcode_certified(url)}')
    print('--------------------------------------------------------------------------------')

def results_to_csv(args, url, counter):
    if counter == 0:
        print(f'Count, Search engine, Search term, Whole url, Processed url, Language, Tertile, Is certified?, Website')

    tertile = (counter // 50) + 1
    processed_url = process_url(url)

    print(f'{counter}, {args.engine}, {args.search}, {url}, {processed_url}, {args.lang}, {tertile}, {honcode_map(is_HONcode_certified(url))}, ')

if __name__ == '__main__':

    if args.search is None:
        raise ValueError('You need to input a search term!')
    else:
        search_term = args.search

    if args.n is None:
        print('Number of urls not specified, running on 50...')
        n_urls = 50
    else:
        n_urls = int(args.n)

    gs = GoogleSearch(search_term, lang=args.lang)
    gs.results_per_page = int(args.perpage)
    counter = 0
    while counter < int(args.n):
        results = gs.get_results()
        if not results:
            raise ValueError('Empty results!')
        for result in results:
            url = result.url
            results_to_csv(args, url, counter)
            counter += 1
