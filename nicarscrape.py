from mechanize import Browser
from bs4 import BeautifulSoup as bs
import re
import sys

class Nicarscrape(object):
    def __init__(self):
        self.url = "https://nic.ar"
        self.br = Browser()
        self.br.addheaders = [('user-agent',
                               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36'
                              )]

    def ask_domain(self, domain):
        urldom = "%s%s" % (self.url, "/buscarDominio.xhtml")
        self.br.open(urldom)
        self.br.select_form(name="busquedaDominioForm2")
        self.br['busquedaDominioForm2:dominio'] = domain
        res = self.br.submit()
        thehtml = res.read()
        data = self.parse_domain(thehtml)
        print data

    def parse_domain(self, html):
        soup = bs(html)
        vacio = soup.find(text=re.compile('El dominio se encuentra disponible'))
        if vacio:
            return {'result': False, 'error': 'No se encontraron datos'}

        table = soup.find('tbody', {'id': 'dominioNoDisponibleForm:j_idt60_data'})
        trs = table.find_all('tr')
        dominio = {}
        for tr in trs:
            tds = tr.find('td', {'role': 'gridcell'})
            div = tds.find('div', {'class': 'ui-dt-c'})
            campo = div.find('span')
            # I need to remove for reading following text
            div.span.extract()
            dominio[campo.string] = div.string

        return dominio



a = Nicarscrape()
dom = sys.argv[1]
print "Buscando %s" % dom
a.ask_domain(dom)
