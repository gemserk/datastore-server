Datastore Server
=============

Datastore-server is a Google App Engine web application written in Python which allows you to manage game high scores remotely.

Installation
-------

The application is really easy to install and use, first download and install [Google App Engine SDK for Python][gae-sdk], and download [datastore-server][datastore-server] from Github.

After that, open [Google App Angine][gae], login with a Google account and create a new application with the name you want for your highscores server, for example, MyGameScoresSystem.

Finally, go to the datastore-server folder and upload the application following this [tutorial][gae-upload].

Your application should be ready to be accessed by opening http://yourapplicationid.appspot.com

Congratulations, you have your Google App Engine high scores application ready :D

Creating Games
-------

After the web application is installed, you will need to create a Game key to be used inside your game to identify it uniquely on datastore-server. 

To do so, open your application at http://yourapplicationid.appspot.com, and Sign in with your google account. 

Now, fill the new Game form by setting a key and a name. The key is a string, in our case we are creating it by calculating the md5sum of the game's name, for example, key = md5sum("Minecraft"), and name = Minecraft. Click submit and you will have a game created.

Usage
-------

The application has different webservices, to simplify usage if you are using Java, there is a Java library named [datastore][datastore] which encapsulates all http requests through a simple API. 

If you are using another language or want to access directly to those web services, you will have to wait we write a guide for them.

TODO: Write docs specifying which web services exists and how to access them.

Web Interface
-------

It also has some pages to help you manage the game scores, 


- The main page which shows a list of games and lets you create new games, at `/`

- Profiles page, shows you all registered profiles at `/profiles`

- Game scores page, shows you all scores of one specific game, at `/game` with the following parameters:

	gameKey 	- required - the key of the game.
	tag* 		- optional - one tag the scores has to have in order to be listed, could be used multiple times.
	distinct	- optional - filter one score per profile, true by default.
	range 		- optional - day/week/month to request for daily/weekly/monthly scores respectively, all scores by default.
	rangeNumber - optional - specify which day/week/month of the year, by default uses current day/week/month.

Finally
-------

That's all for now, explore the API by yourself and propose improvements by suggesting new stuff on [Issues][issues] page.

[gae-sdk]: http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python
[gae]: https://appengine.google.com/
[gae-upload]: http://code.google.com/appengine/docs/python/gettingstarted/uploading.html
[datastore-server]: git://github.com/gemserk/datastore-server.git
[datastore]: https://github.com/gemserk/datastore
[issues]: https://github.com/gemserk/datastore-server/issues
