from bs4 import BeautifulSoup
import requests
import csv

def scrape(source):
    headers = ["Name", "Distance", "Mass", "Radius"]
    data = []
    soup = BeautifulSoup(source, "html.parser")
    for tr_tags in soup.find_all("tr"):
        td_tags = tr_tags.find_all("td")
        templist = []
        for index, tag in enumerate(td_tags):
            if index == 1:
                try:
                    templist.append(tag.find_all("a")[0].contents[0])
                except IndexError:
                    templist.append(tag.contents[0])
            elif index == 3:
                templist.append(tag.contents[-1].encode('utf-8').strip())
            elif index in [5, 6]:
                templist.append(tag.contents[0].encode('utf-8').strip())
        data.append(templist)
    data.pop(0)

    with open("data.csv", "w", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(data)

if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
    source = requests.get(url)
    scrape(source.content)