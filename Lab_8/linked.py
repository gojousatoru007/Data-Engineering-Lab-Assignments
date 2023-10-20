import csv
import time
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome()

sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)

# Task 1.1: Import username and password
username = "harshtomar001.ht@gmail.com"
password = "harsh@13102002"

# Task 1.2: Key in login credentials
email_field = driver.find_element(By.ID, 'username')
email_field.send_keys(username)

password_field = driver.find_element(By.NAME, 'session_password')
password_field.send_keys(password)

# Task 1.3: Click the Login button
signin_field = driver.find_element(By.XPATH, '//*[@type="submit"]')
signin_field.click()
sleep(5)

data = []
dictionary = {}
with open('mydata.csv', 'r') as csvfile: # read csv file containing url of the LinkedIn profile
    csvreader = csv.reader(csvfile)
    for url in csvreader:
        # Login 
        sleep(2)
        profile_url = url[0]
        driver.get(profile_url)
        start = time.time()
        
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000

            # we will stop the script for 3 seconds so that the data can load
            time.sleep(2)
            end = time.time()
            # We will scroll for 10 seconds.
            if round(end - start) > 10:
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')



        # 1 NAME
        try:

            name = None
            name_element = soup.find('h1', {'class':'text-heading-xlarge inline t-24 v-align-middle break-words'})

            name = name_element.text

        #print(name)
        except:
            pass

        # 2 Image Link
        try:
            ImageLink = None
            ImageLink = soup.find('img', {'class': 'pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show evi-image ember-view'})
            ImageLink = (ImageLink.get("src"))
        except:
            pass
        # 3 Title
        try:
            title = None
            title = soup.find('div', {"class": "text-body-medium break-words"}).get_text().replace('\n', '').strip()
        except:
            pass

        # 3 LOCATION

        try:
            loc = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})
            location = loc.get_text().strip()
        except:
            pass 

        # 4 Connections 

        try:
            conn = soup.find('ul', {'class':"pv-top-card--list pv-top-card--list-bullet"})
        #conn2 = conn.find('span')
        #conn3 = conn2.find('span')
            connections = conn.get_text()
            connections = connections
        except:
            pass


        try:
            mutual_conn = soup.find('span', {'class': 't-normal t-black--light t-14 hoverable-link-text'})
            mutual = mutual_conn.get_text()
            #print(mutual)
        except:
            pass

        try:
            about = None
            about = soup.find('div', {'class':'display-flex ph5 pv3'})
            about = about.get_text().replace('\n', '')
            # print(about2)
        except:

            pass



        # 4 EXPERIENCE
        experiences = []
    
        try:
            experience_div = soup.find('div', {"id": "experience"})
            
            exp_list = experience_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li')

            for each_exp in exp_list:
                # exp_temp = each_exp.findChild('div').findChild('div', {
                #     'class':'display-flex flex-column full-width align-self-center'
                # }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('div').findChild('div').get_text()


                exp_temp2 = each_exp.findChild('div').findChild('div', {
                    'class':'display-flex flex-column full-width align-self-center'
                }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('div').findAll('span')
                nn = 0
                text2 = ''
                for i in exp_temp2:
                    if(nn % 2 == 0):

                        #print("hewo")
                        #print(i.get_text().replace('\n', ''))
                        text2 += i.get_text().replace('\n', '')
                    nn = nn + 1
                #print("hello\n")
                
                # text = ''
                
                # for i in exp_temp:
                #     text += i.get_text().replace('\n', '')
                        
                        
                
                
                #print(text2)
                # exp_temp = exp_div+exp_span1+exp_span2
                experiences.append(text2)
                
        except AttributeError:
            pass

        # 5 EDUCATION LEVEL AND HISTORY
        educations = []
        a = []
        try:
            education_div = soup.find('div', {"id": "education"})
            
            edu_list = education_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li')
            
            for each_edu in edu_list:
                #print(i);
                #print(each_edu)
                edu_temp = each_edu.findChild('div').findChild('div', {
                    'class':'display-flex flex-column full-width align-self-center'
                }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('a').findChild('div').get_text()
                #print(edu_temp)
                if(len(edu_temp) > 0):
                    edu_temp = edu_temp[int(len(edu_temp)/2):];

                more = ''
                edu_temp3 = each_edu.findChild('div').findChild('div', {
                    'class':'display-flex flex-column full-width align-self-center'
                }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('a').findAll(
                    'span'
                )
                n = 0
                for i in edu_temp3:
                    if(n % 2 == 0):
                        y = (i.get_text()).replace('\n', '')
                        more += y
                    n += 1;

                
                
                # edu_temp2 = each_edu.findChild('div').findChild('div', {
                #     'class':'display-flex flex-column full-width align-self-center'
                # }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('a').findAll('span').get_text()

                
                # print(edu_temp)
                educations.append(more)

             
        except AttributeError:
            pass

        # 6 lICENSE AND CERTIFICATIONS
        certifications = []
        
        try:
            certification_div = soup.find('div', {"id": "licenses_and_certifications"})
            
            cert_list = certification_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li')
            
            for each_cert in cert_list:
                cert_temp = each_cert.findChild('div').get_text()

                certifications.append(cert_temp.replace('\n', ' '))

        except AttributeError:
            pass

        # 7 SKILLS
        skills = []
        
        try:

            skills_div = soup.find('div', {"id": "skills"})
            
            skill_list = skills_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li')
            #print(len(skill_list))
            for each_skill in skill_list:
                skill_temp = each_skill.findChild('div').findChild('div', {'class':'display-flex flex-column full-width align-self-center'}).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('a').get_text().strip()
                
                skills.append(skill_temp)
        except AttributeError:
            pass


        # 8 LANGUAGES
        languages = []

        try:
            Lang_div = soup.find('div', {"id": "languages"})
            lang_list = Lang_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li')

            for lang in lang_list:
                lang_temp = {
                    lang.findChild('div').findChild('div', {
                    'class':'display-flex flex-column full-width align-self-center'
                }).findChild('div', {'class':'display-flex flex-row justify-space-between'}).findChild('div', {'class':'display-flex flex-column full-width'}).get_text().strip()[:-31].replace('\n', '')
                }
                #print(lang_temp)
                languages.append(list(lang_temp))
        except AttributeError:
            pass

        dictionary = {
            "Name": name,
            "About": about,
            "ProfileImageLink": str(ImageLink),
            "Title": title,
            "Location": location,
            "Experiences": experiences,
            "Education": educations,
            "Certifications": certifications,
            "Skills": skills,
            "Languages": languages

        }

        data.append(dictionary)

driver.quit()

print(data)


with open('data.json', 'w') as file:

    json.dump(dictionary, file, indent = 4)


