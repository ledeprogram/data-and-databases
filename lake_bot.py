import pg8000
import twython
import random

api_key = "your api key"
api_secret = "your api secret"
access_token = "your access token"
token_secret = "your token secret"

def random_lake_sentence(lakes, sentences):
    lake = random.choice(lakes)
    possible_keys = [k for k in lake.keys() if k != 'name' \
            and lake[k] is not None]
    col = random.choice(possible_keys)
    sentence_template = sentences[col]
    output = sentence_template.format(lake['name'], lake[col])
    return output

twitter = twython.Twython(api_key, api_secret, access_token, token_secret)

lakes = []

conn = pg8000.connect(database="mondial") # may need extra auth info!
cursor = conn.cursor()
cursor.execute("SELECT name, area, depth, elevation, type, river FROM lake")
for row in cursor.fetchall():
    lake = {'name': row[0],
           'area': row[1],
           'depth': row[2],
           'elevation': row[3],
           'type': row[4],
           'river': row[5]}
    lakes.append(lake)

sentences = {
    'area': 'The area {} is {} square kilometers.',
    'depth': 'The depth of {} is {} meters.',
    'elevation': 'The elevation of {} is {} meters.',
    'type': 'The type of {} is {}.',
    'river': '{} empties into a river named {}.'
}

flare = ["Wow!", "Cool, huh?", "Now you know.", "WHAAAAT", "Neat-o!!"]
output = random_lake_sentence(lakes, sentences) + " " + random.choice(flare)
twitter.update_status(status=output)
