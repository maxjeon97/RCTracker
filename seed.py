"""Initial data."""

from models import City, Cafe, Restaurant, db, User

from app import app

db.drop_all()
db.create_all()


#######################################
# add cities

sf = City(code='sf', name='San Francisco', state='CA')
berk = City(code='berk', name='Berkeley', state='CA')
oak = City(code='oak', name='Oakland', state='CA')
la = City(code='la', name='Los Angeles', state='CA')
chinohills = City(code='chinohills', name='Chino Hills', state='CA')

db.session.add_all([sf, berk, oak, la, chinohills])
db.session.commit()


#######################################
# add cafes

c1 = Cafe(
    name="Bernie's Cafe",
    description='Serving locals in Noe Valley. A great place to sit and write'
    ' high quality code.',
    address="3966 24th St",
    city_code='sf',
    url='https://www.yelp.com/biz/bernies-san-francisco',
    image_url='https://s3-media4.fl.yelpcdn.com/bphoto/bVCa2JefOCqxQsM6yWrC-A/o.jpg'
)

c2 = Cafe(
    name='Perch Coffee',
    description='Hip and sleek place to get cardamom lattés when biking'
    ' around Oakland.',
    address='440 Grand Ave',
    city_code='oak',
    url='https://perchoffee.com',
    image_url='https://s3-media4.fl.yelpcdn.com/bphoto/0vhzcgkzIUIEPIyL2rF_YQ/o.jpg',
)

c3 = Cafe(
    name='Tastea',
    description='Boba shop that also sells fairly decent food items',
    address='4711 Chino Hills Pkwy STE D',
    city_code='chinohills',
    url='https://www.yelp.com/biz/tastea-chino-hills-9',
    image_url='https://s3-media0.fl.yelpcdn.com/bphoto/evOJO3TmD5MErGnb1LXPog/o.jpg',
)

db.session.add_all([c1, c2, c3])
db.session.commit()

#######################################
# add restaurants

r1 = Restaurant(
    name="San Tung",
    description='Famed dry fried chicken wings, handmade noodles & other Chinese eats in a no-frills setting.',
    address="1031 Irving St",
    city_code='sf',
    url='https://www.yelp.com/biz/san-tung-san-francisco-2',
    image_url='https://s3-media0.fl.yelpcdn.com/bphoto/yivaM7rvfGDtz9W03ZHuIA/o.jpg'
)

r2 = Restaurant(
    name='Base Camp',
    description='Nepali cuisine combining unique spices with California produce.',
    address='2400 Folsom St',
    city_code='sf',
    url='https://www.yelp.com/biz/base-camp-san-francisco',
    image_url='https://s3-media0.fl.yelpcdn.com/bphoto/u2gPwij3vgb6mnkxl2ewbQ/o.jpg',
)

r3 = Restaurant(
    name='Tsujita LA',
    description='Buzzing, modern Japanese outpost serving ramen at lunch, plus sushi & à la carte dinners.',
    address='2057 Sawtelle Blvd',
    city_code='la',
    url='https://www.yelp.com/biz/tsujita-la-artisan-noodle-los-angeles-2',
    image_url='https://s3-media0.fl.yelpcdn.com/bphoto/1eL0BgAfdh9Z0pACyDE4Qg/o.jpg',
)

db.session.add_all([r1, r2, r3])
db.session.commit()


#######################################
# add users

ua = User.register(
    username="admin",
    first_name="Addie",
    last_name="MacAdmin",
    description="I am the very model of the modern model administrator.",
    email="admin@test.com",
    password="secret",
    admin=True,
)

u1 = User.register(
    username="test",
    first_name="Testy",
    last_name="MacTest",
    description="I am the ultimate representative user.",
    email="test@test.com",
    password="secret",
)

db.session.add_all([ua, u1])
db.session.commit()


#######################################
# add likes

u1.liked_cafes.append(c1)
u1.liked_cafes.append(c2)

ua.liked_cafes.append(c1)

u1.liked_restaurants.append(r1)
u1.liked_restaurants.append(r2)

ua.liked_restaurants.append(r1)

db.session.commit()


#######################################
# maps

c1.save_cafe_map()
c2.save_cafe_map()
c3.save_cafe_map()

r1.save_restaurant_map()
r2.save_restaurant_map()
r3.save_restaurant_map()

db.session.commit()
