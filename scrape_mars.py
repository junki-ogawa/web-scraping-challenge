from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd
import requests
from flask import Flask, render_template
import time

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

mars = db.mars

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dictionary = {}

#news title and paragraph text
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_object = soup.select_one('div.list_text')
    mars_dictionary["news_title"] = news_object.find('div', class_='content_title').get_text()
    mars_dictionary["news_p"] = news_object.find('div', class_='article_teaser_body').get_text()

#mars image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_url = soup.find('img', class_='headerimage')
    featured_img_url = img_url.attrs['src']
    mars_dictionary["featured_img_url"] = url + featured_img_url

#mars table
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(mars_facts_url)
    mars_table = table[1]
    mars_table.columns = ["Mars Profile", "Measure"]
    mars_table.to_html()
    mars_dictionary["mars_table"] = mars_table.to_html().replace("\n","")
    
#mars hemispheres
    hemisphere_image_urls = []
    url1 = ('https://marshemispheres.com/cerberus.html')
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    cerberus_img = soup.find('div', class_='downloads')
    cerberus_img = soup.find('a', href='images/full.jpg')
    cerberus_img = cerberus_img.attrs['href']
    cerberus_img = 'https://marshemispheres.com/' + cerberus_img
    cereberus_object = soup.find('div', class_='cover')
    cerberus_title = cereberus_object.find('h2').get_text()
    cerb = {'title':cerberus_title,'img_url':cerberus_img}
    hemisphere_image_urls.append(cerb)

    url2 = ('https://marshemispheres.com/schiaparelli.html')
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    schiaparelli_img = soup.find('div', class_='downloads')
    schiaparelli_img = soup.find('a', href='images/schiaparelli_enhanced-full.jpg')
    schiaparelli_img = schiaparelli_img.attrs['href']
    schiaparelli_img = 'https://marshemispheres.com/' + schiaparelli_img
    schiaparelli_object = soup.find('div', class_='container')
    schiaparelli_title = schiaparelli_object.find('h2').get_text()
    schia = {'title':schiaparelli_title,'img_url':schiaparelli_img}
    hemisphere_image_urls.append(schia)

    url3 = ('https://marshemispheres.com/syrtis.html')
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    syrtis_img = soup.find('div', class_='downloads')
    syrtis_img = soup.find('a', href='images/syrtis_major_enhanced-full.jpg')
    syrtis_img = syrtis_img.attrs['href']
    syrtis_img = 'https://marshemispheres.com/' + syrtis_img
    syrtis_title = soup.find('h2', class_='title').get_text()
    syrtis = {'title':syrtis_title,'img_url':syrtis_img}
    hemisphere_image_urls.append(syrtis)

    url4 = ('https://marshemispheres.com/valles.html')
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    valles_img = soup.find('div', class_='downloads')
    valles_img = soup.find('a', href='images/valles_marineris_enhanced-full.jpg')
    valles_img = valles_img.attrs['href']
    valles_img = 'https://marshemispheres.com/' + valles_img
    valles_title = soup.find('h2', class_='title').get_text()
    valles = {'title':valles_title,'img_url':valles_img}
    hemisphere_image_urls.append(valles)

    mars_dictionary["hemisphere_image_urls"] = hemisphere_image_urls

    # Quit the browser
    browser.quit()
    print(mars_dictionary)
    return mars_dictionary

    # mars.insert_one(mars_dictionary)
scrape()