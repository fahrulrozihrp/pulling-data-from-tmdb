# koneksikan ke API
import tmdbsimple as tmdb

tmdb.API_KEY = 'bd463bc365a9c960f7fc83bdb87aaa3c'

#deklarasikan variabel untuk fungsi search dan discover
search = tmdb.Search()
discover = tmdb.Discover()

# cari info 'Universal' berdasarkan company
response1 = search.company(query='Universal')
response1['results'][:2]

#cari film berdasarkan tahun 2017
response2 = discover.movie(year="2017")
for value in response2['results']:
    print(value['title'])
    
print("Number of results: ", len(response2['results']))

import pandas as pd

watched_df = pd.read_csv ('E:/Tutorial Python/tmdb dataset/watched.csv')
watched_df

# Extract setiap judul ke dalam list
title = watched_df.Name.tolist()
print(title)
print(len(title))

# Extract tahun rilis ke dalam list
released_year = watched_df.Year.tolist()
print(released_year)
print(len(released_year))

#proses pencarian info film berdasarkan title dan released_year
result_count = 0

for i,j in zip(title,released_year):
    response = search.movie(query= i, year=j)
    for value in response['results']:
        if value['title'] == i:                 
            print(value['title'],"  /  ",
                  value['release_date'],"  /  ",
                  value['id'])
            
            result_count+= 1
            break            
            
print("Results count: ", result_count)

#Extract hasil pencarian id film ke movie_id
movie_id = [] 
result_count=0

for i,j in zip(title,released_year):
    response = search.movie(query= i, year=j)
    for value in response['results']:
        if value['title'] == i:
            movie_id.append(value['id'])
            result_count+= 1
            break 
            
print(movie_id)
print("Results count: ", result_count)

# zero_search menghitung jumlah pencarian tv series
zero_search = 0

tv_title = [] #list judul tv series
tv_year = []  #list tahun rilis

for i,j in zip(title,released_year):
    response = search.movie(query=i, year=j)
    if (len(response['results'])) == 0:
        tv_title.append(i)
        tv_year.append(j)
        print(i,j, len(response['results']))
        zero_search+= 1
        
print("0 search: ", zero_search)
print(tv_title)
print(tv_year)

#Extract hasil pencarian id series ke tv_id
total = 0 
tv_id = []

for i,j in zip(tv_title,tv_year):
    response = search.tv(query= i, year=j)
    for value in response['results']:
        if value['name'] == i:
            tv_id.append(value['id'])
            total+= 1
            
print(tv_id)
print("Results count: ", total)

#cek id film
movie = tmdb.Movies(496243)
response = movie.info()
movie.title

#cek id series
tv = tmdb.TV(96129)
response = tv.info()
tv.name

#ekstrak info movie ke list
movie_info=[]

for i in movie_id:
    movie = tmdb.Movies(i)
    response = movie.info()
    movie_info.append([movie.id, movie.title, movie.spoken_languages, movie.production_countries, movie.genres, 
                       movie.runtime, movie.release_date, movie.vote_count, movie.vote_average])
print(len(movie_info))
movie_info[:2]

#ekstrak info series ke list
tv_info=[]

for i in tv_id:
    tv = tmdb.TV(i)
    response = tv.info()
    tv_info.append([tv.id, tv.name, tv.origin_country, tv.genres, 
                   tv.spoken_languages, tv.episode_run_time,
                   tv.first_air_date, tv.number_of_seasons, 
                   tv.number_of_episodes, tv.vote_count, tv.vote_average])
print(len(tv_info))
tv_info[:2]

#convert ke dataframe
movie_df = pd.DataFrame(movie_info, columns =['ID', 'title', 'languages', 'prod_country', 'genres', 'runtime', 'releasedate', 'votecount', 'voteavg'])
movie_df.head()

tv_df = pd.DataFrame(tv_info, columns =['ID', 'title', 'origin_country', 'genres', 'languages', 'eps_runtime', '1st_airdate', 'no_seasons', 'no_eps', 'vote_counts', 'vote_average'])
tv_df

# Export dataframes ke csv
movie_df.to_csv('watchedmovie.csv')
print("Exported movies successfully!")

tv_df.to_csv('watchedtv.csv')
print("Exported tv shows successfully!")

# proses mencari frekunsi genre
from collections import Counter
import ast

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

#mencari frekuensi genre movie
movie['genres'] = movie['genres'].apply(convert)

genres = Counter()

for i in range(movie.shape[0]):
    for j in movie.genres[i]:
        genres[j]+=1
        
genres_df = pd.DataFrame.from_dict(genres, orient='index').reset_index()
genres_df = genres_df.rename(columns = {'index': 'Genres', 0: 'Frequency'})

print(genres_df.shape)
genres_df.head()

#mencari frekuensi genre tv
tv['genres'] = tv['genres'].apply(convert)

genres2 = Counter()

for i in range(tv.shape[0]):
    for j in tv.genres[i]:
        genres2[j]+=1
        
genres2_df = pd.DataFrame.from_dict(genres2, orient='index').reset_index()
genres2_df = genres2_df.rename(columns = {'index': 'Genres', 0: 'Frequency'})

print(genres2_df.shape)
genres2_df.head()

#proses menyatukan genre movie dan genre Tv ke satu table
merged_genre = pd.merge(genres_df, genres2_df, on='Genres',how='outer')
merged_genre

merged_genre.isna().sum()

#isi null dengan 0
merged_genre = merged_genre.fillna(0)
merged_genre

merged_genre['Frequency'] = merged_genre['Frequency_x']+merged_genre['Frequency_y']
merged_genre = merged_genre.drop(["Frequency_x","Frequency_y"], axis=1)
merged_genre

merged_genre.to_csv('genre_freq.csv')
print("Exported successfully!")

# proses mencari frekunsi language
def convert_lang(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['english_name'])
    return L

#mencari frekunsi languages movie
movie['languages'] = movie['languages'].apply(convert_lang)

languages = Counter()

for i in range(movie.shape[0]):
    for j in movie.languages[i]:
        languages[j]+=1
        
lang_df = pd.DataFrame.from_dict(languages, orient='index').reset_index()
lang_df = lang_df.rename(columns = {'index': 'Languages', 0: 'Frequency'})

print(lang_df.shape)
lang_df.head()

#mencari frekunsi languages tv
tv['languages'] = tv['languages'].apply(convert_lang)

languages2 = Counter()

for i in range(tv.shape[0]):
    for j in tv.languages[i]:
        languages2[j]+=1
        
lang2_df = pd.DataFrame.from_dict(languages2, orient='index').reset_index()
lang2_df = lang2_df.rename(columns = {'index': 'Languages', 0: 'Frequency'})

print(lang2_df.shape)
lang2_df.head()

#proses menyatukan languages movie dan languages Tv ke satu table
merged_lang = pd.merge(lang_df, lang2_df, on='Languages',how='outer')
merged_lang

merged_lang = merged_lang.fillna(0)
merged_lang['Frequency'] = merged_lang['Frequency_x']+merged_lang['Frequency_y']
merged_lang = merged_lang.drop(["Frequency_x","Frequency_y"], axis=1)
merged_lang

merged_lang.to_csv('language_freq.csv')
print("Exported successfully!")

#mencari frekuensi negara movie
movie['prod_country'] = movie['prod_country'].apply(convert)

country = Counter()

for i in range(movie.shape[0]):
    for j in movie.prod_country[i]:
        country[j]+=1
        
country_df = pd.DataFrame.from_dict(country, orient='index').reset_index()
country_df = country_df.rename(columns = {'index': 'Countries', 0: 'Frequency'})

print(country_df.shape)
country_df.head()

#mencari frekuensi negara tv
tv['origin_country']=tv['origin_country'].str.strip("[']")
tv

country2 = Counter()

for i in range(tv.shape[0]):
    for j in tv.origin_country:
        country2[j]+=1
        
country2_df = pd.DataFrame.from_dict(country2, orient='index').reset_index()
country2_df = country2_df.rename(columns = {'index': 'Countries', 0: 'Frequency'})

print(country2_df.shape)
country2_df.head()

merged_country = pd.merge(country_df, country2_df, on='Countries',how='outer')

merged_country = merged_country.fillna(0)

merged_country['Frequency'] = merged_country['Frequency_x']+merged_country['Frequency_y']
merged_country = merged_country.drop(["Frequency_x","Frequency_y"], axis=1)
merged_country

merged_country.to_csv('country_freq.csv')
print("Exported successfully!")

#mencari info crew
movie = tmdb.Movies(496243)
response = movie.credits()
movie.crew

#mencari nama director movie
movie_credit=[]

for i in movie_id:
    movie = tmdb.Movies(i)
    response = movie.credits()
    for credit in movie.crew:  
        if credit['job'] == 'Director':  
            movie_credit.append(credit)
            print(credit['name'])
            
print(len(movie_credit))

#mencari nama director tv series
tv_credit=[]

for i in tv_id:
    tv = tmdb.TV(i)
    response = tv.credits()
    for credit in tv.crew:  
        if credit['job'] == 'Director' or credit['job'] == 'Series Director':  
            tv_credit.append(credit)
            print(credit['name'])
            
print(len(tv_credit))

#convert director movie kedalam dataframe
credit_df = pd.DataFrame(movie_credit, columns =['adult', 'gender', 'id', 'known_for_department', 'name', 'popularity', 'profile_path', 'credit_id', 'department', 'job'])
credit_df.head()

#export ke file csv
credit_df.to_csv('creditmovie.csv')
print("Exported movies successfully!")

#convert director tv series kedalam dataframe
credit_tv_df = pd.DataFrame(tv_credit, columns =['adult', 'gender', 'id', 'known_for_department', 'name', 'popularity', 'profile_path', 'credit_id', 'department', 'job'])
credit_tv_df.head()

#export ke file csv
credit_tv_df.to_csv('credit_tv.csv')
print("Exported movies successfully!")

movie_crdt = pd.read_csv('C:/Users/Rozi/Tutorial python/creditmovie.csv')
movie_crdt.head()

#membuat frequensi director movie
freq_dirmovie = movie_crdt['name'].value_counts().rename_axis('director_name').reset_index(name='frequency')
print(freq_dirmovie)

#export ke file csv
freq_dirmovie.to_csv('freq_dirmovie.csv')
print("Exported successfully!")

tv_crdt = pd.read_csv('C:/Users/Rozi/Tutorial python/credit_tv.csv')
tv_crdt.head()

#membuat frequensi director tv
freq_dirtv = tv_crdt['name'].value_counts().rename_axis('director_name').reset_index(name='frequency')
print(freq_dirtv)

#export ke file csv
freq_dirtv.to_csv('freq_dirtv.csv')
print("Exported movies successfully!")

#proses menyatukan freq director movie dan tv series
merged_dir = pd.merge(freq_dirmovie, freq_dirtv, on='director_name',how='outer')
merged_dir

merged_dir.isna().sum()

merged_dir = merged_dir.fillna(0)
merged_dir

merged_dir['frequency'] = merged_dir['frequency_x']+merged_dir['frequency_y']
merged_dir = merged_dir.drop(["frequency_x","frequency_y"], axis=1)
merged_dir

merged_dir.to_csv('movie_tv_freq.csv')
print("Exported successfully!")
