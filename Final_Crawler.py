import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
# import csv
import psycopg2
import random

dotenv_path = "Variable.env"
load_dotenv(dotenv_path)

conn = psycopg2.connect(
    dbname=os.getenv("YOUR_DATABASE_NAME"),
    user=os.getenv("YOUR_USER_NAME_IN_POSTGRES"),
    password=os.getenv("YOUR_PASSWORD"),
    host=os.getenv("YOUR_DATABASE_HOST"),
    port=os.getenv("PORT")
)
cursor = conn.cursor()

def crawl_lottery_results(date):
    url = f"https://xoso.com.vn/xsmb-{date}.html"
        # Danh sách các User-Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.898",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Vivaldi/1.0.435.46",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Whale/1.0.40.5",
    ]
    
    # Chọn ngẫu nhiên một User-Agent từ danh sách
    user_agent = random.choice(user_agents)
    
    headers = {
        'User-Agent': user_agent,
        'Referer': url,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #Crawl giải đặc biệt
        special_prize = soup.find('span', class_='special-prize').text.strip()
        #Crawl giải nhất
        first_prize = soup.find('span', class_='prize1').text.strip()
        #Crawl giải hai
        prize2_elements = soup.find_all('span', class_='prize2')
        prize2_numbers = []

        for prize2_element in prize2_elements:
            prize2_text = prize2_element.text.strip()
            numbers = prize2_text.split()
            prize2_numbers.extend(numbers)
        #Crawl giải ba
        prize3_elements = soup.find_all('span', class_='prize3')
        prize3_numbers = []

        for prize3_element in prize3_elements:
            prize3_text = prize3_element.text.strip()
            numbers = prize3_text.split()
            prize3_numbers.extend(numbers) 
        #Crawl giải tư
        prize4_elements = soup.find_all('span', class_='prize4')
        prize4_numbers = []

        for prize4_element in prize4_elements:
            prize4_text = prize4_element.text.strip()
            numbers = prize4_text.split()
            prize4_numbers.extend(numbers)
        #Crawl giải năm
        prize5_elements = soup.find_all('span', class_='prize5')
        prize5_numbers = []

        for prize5_element in prize5_elements:
            prize5_text = prize5_element.text.strip()
            numbers = prize5_text.split()
            prize5_numbers.extend(numbers) 
        #Crawl Giải Sáu 
        prize6_elements = soup.find_all('span', class_='prize6')
        prize6_numbers = []

        for prize6_element in prize6_elements:
            prize6_text = prize6_element.text.strip()
            numbers = prize6_text.split()
            prize6_numbers.extend(numbers)
        #Crawl Giải Bảy
        prize7_elements = soup.find_all('span', class_='prize7')
        prize7_numbers = []

        for prize7_element in prize7_elements:
            prize7_text = prize7_element.text.strip()
            numbers = prize7_text.split()
            prize7_numbers.extend(numbers)
            # Check if the data already exists in the database
    formatted_date = current_date.strftime("%Y-%m-%d")

    cursor.execute("SELECT * FROM lottery_results WHERE ngay = %s", (formatted_date,))
    existing_data = cursor.fetchone()

    if existing_data:
        print(f"Data for {formatted_date} already exists in the database.")
    else:
        # Insert the data into the database
        sql = """INSERT INTO lottery_results (ngay, giai_dac_biet, giai_nhat, giai_nhi, giai_ba, giai_bon, giai_nam, giai_sau, giai_bay)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            formatted_date,
            special_prize,
            first_prize,
            prize2_numbers,
            prize3_numbers,
            prize4_numbers,
            prize5_numbers,
            prize6_numbers,
            prize7_numbers
        ))
    #    print(f"Data for {formatted_date} inserted into the database.")
        
        print(date)
        # Return a dictionary containing the extracted data
#        return {'Ngày': date, 'Giải Đặc BIệt': special_prize, 'Giải Nhất': first_prize, 'Giải Nhì': prize2_numbers, 'Giải Ba':prize3_numbers, 'Giải Tư':prize4_numbers, 'Giải Năm':prize5_numbers, 'Giải Sáu':prize6_numbers, 'Giải Bảy':prize7_numbers}

# Define start_date and end_date
#start_date = datetime(2018, 1, 1)
#end_date = datetime(2024, 2, 1)
start_date = os.getenv("START_DATE")
end_date = os.getenv("END_DATE")
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")
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
        crawl_lottery_results(formatted_date)
        # Call crawl_lottery_results function to get the data
        # data = crawl_lottery_results(formatted_date)
        # If data is not None (i.e., data was found for this date)
    #     if data:
    #         all_data.append(data)
    current_date += timedelta(days=1)
        
# Write the data to a CSV file
# csv_file_path = os.getenv("CSV_FILE_PATH")
# fieldnames = ['Ngày', 'Giải Đặc BIệt', 'Giải Nhất', 'Giải Nhì', 'Giải Ba', 'Giải Tư', 'Giải Năm', 'Giải Sáu', 'Giải Bảy']

# with open(csv_file_path, mode='w',encoding='utf-8', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(all_data)
conn.commit()
conn.close()
print(f"Data has been written to database.")
