#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import os

from models import db, Artist,Venue,Show
from sqlalchemy import func
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
#database_name = 'venue_artist'
#database_path = "postgres://{}:{}@{}/{}".format('Kaustav', 'k','localhost:5432', database_name)

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
##Code Kaustav
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgres:///venue_artist'
#db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
db.init_app(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  # data = Venue.query.all()
  #data = Venue.query().group_by(Venue.city, Venue.state).all()
  #data = db.session.query(Venue.city,Venue.state).group_by(Venue.city, Venue.state).all()
  all_data = []
  each_data = {}
  all_venue = []
  each_venue ={}

  cities = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
  #print(cities)

  for city_1 in cities:

      each_data = {}
      (city,state)= (city_1)

      each_data['city']= city
      each_data['state'] = state
      #print(city,'$$')

      #venues = db.session.query(Venue.id,Venue.name).filter(city=='Kolkata').all()
      venues = Venue.query.filter_by(city =city, state = state).all()
      #print('Venues:', venues)
      all_venue = []
      ##count =0
      for venue_1 in venues:
          #print(venue_1,'***')
          each_venue ={}
          #(id,name)= (venue_1)
          id = venue_1.id
          name = venue_1.name
          each_venue['id'] = id
          each_venue['name'] = name
          #print('**',id,name)
          #print(each_venue['id'])
          #print( each_venue['name'])
          #print(each_venue)
          all_venue.append(each_venue)
          #count +=1
          #print(count)

      #print(each_data,'$$$')
      each_data['venues']= all_venue


      all_data.append(each_data)

  data = all_data


  ##print(data)
  #print(data)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_term =  request.form.get('search_term', '')
  venues = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term +'%')).all()
  records_count = db.session.query(func.count(Venue.id)).filter(Venue.name.ilike('%' + search_term +'%')).scalar()

  all_response={}
  all_response["count"]=records_count
  all_data =[]
  for venue in venues:
      each_data ={}
      each_data["id"] = venue.id
      each_data["name"] = venue.name
      ##Kaustav update later
      each_data["num_upcoming_shows"] = db.session.query(func.count(Show.id)).filter(Show.venue_id ==venue.id,Show.start_time > datetime.now() ).scalar()

      all_data.append(each_data)
  all_response["data"]= all_data

  #print(records_count)
  #print(all_response)
  response = all_response

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  ##Kaustav
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  venue_data ={}
  venue_details = db.session.query(Venue).get(venue_id)
  #print(venue_details)
  venue_data["id"]=  venue_details.id
  venue_data["name"]=  venue_details.name
  print(venue_details.genres)

  ##Kaustav
  # ##Convert unicode list to list
  # all_genres = []
  # for x in venue_details.genres.split():
  #     print(x.encode('ascii'))
  #     all_genres.append(x.encode('ascii'))
  # venue_data["genres"]= all_genres
  # print(all_genres)
  # print(type(all_genres))
  venue_data['genres'] = venue_details.genres

  venue_data["address"] = venue_details.address
  venue_data["city"] = venue_details.city
  venue_data["state"]= venue_details.state
  venue_data["phone"]= venue_details.phone
  venue_data["website"] = venue_details.website
  venue_data["facebook_link"] = venue_details.facebook_link
  venue_data["seeking_talent"] = venue_details.seeking_talent
  venue_data["image_link"] = venue_details.image_link

 ##Venue Past artist shows
  venue_data["past_shows_count"] = db.session.query(func.count(Show.artist_id)).filter(Show.venue_id ==venue_details.id,Show.start_time < datetime.now() ).scalar()
  print(venue_details.id)
  venue_past_artist_shows = db.session.query(Show).filter(Show.venue_id == venue_details.id,Show.start_time < datetime.now()).all()
  ## genres is the list of all the genres of all the past and upcomming artists
  #genres= []
  venue_data["past_shows"]= []
  for show in venue_past_artist_shows:
      ##Reset
      #print(show.id, show.venue_id)
      past_each_show ={}
      ##Populate
      past_each_show["start_time"] = str(show.start_time)
      ##Artist_id is the primiary key. SO the below line will  always give back 1 create_shows
      ##So we dont have to loop
      artist = db.session.query(Artist).get(show.artist_id)
      #genres.append(artist.genres)
      past_each_show["artist_id"]= artist.id
      past_each_show["artist_name"]= artist.name
      past_each_show["artist_image_link"]= artist.image_link

      venue_data["past_shows"].append(past_each_show)

 ##Venue upcoming artist shows
  venue_data["upcoming_shows_count"] = db.session.query(func.count(Show.artist_id)).filter(Show.venue_id ==venue_details.id,Show.start_time >= datetime.now() ).scalar()

  venue_upcoming_artist_shows = db.session.query(Show).filter(Show.venue_id == venue_details.id, Show.start_time >= datetime.now()).all()
  ## genres is the list of all the genres of all the past and upcomming artists
  ## DONT RESET GENRES HERE
  ##genres= []
  venue_data["upcoming_shows"]=[]

  for show in venue_upcoming_artist_shows:
      ##Reset
      upcoming_each_show ={}
      ##print(show.artist_id, show.venue_id)
      ##Populate
      upcoming_each_show["start_time"] = str(show.start_time)
      ##Artist_id is the primiary key. SO the below line will  always give back 1 create_shows
      ##So we dont have to loop
      artist = db.session.query(Artist).get(show.artist_id)
      #genres.append(artist.genres)
      upcoming_each_show["artist_id"]= artist.id
      upcoming_each_show["artist_name"]= artist.name
      upcoming_each_show["artist_image_link"]= artist.image_link
      venue_data["upcoming_shows"].append(upcoming_each_show)
  ## Populate genres
  #venue_data["genres"] = genres


  print(venue_data)
  data = venue_data
  #print(venue_data)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')

  venue = Venue(name=name, city=city,state= state,phone= phone, genres=genres, facebook_link=facebook_link)
  ##venue.id =1  ##Kaustav
  try:
      venue.add()
      flash("Venue" + request.form['name'] + "was successfully listed!")
  except:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
      #abort(422)
  finally:
      db.session.close()
  ##flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      venue = Venue.session.get(venue_id)
      venue.delete()
      flash('Venue Id'+ venue_id + "deleted")
  except:
      flash("Venue Id" + venue_id + "could not be deleted")
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  ##Kaustav
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  all_artists =[]
  for artist in Artist.query.all():
      each_artist = {}
      each_artist['id'] = artist.id
      each_artist["name"] = artist.name
      all_artists.append(each_artist)

  data = all_artists

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term','')
  data = db.session.query(Artist).filter(Artist.name.ilike('%'+ search_term +'%')).all()

  all_artists =[]
  for artist in data:
      each_artist={}
      each_artist['id'] = artist.id
      each_artist['name'] = artist.name
      each_artist['num_upcoming_shows'] = db.session.query(func.count(Show.id)).filter(Show.artist_id ==artist.id,Show.start_time >= datetime.now() ).scalar()
      all_artists.append(each_artist)

  all_response ={}
  all_response['data'] = all_artists
  all_response['count'] = db.session.query(func.count(Artist.id)).filter(Artist.name.ilike('%'+ search_term +'%')).scalar()

  response = all_response

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]  ##Kaustav

  ##
  artist = Artist.query.get(artist_id)
  print(artist)
  artist_data ={}
  artist_data['id']= artist.id
  artist_data['name'] = artist.name
  artist_data['genres'] = artist.genres
  artist_data['city']= artist.city
  artist_data['state'] = artist.state
  artist_data['phone'] = artist.phone
  artist_data['facebook_link'] = artist.facebook_link
  artist_data['image_link'] = artist.image_link

  ##Past Shows
  past_shows_count = db.session.query(func.count(Show.id)).filter(Show.artist_id == artist.id,Show.start_time < datetime.now()).scalar()
  past_shows = db.session.query(Show).filter(Show.artist_id == artist.id,Show.start_time < datetime.now()).all()
  artist_data['past_shows']=[]
  for show in past_shows:
      each_show ={}
      each_show['start_time']= str(show.start_time)
      ##Get the venue details based on primary_key
      ##venue = Venue.query.get(Show.venue_id)
      venue = db.session.query(Venue).get(show.venue_id)
      each_show['venue_id'] = venue.id
      each_show['venue_name'] = venue.name
      each_show['venue_image_link'] = venue.image_link
      artist_data['past_shows'].append(each_show)

  ##Upcoming Shows
  upcoming_shows_count = db.session.query(func.count(Show.id)).filter(Show.artist_id == artist.id,Show.start_time >= datetime.now()).scalar()
  upcoming_shows = db.session.query(Show).filter(Show.artist_id == artist.id,Show.start_time >= datetime.now()).all()
  artist_data['upcoming_shows']=[]
  for show in upcoming_shows:
      each_show ={}
      each_show['start_time']= str(show.start_time)
      ##Get the venue details based on primary_key
      venue = Venue.query.get(show.venue_id)
      each_show['venue_id'] = venue.id
      each_show['venue_name'] = venue.name
      each_show['venue_image_link'] = venue.image_link
      artist_data['upcoming_shows'].append(each_show)

  data = artist_data

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist_details ={}

  artist_1 = Artist.query.get(artist_id)
  artist_details["id"] = artist_1.id
  artist_details["name"] = artist_1.name
  artist_details["genres"] = artist_1.genres
  artist_details["city"]= artist_1.city

  artist_details["state"] = artist_1.state
  artist_details["phone"] = artist_1.phone
  artist_details["website"] = artist_1.website
  artist_details["facebook_link"] = artist_1.facebook_link
  artist_details["seeking_venue"] = artist_1.seeking_venue
  artist_details["seeking_description"] = artist_1.seeking_description
  artist_details["image_link"] = artist_1.image_link
  artist = artist_details #### Kaustav
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  artist_details = Artist.query.get(artist_id)

  print(request.form)
  artist_details.name = request.form.get('name') ##
  artist_details.genres = request.form.get('genres') ##
  artist_details.city= request.form.get('city')  ##
  artist_details.state = request.form.get('state') ##
  artist_details.phone = request.form.get('phone') ##
  #artist_details.website = request.form.get('website')
  artist_details.facebook_link = request.form.get('facebook_link')
  #artist_details.seeking_venue = request.form.get('seeking_venue')
  #artist_details.seeking_description = request.form.get('seeking_description')
  #artist_details.image_link = request.form.get('image_link')

  try:
      artist_details.update()
      flash('Artist Details id ' + str(artist_id) + ' updated')
  except:
      flash('Error Artist Details id ' + str(artist_id) + ' could not be updated')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  venue_1 = Venue.query.get(venue_id)
  venue_details = {}
  venue_details['id'] =  venue_1.id
  venue_details['name'] = venue_1.name
  venue_details['genres'] = venue_1.genres
  venue_details['address'] = venue_1.address
  venue_details['city'] = venue_1.city
  venue_details['state'] = venue_1.state
  venue_details['phone'] = venue_1.phone
  venue_details['website'] = venue_1.website
  venue_details['facebook_link'] = venue_1.facebook_link
  venue_details['seeking_talent'] = venue_1.seeking_talent
  venue_details['seeking_description'] = venue_1.seeking_description
  venue_details['image_link']  = venue_1.image_link

  venue= venue_details

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)

  venue.name = request.form.get('name')
  venue.city = request.form.get('city')
  venue.state = request.form.get('state')
  venue.address = request.form.get('address')
  venue.phone = request.form.get('phone')
  venue.genres = request.form.get('genres')
  venue.facebook_link = request.form.get('facebook_link')


  try:
      venue.update()
      flash('Venue ' + venue.name + ' updated')

  except:
      db.session.rollback()
      flash('ERROR Venue ' + venue.name + ' not updated')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get("facebook_link")
  try:
      artist = Artist(name= name,city= city, state= state, phone=phone, genres = genres, facebook_link= facebook_link)
      #artist.add()
      db.session.add(artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  except:
      flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
      db.session.rollback()
  finally:
      db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]

  all_data =[]
  shows = Show.query.all()
  for show in shows:
      each_data ={}
      each_data['venue_id'] = show.venue_id
      each_data['venue_name'] = Venue.query.get(show.venue_id).name
      each_data['artist_id'] = show.artist_id
      each_data['artist_name'] = Artist.query.get(show.artist_id).name
      each_data['start_time'] = str(show.start_time)
      all_data.append(each_data)

  data = all_data
  print(data)


  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form.get('artist_id')
  venue_id  = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  show = Show(artist_id=artist_id, venue_id=venue_id, start_time= start_time)

  try:
      show.add()
      flash('Show was successfully listed!')
  except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')



  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    ##port = 5000
    app.run(host='0.0.0.0', port=port)
