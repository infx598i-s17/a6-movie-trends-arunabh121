
from apikeys import TMDB_KEY
import time
import sys
from datetime import datetime                                                                   #import datetime
from bokeh.plotting import *                                                                    #import Bokeh
import requests

def access_api(url, payload):
    """Generic calling function to get information from the TMDB database."""
    r = requests.get(url, params = payload)
    return r.json()

def movie_details(movie_ids):
    """Takes a list called movie_ids list, makes a a list of dictionaries of movies with revenue greater than $10,0000"""
    
    """A list of dictionaries certain info of actor's movies that have revenue greater than $1000 as a filter."""
    movie_details = []                                                          

    for movie_id in movie_ids:
        movies_lists_dict = {}                                                                  # Dictionary to store various lists about movies
        film_url = "https://api.themoviedb.org/3/movie/" + str(movie_id)                        #URL ID pattern
        movie_response = access_api(film_url, {"api_key": TMDB_KEY, \
            "movie_id": id})                                                                    #Using access_api(). Arguments are url variable and payload

        print('.', end = ' ')                                                                   #Print dots to show progress
        sys.stdout.flush()                                                                      #Flush dots from buffer
        if (movie_response['revenue'] >= 10000):                                                #Filter for movies
            movies_lists_dict['release_date'] = movie_response['release_date']
            movies_lists_dict['profit'] = movie_response['revenue'] - movie_response['budget']  #Store profit into a list in movies_lists_dict
            movie_details.append(movies_lists_dict)
    movie_details = sorted(movie_details, key=lambda k: k['release_date'])                      #Sort the list according to release_dates
    
    return(movie_details)

def return_movie_id(name_of_actor):
    """Takes actor name, finds ID of the actor from the API and returns all their movie id's."""

    """Call access_api() to search for movies. Parameters: actor id URL pattern, payload"""
    search_actor = access_api("https://api.themoviedb.org/3/search/person", {"api_key": TMDB_KEY, "query": name_of_actor, \
    "include_adult" : True})                                                                    
    
    actor_id = search_actor['results'][0]['id'] #Store ID of the actor in a list, assuming 0th element is the correct search result

    """Call access_api() to search for movies. Parameters: actor id URL pattern, payload"""
    search_movie_credits = access_api("https://api.themoviedb.org/3/person/" + str(actor_id) + "/movie_credits", \
    {"api_key": TMDB_KEY, "actor_id": actor_id})                                               

    """Create empty list and put all the retrieved movie ID's into a list"""
    movie_ids = []                                                                            
    for num in range(0, len(search_movie_credits['cast'])):
        movie_ids.append(search_movie_credits['cast'][num]['id'])                                    
    return(movie_ids)


def create_graph(name_of_actor,movie_deets):
    """Create graph using Bokeh. x-axis is date(in terms of years) and y-axis is revenue in dollars"""

    output_file("actor_popularity.html")                                   						#Output file created

    profits =[]
    year_of_release=[]
    
    for i in range(len(movie_deets)):
        release_date = movie_deets[i]['release_date']
        date_object = datetime.strptime(release_date, '%Y-%m-%d').date()         				#Convert 'release date' into an object to extract year.
        year_of_release.append(date_object.year)                                  				#Append years of the above date object to a list
        profits.append(movie_deets[i]['profit'])                     							#Append movie profits to another list
    
    """ Plot creation and stylization"""
    p = figure(plot_width = 1200, plot_height = 600, title= "Popularity of " + name_of_actor.title() \
        + " over time", x_axis_label='Year of release', y_axis_label='Revenue(USD)')
    p.left[0].formatter.use_scientific = False
    p.yaxis.major_label_orientation = 45
    p.xaxis.axis_label_text_font = 'avenir'
    p.xaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_text_font = 'avenir'
    p.yaxis.axis_label_text_font_style = 'normal'
    p.title.text_font = 'futura'
    p.title.text_font_style = 'normal'
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.background_fill_color = "beige"
    p.background_fill_alpha = 0.2
    p.outline_line_width = 1
    p.outline_line_color = 'black'

    p.line(year_of_release, profits, line_width=2, line_color = "red", line_alpha = 0.6)        #Specify the glyph and its attributes

    show(p)

if __name__ == "__main__":
    """ Initiate program. """
    
    name_of_actor = input('\nEnter actor name: ')                                            	#Input actor name with UI for user on bash
    movie_ids = return_movie_id(name_of_actor)                                           		#Get name_of_actor's movie IDs
    print('\nCreating popularity graph for '+ name_of_actor.capitalize() + ' movies')			#UI for user on bash
    movie_deets = movie_details(movie_ids)                             							#Call movie_details function
    print('\n')
    create_graph(name_of_actor,movie_deets)                           							#Plot using Bokeh
