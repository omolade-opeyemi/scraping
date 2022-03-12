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
    
    #final_url = opp(HOME_URL)
    #page = final_url.read() 
    response = requests.get('https://www.jumia.com.ng')
    data = response.text
    #soup = BeautifulSoup(data, features='html.parser')
    #data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    listings = soup.find_all('div',{'class':'itm col'})

    final = []
    for post in listings:
        image = post.find('img',class_='img' ).get('data-src')
        desc = post.find('div', class_='name').text
        price = post.find('div', class_='prc').text
        url = 'https://www.jumia.com.ng/'+post.find('a').get('href')
        final.append((image,desc,price,url))
    context={'final':final}
    return render(request, 'index.html', context)

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

 