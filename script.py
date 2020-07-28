from bs4 import BeautifulSoup
import  requests
import  csv

data = open("fathers-day.csv","w",encoding='utf8')
dataWriter = csv.writer(data)
dataWriter.writerow(['Title','Category','Price','Rating','URL','Description'])

# i have used html for men and women seperated since the are defferentiated in the website but the will b inserted in the same table
url='https://www.hediyehanem.com/babaya-hediye/'
productsCounter=0
pageCounter=1
while True:
    pageurl=url+'?page='+str(pageCounter)
    pagehtml=requests.get(pageurl).text
    pagesoup=BeautifulSoup(pagehtml,'html.parser')
    products = pagesoup.find_all('div', {"class": "product-item"})
    if len(products) == 0:
        break
    for product in products:
        itemurl=product.find('a').get('href')
        productHtml=requests.get(itemurl).text
        productSoup=BeautifulSoup(productHtml,"html.parser")
        title=productSoup.find('div',{"class":"product-name"}).find("h1").text.strip()
        category=productSoup.find('div',{'class':'breadcrumbs-container'}).find('div',{"class":"container"}).find('ol').find_all('li')[1].text.strip()
        try:
            price=productSoup.find('div',{'itemprop':'price'}).get('content')
        except:
            price="out of stock"
        rating= productSoup.find('div', {"id": "rating"}).get('data-score')
        if int(rating) == 0:
            rating = "product has not been rated yet"
        try:
            description=productSoup.find('div',{'class':'details'}).text.strip()
        except:
            description="description is not available"
        dataWriter.writerow([title,category,price,rating,itemurl,description])
        productsCounter=productsCounter+1
        print("page counter:", productsCounter)
    pageCounter = pageCounter + 1
    print(pageCounter)
    if productsCounter >= 1000:
        break
data.close()