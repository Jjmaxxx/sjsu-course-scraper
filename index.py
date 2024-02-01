import csv
from prefixes import prefix
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#need this bc the course website sometimes just doesnt load correctly for some reason and needs a refresh
#why is sj's own course website broken
def findRows(index):
    for i in range(5):
        try:
            rows = WebDriverWait(driver,5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"width"))
            )
            return rows
        except:
            driver.refresh()
            continue
    return None
    
try:
    with open('courses.csv','w', encoding="utf-8") as file:
        writer = csv.writer(file)
        for tag in prefix:
            driver.get(f'https://catalog.sjsu.edu/content.php?filter[27]={tag}&filter[29]=&filter[keyword]=&filter[32]=1&filter[cpage]=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter[exact_match]=1#acalog_template_course_filter')
            print(tag)
            rows = findRows(0)
            if rows == None:
                print('didnt find anything')
                continue
            
            for row in rows:
                link = WebDriverWait(row,5).until(
                    EC.presence_of_element_located((By.TAG_NAME,"a"))
                ).click()
                title = WebDriverWait(row,5).until(
                    EC.presence_of_element_located((By.TAG_NAME,"h3"))
                )
                body = WebDriverWait(title,5).until(
                    EC.presence_of_element_located((By.XPATH,".."))
                ).text
                body= list(filter(None, body.split("\n")))
                writer.writerow(body)
except Exception as e:
    print(e)
    driver.quit()




