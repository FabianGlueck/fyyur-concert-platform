#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import collections
import collections.abc
import sys
collections.Callable = collections.abc.Callable
import json
import dateutil.parser
import babel
from flask import Flask, abort, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import Venue, Artist, Show
from models import db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)






#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # Query all venues
  venues = Venue.query.all()

  # Initialize a dictionary to hold the city and state data
  data_dict = {}

  # Iterate over each venue and organize the data
  for venue in venues:
      city_state_key = (venue.city, venue.state)
      print(city_state_key)
      # If the city and state combination is not in the dictionary, add it
      if city_state_key not in data_dict:
          data_dict[city_state_key] = {
              "city": venue.city,
              "state": venue.state,
              "venues": []
          }
      # Append venue information to the correct city and state
      
      data_dict[city_state_key]["venues"].append({
          "id": venue.id,
          "name": venue.name,
      })

  # Convert the dictionary to the list format you need
  data = list(data_dict.values())

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  form_data = request.form.to_dict()
  search_value = form_data['search_term']
  filteredVenues = Venue.query.filter(Venue.name.ilike(f'%{search_value}%')).all()
  response = {
    "count": len(filteredVenues),
    "data": filteredVenues
  }
  print(form_data)


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  print(venue_id)
  # shows the venue page with the given venue_id
  data = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows = []
  for show in shows:
    if show.start_time > str(datetime.now()):
      upcoming_shows.append(show)
    else:
      past_shows.append(show)

  data.past_shows_count = len(past_shows) if past_shows else 0
  data.upcoming_shows_count = len(upcoming_shows) if upcoming_shows else 0
  data.upcoming_shows = upcoming_shows
  print('data type: ' + str(type(data)))
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    print('create_venue_submission() called')
    form_data = request.form.to_dict()
    print(form_data)
    value_from_form = form_data.get('seeking_talent', 'n')
    genre_data = request.form.getlist('genres')
    print(genre_data)
    # Convert to Python Boolean
    boolean_value = True if value_from_form.lower() == 'false' else False

    new_venue = Venue(
        name=form_data['name'],
        genres=genre_data,
        address=form_data['address'],
        city=form_data['city'],
        state=form_data['state'],
        phone=form_data['phone'],
        website=form_data['website_link'],
        facebook_link=form_data['facebook_link'],
        seeking_talent=boolean_value,
        seeking_description=form_data['seeking_description'],
        image_link=form_data['image_link'],
    )
    print(new_venue)
    try:
      print('try')
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      print('except')
      print(sys.exc_info())
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

    finally:
      print('finally')
      db.session.close()
      return render_template('pages/home.html')



@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):

  try:
    Venue.query.filter(Venue.id == venue_id).delete()
    db.session.commit()
    flash('Venue was successfully deleted!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue could not be deleted.')
    print(sys.exc_info())
  finally:
    db.session.close()


  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  form_data = request.form.to_dict()
  search_value = form_data['search_term']
  filteredArtists = Artist.query.filter(Artist.name.ilike(f'%{search_value}%')).all()
  response = {
    "count": len(filteredArtists),
    "data": filteredArtists
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    print(artist_id)
    # shows the artist page with the given artist_id
    data = Artist.query.get(artist_id)
    shows = Show.query.filter_by(artist_id=artist_id).all()
    past_shows = []
    upcoming_shows = []
    for show in shows:
      if show.start_time > str(datetime.now()):
        upcoming_shows.append(show)
      else:
        past_shows.append(show)

    data.past_shows_count = len(past_shows) if past_shows else 0
    data.upcoming_shows_count = len(upcoming_shows) if upcoming_shows else 0
    data.upcoming_shows = upcoming_shows
    return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):

  try:
    Artist.query.filter(Artist.id == artist_id).delete()
    db.session.commit()
    flash('Artist was successfully deleted!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist could not be deleted.')
    print(sys.exc_info())
  finally:
    db.session.close()


  return render_template('pages/home.html')
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    
      print('update_artist_submission() called')
      form_data = request.form.to_dict()
      print(form_data)
      value_from_form = form_data.get('seeking_venue', 'false')
      genre_data = request.form.getlist('genres')
      print(genre_data)
      # Convert to Python Boolean
      boolean_value = True if value_from_form.lower() == 'y' else False
  
      try:
          print('try')
          # Retrieve the existing artist
          artist = Artist.query.get(artist_id)
          if artist is None:
              flash(f'Artist with id {artist_id} not found.')
              return redirect(url_for('index'))  # or appropriate redirect
  
          # Update the artist's attributes
          artist.name = form_data['name']
          artist.genres = genre_data
          artist.city = form_data['city']
          artist.state = form_data['state']
          artist.phone = form_data['phone']
          artist.website = form_data['website_link']
          artist.facebook_link = form_data['facebook_link']
          artist.seeking_description = form_data['seeking_description']
          artist.image_link = form_data['image_link']
          artist.seeking_venue = boolean_value
  
          # Commit the changes to the database
          db.session.commit()
          flash('Artist ' + request.form['name'] + ' was successfully updated')
  
      except Exception as e:
          print('except')
          print(e)
          db.session.rollback()
          flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  
      finally:
          print('finally')
          db.session.close()

      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    print('update_venue_submission() called')
    form_data = request.form.to_dict()
    print(form_data)
    value_from_form = form_data.get('seeking_talent', 'false')
    genre_data = request.form.getlist('genres')
    print(genre_data)
    # Convert to Python Boolean
    boolean_value = True if value_from_form.lower() == 'y' else False

    try:
        print('try')
        # Retrieve the existing venue
        venue = Venue.query.get(venue_id)
        if venue is None:
            flash(f'Venue with id {venue_id} not found.')
            return redirect(url_for('index'))  # or appropriate redirect

        # Update the venue's attributes
        venue.name = form_data['name']
        venue.genres = genre_data
        venue.address = form_data['address']
        venue.city = form_data['city']
        venue.state = form_data['state']
        venue.phone = form_data['phone']
        venue.website = form_data['website_link']
        venue.facebook_link = form_data['facebook_link']
        venue.seeking_description = form_data['seeking_description']
        venue.image_link = form_data['image_link']
        venue.seeking_talent = boolean_value

        # Commit the changes to the database
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated')

    except Exception as e:
        print('except')
        print(e)
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

    finally:
        print('finally')
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    print('create_artist_submission() called')
    form_data = request.form.to_dict()
    print(form_data)
    value_from_form = form_data.get('seeking_venue', 'False')
    genre_data = request.form.getlist('genres')
    # Convert to Python Boolean
    boolean_value = True if value_from_form.lower() == 'y' else False

    new_artist = Artist(
        name=form_data['name'],
        genres=genre_data,
        city=form_data['city'],
        state=form_data['state'],
        phone=form_data['phone'],
        facebook_link=form_data['facebook_link'],
        seeking_venue=boolean_value,
        seeking_description=form_data['seeking_description'],
        image_link=form_data['image_link'],
    )
    print(new_artist)
    try:
      print('try')
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      print('except')
      print(sys.exc_info())
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

    finally:
      print('finally')
      db.session.close()
      return render_template('pages/home.html')





#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = Show.query.all()
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
  form_data = request.form.to_dict()
  new_show = Show(
      venue_id=form_data['venue_id'],
      artist_id=form_data['artist_id'],
      start_time=form_data['start_time'],
      artist_image_link=Artist.query.get(form_data['artist_id']).image_link,
      venue_name=Venue.query.get(form_data['venue_id']).name,
      artist_name=Artist.query.get(form_data['artist_id']).name,
      venue_image_link=Venue.query.get(form_data['venue_id']).image_link,
  )
 
  try:
    db.session.add(new_show)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')

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
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
