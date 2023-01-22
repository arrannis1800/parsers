import requests
from bs4 import BeautifulSoup


def main():
	while True:
		isbn = input('input your isbn(or "stop" for exit): ')
		if isbn.lower() == 'stop':
			print('Thanks')
			break
		link = f'https://www.labirint.ru/search/{isbn}/?stype=0&available=1&paperbooks=1'
		r = requests.get(link)

		soup = BeautifulSoup(r.text, 'html.parser')
		if soup.find('div', class_='b-stab-e-empty-result'):
			print('Нет книги')
		else:
			print(f"https://www.labirint.ru/{soup.find(class_='cover')['href']}")


if __name__ == '__main__':
	main()
