from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import PostReview, Search
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import  MyList, Review, KeyWords, Description
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustomUser

from django.db.models import Q

from django.core.paginator import Paginator

from django.http import JsonResponse

from django.views import generic

from dictknife import deepmerge

import requests
import urllib.parse
import os
from django.http import Http404

TMDB_TOKEN = os.environ.get("TMDB_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": TMDB_TOKEN
}

#一覧に表示させる種類リスト(これに含めないものは表示させない。)
genres = ["now_playing", "upcoming"]

genresLists = requests.get("https://api.themoviedb.org/3/genre/movie/list?language=ja", headers=headers).json().get("genres")

keywords = ""
descriptionContent = ""

def __init__(self,):
    try:
        if Description.objects.filter().exists():
            descriptionContent = str(Description.objects.get().description)

        if KeyWords.objects.filter().exists():
            keywords = str(KeyWords.objects.get().keywords)
    except ObjectDoesNotExist:
        pass


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect("movies")


class movies(View):
    def get(self, request, *args, **kwargs):
        request.session['TempPage'] = request.build_absolute_uri()
        
        movie_id=kwargs.pop('movie_id', None)

        modal = False
        adult = "False"
        video = ""
        credits = ""
        similars = ""
        review_rate = ""
        feature = False
        movies = []

        url = "https://api.themoviedb.org/3/movie/now_playing?language=ja&page=1"
        playing = requests.get(url, headers=headers).json().get("results")

        url = "https://api.themoviedb.org/3/movie/top_rated?language=ja&page=1"
        response = requests.get(url, headers=headers)
        j = response.json()

        
        url = "https://api.themoviedb.org/3/movie/popular?language=ja&page=1"
        popular = requests.get(url, headers=headers).json().get("results")

        url = "https://api.themoviedb.org/3/movie/upcoming?language=ja&page=1"
        upcoming = requests.get(url, headers=headers).json().get("results")

        for up in upcoming:
            upId = up["id"]
            url = f"https://api.themoviedb.org/3/movie/{upId}/videos?language=ja"
            results = requests.get(url, headers=headers).json().get("results")
            
            if len(results) != 0:
                if results[0]["site"] in "YouTube":
                    banner = results[0]
                break
            
        result = j.get("results")
        reviews = Review.objects.all()

        mylist = MyList.objects.filter(user__id=request.user.id).all().order_by('-created')[:20]
            
        for list in mylist:
            url = f"https://api.themoviedb.org/3/movie/{list.movie_id}?language=ja"
            movie = requests.get(url, headers=headers).json()

            movies.append({
                            "movie_id": movie.get("id"), 
                            "title": movie.get("title"), 
                            "overview": movie.get("overview"), 
                            "poster_path": movie.get("poster_path")
                    }
                    )

        context={
            "genresLists": genresLists,
            "Description": descriptionContent,
            "Keywords": keywords,

            "upcoming": upcoming,
            "banner": banner,
            "playing": playing,
            "results": result,
            "popular": popular,
            "modal": modal,
            "reviews": reviews,
            "video": video,
            "casts": credits,
            "similars": similars,
            "review_rate": review_rate,
            "mylists": movies,
            "feature": feature,

            "movie_id": movie_id
        }
        return render(request, 'app/movies/movies.html', context)
    
    def post(self, request, *args, **kwargs):
        word = urllib.parse.quote(self.request.POST.get('word'))
        adult = "false"
        language = "ja"
        url = f"https://api.themoviedb.org/3/search/movie?query={word}&include_adult={adult}&language={language}&page=1"

        response = requests.get(url, headers=headers)
        j = response.json()
        searchResults = j.get("results")
        
        
        context={
            'searchResults': searchResults,
            "genresLists": genresLists,
        }
        return render(request, 'app/movies/movies.html', context)


class genres(View):
    def get(self, request, *args, **kwargs):
        
        request.session['TempPage'] = request.build_absolute_uri()

        genre_id = self.kwargs['genre_id']
        modal = False
        adult = "False"
        video = ""
        credits = ""
        similars = ""
        review_rate = ""
        genreName = ""
        
        if genre_id != None:
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video=true&language=ja&page=1&sort_by=popularity.desc&with_genres={genre_id}"
            feature = requests.get(url, headers=headers).json().get("results")

        reviews = Review.objects.all()
        for id in genresLists:
            if (id["id"] == genre_id):
                genreName = id["name"]
                break

        context={
            "genresLists": genresLists,
            "Description": descriptionContent,
            "Keywords": keywords,

            "genre_id": genre_id,
            "modal": modal,
            "reviews": reviews,
            "video": video,
            "casts": credits,
            "similars": similars,
            "review_rate": review_rate,
            "feature": feature,
            "genreName": genreName
        }
        return render(request, 'app/movies/genre.html', context)


class ReviewPost(View):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        movie_id=self.kwargs['movie_id']
        
        Review_Data = Review.objects.filter(Q(author_id=user_id) & Q(movie_id=movie_id))
        
        if Review_Data.count() > 0:
            return redirect("review_edit", id=Review_Data[0].id)
        else:
            # movie_id = request.GET.get("movie_id")
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ja"
            
            movie = requests.get(url, headers=headers).json()

            
            form = PostReview(request.GET or None)
            
            context={
                'genresLists': genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,
                'form': form,
                'movie': movie
            }
            return render(request, "app/review/review_post.html", context)
    
    def post(self, request, *args, **kwargs):
        movie_id=self.kwargs['movie_id']
        rate = request.POST['rate']
        
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ja"
        
        movie = requests.get(url, headers=headers).json()

        if not(1 <= int(rate) <=5):
            raise ValueError('評価基準がおかしい。')
        
        form = PostReview(request.POST or None)
        if form.is_valid():
            spoiler = form.cleaned_data['spoiler']
            publish = form.cleaned_data['publish']
            if spoiler != True:
                spoiler = False
                
            if publish != False:
                publish = True

            obj = Review(
                author=request.user, movie_id=movie_id,
                title=form.cleaned_data['title'], 
                content=form.cleaned_data['content'],
                spoiler=spoiler,
                like=rate,
                publish=publish,
                updated= timezone.now(),
                )

            obj.save()
            return redirect('movies')
        else:
            if form.is_valid() == False:
                for ele in form :
                    print(ele)

        context={
            'form': form
            # 'Item': item_data
        }
        # return render(request, "app/review_check.html", context)
        # return render(request, "app/review/review_post.html", context)
        return redirect(request.session['TempPage'])

class ReviewSuccess(View):
    def get(self, request, *args, **kwargs):
        UserName = CustomUser.objects.get(id=request.user.id)
        context = {
            'User': UserName.first_name
        }
        return render(request, "app/review/review_success.html", context)

class ReviewList(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            movies = []
            request.session['TempPage'] = request.build_absolute_uri()
            
            review_data = Review.objects.filter(Q(author_id=request.user.id)).all().order_by('-updated')

            paginator = Paginator(review_data, 10)
            p = request.GET.get('p')
            review_data = paginator.get_page(p)
            for result in review_data:
                url = f"https://api.themoviedb.org/3/movie/{result.movie_id}?language=ja"
                movie = requests.get(url, headers=headers).json()
                movies.append({
                                "movie_id": movie.get("id"), 
                                "title": movie.get("title"), 
                                "overview": movie.get("overview"), 
                                "poster_path": movie.get("poster_path")
                        }
                        )
            
            context={
                'Reviews': review_data,
                'genresLists': genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,
                "movies": movies
            }
            return render(request, 'app/review/review_list.html', context)
        else:
                response = redirect('Index')
                return response


class ReviewEdit(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            user_id = request.user.id
            review_id = self.kwargs['id']

            Review_Data = Review.objects.filter(Q(author_id=user_id) & Q(id=review_id))
            
            url = f"https://api.themoviedb.org/3/movie/{Review_Data[0].movie_id}?language=ja"
            movie = requests.get(url, headers=headers).json()


            form = PostReview(request.GET or None)
            if Review_Data.count() > 0:
                form = PostReview(
                request.GET or None,
                initial = {
                    'title': Review_Data.last().title,
                    'content': Review_Data.last().content,
                    'spoiler': Review_Data.last().spoiler,
                    'publish': Review_Data.last().publish,
                    })
            else:
                redirect("movies")
        
            context={
                'genresLists': genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,
                'movie': movie,
                'form': form
            }
            return render(request, 'app/review/review_edit.html', context)
        else:
                response = redirect('Index')
                return response
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_id = request.user.id
            review_id = self.kwargs['id']
            review_data = Review.objects.filter(Q(author_id=user_id) & Q(id=review_id)).last()
        
            rate = request.POST['rate']
            
            
            form = PostReview(request.POST or None)

            if form.is_valid():
                spoiler = form.cleaned_data['spoiler']
                publish = form.cleaned_data['publish']
                if spoiler != True:
                    spoiler = False
                if publish != False:
                    publish = True
                
                review_data.title = form.cleaned_data['title']
                review_data.content = form.cleaned_data['content']
                review_data.spoiler = spoiler
                review_data.like = rate
                review_data.publish = publish
                review_data.updated = timezone.now()
                review_data.save()

            return redirect(request.session['TempPage'])
        else:
                response = redirect('Index')
                return response

class ReviewDelete(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            user_id = request.user.id
            review_id = self.kwargs['id']
            review_data = Review.objects.filter(Q(author_id=user_id) & Q(id=review_id))


            if review_data.count() > 0:
                review_data.last().delete()
            else:
                # return redirect("review_list")
                return redirect(request.session['TempPage'])
            # return redirect("review_list")
        
            return redirect(request.session['TempPage'])
        
        else:
            # return redirect("review_list")
            
            return redirect(request.session['TempPage'])


class ReviewMenuView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            request.session['TempPage'] = request.build_absolute_uri()
            return render(request, 'app/review/review_menu.html')
        else:
                response = redirect('Index')
                return response


class MyListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            mylist = MyList.objects.filter(user__id=request.user.id).all().order_by('-created')
            
            request.session['TempPage'] = request.build_absolute_uri()
            paginator = Paginator(mylist, 20)
            mylist = paginator.get_page(1)

            movies = []
            for list in mylist:
                url = f"https://api.themoviedb.org/3/movie/{list.movie_id}?language=ja"
                movie = requests.get(url, headers=headers).json()

                movies.append({
                                "movie_id": movie.get("id"), 
                                "title": movie.get("title"), 
                                "overview": movie.get("overview"), 
                                "poster_path": movie.get("poster_path")
                        }
                        )
                
            context={
                "genresLists": genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,
                "movies": movies
            }
            return render(request, 'app/movies/mylist.html', context)
        else:
                return redirect('Index')

def MyListAdd(request):
    if request.user.id:
        movie_id = request.POST.get('movie_id')
        status = ""
        mylist = MyList.objects.filter(Q(user_id=request.user.id) & Q(movie_id=movie_id)).all()
        if mylist.count() == 0:
            obj = MyList(
                user_id=request.user.id,
                movie_id=movie_id
            )
            obj.save()
            status = "True"
        else:
            mylist.delete()
            status = "False"

        d = {
            "status": status
        }

        return JsonResponse(d)
    else:
        status = "login"
        d = {
            "status": status
        }

        return JsonResponse(d)
    # return redirect("movies")


class PlayingView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            request.session['TempPage'] = request.build_absolute_uri()

            url = "https://api.themoviedb.org/3/movie/now_playing?language=ja&page=1"
            playing = requests.get(url, headers=headers).json().get("results")

            context={
                "genresLists": genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,

                'lists': playing,
                "movies": movies,
                "genre_name": "now_playing"
            }
            return render(request, 'app/movies/list.html', context)
        else:
                response = redirect('movies')
                return response


class UpcomingView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            
            request.session['TempPage'] = request.build_absolute_uri()

            url = "https://api.themoviedb.org/3/movie/upcoming?language=ja&page=1"
            upcoming = requests.get(url, headers=headers).json().get("results")

            context={
                
                "genresLists": genresLists,
                "Description": descriptionContent,
                "Keywords": keywords,

                'lists': upcoming,
                "movies": movies,
                "genre_name": "upcoming"
            }
            return render(request, 'app/movies/list.html', context)
        else:
                response = redirect('movies')
                return response


def scroll(request):
    page = request.GET.get('page')
    genre = request.GET.get('genre')

    url = f"https://api.themoviedb.org/3/movie/{genre}?language=ja&page={page}"
    results = requests.get(url, headers=headers).json().get("results")

    
    d = {
        "results": results,
    }

    return JsonResponse(d)
    # else:
    #     return "Failed"

def upcomingScroll(request):
    page = request.GET.get('page')
    genre = request.GET.get('genre')
    url = f"https://api.themoviedb.org/3/movie/upcoming?language=ja&page={page}"
    results = requests.get(url, headers=headers).json().results.get("results")

    d = {
        "results": results
    }

    return JsonResponse(d)

def genreScroll(request):
    page = request.GET.get('page')
    id = request.GET.get('genre_id')
    adult = "false"
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video=true&language=ja&page={page}&sort_by=popularity.desc&with_genres={id}"
    results = requests.get(url, headers=headers).json()
    genres = results.get("results")
    d = {
        "genres": genres
    }

    return JsonResponse(d)

def mylistScroll(request):
    switch = "true"
    page = request.GET.get('page')
    page_cnt = 20
    movies = []

    mylistDB = MyList.objects.filter(user__id=request.user.id).all().order_by('-created')
    count = (mylistDB.count() - ((int(page) - 1) * page_cnt))

    paginator = Paginator(mylistDB, page_cnt)
    mylistPaginator = paginator.get_page(page)
    
    if count > 0:
        for list in mylistPaginator:
            url = f"https://api.themoviedb.org/3/movie/{list.movie_id}?language=ja"
            movie = requests.get(url, headers=headers).json()

            movies.append({
                            "movie_id": movie.get("id"), 
                            "title": movie.get("title"), 
                            "overview": movie.get("overview"), 
                            "poster_path": movie.get("poster_path")
                    }
                    )
    else:
        switch = "false"
        
    if (not(mylistDB.count() - ((int(page)) * (page_cnt + 1))) > 0):
        switch = "false"

    d = {
        "movies": movies,
        "switch": switch
    }

    return JsonResponse(d)


def modal(request):
    movie_id = request.GET.get('movie_id')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ja"
    modal = requests.get(url, headers=headers).json()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=ja"
    videos = requests.get(url, headers=headers).json().get("results")
    video = ""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?language=ja&page=1"
    
    similars = requests.get(url, headers=headers).json().get("results")

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ja"
    credits = requests.get(url, headers=headers).json().get("cast")
    for video in videos:
        if (video["type"] == "Trailer") : #& video["official"] == True
            video = video["key"]
            break
    
    
    rc = 0
    review_rate = Review.objects.filter(movie_id=movie_id).all()
    if review_rate.count() > 0:
        for rate in review_rate:
            rc += rate.like
        review_rate = round(rc / review_rate.count(), 1)
    else:
        review_rate = 0

    status = "False"
    mylist = MyList.objects.filter(Q(user_id=request.user.id) & Q(movie_id=movie_id)).all()
    if mylist.count() > 0:
        status = "True"

    d = {
        "modal": modal,
        # "reviews": reviews,
        "video": video,
        "casts": credits,
        "similars": similars,
        "review_rate": review_rate,
        "status": status
    }

    return JsonResponse(d)


def review(request):
    page = request.GET.get('page')
    id = request.GET.get('movie_id')
    page_cnt = 4
    
    reviews = []
    userDB = []
    switch = "true"
    
    userReview = Review.objects.filter(Q(movie_id=id) & Q(author=request.user.id)).order_by('like').all()
    reviewDB = Review.objects.filter(movie_id=id).order_by('like').all().exclude(Q(author=request.user.id) | Q(publish=False))
    # reviewDB = Review.objects.filter(movie_id=id).all()
    count = (reviewDB.count() - ((int(page) - 1) * page_cnt))
    # "avatar": review.author.avatar,
    paginator = Paginator(reviewDB, page_cnt)
    reviewPaginator = paginator.get_page(page)

    
    if count > 0:
        for review in reviewPaginator:
            reviews.append({
                            "avatar": review.author.avatar.url,
                            "name": review.author.nick_name,
                            "screen": review.author.user_screen_id,
                            "title": review.title,
                            "like": review.like,
                            "content": review.content,
                            "spoiler": review.spoiler,})
    else:
        switch = "false"


    if userReview.count() > 0:
        review =  userReview[0]
        userDB = ({"id": review.id,
                    "avatar": review.author.avatar.url,
                    "name": review.author.nick_name,
                    "screen": review.author.user_screen_id,
                    "title": review.title,
                    "like": review.like,
                    "content": review.content,
                    "spoiler": review.spoiler})
    else:
        userDB = "false"

    if (not(reviewDB.count() - ((int(page)) * (page_cnt + 1))) > 0):
        switch = "false"
        
    d = {
        "reviews": reviews,
        "switch": switch,
        "userReview": userDB
    }

    return JsonResponse(d)


#例外処理
def error_400page(request, exception): # 以下追記箇所
    return render(request, 'app/errors/404.html', status=400)

def error_403page(request, exception): # 以下追記箇所
    return render(request, 'app/errors/403.html', status=403)

def error_404page(request, exception): # 以下追記箇所
    return render(request, 'app/errors/404.html', status=404)

def error_500page(request, exception): # 以下追記箇所
    return render(request, 'app/errors/500.html', status=500)