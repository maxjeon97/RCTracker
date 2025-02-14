## RCTracker

RCTracker is a way for you to keep track of your favorite cafes and restaurants.
Logged in users can browse the existing locations and can request to obtain admin privileges,
allowing them to add their own cafes and restaurants to the application.

<br/>

See deployed app <a href="https://rctracker.onrender.com/">here</a>.
<br/>
<br/>
Login with these credentials if you do not wish to make an account:
<br/>
Username: test
<br/>
Password: secret

### Features
* __Authentication__: Users can sign up, log in, and log out. Passwords are hashed with bcrypt.
* __Authorization__: Protect routes so only authorized users can view.
* __Likes__: Authenticated users can like/unlike restaurants and cafes. Likes will show up on their profile page.
* __Add/Remove Cities, Cafes, Restaurants__: Users with admin privileges can add or remove covered cities, cafes, and restaurants.
* __Profile management__: Authenticated users can edit account information.


### Built With

* [![Flask][Flask.com]][Flask-url]
* [![SQLAlchemy][SQLAlchemy.com]][SQLAlchemy-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]


### Installation

1. Clone the repo:
   ```
   git clone https://github.com/maxjeon97/rctracker
   ```
2. cd into project directory and create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
 4. Set up database:
    ```
    createdb warbler
    python seed.py
    ```
5. Create a .env file with following variables:
    ```
    SECRET_KEY=abc123
    DATABASE_URL=postgresql:///flask_cafe
    ```
6. Start the server:
    ```
    flask run
    ```



### Testing

There are four test files for testing data models and views for messages and users.

Run test files with the following command:

```
FLASK_DEBUG=False python -m unittest <name-of-test-file>
```



[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Flask.com]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[PostgreSQL.com]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[SQLAlchemy.com]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
