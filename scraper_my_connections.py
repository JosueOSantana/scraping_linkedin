# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import re
print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')
sleep(2)

# Task 1.2: Key in login credentials
email_field = driver.find_element('id','username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(3)

password_field = driver.find_element('name','session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)

# Task 1.2: Click the Login button
signin_field = driver.find_element('xpath','//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(3)

print('- Finish Task 1: Login to Linkedin')

# Task 3: Importing the URLs_all_page created with my connections list 
with open(file="C:/JOSUÉ/FACULDADES/MBA - USP/Portifólio/PowerBI/My LinkedIn_CV/Scraping/Linkedin-profiles-scraping-main/url.txt", mode='r',encoding='utf8') as arquivo:
    texto = arquivo.read()
    urls_ext = re.findall('https://www.linkedin.com/in/+\S+',texto)
    
def clean(a):
    return a.strip('"')

URLs_clean = list(map(clean, urls_ext))
URLs_all_page = []
[URLs_all_page.append(x) for x in URLs_clean if x not in URLs_all_page]
del URLs_all_page[0]
del URLs_all_page[len(URLs_all_page)-1]

print('- All URLs were compiled!')

# Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Location', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        try:
            info_div = page_source.find('div',{'class':'ph5 pb5'})
            name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile name is: ', name)
            location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile location is: ', location)
            #title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
            #print('--- Profile title is: ', title)
            #writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:linkedin_URL})
            writer.writerow({headers[0]:name, headers[1]:location, headers[2]:linkedin_URL})
            print('\n')
        except:
            try:
                info_div = page_source.find('div',{'class':'ph5'})
                name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
                print('--- Profile name is: ', name)
                location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters 
                print('--- Profile location is: ', location)
                #title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
                #print('--- Profile title is: ', title)
                #writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:linkedin_URL})
                writer.writerow({headers[0]:name, headers[1]:location, headers[2]:linkedin_URL})
                print('\n')
            except:
                writer.writerow({headers[0]:'name', headers[1]:'location', headers[2]:linkedin_URL})
                print('\n')
                pass

print('Mission Completed!')