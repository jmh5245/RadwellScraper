import bs4
import urllib.request
import ssl
import json
import requests

class Scraper:
    def __init__(self):
        self.master_list = []
        # ignoring ssl cert
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        self.page = 1
        self.pagesToScrape = 1
        self.results = []

        self.IDs = []

        self.base_url = "https://www.zoro.com/"
        self.params = f"search?q="
        self.search_terms = []
        self.pageSearch = "&page="
        self.cardTags = ("div", {"class": "product-card"})
        self.productIDTag = "gtm-data-productid"

        self.API_url = "https://www.zoro.com/product/?products="
        self.IMG_url = "https://www.zoro.com/static/cms/product/full/"

    def getFullURL(self):
        return self.base_url + self.params + "%20".join(self.search_terms) + self.pageSearch

    def Scrape(self):
        searchFor = input("enter search terms: ")
        self.pagesToScrape = int(input("how many pages would you like to scrape? "))
        self.search_terms = searchFor.split(" ")
        while self.page <= self.pagesToScrape:
            full_link = self.getFullURL() + str(self.page)
            self.get_page_results(full_link)
            self.page+=1

        self.writeFile()
        print("total products scraped: ", len(self.master_list))

    def get_page_results(self, url):
        IDs = []
        content = urllib.request.urlopen(url, context=self.ctx).read()  # Get page content
        full_soup = bs4.BeautifulSoup(content, 'html.parser')  # Parse page content
        all_results = full_soup.findAll(self.cardTags[0], self.cardTags[1])

        for i in all_results:
            IDs.append(i["gtm-data-productid"])
        self.get_products(IDs)


    def get_products(self, productIDs):

        if len(productIDs) == 0:
            print("page results not scrapable")
            return
        base_url = "https://www.zoro.com/product/?products="
        query = ",".join(productIDs)
        url = base_url + query
        payload = {}
        headers = {
            'authority': 'www.zoro.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            # removed 'cookies' and 'referer'
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        print("making request...")
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)
        items = json.loads(response.content)

        for i in items["products"]:
            self.master_list.append(i)

    def writeFile(self):
        with open("results.txt", "w") as file:
            file.write(json.dumps(self.master_list, indent=2))

scraper = Scraper()
scraper.Scrape()