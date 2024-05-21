from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class Game:
    def __init__(self, name, off, price, rating, release_date):
        self.name = name
        self.off = off
        self.price = price
        self.rating = rating
        self.release_date = release_date

driver = webdriver.Firefox()
driver.get('https://steamdb.info/sales/')
wait = WebDriverWait(driver, 10)
select_element = wait.until(EC.visibility_of_element_located((By.ID, "dt-length-0")))

select = Select(select_element)
select.select_by_value("-1")

page_source = driver.page_source
df = pd.read_html(page_source)[0]

REGEX_WORDS = ['Midweek','Daily Deal','Introductory','new historical low', 'low:','Week Long Deal','all-time', 'Week Long Deal all-time', '2-year']
games_list = []

for index, row in df.iterrows():
    for word in REGEX_WORDS:
        if word in row['Name']:
            name_split = row['Name'].split(word)
            name = name_split[0].strip()
            break
        else:
            name = row['Name']
    off = row['%']
    price = row['Price']
    rating = row['Rating']
    release = row['Release']
    
    game = Game(name, off, price, rating, release)
    games_list.append(game)

driver.quit()

games_data = []
for game in games_list:
    games_data.append({
        'Name': game.name,
        'Off': game.off,
        'Price': game.price,
        'Rating': game.rating,
        'Release Date': game.release_date
    })

df_export = pd.DataFrame(games_data)

df_export.to_csv('games_data.csv', index=False, encoding='utf-8')

print("Dados exportados para games_data.csv")
