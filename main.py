from bs4 import BeautifulSoup
import requests

imdb_root = 'https://www.imdb.com/'
imdb_tvshows = 'https://www.imdb.com/chart/toptv/'

page = requests.get(imdb_tvshows)

bs = page.text

soup = BeautifulSoup(bs, 'html.parser')

# soup.find_all returns
#<class 'bs4.element.ResultSet'>
all_titles = soup.find_all('td', class_='titleColumn')

# def return_title
for title in all_titles:

    tvshow_url = title.find('a').attrs['href']
    show_id = tvshow_url.split('/')[2]
    tvshow_name = title.find('a').contents
    #print(tvshow_name)




# each element of a ResultSet is a
#<class 'bs4.element.Tag'>

# methods of element.tag:
# contents (returns an array of all contents)
# name (returns the name of the tag, in this case it returns td, because we searched fot td)
# children (returns a python iter object)
# attrs (a tag can have many attributes, so it returns the all)

#print(all_a[].contents)

tvshow_url = 'https://www.imdb.com/title/tt2560140/episodes'
tvshow_url_request = requests.get(tvshow_url)

tvshow_url_html = tvshow_url_request.text

tvshow_url_bs = BeautifulSoup(tvshow_url_html, 'html.parser')
number_of_seasons_resultset = tvshow_url_bs.find_all('div', class_='episode-list-select')


mylist= []
for tag in number_of_seasons_resultset:
    #print(tag)
    for other_tag in tag.find_all('option'):
        if 'value' in other_tag.attrs:
            mylist.append(other_tag.attrs['value'])
mylist = [int(x) for x in mylist]
mylist.sort()
seasons = [x for x in mylist if x < 100 and x > 0]

#show_id:
#show_name:
#show_seasons:
#show_rating:
#season:
    #number:
        #episode:
        #epise_name:
        #episode_rating:
        #episode_votes:


catalog = []
show = {}
show['show_id'] = '3'
show['season'] = {}

for season_number in seasons:
    show['season'][season_number] = []
    season_url = tvshow_url + '?season=' + str(season_number)
    print(season_url)
    season_url_request = requests.get(season_url)
    season_url_html = season_url_request.text
    season_url_bs = BeautifulSoup(season_url_html, 'html.parser')
    print('======SEASONNUMBER======')
    episode_info = season_url_bs.find_all('div', class_='info')
    for title_info in episode_info:
        for title in title_info.find('a'):
            show['season'][season_number].append({'title': title})
    for rating_info in episode_info:
       # Some episodes might not be rated yet
        if rating_info.find('span', class_='ipl-rating-star__rating'):
            for rating in rating_info.find('span', class_='ipl-rating-star__rating'):
                show['season'][season_number].append({'rating': rating})
        else:
            print('SPISODE HAS NOT BEEN RATER')
    print(show)
    for number_of_rates_info in episode_info:
        if number_of_rates_info.find('span', class_='ipl-rating-star__total-votes'):
            for number_of_rates in number_of_rates_info.find('span', class_='ipl-rating-star__total-votes'):
                show['3']['season'][season_number]['number_of_rates'] = number_of_rates
                print(number_of_rates)
        else:
            print("EPISODE HAS NOT BEEN RATED")

    for episode_number_info in episode_info:
        print(episode_number_info.find('meta').attrs['content'])
        show['3']['season'][season_number]['episode_number'] = episode_number

print(show)
