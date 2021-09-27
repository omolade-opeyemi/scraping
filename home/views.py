from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from .import models

BASE_URL = 'https://www.jumia.com.ng/catalog/?q={}'
HOME_URL = 'https://www.jumia.com.ng/'

# Create your views here.
def homePage(request):
    
    fanal_url = HOME_URL
    response = requests.get(fanal_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    listings = soup.find_all('article',{'class':'prd _box _hvr'})

    final = []
    for post in listings:
        image = post.find('img').get('data-src')
        desc = post.find(class_='name').text
        price = post.find(class_='prc').text
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

 