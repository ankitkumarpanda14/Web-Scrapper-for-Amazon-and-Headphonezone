from bs4 import BeautifulSoup
import requests
import pandas as pd


with open('Amazon.html',encoding = "utf8") as html_file:
    soup = BeautifulSoup(html_file,'lxml');

itemName = []
itemPrice = []
itemStarRating = []

for itemNameClass in soup.find_all('span',class_='a-size-base-plus a-color-base a-text-normal'):

    itemNametext = itemNameClass.text
    itemName.append(itemNametext)
    

for itemPriceClass in soup.find_all('span',class_ = 'a-price-whole'):
    itemPricetext = itemPriceClass.text
    itemPrice.append(itemPricetext)
    
for itemStarRatingClass in soup.find_all('span',class_='a-icon-alt'):
    itemStarRatingtext = itemStarRatingClass.text
    itemStarRating.append(itemStarRatingtext)
    
itemStarRating = itemStarRating[4:]
itemStarRating = [x for x in itemStarRating if x!= 'Next']
print(itemName)
print()
print(itemPrice)
print()
print(itemStarRating)


#df = pd.DataFrame(list(zip(itemName, itemPrice,itemStarRating)), columns =['Name', 'Value','Star Rating'])
#print(df)
#df.to_csv('AmazonGroceryProducts.csv')
