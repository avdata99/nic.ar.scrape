# obtener los dominios menos actualizados via api y procesarlos
# la cantidad de dominios se puede especificar via sys.argv[1]

import json
import urllib2
import time
import os
from random import randint
import sys
import ConfigParser

here = os.path.dirname(os.path.abspath(__file__))
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(here,"config.ini"))

print "BUSCANDO \n"
tot = 1
if len(sys.argv) > 0:
    tot = sys.argv[1]

url = Config.get("servers", 'readDomainsFrom')
url = url % tot
print url
response=urllib2.urlopen(url)
print response
data = json.load(response)

print "ENCONTRADO \n"
print data

print "RESULTADOS \n"
print data["result"]

c = 0
for f in data["result"]:
    c = c + 1
    print "\nDATA\n %s" % f
    print "OK %s lastUpdate %s" % (f["dominio"], f["lastUpdated"])
    dom = f["dominio"].replace(".com.ar", "").encode("latin-1")
    print "\n******\n %s \n*******\n" % dom

    cmd = "python %snicarscrape.py %s send" % (Config.get("servers", "scraperFolder"), dom)
    cmd = unicode(cmd)
    test = os.system(cmd)

    print "\nprocesando %i de %s" % (c, tot)
    if c < int(tot):
        r = randint(2, 9)
        time.sleep(r)
