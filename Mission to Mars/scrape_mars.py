from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests 
import time


# In[3]:

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    news_title, news_p = mars_news(browser)
    data_result = {
    "news_title" : news_title,
    "news_p" : news_p,
    "image" : image(browser),
    "weather" : weather(browser),
    "facts" : facts(),
    "hemispheres" :hemisphere(browser)
    }

    browser.quit()
    return data_result

def mars_news(browser):
    # # NASA Mars News
    
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    
    # In[12]:


    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    return news_title, news_p

def image(browser):
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(3)
        # Have splinter click full image button
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
# Have splinter click more info button
    browser.click_link_by_partial_text("more info")
    featured_pg = browser.html
    img_soup = BeautifulSoup(featured_pg, "html.parser")
    # Get featured image url
    featured_img = img_soup.find("figure", class_ = "lede")
    featured_img_url =featured_img.a["href"]
    featured_img_url = ("https://www.jpl.nasa.gov" + featured_img_url)
    return featured_img_url

def weather(browser):
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
        #HTML object
    weather = browser.html
#Create beautifulsoup object parse with HTML parser
    wea_soup = BeautifulSoup(weather,"html.parser")
        #get latest weather update by going thru the url html code
    latest_tweet = wea_soup.find('p', class_='TweetTextSize').text
    return latest_tweet

def facts():
    # # Mars Facts

    url_fact = "https://space-facts.com/mars/"

    tables = pd.read_html(url_fact)

    df = tables[0]
    df.columns = ['Parameter','Value']

    html_table = df.to_html()

    html_table = html_table.replace("\n","")
    return df.to_html(index=False)

def hemisphere(browser):
    # # Mars Hemispheres

    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    
    html = browser.html 
    soup = bs(html,"html.parser")
    items = soup.find_all("div", class_='item')

    hemisphere_image_urls = []
    hemisphere_main_url = "https://astrogeology.usgs.gov"
    for item in items: 
        title = item.find('h3').text

        item_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemisphere_main_url + item_url)
        item_html = browser.html 
        soup = bs(item_html, 'html.parser')
        img_url = soup.find('div', class_='downloads').find("a")["href"]
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    return hemisphere_image_urls
        
