"""загрузить с каждой карточки 
название
описание
сайт
собрать ссылки на все изображения
ссылуа на карточку"""

import requests
import csv


headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
fieldnames = ["title", "description", "url", "url_on_folio"]


def request_links(headers):
	num_of_page = 0
	result_list = []
	result_in_list = 0

	while True:

		url = f"https://s1.landingfolio.com/api/v1/inspiration/?offset={num_of_page}&color=%23undefined"

		r = requests.get(url=url, headers=headers)
		data = r.json()

		for item in data:
			if "description" in item:
				result_list.append(
					{
						"title": item.get("title"),
						"description": item.get("description"),
						"url": item.get("url"),
						"url_on_folio": "https://www.landingfolio.com/inspiration/post/" + item.get("title").replace(" ", "-"),
					}
				)
				result_in_list += 1
			else:
				with open("result_list.csv", "a", encoding='UTF8', newline='') as file:
					writer = csv.DictWriter(file, fieldnames=fieldnames)
					for data in result_list:
						writer.writerow(data)

				return f"[INFO] work finished"

		print(f"[+] Processed {num_of_page}")
		num_of_page += 1

	# r = requests.get(url=url,headers=headers)
	# r_text = r.text
	# print(r_text)


def main():
	request_links(headers=headers)


if __name__ == "__main__":
	main()
