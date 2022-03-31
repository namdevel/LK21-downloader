import re
import requests


class LK21Downloader:

    def __init__(self):
        self.INDEX_MOVIE_URL = "https://dl.indexmovies.xyz"

    def getSlug(self, url):
        try:
            movie_param = url.split("/")[2 + 1]
            return movie_param
        except Exception:
            print("Can't find slug from movie URL")
            exit(1)

    def generate(self, url):
        try:
            slug = self.getSlug(url)
            source = requests.get(self.INDEX_MOVIE_URL + f"/iframe/top.php?slug={slug}")
            search = (
                re.search('<p id="skip"><a href="(.*)" target="', source.text)
                .group(1)
                .replace("/get/", "/verifying.php?slug=")
            )
            
            result = requests.get(search)
            data = result.text.replace("'", '"').replace(' target="_blank"', "")
            find_provider = re.findall("<td><strong>(.*)</strong></td>", data)
            find_url = re.findall('<a href="(.*)" class="', data)
            print("\nDownload link:\n")
            
            for (provider, link) in zip(find_provider, find_url):
                print(f"> {provider.ljust(15)} : {link}")
                
        except Exception:
            print("Download link not found, check again your movie URL")
            exit(1)
