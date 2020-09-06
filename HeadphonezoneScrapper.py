import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
from selenium import webdriver
import time
import pickle
import re
import os

my_url = "https://www.headphonezone.in/collections/wireless-bluetooth-headphones"
main_url = "https://www.headphonezone.in"

uClient_home = uReq(main_url)
page_html_home = uClient_home.read()
uClient_home.close()

page_home = soup(page_html_home, "html.parser")

href_home = page_home.findAll("a", {"class" : "outer_img"})

cats_href = []
for hrefs in href_home:
    cats_href.append(hrefs["href"])
    
parent_home = page_home.findAll("a", {"class" : "outer_img"})

parent = []
p_counter = 0
for p_name in parent_home:
    parent.append(p_name.div["class"])
    parent[p_counter] = parent[p_counter][0]
    p_counter += 1

main_dict = dict()

main_counter = 0
home_link = cats_href[main_counter]

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
path = 'C:/Users/USER/Desktop/ALLEARS/WebScrape/chromedriver.exe'
driver = webdriver.Chrome(executable_path= path, options=options)

#df_new = pd.read_pickle('C:/Users/USER/Desktop/randi/df.pkl')


uClient = uReq(home_link)
page_html = uClient.read()
uClient.close()

page_init = soup(page_html, "html.parser")

number = page_init.find("div", {"class" : "eight columns breadcrumb_text"}).text.split('/')[-1][-1]

driver.get(home_link)

for num in range(int(number) - 1):
    more_buttons = driver.find_elements_by_class_name("bc-sf-filter-load-more-button")
    driver.execute_script("arguments[0].click();", more_buttons[0])
    time.sleep(8)
    print("Loop", num)
    
page_source = driver.page_source

page_soup = soup(page_source, "html.parser")
#    page_source_bang = page_soup.prettify()
#Titles
titles_class = page_soup.findAll("span", {"class" : "title"})
titles = []

for title in titles_class:
    titles.append(title.text.replace(" ", ""))

#HREF
href_class = page_soup.findAll("a", {"class" : "product-info__caption"})
href = []
for hrefs in href_class:
    href.append(hrefs["href"])
    
df_new = pd.DataFrame(list(zip(titles, href)), columns =['Name','Links'])

#df_new = df

prices = []
stars = []

main_count = 0
#This loop is for getting reviews and prices
for (link, prod_name) in zip(df_new["Links"], df_new["Name"]):
#    if main_count > 3:
#        break
    
    link_ind = main_url + link
    
    uClient_ind = uReq(link_ind)
    page_html_ind = uClient_ind.read()
    uClient_ind.close()
    
    page_soup_ind = soup(page_html_ind, "html.parser")
    
    try:
        price = page_soup_ind.find("span", {"itemprop" : "price"})["content"]
        prices.append(price)
    except:
        prices.append("NA")

    try:
        star = page_soup_ind.find("span", {"class" : "jdgm-prev-badge__stars"})["data-score"]
        stars.append(star)
    except:
        stars.append("NA")
        
#    main_count += 1
        
    page_clean = page_soup_ind.prettify()
    item_id_search = re.search(r'product_gallery_nav product-(\d+)', page_clean, re.IGNORECASE)
    item_id = item_id_search.group().split("-")[1]
    
    class_name = "product_gallery_nav product-" + item_id + "-gallery-nav"
    pic_home = page_soup_ind.findAll("div", {"class" : class_name})
    list_div = pic_home[0].findAll("div")
    
    img_srcs = []
    data_variants = []
    for src in list_div:
        img_srcs.append("https:" + src.img["srcset"])
        if (src.img["data-variant"]).find("/") != -1:
            data_variants.append("NA")
        else:
            data_variants.append(src.img["data-variant"])
        
    count = 0 
    #a = 1   
    for (img_link, color) in zip(img_srcs, data_variants):
        save_path = "C:/Users/USER/Desktop/ALLEARS/WebScrape/Images/"
        save_path += prod_name + "/"
        print(save_path)
    
        try:
            os.mkdir(save_path)
        except:
            print("Exception in creating prod folder!!")
            pass
        
        save_path += color + "/"
        try:
            os.mkdir(save_path)
        except:
            print("Exception in creating variant folder!!")
            pass
            
        dwnld_path = save_path + "img" + str(count) + ".jpg"
        urllib.request.urlretrieve(img_link, dwnld_path)
        
        count += 1
        print("Downloaded and Saved", count)

    print("Loop done", main_count)
    main_count += 1
    
df_new["Price"] = prices
df_new["Rating"] = stars    


#This loop is for product specs

audio = []
control = []
design = []
main_count = 0

problem = []    

for (link,name) in zip(df_new["Links"], df_new["Name"]):
#    if main_count > 1:
#        break
    
    link_ind = main_url + link + "#specs"
    
    uClient_ind = uReq(link_ind)
    page_html_ind = uClient_ind.read()
    uClient_ind.close()
    
    page_soup_ind = soup(page_html_ind, "html.parser")
    
    specs = page_soup_ind.findAll("div", {"class" : "eight columns table-content"})
    print(len(specs))    
    acd = [False, False, False]
    
    inner_count = 0
    a_table = -1
    c_table = -1
    d_table = -1
    
    for main_name in specs:
        try:
            if main_name.strong.text.find("SPECIFICATION") != -1:
                acd[0] = True
                a_table = inner_count
        
            if main_name.strong.text.find("CONTROL") != -1:
                acd[1] = True
                c_table = inner_count
        
            if main_name.strong.text.find("DESIGN") != -1:
                acd[2] = True
                d_table = inner_count
                
            inner_count += 1
        except:
            problem.append(name)
            pass
    
    print(acd)
#    visited = [False, False, False]
    
#    for main_name in specs:
    if acd[0] == True:
        a_specs = specs[a_table].table.tbody.findAll("td")
        count = 0
        cols = []
        a_spec_list = []
        for i in a_specs:
            cols.append(i.text) if count % 2 == 0 else a_spec_list.append(i.text.replace("\n", ""))
            count += 1

        a_spec_df = dict()
            
        for i in range(len(cols)):
            a_spec_df[cols[i]] = a_spec_list[i]
        
        audio.append(a_spec_df)
        print("if a", main_count)
#        visited[0] = True

    elif acd[0] == False:
        audio.append("NA")
        print("elif a", main_count)
#        visited[0] = True
        

    if acd[1] == True:
        c_specs = specs[c_table].table.tbody.findAll("td")
        count = 0
        cols = []
        c_spec_list = []
        for i in c_specs:
            cols.append(i.text) if count % 2 == 0 else c_spec_list.append(i.text.replace("\n", ""))
            count += 1

        c_spec_df = dict()
            
        for i in range(len(cols)):
            c_spec_df[cols[i]] = c_spec_list[i]
    
        control.append(c_spec_df)
        print("if c", main_count)
#        visited[1] = True

    elif acd[1] == False:
        control.append("NA")
        print("elif c", main_count)
#        visited[1] = True

    if acd[2] == True:
        d_specs = specs[d_table].table.tbody.findAll("td")
        count = 0
        cols = []
        d_spec_list = []
        for i in d_specs:
            cols.append(i.text) if count % 2 == 0 else d_spec_list.append(i.text.replace("\n", ""))
            count += 1

        d_spec_df = dict()
            
        for i in range(len(cols)):
            d_spec_df[cols[i]] = d_spec_list[i]
    
        design.append(d_spec_df)
        print("if d", main_count)
#        visited[2] = True

    elif acd[2] == False:
        design.append("NA")
        print("elif d", main_count)
#        visited[2] = True
            
    print("Successfully completed!!")
    main_count += 1

df_new["Audio_specs"] = audio
df_new["Control"] = control
df_new["Design"] = design

main_dict[parent[main_counter]] = df_new

path_temp = 'C:/Users/USER/Desktop/ALLEARS/WebScrape/main_scrape_' + parent[main_counter] + '.pickle'

with open(path_temp, 'wb') as handle:
    pickle.dump(main_dict, handle)
    
print("MAIN_LOOP_DONE", main_counter)
main_counter += 1

#with open('C:/Users/USER/Desktop/ALLEARS/WebScrape/filename.pickle', 'rb') as handle:
#    b = pickle.load(handle)#df_new.to_pickle('C:/Users/USER/Desktop/ALLEARS/WebScrape/df.pkl')
