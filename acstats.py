import sys
import requests
from requests.auth import HTTPBasicAuth 

# assumes you have done a "pip install beautifulsoup4"
from bs4 import BeautifulSoup

if  len(sys.argv) < 3:
    print("syntax:  python acstats.py] [W3C user name] [W3C password]")
    quit()

# Load the HTML meeting minutes
resp = requests.get(sys.argv[1], auth = HTTPBasicAuth(sys.argv[2], sys.argv[3]))
result = resp.text

#parse the minutes into a Beautiful Soup tree
soup = BeautifulSoup(result, features="lxml")

# extract a list of all <cite> elements
c = soup.find_all('cite')

# build a list of the speaker names, encoded as the contents of <cite> elements in the HTML
names = []
for person in c:
    names.append(person.text)

# build a dictionary of speaker statistics; r name as the key and number of times speaking as the value
stats = {}
for i in names:
    if i in stats:
        stats[i] += 1
    else:
        stats[i] = 1

# walk the dictionary in reverse order of the values 
sort_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

# show speaker stats sorted by most frequent speaker

print("%4d speakers during %s" %(len(sort_stats), sys.argv[1]))

for s in sort_stats:
    print("%20s,  %4d  " %(s[0], s[1])) 
