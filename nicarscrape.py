# -*- coding: utf-8 -*-
from mechanize import Browser
from bs4 import BeautifulSoup as bs
import re
import ConfigParser
import os


class Nicarscrape(object):
    def __init__(self):
        self.url = "https://nic.ar"
        self.br = Browser()
        self.br.addheaders = [('user-agent',
                               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36'
                              ),
                            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        self.Config = ConfigParser.ConfigParser()
        here = os.path.dirname(os.path.abspath(__file__))
        self.Config.read(os.path.join(here, "config.ini"))


    def ask_domain(self, domain, printit=True):
        urldom = "%s%s" % (self.url, "/buscarDominio.xhtml")
        self.br.open(urldom)
        self.br.select_form(name="busquedaDominioForm2")
        self.br['busquedaDominioForm2:dominio'] = domain
        res = self.br.submit()
        thehtml = res.read()
        data = self.parse_domain(domain, thehtml)
        if printit:
            print data
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

        table = soup.find('tbody', {'id': 'dominioNoDisponibleForm:j_idt60_data'})
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
    print "Buscando %s" % dom
    dom = nic.ask_domain(dom, printit = False)
    print "Recibido"
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

        import requests
        import json
        datasend = json.dumps(dom)
        headers = {'content-type': 'application/json'}
        print "recibiendo ..."
        r = requests.post(nic.Config.get("servers", "postDomainsTo"), data=datasend, headers=headers)

        print "Info enviada, gracias por colaborar"
        #print unicode(r.text)


