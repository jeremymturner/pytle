import ephem
import os
from os.path import join, dirname, abspath, isfile
from datetime import datetime, timedelta
import logging
import json

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_path(filename):
        packagedir = abspath(__file__)
        fulldir = join(dirname(packagedir), 'data')
        fullname = join(fulldir, filename)
        return fullname


class pytle:
    def __init__(self, keps_url='', cache=False):

        if keps_url:
            if cache:
                cache_dir = os.environ.get('HOME') + '/.' + type(self).__name__
                keps = self.try_cache(keps_url, cache_dir)
            else:
                keps = self.download_keps(keps_url)

            self.satlist = self.load_keps(keps)

    def download_keps(self, keps_url):
        logging.info("Downloading keps from " + keps_url)
        try:
            with urlopen(keps_url) as response:
                self.data = data = response.read()
                kep_lines = data.decode().split('\n')
        except TimeoutError:
            logging.error("Timeout in accessing " + keps_url)
            exit()

        return kep_lines

    def cache_keps(self, cache_file):
        logging.info("Writing keps cache to " + cache_file)
        with open(cache_file, 'wb') as out_file:
            out_file.write(self.data)

    def load_keps(self, keps):
        satlist = {}
        kepslist = []
        self.names = names = [line for i, line in enumerate(keps) if i % 3 == 0]
        for i, line in enumerate(keps):
            if i % 3 == 2:
                name = keps[i - 2].strip()
                eph = ephem.readtle(
                    keps[i - 2],
                    keps[i - 1],
                    keps[i])
                # satlist.append(sat)
                # satlist.append({"name": name, "ephem": eph})
                logging.debug("Loaded " + name)
                satlist[name] = {}

                # Load satellite specific defaults (band, frequencies, mode)
                if isfile(get_path("sats/" + name + ".json")):
                    with open(get_path("sats/" + name + ".json")) as file:
                        satinfo = json.loads(file.read())

                    for key, value in satinfo[name].items():
                        try:
                            # Python 2
                            key = key.encode('utf-8') if isinstance(key, unicode) else key
                            value = value.encode('utf-8') if isinstance(value, unicode) else value
                        except NameError:
                            # Python 3 (nothing)
                            pass

                        satlist[name][key] = value

                satlist[name]["ephem"] = eph

        logging.info("Loaded %s satellites" % len(names))
        return satlist

    def try_cache(self, keps_url, cache_dir):
        cache_file = cache_dir + '/keps.txt'
        cache_days = 7
        cache_file_ts = None
        keps = None

        # If the cache dir does not exist
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)

        # If the cache file does not exist
        if not os.path.isfile(cache_file):
            keps = self.download_keps(keps_url)
            self.cache_keps(cache_file=cache_file)

        # If the cache file exits
        else:
            weekago = datetime.now() - timedelta(days=cache_days)
            cache_file_ts = datetime.fromtimestamp(os.path.getctime(
                cache_file))

            # If the cache exists and is up to date
            if cache_file_ts > weekago:
                logging.info("Using cached keps from " + cache_file)
                with open(cache_file) as file:
                    return file.read().split('\n')
            else:
                keps = self.download_keps(keps_url)
                self.cache_keps(cache_file=cache_file)

        return keps


def main():
    # args = argsc.get_args(sys.argv[1:])
    # http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt
    # https://www.celestrak.com/NORAD/elements/amateur.txt
    tle = pytle(
        keps_url="http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt",
        cache=True)
    # print(" ".join(tle.names))
    # from pprint import pprint
    # pprint(tle.satlist)


if __name__ == "__main__":
    main()
