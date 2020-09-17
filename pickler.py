"""Script to download honcode database as pickled python dictionary"""


import argparse
import os
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("--path", default=None, help="Desired database location.")
args = parser.parse_args()


def download_honcode_database(path="data"):
    """downloads honcode database as .txt file to `path`"""
    os.system(f"wget -P {path} https://www.honcode.ch/HONcode/Plugin/listeMD5.txt")


def pickle_honcode_database(path="data"):
    """pickles honcode .txt database at `path`"""
    d = {}
    file_path = os.path.join(os.getcwd(), path, "listeMD5.txt")
    with open(file_path, "r", encoding="utf-8") as md5_file:
        for line in md5_file:
            if len(line.split()) == 2:
                url_hash, hon_code = line.split()
                d[url_hash] = hon_code

    out_file = os.path.join(os.getcwd(), path, "honcode.dat")
    with open(out_file, "wb+") as dat_file:
        pickle.dump(d, dat_file)
        print(f"Data written to {out_file}")


if __name__ == "__main__":
    download_honcode_database(
        args.path
    ) if args.path is not None else download_honcode_database()
    pickle_honcode_database(
        args.path
    ) if args.path is not None else pickle_honcode_database()
