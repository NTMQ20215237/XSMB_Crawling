# %%
import requests
from bs4 import BeautifulSoup

# %%
url1 = 'https://xoso.com.vn/xsmb-300-ngay.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Referer': url1,
}
response = requests.get(url1, headers=headers)

# %%
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='table-result font-skq')

    for table in tables:
        # Extract the date of the lottery results
        # Extract special prize and first prize numbers
        date_element = table.find('h3', class_='head-th').text.strip()
        special_prize = table.find('span', class_='special-prize').text.strip()
        first_prize = table.find('span', class_='prize1').text.strip()

        # Print the results
        print("Ngày:", date_element)
        print("Giải Đặc Biệt:", special_prize)
        print("Giải Nhất:", first_prize)
        print()  # Add a blank line between each set of results

