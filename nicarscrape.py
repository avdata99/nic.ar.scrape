# -*- coding: utf-8 -*-
from mechanize import Browser
from bs4 import BeautifulSoup as bs
import re
import ConfigParser
import os
from datetime import datetime
from random import randint
import time


class Nicarscrape(object):
    def __init__(self):
        self.url = "https://nic.ar"
        self.br = Browser()
        #self.br.addheaders = [('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36'),('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        self.br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        """
        self.br.addheaders = [('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36')
                ,('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
                #,('Accept-Encoding','gzip,deflate')
                ,('Accept-Language','es-419,es;q=0.8,ca;q=0.6,en;q=0.4,fr;q=0.2,it;q=0.2,pt;q=0.2,ro;q=0.2')
                ,('Connection','keep-alive')]
        """
        self.Config = ConfigParser.ConfigParser()
        here = os.path.dirname(os.path.abspath(__file__))
        self.Config.read(os.path.join(here, "config.ini"))


    def ask_domain(self, domain, printit=True):
        urldom = "%s%s" % (self.url, "/buscarDominio.xhtml")
        res = self.br.open(urldom)
        try:
            self.br.select_form(name="busquedaDominioForm2")
        except Exception, e:
            # shit, HTML change?
            response = res.read()
            if "Algo sali&oacute; mal." in response:
                print "mmmm, 'Algo salio mal' dice el servidor "
                return False

            print "HTML changed?. FORMs:"
            for form in self.br.forms():
                print form.name
            print "Error %s %s" % (str(e), repr(e))
            print "-------HEADERS-------------"
            print res.info()
            print "-------BODY----------------"
            print res.read()
            return False

        self.br['busquedaDominioForm2:dominio'] = domain
        # check for captcha div ID "recaptcha_widget_div"
        if "recaptcha_response_field" in res.read():
            print "------ HABEMUS CAPTHCA ------"
            captcha = randint(100, 999)
            self.br['recaptcha_response_field'] = str(captcha)

        res = self.br.submit()
        thehtml = res.read()
        data = self.parse_domain(domain, thehtml)
        if printit:
            print data

        if data == False: # error
            return False
        return data

    def parse_domain(self, domain, html):
        soup = bs(html)
        # print (soup.prettify('latin-1'))

        disponible = soup.find(text=re.compile('El dominio se encuentra disponible'))
        if disponible:
            return {'dominio': domain, 'result': False, 'cerror': 'AVAILABLE', 'error': 'No se encontraron datos'}

        invalido = soup.find(text=re.compile('El nombre de dominio que ingresaste no es '))
        if invalido:
            return {'dominio': domain, 'result': False, 'cerror':'INVALID' , 'error': 'Dominio invalido'}

        """ They start changing the ID!
        table = soup.find('tbody', {'id': 'dominioNoDisponibleForm:j_idt60_data'})
        table = soup.find('tbody', {'id': 'dominioNoDisponibleForm:j_idt61_data'})
        table = soup.find('tbody', {'id': 'dominioNoDisponibleForm:j_idt62_data'})
        """
        table = soup.find('tbody')
                
        if table == None:
            print "Can't find spected table"
            print html
            return False

        trs = table.find_all('tr')
        dominio = {}
        for tr in trs:
            tds = tr.find('td', {'role': 'gridcell'})
            div = tds.find('div', {'class': 'ui-dt-c'})
            campo = div.find('span')
            # I need to remove for reading following text
            div.span.extract()
            dominio[campo.string.strip()] = div.string.strip()

        dominio["dominio"] = domain
        dominio["result"] = True
        return dominio


if __name__ == "__main__":
    import sys

    dom = sys.argv[1]

    print "Inicializando nicarscrape"
    nic = Nicarscrape()
    r = randint(12, 27)
    print "***********************************"
    print "********* Buscando %s" % dom
    print "********* starting at %s" % str(datetime.now())
    print "***********************************"

    lastime = datetime.now()
    dom = nic.ask_domain(dom, printit = False)
    if dom == False:
        print "Error on ASK_DOMAIN"
        sys.exit()

    print "Recibido en %s " % str(datetime.now() - lastime)
    print dom

    if len(sys.argv) == 2:
        print "Terminado"
        sys.exit()

    # maybe you want to send this to your server (define it your config.ini)
    if sys.argv[2] == "send":
        print "Enviando datos ..."
        
        # send this data (via config.ini)
        import hashlib
        # solo para asegurate que version de tu script lo envia
        dom["md5"] = hashlib.md5(open(sys.argv[0]).read()).hexdigest()

        import requests, requests.utils, pickle
        import json
        datasend = json.dumps(dom)
        headers = {'content-type': 'application/json'}
        s = requests.session()
        url = nic.Config.get("servers", "postDomainsTo")
        req = requests.Request('POST', url, data=datasend, headers=headers)
        prepped = req.prepare()
        print "recibiendo ..."
        lastime = datetime.now()
        r = s.send(prepped, stream=False)
        print "Info enviada en %s, gracias por colaborar" % str(datetime.now() - lastime)

        r = randint(9, 21)
        print "********* Wait %d" % r
        time.sleep(r)
        



