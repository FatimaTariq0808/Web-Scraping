from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd

driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
driver.get('https://www.youtube.com/playlist?list=PL8dPuuaLjXtOVe7Q88hA-IJ1l6BkzxxDC')
driver.maximize_window()
wait = WebDriverWait(driver, 10)
sleep(5)
df = pd.DataFrame(columns = ['title', 'link' , 'views', 'duration', 'thumbnails', 'comments'])
for i in range(5):
    driver.execute_script("window.scrollBy(0,400)")
    sleep(2)
sleep(10)

video_data = []
video_links = []
title_list = []
counter = 0

titles = driver.find_elements(By.ID, "video-title")
for title_element in titles:
    # Get video link (href attribute)
    title = title_element.text
    title_list.append(title)
    video_link = title_element.get_attribute('href')
    video_links.append(video_link)
    # print("Video Link:", video_link)
    # print(title)

for i,j in zip(video_links,title_list):
    if(counter<=2):
    # print(i)
        driver.get(i)
        sleep(5)

        views_element = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]')
        
        image_element = 'img[src^="https://i.ytimg.com/vi/"]'
        v_thumbnail = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, image_element)))
        image_urls = v_thumbnail.get_attribute('src')
        
        duration_element = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]')

        views = views_element.text
        duration = duration_element.text

        for i in range(2):
            driver.execute_script("window.scrollBy(0,700)","")
        sleep(2)
        sleep(10)
        comments=[]

        # comment=driver.find_elements(By.XPATH,"""//*[@id="content-text"]/span""") 
        # for i in comment:
        #     comments.append(i.text)
        # df = df.append({ 'title': j, 'link': video_link, 'views': views, 'duration': duration, 'thumbnails': image_urls, 'comments': comments}, ignore_index=True)
        comments = [comment.text for comment in driver.find_elements(By.XPATH, '//*[@id="content-text"]')]

        for comment in comments:
            df = df.append({'title': j,
                            'link': video_link,
                            'views': views,
                            'duration': duration,
                            'thumbnails': image_urls,
                            'comments': comment},
                        ignore_index=True)
        counter += 1 

df.to_csv("scraped_data.csv",index=False)
driver.quit()
