nic.ar.scrape
-------------

Scrape del sitio NIC.AR para leer info de dominios con el nuevo sitio 2013

Uso

	python nicarscrape.py dominioabuscar

o

	python nicarscrape.py dominioabuscar send

para enviar los datos del scrape via json-post a tu servidor

Mas info en 
	http://andresvazquez.com.ar/data/nic-argentina

**Solo busca por ahora dominio .com.ar**

*Basado en el repo https://github.com/gonzafirewall/PycNic del usuario GIT @gonzafirewall*

Como automatizar el scrape?
---------------------------------------------

El script *getOldestUpdated.py* permite automatizar el proceso de en base a una lista de dominios (provista de un servicio web externo que deberás desarrollar)
Además este script envia a un servicio externo los resultados del scrape. Este servicio externo (que deberás desarrollar) puede por ejemplo almacenarlos en una base de datos.  
Esta herramienta es externa debe proveer en formato JSON los dominios a buscar en NIC.  
En el archivo de configuración *config.ini* (en base a *config.ini.sample* deben indicarse las URLs de pedido de dominios a buscar y de envio de las respuestas que esta herramienta recolecta)

La variable: *readDomainsFrom* debe ser de la forma:  
 * http://mi-servicio-externo.com/proveedor-de-dominios-a-buscar.com/%s (donde **%s** es obligatorio e indicará la cantidad de dominios que se pidieron desde el script *getOldestUpdated.py*)  
La variable *postDomainsTo* es de la forma http://mi-servicio-externo.com/add/dominio/ (a modo de ejemplo)  
La variable *scraperFolder* es el path donde estan los scrips de este repositorio, por ejemplo */home/yo/dev/nic.ar.scrape/*  
  
Antes de ejecutar estos scripts se requiere que tengas instalado python y las librerías:  
requests  
mechanize  
beautifulsoup4  
En general podras instalarlas con el comando *pip*

Podrás probar si todo funciona ejecutando desde la consola:  
**/home/yo/dev/nic.ar.scrape/getOldestUpdated.py 3** (traera y procesará 3 dominios)
Si usas numeros muy grandes o los ejecutas muy seguido NIC bloquera tu IP. Usalo prudentemente.  
  
  
Si todo funciona puedes dar de alta un *cron* que por ejemplo actualice un dominio cada 3 minutos.


