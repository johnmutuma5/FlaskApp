from application import app, db
from application.helpers import fetchRows, NoQueryResultError
from flask import jsonify, request
import re
from application.getResturant import findARestaurant


@app.route('/index/')
@app.route('/index')
@app.route('/')
def index():
    return 'Hallo friend, Welcome! Please interact with our API on localhost:5000/restaurant'


@app.route('/restaurants/', methods=['GET', 'POST'])
@app.route('/restaurants', methods=['GET', 'POST'])
def restaurant():
    # establish a db connection
    conn = db.connect()
    cur = conn.cursor()

    # handle requests when the user does not provide url query parameters by returning all the restaurants in the db
    if not request.args:
        cur.execute('''SELECT * FROM restaurants;''')
        rv = cur.fetchall()
        rows = fetchRows(cur, rv)
        return jsonify(rows)

    # else, limit the return values to the users' query parameters
    location = request.args['location']
    mealType = request.args['mealType']
    first_venue = findARestaurant(mealType, location)

    if first_venue:
        venue_name = first_venue[0]['Restaurant Name']
        venue_id = first_venue[0]['venue id']
        venue_address = first_venue[0]['Restaurant Address']
        venue_image = first_venue[0]['Image']

        try:
            cur.execute("SELECT post_id FROM restaurants WHERE venue_id=%s", (venue_id,))
            rv = cur.fetchone()
            if not rv:
                raise Exception("no db match!")
        except Exception as no_match:
            cur.execute("INSERT INTO restaurants (restaurant_name, restaurant_address, image, venue_id) "
                        "VALUES (%s, %s, %s, %s)",(venue_name, venue_address, venue_image, venue_id))
            conn.commit()
        finally:
            cur.execute("SELECT post_id FROM restaurants WHERE venue_id=%s", (venue_id,))
            rv = cur.fetchone()
            first_venue[0]['entry id'] = rv[0]
            conn.close()

        return jsonify(first_venue)
    else:
        # if a venue could not be found
        return 'We couldn\'t find anything there!'


@app.route ('/restaurants/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def getRestaurantWithId(id):
    method = request.method
    conn = db.connect()
    cur = conn.cursor()

    try:
        cur.execute('''SELECT * FROM restaurants WHERE post_id=%s''', (id,))
        rv = cur.fetchmany(1) # fetchone() may not function well with a helper function fetchRows; use fetchmany(1) instead
        print("retrun value fgro db", rv)
        if not rv:
            raise NoQueryResultError
        else:
            rows = fetchRows(cur, rv)

        if method == 'DELETE':
            cur.execute('''DELETE FROM restaurants WHERE post_id=%s''', (id,))
            conn.commit()
            return "Deleted entry {id:0>5d}!".format(id=id)

        if method == 'PUT':
            # set names to the request args or else the name already in the db
            args = {}
            for key, ref in zip(['name', 'location', 'image'], ['restaurant_name', 'restaurant_address', 'image']):
                args[key] = request.args.get(key)
                if not args[key]:
                    args[key] = rows[0][ref]
            cur.execute('''UPDATE restaurants SET restaurant_name=%s, restaurant_address=%s, image=%s WHERE post_id=%s''',
                        (args['name'], args['location'], args['image'], id))
            conn.commit()
            return re.sub(r'[\[\]\']', '', '''Updated entry as Restaurant Name to {name:}'''.format(**request.args))

    except NoQueryResultError as noMatch:
        return noMatch.msg
    finally:
        conn.close()

    return jsonify (rows)
