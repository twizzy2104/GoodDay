# -*- coding: utf-8 -*-
import requests
from lxml import html
import tweepy

from django.shortcuts import render
from enjoy_app.forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request,'enjoy_app/index.html')
@login_required
def transports(request):
    return render(request,'enjoy_app/transports.html')


def registration(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'enjoy_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

#
@login_required
def special(request):
    return HttpResponse("You are logged in, Nice !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('enjoy_app:user_login'))


@login_required
def meteo(request):
    url_meteo = 'https://www.tameteo.com/meteo_Choisy+le+Roi-Europe-France-Val+de+Marne--1-24815.html'
    session = requests.Session()
    result = session.get(url_meteo)

    tree = html.fromstring(result.content)
    temperature = tree.xpath('//span[@class="dato-temperatura changeUnitT"]/text()')[0]
    temperature_sensation = tree.xpath('//span[@class="sensacion changeUnitT"]/strong/text()')[0]
    description = tree.xpath('//span[@class="proximas-horas"]/text()')[0]
    ville = tree.xpath('//h1[@class="titulo"]/text()')[0]
    dico_meteo = {'ville':ville,'temperature':temperature,'description':description,'temperature_ressenti':temperature_sensation}

    return render(request,'enjoy_app/meteo.html',dico_meteo)


@login_required
def horoscope(request) :

    url_taureau ='http://www.sympatico.ca/horoscope/traditionnel/Taureau-1.1478042'
    session = requests.Session()
    result = session.get(url_taureau)

    tree = html.fromstring(result.content)
    texte_horo = tree.xpath("//div[@class='txt short_description']/p/text()")[1].encode('utf-8')
    texte_horo=texte_horo.decode('utf-8')

    image_taureau = 'http://www.sympatico.ca/img/sympatico/horoscope/traditionnel/taureau.png'
    horo_dict = {'image':image_taureau,'description':texte_horo}
    return render(request,'enjoy_app/horoscope.html',horo_dict)



@login_required
def rerc(request):

    import tweepy

    auth = tweepy.OAuthHandler('2AdSRso0UdW3cMlwPDoRD8QG2','pKO1t67v79M5tfbsEVcJxG6HsZ0E4mM0QRX1edPpCFpNem9JJS')
    auth.set_access_token('882928972585201664-l9yHYp3rvKOxycghUwDBNdz0PHCCVMA','IsKxhlIW8JdGaxLU7u0tbb7hhGyjR4u8Wt9lDbNtGriO3')

    api = tweepy.API(auth)

    lst_rerc =[]
    dico_build = {}
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='@rerc_sncf', tweet_mode='extended').items(50):
    	# lst_rerc.append(tweet.full_text)
        dico_build[tweet.id]=[tweet.created_at,tweet.full_text]

    dico_rerc = {'rerc':dico_build}

    return render(request,'enjoy_app/rerc.html',dico_rerc)




@login_required
def rera(request):

    import tweepy

    auth = tweepy.OAuthHandler('2AdSRso0UdW3cMlwPDoRD8QG2','pKO1t67v79M5tfbsEVcJxG6HsZ0E4mM0QRX1edPpCFpNem9JJS')
    auth.set_access_token('882928972585201664-l9yHYp3rvKOxycghUwDBNdz0PHCCVMA','IsKxhlIW8JdGaxLU7u0tbb7hhGyjR4u8Wt9lDbNtGriO3')

    api = tweepy.API(auth)

    lst_rerc =[]
    dico_build = {}
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='@RER_A', tweet_mode='extended').items(50):
    	# lst_rerc.append(tweet.full_text)
        dico_build[tweet.id]=[tweet.created_at,tweet.full_text]

    dico_rera = {'rera':dico_build}

    return render(request,'enjoy_app/rera.html',dico_rera)


@login_required
def m14(request):

    import tweepy

    auth = tweepy.OAuthHandler('2AdSRso0UdW3cMlwPDoRD8QG2','pKO1t67v79M5tfbsEVcJxG6HsZ0E4mM0QRX1edPpCFpNem9JJS')
    auth.set_access_token('882928972585201664-l9yHYp3rvKOxycghUwDBNdz0PHCCVMA','IsKxhlIW8JdGaxLU7u0tbb7hhGyjR4u8Wt9lDbNtGriO3')

    api = tweepy.API(auth)

    dico_build = {}
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='@Ligne14_RATP', tweet_mode='extended').items(50):
    	# lst_rerc.append(tweet.full_text)
        dico_build[tweet.id]=[tweet.created_at,tweet.full_text]

    dico_m14 = {'m14':dico_build}

    return render(request,'enjoy_app/m14.html',dico_m14)


@login_required
def news(request):

    import requests
    from lxml import html

    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?hl=fr&gl=FR&ceid=FR%3Afr"
    session = requests.Session()
    result = session.get(url)
    tree = html.fromstring(result.content)

    articles =tree.xpath('//div[@class="NiLAwe mi8Lec  gAl5If jVwmLb Oc0wGc R7GTQ keNKEd j7vNaf nID9nc"]')

    dico_news = {}
    dico={}

    for article in articles :
        url = article.xpath('.//article/a/@href')[0]
        titre = article.xpath('.//a/text()')[0]
        image = article.xpath('.//figure/img/@src')[0]
        url = url.replace('./',"https://news.google.com/")

        dico[url] = [titre,image]
    dico_news['news']=dico

    return render(request,'enjoy_app/news.html',dico_news)




@login_required
def base(request):
    return render(request,'enjoy_app/base.html')


@login_required
def accueil(request):
    return render(request,'enjoy_app/accueil.html')


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('enjoy_app:accueil'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'enjoy_app/login.html', {})
