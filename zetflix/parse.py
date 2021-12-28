import requests
from bs4 import BeautifulSoup
import csv
import time


headers = {
"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36",
"accept": "*/*"}
fieldnames = ["Название", "Жанры", "Описание", "Ссылка на трейлер", "Ссылка на сайт"]

def find_tvshow(headers):
	page = 1
	list_of_cards = []
	cards= []
	description_of_cards = []
	while page <= 30:
		if page == 1:
			url = f"https://hdi.zetflix.online/serials/"
		else:
			url = f"https://hdi.zetflix.online/serials/page/{page}/"

		r = requests.get(url=url, headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')

		cards = soup.find(class_="sect-items fx-in").find_all(class_="vi-img img-resp-h")
		for card in cards:
			list_of_cards.append(card['href'])

		page += 1

	for card in list_of_cards:
		print(card)
		time.sleep(0.5)
		r = requests.get(url=card, headers=headers)
		print(r)
		soup = BeautifulSoup(r.text, 'html.parser')
		description = soup.find(id="finfo").find_all("li")
		description_of_cards.append({
			"Название": description[0].text[10:],
			"Жанры": description[1].text[6:],
			"Описание": soup.find(id="serial-kratko").text,
			"Ссылка на трейлер": soup.find(class_="fbtn to-trailer")["data-src"],
			"Ссылка на сайт": card,
			})
	with open("result_list.csv", "a", encoding='UTF8', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		for data in description_of_cards:
			writer.writerow(data)

		print("done")




def main():
	find_tvshow(headers)


if __name__ == '__main__':
	main()
