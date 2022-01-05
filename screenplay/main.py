import re
import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

list_script = []

def get_page(url):
    response = requests.get(url)
    page = remove_parentheses(response.text)
    return page

def get_soup(url):
    page = get_page(url)
    soup = BeautifulSoup(page,'lxml')
    return soup

def remove_parentheses(text):
    """
    Remove all blocks of text wrapped in parentheses or brackets, squeeze the spaces and strip the text.
    """
    reP = '(\[[^\]]*\]|\([^\)]*\))'
    reS = '\s+'
    return re.sub(reS, ' ', re.sub(reP, ' ', text.replace('\xa0',' '))).strip()


def get_script_list(soup):
    character_list = soup.find_all('dt')                #собираю всех персонажей 
    speech_list = soup.find_all('dd')                   #собираю все реплики 
    # добавляю в пустой список все реплики и персонажей
    for speech in range(len(speech_list)):
        list_script.append({
            'Character':character_list[speech].text,
            'Speech':speech_list[speech].text
            })

# превращаю список словарей в датафрейм
def get_DF(speech_list):
    df = pd.DataFrame.from_dict(speech_list)
    df.to_csv('script.csv',index=False)                 # и сохраняю его на всякий случай для дальнейшей работы
    return df

if __name__ == "__main__":
    get_script_list(get_soup("http://www.fpx.de/fp/Disney/Scripts/SleepingBeauty/sb.html"))
    print(get_DF(list_script))