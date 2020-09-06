from selenium import webdriver
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib
from urllib.parse import urlparse

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
path = 'C:/Users/hp/Desktop/WebScrape/chromedriver.exe'
driver = webdriver.Chrome(executable_path= path, options=options)

url = "https://eapplication.nitrkl.ac.in/nitris/Login.aspx"

driver.get (url)

driver.find_element_by_id("txtUserName").send_keys("716ec5071")
time.sleep(1)
print("1")
driver.find_element_by_id ("txtPassword").send_keys("")
time.sleep(1)                          
print("2")
driver.find_element_by_id("btnLogin").click()
time.sleep(5)
print("Done 1")

page_source = driver.page_source

msg_url = "https://eapplication.nitrkl.ac.in/nitris/Student/Home/AllMessages.aspx"
driver.get (msg_url)

view_elem = []
view_elem = driver.find_elements_by_class_name("Deletebuttonstyle")
count = len(view_elem)
#view_elem = [link.get_attribute("href") for link in driver.find_elements_by_class_name("Deletebuttonstyle")]

time.sleep(5)
print("Done 2")

#count = 0
problem = []
for i in range(2):
#    if count == 1:
#        break
    driver.get (msg_url)
    
    view_elem = []
    view_elem = driver.find_elements_by_class_name("Deletebuttonstyle")

    temp = view_elem[i].click()
    msg_source = driver.page_source
    
    msg_soup = soup(msg_source, "html.parser")
    
    save_path = "C:/Users/hp/Desktop/WebScrape/NITRIS/Nsub/"
    replace_path = "https://eapplication.nitrkl.ac.in/nitris"
    try:
    href = msg_soup.find("a", {"class" : "Editbuttonstyle"})["href"].replace("../..", replace_path)
    sub = msg_soup.find("span", {"id" : "ContentPlaceHolder2_lblSubject"}).text.replace(":", ",")
    dwnld_path = save_path + sub + href[-4:]
    if not urlparse(href).scheme:
        href = 'http://' + href
    urllib.request.urlretrieve(href, dwnld_path)
    print("Downloaded with pdf")
#        driver.execute_script("window.history.go(-1)")
#        time.sleep(3)
#        driver.execute_script("window.history.go(-1)")
#        time.sleep(3)
        # if(".rar" == href[-4:]):
        #     with open("1.zip", "wb") as code:
        #         code.write(r.content)
    print("done")
    except:
        print("You got no attachments!!")
        problem.append(i+1)    
        pass
    print(i+1)
print(problem)