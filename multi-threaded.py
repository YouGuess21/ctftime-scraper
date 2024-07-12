import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to scrape data from a given URL
def scrape_writeup(url):
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
    writeup = writeup_div.get_text(separator='\n').strip() if writeup_div else ""

    writeup_id = url.split('/')[-1]

    task_link = breadcrumb.find_all('li')[4].find('a')['href']
    task_id = task_link.split('/')[-1]

    folder_name = 'writeups'
    os.makedirs(folder_name, exist_ok=True)

    writeup_file_path = os.path.join(folder_name, f"{writeup_id}.txt")
    with open(writeup_file_path, 'w', encoding='utf-8') as file:
        file.write(writeup)

    return {
        'Event': event,
        'Challenge Name': challenge_name,
        'Writeup ID': writeup_id,
        'Task ID': task_id,
        'Writeup File': writeup_file_path
    }

def main():
    base_url = 'https://ctftime.org/writeup/'
    urls = [base_url + str(i).zfill(5) for i in range(1, 10)]  # Generates URLs from 39313 to 1

    all_data = []
    max_workers = 10

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_writeup, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                all_data.append(data)
                print(f'Successfully scraped {url}')
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f'Error scraping {url}: 404 Not Found')
                else:
                    print(f'Error scraping {url}: {str(e)}')
            except Exception as e:
                print(f'Error scraping {url}: {str(e)}')

    df = pd.DataFrame(all_data)

    # Sorting the DataFrame by 'Writeup ID'
    df = df.sort_values(by='Writeup ID', ascending=True)

    output_file = 'ctftime_writeups.xlsx'
    df.to_excel(output_file, index=False)

    print(f'All data successfully scraped, sorted, and saved to {output_file}')

if __name__ == '__main__':
    main()
