import requests
import json


def parce_books(quantity=0):
    scrap = True
    page_num = 0
    books = []

    print('parse links')
    while scrap:
        page_num += 1
        print(f'page num - {page_num}')
        link = f'http://freebook.su/getbook.php?page={page_num}'
        r = requests.get(link)

        page = r.json()
        if not page:
            scrap = False
        for note in page:
            if int(note['raznost']) <= quantity\
                    and int(note['on_hand']) > 0:
                books.append({
                    'Название': note['name'],
                    'Ссылка': note['href'],
                    'Осталось': note['raznost'],
                    'На руках': note['on_hand']
                })

    print(f'quantity books: {len(books)}')
    print('save json')
    with open("books.json", "w") as write_file:
        json.dump(books, write_file, indent=4, ensure_ascii=False)
        print('json is ready')

    text = get_text()
    return text


def get_text():
    text = {0: 'Полученные книги\n\n'}

    raw_json = json.load(open('books.json'))
    i = 0
    for row in raw_json:
        line = (
            f'''<a href="{row['Ссылка']}">{row['Название']}</a>\nОсталось в библиотеке: {row['Осталось']}, На руках: {row['На руках']}\n\n''')

        if len(text[i] + line) > 4000:
            i += 1
            text[i] = ''
        text[i] += line

    return text


if __name__ == '__main__':
    parce_books()
    get_text()
