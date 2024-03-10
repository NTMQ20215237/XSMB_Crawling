import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

def crawl_lottery_results(date):
    url = f"https://xoso.com.vn/xsmb-{date}.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': url,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        special_prize = soup.find('span', class_='special-prize').text.strip()
        first_prize = soup.find('span', class_='prize1').text.strip()
        prize2_elements = soup.find_all('span', class_='prize2')
        prize2_numbers = []

        for prize2_element in prize2_elements:
            prize2_text = prize2_element.text.strip()
            numbers = prize2_text.split()
            prize2_numbers.extend(numbers)
        print(date)
        # Return a dictionary containing the extracted data
        return {'Date': date, 'Special Prize': special_prize, 'First Prize': first_prize, 'Second Prize': prize2_numbers}

# Define start_date and end_date
start_date = datetime(2018, 1, 1)
end_date = datetime(2024, 2, 1)

# Initialize a list to store the extracted data
all_data = []

# Loop through the dates
current_date = start_date
while current_date <= end_date:
    formatted_date = current_date.strftime("%d-%m-%Y")
    # Check if the date is not within the excluded range
    if not ((current_date >= datetime(2018, 2, 15) and current_date <= datetime(2018, 2, 18)) or
            (current_date >= datetime(2019, 2, 4) and current_date <= datetime(2019, 2, 7)) or
            (current_date >= datetime(2020, 1, 24) and current_date <= datetime(2020, 1, 27)) or
            (current_date >= datetime(2021, 2, 11) and current_date <= datetime(2021, 2, 14)) or
            (current_date >= datetime(2022, 1, 31) and current_date <= datetime(2022, 2, 3)) or
            (current_date >= datetime(2023, 1, 21) and current_date <= datetime(2023, 1, 24)) or
            (current_date >= datetime(2020, 4, 1) and current_date <= datetime(2020, 4, 22))):
        # Call crawl_lottery_results function to get the data
        data = crawl_lottery_results(formatted_date)
        # If data is not None (i.e., data was found for this date)
        if data:
            all_data.append(data)
    current_date += timedelta(days=1)

# Write the data to a CSV file
csv_file_path = 'lottery_results.csv'
fieldnames = ['Date', 'Special Prize', 'First Prize', 'Second Prize']

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f"Data has been written to {csv_file_path}.")
