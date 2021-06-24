# code adapted from scripts made by users ZipBomb and saracoop on Github 
import spotipy
import spotipy.util as util
import json
import pandas as pd
import urllib
import urllib.request

usn = 'REDACTED :)'
client_id = 'REDACTED :)'
secret_id = 'REDACTED :)'
redirect_uri = 'http://localhost:8888/callback'
gather_type = 'user-library-read'

token = util.prompt_for_user_token(username = usn,
								   scope = gather_type,
								   client_id = client_id,
								   client_secret = secret_id,
								   redirect_uri = redirect_uri)


spotify = spotipy.Spotify(auth = token) #auth = token

valid_genres = []

# genres list taken from ZipBomb's Github page for selecting a random spotify song from the API
# I also edited the file to ensure that we have a smaller, but still aesthetically diverse set of genre labels
# currently 75 genres
with open('genres.json', 'r') as infile:
	valid_genres = json.load(infile)

print('success loading genres, size of list: ' + str(len(valid_genres)))
#valid_genres = [v.replace(" ", "-") for v in valid_genres]

# NECESSARY LISTS IN USE ORDER
# get artist ids
allartists = []
# general album id list
idList = []
# album art urls
artURLs = []
# genre list
genreList = []

# MAIN LOOP

# get unique artist ids
# HAVE TO REDO singer songwriter - classical [11:16]
# AS WELL AS post punk - vaporwave [21:26]
# CHANGE THE URL LINKS!!!!!!!!
print("starting artist by genre search...")
for genre in valid_genres[21:26]:
	# search list of artists that fall under the current genre 
	artists = []
	for i in range(0, 100, 50):
		nice = spotify.search(q = 'genre:\"' + genre + "\"", type = 'artist', limit = 50, offset = i)
		# iterate over artist ids from genre query
		for i, item in enumerate(nice['artists']['items']):
			# append artist id to both lists if not already added to master list, don't want duplicates
			if item['id'] not in allartists:
				allartists.append(item['id'])
				artists.append(item['id'])
	# print # of artists for current genre
	print("artists queried for genre " + genre + "!" + " size: " + str(len(artists)))
	# query albums of artists we've gathered
	print("gathering albums for each artist under genre " + genre + "...")
	for a in artists:
		query = spotify.artist_albums(a)
		for i, item in enumerate(query['items']):
			# append to idList
			idList.append(item['id'])
	# print # of albums gathered
	print("albums queried! size: " + str(len(idList)))
	# query all artists' albums and label them w/ current genre, since spotify api is absolute ass and is poorly documented!!!
	print("getting album art...")
	for id in idList:
		album = spotify.album(id)
		# store info
		if len(album["images"]) == 3:
			genreList.append(genre)
			artURLs.append(album['images'][2]['url'])
	# confirmation statement
	print("album info gathered for " + genre + "! size of arrays should be equal... " + str(len(genreList)) + " " + str(len(artURLs)))

# DOWNLOAD IMAGES
i = 131671 # where loop 3 ended
downloadedURLs = []
print("downloading urls...")
for url in range(len(artURLs)):
    urllib.request.urlretrieve(url = artURLs[url], 
      filename = "AlbumArt/{}.jpg".format("Album"+str(i)))
    downloadedURLs.append("/Users/johncorio/Documents/EECS 442 Files/project/AlbumArt/Album{}.jpg".format(str(i)))
    i = i + 1

# EXPORT TO CSV FILE
print("exporting to csv file... ") 
fields = {'Art Link' : downloadedURLs, 'Genre' : genreList, 'jpg' : ['.jpg' for i in range(len(artURLs))]}
df = pd.DataFrame(fields)
df.to_csv('ProjectData3.csv')
