
# Archived

This was my first project to go live and my first entrepreneurship, by that time (2014-2015) I did not know about git, so I did not use it to save development progress. There was a sublime plugin called Sublime Merge that I used instead.

This project was made with

- Django 1.8 (this is based on a template system views, so there is no Restful API)
- Postgres
- Bootstrap 3, CSS 3 and HTML 5 that by that time it was the coolest thing to work with

To run this project, after successfully installed all the packages in `requirements.txt` in a python 2.7 enviroment (maybe in a Ubuntu 16)

```
cd wsgi/hv
python manage.py makemigrations
python manage.py migrate
python manage.py shell
```

Inside the shell run the following
```
from geoservicios.hv.views import inicializar_idiomas, inicializar_categorias, inicializar_niveles
inicializar_idiomas()
inicializar_categorias()
inicializar_niveles()
```

The exit and run
`python manage.py createsuperuser`

And your done with the setup.

By default it will try to create an Sqlite database and run on the port 8000

Even when as a business I could not achieve success, I learned python, css, business related stuff too (Business model canvas, Customer Journey, etc), marketing (I achieved a little more than 300 likes on a weekend, sadly the account was blocked by facebook. I did not know that I could not create an account on facebook with a company name).

After that, I runned out of money to keep running the business, so I focused on ending my college carrer.

I also attended to a few entrepreneur programs with this idea to try to compete (that is where I learned that I needed to work on my selling skills). https://www.instagram.com/p/BC3dZUCguij

This project was a marketplace for digital jobs aiming to solve or reduce the Venezuela crisis by the year 2014, and then hopefully extend to Latin America later on. You could see the demo on this youtube video  `https://youtu.be/EGY_NsZGuSc`

There was not too much competition, actually my direct rival apps where freelance.com and fiverr.com. Big, but not with a strong presence at the time in Latin America.

I leave it here just to remind me someday how much progress I have made since then.
