from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from requests.compat import quote_plus
import bs4
from bs4 import BeautifulSoup
from .import models
from urllib.request import urlopen as opp

BASE_URL = 'https://www.jumia.com.ng/catalog/?q={}'
HOME_URL = 'https://www.jumia.com.ng'

# Create your views here.
def homePage(request):
    response = requests.get('https://www.jumia.com.ng/flash-sales/')
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    listings = soup.find_all('article',{'class':'prd _fb _p col c-prd'})
    final = []
    for post in listings:
        image = post.find('img').get('data-src')
        desc = post.find('h3', class_='name').text
        price = post.find('div', class_='prc').text
        url = 'https://www.jumia.com.ng/'+post.find('a').get('href')
        final.append((image,desc,price,url))
    response2 = requests.get('https://www.jumia.com.ng/mlp-pernod-ricard-store/')
    data2 = response2.text
    soup2 = BeautifulSoup(data2, features='html.parser') 
    listings2 = soup2.find_all('article',{'class':'prd _fb col c-prd'})
    final2 = []
    
    for post2 in listings2:
        image2 = post2.find('img').get('data-src')
        desc2 = post2.find('h3', class_='name').text
        price2 = post2.find('div', class_='prc').text
        url2 = 'https://www.jumia.com.ng/'+post2.find('a').get('href')
        final2.append((image2,desc2,price2,url2))
    context={'final':final, 'final2':final2}
    
    return render(request, 'index.html', context)

    # image = post.article.a.find('img',class_='img' ).get('data-src')
    #     desc = post.article.find('div', class_='name').text
    #     price = post.article.find('div', class_='prc').text
    #     url = 'https://www.jumia.com.ng/'+post.find('a').get('href')

def productsPage(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    fanal_url = BASE_URL.format(quote_plus(search))
    response = requests.get(fanal_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    listings = soup.find_all('article',{'class':'prd _fb col c-prd'})

    final = []
    for post in listings:
        image = post.find('img').get('data-src')
        desc = post.find(class_='name').text
        price = post.find(class_='prc').text
        url = 'https://www.jumia.com.ng/'+post.find('a').get('href')
        final.append((image,desc,price,url))
    context={'find': search, 'final':final}
    return render(request, 'products.html', context)

def newSearch(request):
    search = request.POST['search']
    context={'find': search}
    return render(request, 'test.html', context)

 