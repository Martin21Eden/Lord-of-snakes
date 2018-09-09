import requests
from bs4 import BeautifulSoup
import csv
import re
import sys, getopt


class Parser:
    def __init__(self, url, values):
        self.url = url
        self.values = values
        self.urls_items = []
        self.data = []

    def request(self, url):
        source = requests.get(url).text
        return BeautifulSoup(source, 'lxml')

    @property
    def get_urls_items(self):
        for one in self.request(self.url).find_all('li',
                                     class_='grid__item one-fifth medium--one-quarter small--one-half product-list__item'):
            self.urls_items.append('https://suzyshier.com' + str(one.a['href']))
        return self.urls_items

    def get_info(self):
        for one in self.get_urls_items:
            soup = self.request(one)
            pop = {}
            if 'title' in self.values:
                pop['title'] = soup.find('div',
                                     class_='grid__item large-up--one-third product__selector-container').h1.text[11:]
            if 'color' in self.values:
                pop['color'] = [o.input['value'] for o in soup.find_all('label', class_='radio-color')]

            if 'price' in self.values:
                price = soup.find('div', class_='product__price-wrapper').span.text
                if price == 'Regular price':
                    price = soup.find('span', class_='product__compare-at').text
                    pop['price'] = re.search(r'\d+\.\d+', price).group()
                else:
                    try:
                        pop['price'] = re.search(r'\d+\.\d+', price).group()
                    except AttributeError:
                        pop['price'] = 'No price'
            if 'discount_price' in self.values:
                try:
                    discount_price = soup.find('span',
                                      class_='product__discount').text
                    pop['discount_price'] = re.search(r'\d+\.\d+', discount_price).group()
                except AttributeError:
                    pop['discount_price'] = 'Not discount_price'
            if 'sizes' in self.values:
                pop['sizes'] = [o.input['value'] for o in soup.find_all('label', class_='radio-size')]
            if 'description' in self.values:
                pop['description'] = soup.find('span', class_='description').text.rstrip()
            if 'specs' in self.values:
                pop['specs'] = soup.find('div', class_='resp-tabs-container resp-element').ul.text.rstrip()
            self.data.append(pop)

    def save_csv(self):
        with open(f'{self.url.split("/")[-1]}.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(self.data)


def main(argv):
    url = None
    try:
        opts, args = getopt.getopt(argv, "h:u:", ["url="])
    except getopt.GetoptError as o:
        print(o)
        print('name.py -u <url>  <values> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('name.py -u <url> -v <values> ')
            sys.exit()
        elif opt in ("-u", "--url"):
            url = str(arg)
    if url is None:
        print('please enter your url!')
        sys.exit()
    elif len(args) == 0:
        print('please enter your values!')
        sys.exit()

    instance = Parser(url=url, values=args)
    instance.get_info()
    instance.save_csv()


if __name__ == '__main__':
    main(sys.argv[1:]) 
