from bs4 import BeautifulSoup
import requests

# each element of a ResultSet is a
#<class 'bs4.element.Tag'>

# methods of element.tag:
# contents (returns an array of all contents)
# name (returns the name of the tag, in this case it returns td, because we searched fot td)
# children (returns a python iter object)
# attrs (a tag can have many attributes, so it returns the all)

#print(all_a[].contents)


imdb_root = 'https://www.imdb.com/'
imdb_tvshows = 'https://www.imdb.com/chart/toptv/'

page = requests.get(imdb_tvshows)

bs = page.text

soup = BeautifulSoup(bs, 'html.parser')

# soup.find_all returns
#<class 'bs4.element.ResultSet'>
all_titles = soup.find_all('td', class_='titleColumn')


def get_number_of_seasons(resultset):
    #print(resultset)
    #print(type(resultset))
    mylist= []
    for tag in resultset:
        for other_tag in tag.find_all('option'):
            if 'value' in other_tag.attrs:
                mylist.append(other_tag.attrs['value'])
    mylist = [int(x) for x in mylist]
    mylist.sort()
    seasons = [x for x in mylist if x < 100 and x > 0]
    return max(seasons)



catalog = []
# def return_title
shows=0
for title in all_titles:
    shows+=1
    if shows > 10:
        break
    tvshow_url = title.find('a').attrs['href']
    show_id = tvshow_url.split('/')[2]
    tvshow_name = title.find('a').contents
    print(show_id)
    print(tvshow_name)


    tvshow_url = 'https://www.imdb.com/title/' + show_id + '/episodes'
    tvshow_url_request = requests.get(tvshow_url)

    tvshow_url_html = tvshow_url_request.text

    tvshow_url_bs = BeautifulSoup(tvshow_url_html, 'html.parser')
    number_of_seasons_resultset = tvshow_url_bs.find_all('div', class_='episode-list-select')
    number_of_seasons = get_number_of_seasons(number_of_seasons_resultset)
    print(number_of_seasons)

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


    show = {}
    show['show_id'] = show_id
    show['season'] = {}
    for season_number in range(number_of_seasons):
        season_url = tvshow_url + '?season=' + str(season_number)
        season_url_request = requests.get(season_url)
        season_url_html = season_url_request.text
        season_url_bs = BeautifulSoup(season_url_html, 'html.parser')
        episode_info_all = season_url_bs.find_all('div', class_='info')

        index = 0
        show['season'][season_number] = [{} for i in range(len(episode_info_all))]
        for episode_info in episode_info_all:

            show['season'][season_number][index]['title'] = episode_info.find('a').attrs['title']
           # Some episodes might not be rated yet
            if episode_info.find('span', class_='ipl-rating-star__rating'):
                show['season'][season_number][index]['rating'] = episode_info.find('span', class_='ipl-rating-star__rating').contents
            else:
                print('SPISODE HAS NOT BEEN RATER')
        #for number_of_rates_info in episode_info:
            if episode_info.find('span', class_='ipl-rating-star__total-votes'):
                show['season'][season_number][index]['episode_votes'] = episode_info.find('span', class_='ipl-rating-star__total-votes').contents
            else:
                print("EPISODE HAS NOT BEEN RATED")

            show['season'][season_number][index]['episode_number'] = episode_info.find('meta').attrs['content']
            index = index + 1
            if index == len(episode_info_all):
                index = 0
    catalog.append(show)
print(catalog)
