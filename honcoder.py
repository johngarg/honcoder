import hashlib
import pickle
import pprint
from googlesearch import search
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--search', default=None, help='Search term')
parser.add_argument('--n', default=None, help='Number of urls to pull from google search')
parser.add_argument('--lang', default='en', help='Language for google search')
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


if args.search is None:
    raise ValueError('You need to input a search term!')
else:
    search_term = args.search 

if args.n is None:
    print('Number of urls not specified, defaulting to 50...')
    n_urls = 50
else:
    n_urls = int(args.n)

if __name__ == '__main__':
    counter = 0
    for url in search(search_term, stop=n_urls, lang=args.lang):
        print(f'Url number: {counter+1} of {n_urls}')
        print(f'Whole url: {url}')
        print(f'Processed url: {process_url(url)}')
        print(f'Is certified? {is_HONcode_certified(url)}')
        print('--------------------------------------------------------------------------------')
        counter += 1
