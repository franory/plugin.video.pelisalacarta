# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "aquitorrent"
__category__ = "F"
__type__ = "generic"
__title__ = "Aquitorrent"
__language__ = "ES"

host = "http://www.aquitorrent.com/"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.aquitorrent mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas"      , action="peliculas", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS", thumbnail="http://imgc.allpostersimages.com/images/P-473-488-90/37/3710/L3YAF00Z/posters/conrad-knutsen-cinema.jpg", fanart="http://bancofotos.net/photos/20141124141682717398995.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Series", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=SERIES", thumbnail="http://bancofotos.net/photos/20141124141683328161849.jpg", fanart="http://bancofotos.net/photos/20141124141683047131743.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas HD", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Peliculas%20HD", thumbnail="http://bancofotos.net/photos/20141124141683309115283.jpg", fanart="http://bancofotos.net/photos/20141124141686953165098.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas 3D", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%203D", thumbnail="http://bancofotos.net/photos/20141124141683192143137.jpg", fanart="http://bancofotos.net/photos/20141124141683172290509.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Películas V.O.S.", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%20V.O.S.", thumbnail="http://bancofotos.net/photos/20141125141690985115975.jpg", fanart="http://bancofotos.net/photos/20141125141691013365023.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Docus y TV", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Docus%20y%20TV",  thumbnail="http://bancofotos.net/photos/20141125141692486934931.jpg", fanart="http://bancofotos.net/photos/20141125141692618165662.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Clásicos Disney", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=CLASICOS%20DISNEY", thumbnail="http://bancofotos.net/photos/20141125141692719118972.jpg", fanart="http://bancofotos.net/photos/20141125141692728192361.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="F1 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=F1%202014", thumbnail="http://bancofotos.net/photos/20141125141692996162712.png", fanart="http://bancofotos.net/photos/20141125141693002355368.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="MotoGP 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=MotoGP%202014", thumbnail="http://bancofotos.net/photos/20141125141693075137401.jpg", fanart="http://bancofotos.net/photos/20141125141693097147835.jpg"))
    itemlist.append( Item(channel=__channel__, action="peliculas", title="Mundial 2014", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Mundial%202014", thumbnail="http://bancofotos.net/photos/20141125141694744338051.png", fanart="http://bancofotos.net/photos/20141125141694642206662.jpg"))
    itemlist.append( Item(channel=__channel__, action="search", title="Buscar...", url="", thumbnail="http://bancofotos.net/photos/20141126141699798171439.jpg", fanart="http://bancofotos.net/photos/20141126141699787152701.jpg"))
    
    

    return itemlist


                

def search(item,texto):
    logger.info("[pelisalacarta.aquitorrent search texto="+texto)
    
    item.url = "http://www.aquitorrent.com/buscar.asp?pagina=1&buscar=%s" % (texto)
    try:
        fanart="http://s9.postimg.org/lmwhrdl7z/aquitfanart.jpg"
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []




def peliculas(item):
    logger.info("pelisalacarta.aquitorrent peliculas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #quitamos los titulos de los href en enlaces<
    data = re.sub(r'&/[^"]+">','">',data)
    
    patron = '<div class="div_pic" align="center">'
    patron += '<a href="([^"]+)".*?>'
    patron += '<img src="([^"]+)".*?'
    patron += 'alt="([^"]+)"'
    

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
   
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        # Arregla la url y thumbnail
        #scrapedurl = fix_url(scrapedurl)
        scrapedthumbnail = fix_url(scrapedthumbnail)

        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action="findvideos", fanart="http://s9.postimg.org/lmwhrdl7z/aquitfanart.jpg", thumbnail=scrapedthumbnail) )

    ## Paginación
    pagina = int(scrapertools.get_match(item.url,"pagina=(\d+)"))+1
    pagina = "pagina=%s" % (pagina)
    next_page = re.sub(r"pagina=\d+", pagina, item.url)
    if pagina in data:
        itemlist.append( Item(channel=__channel__, title=">> Página siguiente", url=next_page,
            action="peliculas", folder=True) )


    
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.aquitorrent findvideos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    # Torrent en zip
    patron = '<td class="wrapper_pic_td">.*? '
    patron+= 'alt="([^"]+)".*? '
    patron+= 'href="(.*?\.zip)".*?'
    patron+= '"2"><br><br>(.*)<br><br><img'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        for scrapedtitle, scrapedzip, scrapedplot in matches:
            plotformat = re.compile('(.*?:).*?<br />',re.DOTALL).findall(scrapedplot)
            for plot in plotformat:
                scrapedplot = scrapedplot.replace(plot,"[COLOR green][B]"+plot+"[/B][/COLOR]")
            scrapedplot = scrapedplot.replace("<br />","[CR]")
            scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
            # Arregla la url y extrae el torrent
            scrapedtorrent = unzip(fix_url(scrapedzip))
                    
            itemlist.append( Item(channel=__channel__, title =item.title+" [torrent]" , url=scrapedtorrent, plot=scrapedplot, action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.thumbnail , folder=False) )

    #Vamos con el normal

    patron = '<td class="wrapper_pic_td">.*? '
    patron+= 'alt="([^"]+)".*? '
    patron+= 'href="(magnet[^"]+)".*?'
    patron+= 'title="Visionado Online".*?'
    patron += '<a href="http://www.bitlet.org/video/play.torrent=([^&]+)&.*?'
    patron+= '<br><br>>(.*)<br><br><img'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedtitle, scrapedmagnet, scrapedtorrent, scrapedplot in matches:
        # Busca las etiquetas en scrapedplot
        plotformat = re.compile('(.*?:).*?<br />',re.DOTALL).findall(scrapedplot)
        # Reemplaza las etiquetas con etiquetas formateadas con color azul y negrita
        for plot in plotformat:
            scrapedplot = scrapedplot.replace(plot,"[COLOR green][B]"+plot+"[/B][/COLOR]")
         # reemplaza los <br /> por saltos de línea del xbmc
        scrapedplot = scrapedplot.replace("<br />","[CR]")
         # codifica el texto en utf-8 para que se puedan ver las tíldes y eñes
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
            
        
    
        
        itemlist.append( Item(channel=__channel__, title =item.title+" [magnet]" , url=scrapedmagnet, plot=scrapedplot, action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.thumbnail , folder=False) )
        itemlist.append( Item(channel=__channel__, title =item.title+" [torrent]" , url=scrapedtorrent, plot=scrapedplot, action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.thumbnail ,folder=False) )
    #nueva variacion
    if len(itemlist) == 0:
        patron = '<td class="wrapper_pic_td">.*? '
        patron+= 'alt="([^"]+)".*? '
        patron+= 'href="([^"]+)".*?'
        patron+= '<br><br>(.*?)<br><br>'
    
    
        matches = re.compile(patron,re.DOTALL).findall(data)
    
        for scrapedtitle, scrapedtorrent, scrapedplot in matches:
            
            # codifica el texto en utf-8 para que se puedan ver las tíldes y eñes
            scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")


        
        
        
        itemlist.append( Item(channel=__channel__, title =item.title+" [torrent]" , url=scrapedtorrent, plot=scrapedplot, action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.thumbnail , folder=False) )


    
    return itemlist


def fix_url(url):
    if url.startswith("/"):
        url = url[1:]
        if not url.startswith("http://"):
            url = host+url
    return url

def unzip(url):
    import zipfile
    
    # Path para guardar el zip como tem.zip los .torrent extraidos del zip
    torrents_path = config.get_library_path()+'/torrents'
    if not os.path.exists(torrents_path):
        os.mkdir(torrents_path)

    ## http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
    # Open the url
    try:
        f = urllib2.urlopen(url)
        with open( torrents_path+"/temp.zip", "wb") as local_file:
            local_file.write(f.read())
        
        # Open our local file for writing
        fh = open(torrents_path+"/temp.zip", 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, torrents_path)
        fh.close()

    #handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url

    torrent = "file:///"+torrents_path+"/"+name

    if not torrents_path.startswith("/"):
        torrents_path = "/"+torrents_path
    
    torrent = "file://"+torrents_path+"/"+name
    
    return torrent
