import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = 'https://ctftime.org/writeup/39313'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

breadcrumb = soup.find('ul', class_='breadcrumb')
event = breadcrumb.find_all('li')[2].find('a').text.strip()
challenge_name = breadcrumb.find_all('li')[4].find('a').text.strip()

writeup_div = soup.find('div', class_='well', id='id_description')
writeup = writeup_div.get_text(separator='\n').strip()

writeup_id = url.split('/')[-1]

task_link = breadcrumb.find_all('li')[4].find('a')['href']
task_id = task_link.split('/')[-1]

folder_name = 'writeups'
os.makedirs(folder_name, exist_ok=True)

writeup_file_path = os.path.join(folder_name, f"{writeup_id}.txt")
with open(writeup_file_path, 'w', encoding='utf-8') as file:
    file.write(writeup)
data = pd.DataFrame({
    'Event': [event],
    'Challenge Name': [challenge_name],
    'Writeup ID': [writeup_id],
    'Task ID': [task_id],
    'Writeup File': [writeup_file_path]
})

data.to_excel('ctftime_writeup.xlsx', index=False)

print('Data successfully scraped and saved to ctftime_writeup.xlsx and the writeup text file.')
