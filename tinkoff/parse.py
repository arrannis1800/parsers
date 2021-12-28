import requests
from bs4 import BeautifulSoup
import csv

headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
	}
fieldnames = ["ticker", "Название", "Цена",	"Валюта"]
list_of_cards = []
result_list = []



def get_links(headers,quantity):
	print("Начинаю парсинг")
	url = f"https://www.tinkoff.ru/invest/stocks/?country=All&orderType=Asc&sortType=ByName&start=0&end={quantity}"
	r = requests.get(url = url, headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')

	list_of_cards = soup.find_all(class_="Table-module__row_2rIfz")
	print(len(list_of_cards))
	for item in list_of_cards:
		result_list.append({
			"ticker": item.find(class_="Caption__subcaption_igeJU").text,
			"Название": item.find(class_="NameColumn__nameWrapper_177eF").text,
			"Цена": item.find(class_="SecurityColumn__cellPriceSecurities_38_gE").find(class_="Money-module__money_3h4MT").text.replace("\xa0$",""),
			"Валюта": item.find(class_="SecurityColumn__cellPriceSecurities_38_gE").find(class_="Money-module__money_3h4MT").text[-1]
			})
	with open("result_list.csv", "a", encoding='UTF8', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		for data in result_list:
			writer.writerow(data)

def main():
	quantity = input("сколько первых акций нужно спарсить?")
	get_links(headers, quantity)

if __name__ == "__main__":
	main()