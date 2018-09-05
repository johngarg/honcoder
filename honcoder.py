import hashlib
import pprint
from googlesearch import search


def process_url(url):
    """Function to process string into format preferred by honcode."""
    if url.startswith('htt'):
        url = url.split('//')[1]
    if url.startswith('www.'):
        url = url.split('www.')[1]
    base_url = url.split('/')[0] + '/'
    return base_url

def is_HONcode_certified(url):
    """Function returns Boolean value representing certification status of url.
    The url does not already need to be processed.
    """
    base_url = process_url(url)
    # print(base_url)
    m = hashlib.md5()
    m.update(base_url.encode('utf-8'))
    h = m.hexdigest()
    with open('listeMD5.txt', 'r', encoding='utf-8') as md5_file:
        for line in md5_file:
            if len(line.split()) == 2:
                url_hash, hon_code = line.split()
                if url_hash == h:
                    return True
    return False


# define search term and number of sites
search_term = 'lung cancer'
n_urls = 20

# compare Greek and English
# see https://developers.google.com/custom-search/docs/ref_languages for list of languages available
#pprint.pprint({url: is_HONcode_certified(url) for url in search(search_term, stop=n_urls, lang='el')})
pprint.pprint({url: is_HONcode_certified(url) for url in search(search_term, stop=n_urls, lang='en')})
