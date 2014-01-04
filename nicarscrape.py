from mechanize import Browser
from bs4 import BeautifulSoup as bs
import re

class Nicarscrape(object):
    def __init__(self):
        self.url = "https://nic.ar"
        self.br = Browser()
        self.br.addheaders = [('user-agent',
                               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36'
                              )]

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
    a = Nicarscrape()
    print "Buscando %s" % dom
    dom = a.ask_domain(dom, printit = False)
    print "Recibido"
    print dom

    if len(sys.argv) > 2:
        if sys.argv[2] == "nosend":
            print ""
            sys.exit()

    print "Enviando datos ..."
    # send me this data
    import hashlib
    dom["md5"] = hashlib.md5(open(sys.argv[0]).read()).hexdigest()

    import requests
    import json
    datasend = json.dumps(dom)
    headers = {'content-type': 'application/json'}
    print "recibiendo ..."
    r = requests.post('http://andresvazquez.com.ar/data/nic-argentina/api/add/dominio/', data=datasend, headers=headers)

    print "Info enviada, gracias por colaborar" # r.text


