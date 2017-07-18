from bs4 import BeautifulSoup
import requests

endpt = 'https://newyork.craigslist.org/search/mis'

page_nums = range(700)[::120]

entry_urls = list()

for num in page_nums:
    payload = {'s': str(num)}
    res = requests.get(endpt, params=payload)
    soup = BeautifulSoup(res.text)
    tgt_links = soup.select('a.result-title')

    for link in tgt_links:
        entry_urls.append(link['href'])


# print entry_urls

i = 0
for url in entry_urls:
    url = 'https://newyork.craigslist.org' + url
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    try:
        tgt_section = soup.select('#postingbody')[0]
    except IndexError:
        pass
    else:
        tgt_text = tgt_section.get_text()

        # print tgt_text
        # break

        final_text = tgt_text.replace('QR Code Link to This Post', '').strip()

        with open('data/%i.txt' % i, 'w') as outfile:
            outfile.write(final_text.encode("utf8"))

    i += 1
