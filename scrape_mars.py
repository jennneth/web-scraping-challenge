################################################
# Jupyter Notebook Conversion to Python Script
################################################

#Establish Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time

mars_data= {}

################################################
# Setup the browser for Windows
################################################
def init_browser():
    #this functiin initializes the instance of the browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

################################################
# Get the NASA Mars News
################################################
def mars_news(browser):
    #GET THE LATEST MARS NEWS FROM THE NASA WEBPAGE 
    #the URL of the page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    print("finished visit")
    #create beautifulSoup object, parse with html parser
    html = browser.html
    
    print("finished html")
    soup = bs(html,'html.parser')
    #time.sleep(3)
    print("finished soup")
    # results are returned as an iterable list
    results = soup.find_all('li', class_="slide")
    latest_news = results[0]
    news_title = latest_news.find('div', class_="content_title").text
    news_p = latest_news.find("div", class_="article_teaser_body").text
    print("-----------------")
    print(news_title)
    print(news_p)
    #add the title and paragraph to the dictionary
    #mars_data["title"] = news_title
    #mars_data["paragraph"] = news_p
    return news_title, news_p

################################################
# Get the JPL Mars Space Images
################################################    
def jpl_images(browser):
    #the URL of the page to be scraped
    url2="https://www.jpl.nasa.gov/images/"
    base_1="https://www.jpl.nasa.gov"
    browser.visit(url2)
    print("browser.visit(url2)")
    #create beautifulSoup object, parse with html parser
    html2 = browser.html
    soup2 = bs(html2,'html.parser')
    #examine the results
    #print(soup2.prettify())
    # results are returned as an iterable list
    results2= soup2.find_all('div', class_="SearchResultCard")
    first_results = results2[0]
    print(results2)
    extend_url = first_results.find('a')["href"]
    print(extend_url)
    img_url=base_1+extend_url
    print(img_url)
    browser.visit(img_url)
    img_html=browser.html
    soup3=bs(img_html,'html.parser')
    large_image=soup3.find_all('div', class_="BaseImagePlaceholder")
    large=large_image[0]
    print(large)
    featured_image_url=large.find('img')['src']
    print(featured_image_url)
    return featured_image_url

#################################################
# MARS Facts
#################################################  
def mars_facts():
    #the URL of the page to be scraped
    url="https://space-facts.com/mars/"
    browser.visit(url)

    facts_table=pd.read_html(url)[0]
    #print(facts_table)

    #create a header row with the names of the columns
    facts_table.columns=["Attribute", "Mars_Value"]

    #set the index to "attribute"
    facts_table.set_index("Attribute", inplace=True)

    html_table=facts_table.to_html(header=True)


    return html_table

#################################################
# Run all the scraping functions
#################################################    
def scrape_all():
    #this function runs all of the data gathering/scraping
    
    #call the initialize browser function, do this once
    browser = init_browser()
    news_title, news_p = mars_news(browser)
    featured_image_url = jpl_images(browser)
    html_table = mars_facts(browser)
  
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "table":html_table
    }
    browser.quit()
    return mars_data

if __name__ == "__main__":
    print(scrape_all())


    