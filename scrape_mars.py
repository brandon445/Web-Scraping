from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    listings = {}

    file = "NewsNASAMarsExplorationProgram/News_NASA_Mars_Exploration_Program.html"

    nasa_html = open(file, "r").read()

    soup = bs(nasa_html, "html.parser")

    nasa_news_title = soup.find("div",class_="content_title").text
    nasa_news_paragraph = soup.find("div",class_="article_teaser_body").text.replace("\n","")

    nasa_news_title

    nasa_news_paragraph

# MARS WEATHER--------------------
    mars_twitter = requests.get("https://twitter.com/marswxreport?lang=en").text

    mars_soup = bs(mars_twitter, "html.parser")

    mars_weather = mars_soup.find("div", class_="js-tweet-text-container").text.replace("\n","")

    mars_weather

# MARS FACTS-----------------------
    mars_facts_url = "https://space-facts.com/mars/"

    mars_read_table = pd.read_html(mars_facts_url)

    mars_df = mars_read_table[0]

    mars_final_df = mars_df.to_html().replace("\n","")
    mars_final_df

# MARS HEMISPHERES
    #URL
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    # ----------------------------------------------------------
    browser.visit(mars_hemispheres_url)
    # hemis_html = urlopen(mars_hemispheres_url)
    hemis_html = browser.html
    soup_hemis = bs(hemis_html, "lxml")


    hemis_images = soup_hemis.find_all("div", class_="item")

    for img in hemis_images:
        href = img.find("a", class_="itemLink product-item")
        clicked = base_url + href["href"]
        browser.visit(clicked)
        
        
        hemis_html2 = browser.html
        soup_hemis2 = bs(hemis_html2, "lxml")
        
        href2 = soup_hemis2.find("div", class_="downloads").find("a")["href"]
        title = soup_hemis.find_all("div", class_="description")
        title_called = img.h3.text
        
        #Dictionary calls
        hemisphere_image_urls = []
        dictionary = {}
        dictionary["title"] = title_called
        dictionary["img_url"] = href2
        hemisphere_image_urls.append(dictionary)
        
        print(hemisphere_image_urls)