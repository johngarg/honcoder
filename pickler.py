
def read_list_to_dict(path_to_txt):
    with open('listeMD5.txt', 'r', encoding='utf-8') as md5_file:
        for line in md5_file:
            if len(line.split()) == 2:
                url_hash, hon_code = line.split()
                good_urls.add(url_hash)
    
