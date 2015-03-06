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
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "F,A,D,VOS"
__type__ = "generic"
__title__ = "Cultmoviez"
__channel__ = "cultmoviez"
__language__ = "ES"
__creationdate__ = "20141102"

host = "http://www.cultmoviez.info/"
wp_plugin = "/wp-content/plugins/seriesnav/seriesajaxresp.php"
fanart="http://robalo.esy.es/img/cultmoviez-poster.png"


def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cultmoviez mainlist")

    itemlist = []
    itemlist.append( Item( channel=__channel__, action="peliculas", title="Películas", url=urlparse.urljoin(host,"/archivos/peliculas"), fanart=fanart ) )
    itemlist.append( Item( channel=__channel__, action="series", title="Series", url=urlparse.urljoin(host,"/archivos/series"), fanart=fanart ) )
    itemlist.append( Item( channel=__channel__, action="commonlists", title="Documentales y Cortos", url=urlparse.urljoin(host,"/archivos/documentales"), fanart=fanart ) )
    itemlist.append( Item( channel=__channel__, action="commonlists", title="Música [Conciertos]", url=urlparse.urljoin(host,"/archivos/especiales"), fanart=fanart ) )
    itemlist.append( Item( channel=__channel__, action="search", title="Buscar", url=urlparse.urljoin(host,"/?s=%s&cat=1"), fanart=fanart ) )

    return itemlist

	
def peliculas(item):
	logger.info("pelisalacarta.channels.cultmoviez peliculas")
	itemlist = []
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Estrenos", url=urlparse.urljoin(host,"/archivos/estrenos"), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Todo", url=urlparse.urljoin(host,"/archivos/peliculas" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Comedia", url=urlparse.urljoin(host,"/archivos/peliculas?genero=comedia" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Acción", url=urlparse.urljoin(host,"/archivos/peliculas?genero=accion" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Drama", url=urlparse.urljoin(host,"/archivos/peliculas?genero=drama" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Ficción", url=urlparse.urljoin(host,"/archivos/peliculas?genero=ciencia-ficcion" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Terror", url=urlparse.urljoin(host,"/archivos/peliculas?genero=terror" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Animación", url=urlparse.urljoin(host,"/archivos/peliculas?genero=animacion" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Thriller", url=urlparse.urljoin(host,"/archivos/peliculas?genero=thriller" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Romance", url=urlparse.urljoin(host,"/archivos/peliculas?genero=romance" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Aventuras", url=urlparse.urljoin(host,"/archivos/peliculas?genero=aventuras" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Cine negro", url=urlparse.urljoin(host,"/archivos/peliculas?genero=ciencia-ficcion" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Gore", url=urlparse.urljoin(host,"/archivos/peliculas?genero=gore" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Exploitation", url=urlparse.urljoin(host,"/archivos/peliculas?genero=exploitation" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Fantasía", url=urlparse.urljoin(host,"/archivos/peliculas?genero=fantasia" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Crimen", url=urlparse.urljoin(host,"/archivos/peliculas?genero=crimen" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Intriga", url=urlparse.urljoin(host,"/archivos/peliculas?genero=intriga" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Bélico", url=urlparse.urljoin(host,"/archivos/peliculas?genero=belico" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Western", url=urlparse.urljoin(host,"/archivos/peliculas?genero=western" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Musical", url=urlparse.urljoin(host,"/archivos/peliculas?genero=musical" ), fanart=fanart ) )
	itemlist.append( Item( channel=__channel__, action="commonlists", title="Conciertos", url=urlparse.urljoin(host,"/archivos/especiales" ), fanart=fanart ) )
	return itemlist
	
	
def search(item,texto):
    logger.info("pelisalacarta.channels.cultmoviez search")
	
    itemlist = []
    # Descarga la pagina
    data = scrapertools.cache_page("http://www.cultmoviez.info/?cat=1&s=" + texto)
    logger.info("data="+data)
    # Extrae las entradas
	
    patron = '<div class="poster"[^>]+>(.*?)</div></div>'
    logger.info("patron="+patron)
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for match in matches:
        #<a class="aimg" href="http://www.cultmoviez.info/18072/nymphomaniac-vol-ii.html" rel="tooltip" title="<h2>Nymphomaniac Extended Director&#8217;s Cut: Vol. II (</strong>2013)</h2><p>Ahora podrás VerNymphomaniac Extended Director&#8217;s Cut: Vol. II (Nymphomaniac. Volume II / Nymphomaniac (2) / Nymphomaniac. Volumen 2 / Ninfomanía Vol 2) Online en HD Del director Lars von Trier Historia de una ninfómana contada por&hellip;</p><h2></h2><p></p><p><strong>Director: </strong></strong>Lars von Trier</p><p><strong>Reparto: </strong></strong>Charlotte Gainsbourg, Stellan Skarsgård, Shia LaBeouf, Willem Dafoe, Jamie Bell</p><p><strong>G&eacute;nero: </strong>Drama, Erótico, Misterio</p><p><strong>Duraci&oacute;n: </strong>178 min.</p>"><img src="https://lh3.googleusercontent.com/wabBjQbwW8oQgeyoUAa6XUM7_QiH2y19qU80couhK4s=w150-h171-no"  title="" /></a><img style="position:relative;top:-184px;left: 5px;" src="/wp-content/uploads/2013/03/hd_thumb.png" title=""><div class="mdata" style="margin-bottom:-5px;margin-top:-29px;"><center><a href="http://www.cultmoviez.info/18072/nymphomaniac-vol-ii.html"><strong>Nymphomaniac Extended Director&#8217;s Cut: Vol. II</strong></a></center><br /><p></p>
		match = re.sub(r"&#8217;","'",match)
		match = re.sub(r"&#8211;","-",match)
		match = re.sub(r"<strong>|</strong>","",match)
		title = html2symbol(scrapertools.get_match(match,'title="<h2>([^<]+)</h2>'))
		url = scrapertools.get_match(match,'<a class="aimg" href="([^"]+)"')
		thumbnail = scrapertools.get_match(match,'<img src="([^"]+)"')
		itemlist.append( Item(channel=__channel__, action="findvideos" ,title=title, url=urlparse.urljoin(host,url), thumbnail=thumbnail, fanart=fanart ) )
	
    return itemlist
	

def commonlists(item):
	
	logger.info("pelisalacarta.channels.cultmoviez commonlists")
	itemlist=[]
	data = scrapertools.cache_page(item.url)
	patron = '<div class="poster"[^>]+>(.*?)</div></div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	for match in matches:
			match = re.sub(r"&#8217;","'",match)
			match = re.sub(r"&#8211;","-",match)
			match = re.sub(r"<strong>|</strong>","",match)
			title = html2symbol(scrapertools.get_match(match,'title="<h2>([^<]+)</h2>'))
			url = scrapertools.get_match(match,'<a class="aimg" href="([^"]+)"')
			thumbnail = scrapertools.get_match(match,'<img src="([^"]+)"')
			hd=''
			hd = scrapertools.get_match(match,'</a>(.*?)<div class="mdata"')
			logger.info ("match "+match)
			if hd!='':
			    hd=' HD'
			duration=scrapertools.get_match(match,'<p>Duraci(.*?)</p>')
			duration=scrapertools.get_match(duration,'n: (.*?)min')
			logger.info("duration "+duration)
			itemlist.append( Item(channel=__channel__, action="findvideos" ,title=(title+hd), url=urlparse.urljoin(host,url), thumbnail=thumbnail, fanart=fanart, duration=duration ) )
	actual = scrapertools.get_match(data,"<span class='current'>([^<]+)</span>")
	logger.info("actual"+actual)
	#next_page = scrapertools.get_match(data,'<a class="nextpostslink"([^<]+)</a>')
	next_page = scrapertools.find_single_match(data,'<a class="nextpostslink"([^<]+)</a>')
	logger.info("s"+next_page)
	
	
	if next_page!="":
		url = scrapertools.get_match(next_page,'href="([^"]+)"')
		itemlist.append( Item(channel=__channel__, action="commonlists" ,title="Siguiente", url=urlparse.urljoin(host,url), thumbnail="", fanart=fanart ) )
			
	return itemlist

def series(item):
    logger.info("pelisalacarta.channels.cultmoviez series")

    itemlist=[]

    data = scrapertools.cache_page(item.url)

    #<div id="seriesnav-selector" ><div id="series-list" class="column1" ><ul><li><a href="2546">Alfred Hitchcock Presents</a></li><li><a href="12892">American Horror Story</a></li><li><a href="1939">Berlin Alexanderplatz</a></li><li><a href="12869">Breaking Bad</a></li><li><a href="16037">CarnivÃ le</a></li><li><a href="10814">Cosmos</a></li><li><a href="610">Dead Set</a></li><li><a href="12800">Game of Thrones</a></li><li><a href="14461">Generation War</a></li><li><a href="17527">Misfits</a></li><li><a href="3539">Monty Python's Flying Circus</a></li><li><a href="8412">Ninja Scroll: The Series</a></li><li><a href="2860">Paranoia Agent</a></li><li><a href="10700">Riget I - El Reino I</a></li><li><a href="10728">Riget II â€“ El Reino II</a></li><li><a href="13770">Seinfeld</a></li><li><a href="7009">Serial Experiments Lain</a></li><li><a href="15188">Storm Of The Century</a></li><li><a href="17640">The Decalogue</a></li><li><a href="16148">The IT Crowd</a></li><li><a href="17573">The Returned</a></li><li><a href="14005">The Wire</a></li><li><a href="16748">True Detective</a></li><li><a href="407">Twin Peaks</a></li><li><a href="18402">V</a></li></ul></div>

    patron = '<div id="series-list" class="column1" ><ul>(.*?)</ul></div>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="(\d+)">([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for serie_id, scrapedtitle in matches:
        url_wp_plugin = urlparse.urljoin(host,wp_plugin)
        data = scrapertools.cache_page(url_wp_plugin,post="serie="+serie_id)

        #<ul><li><a href="2547">Temporada 1</a></li></ul><div id='hidden-desc'><h1>Serie: Alfred Hitchcock Presents</h1>
        #<div style="float:left;"><img title="Alfred Hitchcock Presents" src="https://lh3.googleusercontent.com/-f5ex05nP_6Q/UCrCfPf0YeI/AAAAAAAADv0/RSa4c5IP91g/s211/rsz_l_47708_dab45f82.jpg" alt="" width="132" height="175"  border="1" bordercolor="#000000" style="margin-right:10px; margin-bottom:10px;"  align="left"/></div>
        #<p><strong>Sinopsis:</strong> Alfred Hitchcock Presents es una antológica serie de televisión estadounidense presentada por Alfred Hitchcock. La serie incluye dramas, thrillers y misterios. La revista Time nombró a esta serie una de los &#8220;100 mejores programas de televisión de todos los tiempos”.</p>
        #<p><strong>Reparto:</strong> Kyle MacLachlan, Michael Ontkean, Mädchen Amick, Dana Ashbrook, Richard Beymer, Lara Flynn Boyle, Joan Chen<br />
        #<strong>Director:</strong> Alfred Hitchcock<br />
        #<strong>Género:</strong> Drama, Thriller, Misterio, Crimen<br />
        #<strong>Lenguaje:</strong> Inglés </p>
        #<h1></h1>
        #<div style="clear:both;"></div>
        #</div>

        thumbnail = scrapertools.get_match(data,'src="([^"]+)"')

        patron = '<a href="(\d+)">([^>]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)

        extra = ""
        for temporada_id, temporada in matches:
            extra+= temporada+","+serie_id+"|"

        itemlist.append( Item(channel=__channel__, action="episodios" ,title=scrapedtitle, url="",  extra=extra[:-2], thumbnail=thumbnail, fanart=fanart ) )

    return itemlist

def episodios(item):
    logger.info("pelisalacarta.channels.cultmoviez episodios")

    itemlist=[]

    matches = item.extra.split("|")

    for match in matches:
        title =  match.split(",")[0]
        serie_id = match.split(",")[1]

        url_wp_plugin = urlparse.urljoin(host,wp_plugin)
        data = scrapertools.cache_page(url_wp_plugin,post="serie="+serie_id+"&episodios=1")

        ## Datos devueltos cuando se creó la función
        #<ul><li><a href="12907">1.01 Pilot</a></li><li><a href="6836">1.02 Home Invasion</a></li><li><a href="6837">1.03 Murder House</a></li><li><a href="6838">1.04 Halloween</a></li><li><a href="6839">1.05 Halloween (2)</a></li><li><a href="6840">1.06 Piggy, Piggy</a></li><li><a href="6841">1.07 Open House</a></li><li><a href="6842">1.08 Rubber Man</a></li><li><a href="6843">1.09 Spooky Little Girl</a></li><li><a href="6844">1.10 Smoldering Children</a></li><li><a href="6845">1.11 Birth</a></li><li><a href="6846">1.12 Afterbirth</a></li></ul><div id='hidden-desc-season'></div>

        ## Datos devueltos al poco tiempo de la creación de la función
        #<ul><li><a href="12907">1.01 Pilot</a></li><li><a href="6836">1.02 Home Invasion</a></li><li><a href="6837">1.03 Murder House</a></li><li><a href="6838">1.04 Halloween</a></li><li><a href="6839">1.05 Halloween (2)</a></li><li><a href="6840">1.06 Piggy, Piggy</a></li><li><a href="6841">1.07 Open House</a></li><li><a href="6842">1.08 Rubber Man</a></li><li><a href="6843">1.09 Spooky Little Girl</a></li><li><a href="6844">1.10 Smoldering Children</a></li><li><a href="6845">1.11 Birth</a></li><li><a href="6846">1.12 Afterbirth</a></li><li><a href="5579">2.01 Welcome To Briarcliff</a></li><li><a href="6847">2.02 Tricks And Treats</a></li><li><a href="6848">2.03 Noreaster</a></li><li><a href="5732">2.04 I Am Anne Frank Pt. 1</a></li><li><a href="5818">2.05 I Am Anne Frank, Pt. 2</a></li><li><a href="5888">2.06 The Origins of Monstrosity</a></li><li><a href="5957">2.07 Dark Cousin</a></li><li><a href="11918">2.08 Unholy Night</a></li><li><a href="11921">2.09 Asylum The Coat Hanger</a></li><li><a href="13102">2.10 The Name Game</a></li><li><a href="13104">2.11 Spilt Milk</a></li><li><a href="13106">2.12 Continuum</a></li><li><a href="13108">2.13 Madness Ends</a></li><li><a href="13651">3.01 Bitchcraft</a></li><li><a href="13720">3.02 Boy Parts</a></li><li><a href="17014">3.03 The Replacements</a></li><li><a href="17067">3.04 Fearful Pranks Ensue</a></li><li><a href="17133">3.05 Burn, Witch. Burn!</a></li><li><a href="17202">3.06 The Axeman Cometh</a></li><li><a href="17242">3.07 The Dead</a></li><li><a href="17367">3.08 The Sacred Taking</a></li><li><a href="17422">3.09  Head</a></li><li><a href="17632">3.10 The Magical Delights of Stevie Nicks</a></li><li><a href="17696">3.11 Protect the Coven</a></li><li><a href="17783">3.12 Go to Hell</a></li><li><a href="17814">3.13 The Seven Wonders</a></li><li><a href="19564">4.01 Monsters Among Us</a></li><li><a href="19594">4.02 Massacres and Matinees</a></li><li><a href="19599">4.03 Edward Mordrake: Part 1</a></li><li><a href="19680">4.04 Edward Mordrake: Part 2</a></li><li><a href="19682">4.05 Pink Cupcakes</a></li><li><a href="19687">4.06 Bullseye</a></li><li><a href="19714">4.07 Test of Strength</a></li><li><a href="19735">4.08 Blood Bath</a></li><li><a href="19784">4.09 Tupperware Party Massacre</a></li><li><a href="19786">4.10 Orphans</a></li></ul>

        patron = '<a href="(\d+)">([^>]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)

        if len(matches) > 0:
            for episodio_id, episodio in matches:
                title = html2symbol(episodio.replace(".","x"))
                extra = urllib.quote_plus(episodio)+"|"+ episodio_id
                itemlist.append( Item(channel=__channel__, action="findvideos" ,title=title, url="", extra=extra, thumbnail=item.thumbnail, fanart=fanart ) )
        else:
            itemlist.append( Item(channel=__channel__, title="Aún no se han añadido episodios", thumbnail=item.thumbnail, fanart=fanart, folder=False ) )
        ## fixe: Por lo visto ha cambiado al poco tiempo de la creación de la función
        break

    itemlist = sorted(itemlist, key=lambda Item: Item.title)

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.cultmoviez findvideos")

    itemlist=[]

    try:
        serie = item.extra.split("|")[0]
        id = item.extra.split("|")[1]

        url_wp_plugin = urlparse.urljoin(host,wp_plugin)
        data = scrapertools.cache_page(url_wp_plugin,post="serie="+serie+"&episodios=1&id="+id)

        #<div style='float:left; margin-right:10px; margin-bottom:10px;'><img src='https://lh4.googleusercontent.com/-_uQM5fI03ZE/UhrwpxoqEqI/AAAAAAAAIlA/pMF4wCIgNW8/s171/rsz_american-horror-story-season-1-new-promotional-poster-american-horror-story-24824740-1125-1500.jpg' width='132' height='175'/></div><p><div><strong><u>1.01 Pilot</u></strong></div></p><div><strong>Sinopsis:</strong> Ahora podrás ver American Horror Story: Murder House 1.01 Pilot online subtitulada
        #                                            Primer capítulo de La primera temporada de American Horror Story la serie creada por Ryan Murphy y Brad Falchuk
        #                                            
        #                                            Un terapeuta y su familia se mudan de la ciudad para escaparse de sus problemas del pasado, pero rápidamente descubren que su nueva casa viene con su propio<p><div><a href='http://www.cultmoviez.info/12907'><img src='http://www.cultmoviez.info/wp-content/uploads/2013/10/ver-capitulo.png'/></a></div></p></div><div style='clear:both;'></div>

        url_for_servers_data = scrapertools.get_match(data,"<a href='([^']+)'>")
        data = scrapertools.cache_page(url_for_servers_data)
    except:
        data = scrapertools.cache_page(item.url)

    data = re.sub(r"hd=","=",data)
    data = data.replace("?&","?")

    #<iframe width="650" height="360" scrolling="no" src="http://www.cultmoviez.info/newplayer/play.php?uphd=jxr5zqbl5tdt&bshd=ge8cd4xp&fkhd=5v4vb9em/CS01E01.mp4.html&billhd=ojgo8mwi1dvz&moohd=070i7sxmckbq&plahd=3rm7pwhruyk4&upahd=1n0yqd53swtg&vbhd=ugezmymo75bg&vk1hd=oid=191530510|id=167180035|hash=57a118c8723792e6|hd%3D2&id=00C01&sub=,ES&sub_pre=ES" frameborder="0" allowfullscreen></iframe>

    # <iframe width="650" height="360" scrolling="no" src="http://www.cultmoviez.info/newplayer/play.php?bs=aeosek34&fk=t729bc9t/CultG240.mp4.html&up=k4n47ii5mgg7&vb=1wlt1mjdh5hx&dp=k8vs5y6j8&moo=p3b3vrlb421b&pla=xq5o2b930e7f&upa=22k5u2ivnts9&vk1=oid=251747296|id=169564765|hash=4947cca79d1da180|hd%3D2&v=2.0.2" frameborder="0" allowfullscreen></iframe>

    #<iframe width="650" height="360" scrolling="no" src="http://www.cultmoviez.info/newplayer/play.php?&bs=ricxefnc&fk=gamnlwjx/American.Horror.Story.S01E02.DVDRip.XviD-DEMAND.mp4.html&up=zjqtcmeio58c&id=001AHS2&sub=,ES&sub_pre=ES" frameborder="0" allowfullscreen></iframe>

    try:
        search_data_for_servers = scrapertools.get_match(data,"<iframe[^\?]+\?(.*?)&id=").split("&")
    except:
        search_data_for_servers = scrapertools.get_match(data,"<iframe[^\?]+\?(.*?)&v=").split("&")

    servers_data_list = []
    for serverdata in search_data_for_servers:
        server_id = scrapertools.get_match(serverdata,"(^\w+)") 
        video_id = scrapertools.get_match(serverdata,"^\w+=(.*?$)") 
        servers_data_list.append( [server_id, video_id] )

    for server_id, video_id in servers_data_list:
        server = server_label(server_id)
        video_link = server_link(server_id) % (video_id.replace("|","&"))
        title = item.title + " [" + server + "]"
        thumbnail = "http://pelisalacarta.mimediacenter.info/squares/channelselector.png"
        itemlist.append( Item(channel=__channel__, title =title, url=video_link, action="play", thumbnail=thumbnail, fanart=fanart ) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.cultmoviez play url="+item.url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.channel = __channel__

    return itemlist

def server_label(id):
    lista = {"180":"180upload","bf":"bayfiles","bill":"billionuploads","bit":"Bit","bs":"bitshare","cra":"cramit","dir":"dir","dir1":"dir1","doc":"doc","dp":"depositefiles","dv":"donevideo","epic":"epicshare","fb":"filebox","ff":"filefactory","fk":"freakshare","gor":"gorillavid","hf":"hotfile","hk":"hulkshare","ifvm":"videomega","jb":"jumbofiles","megr":"megarelease","mf":"mediafire","mig":"mightyupload","moo":"mooshare","mov":"movreel","pic":"Pic","pla":"playedto","pow":"powvideo","pt":"putlocker","ra":"rapidgator","uc":"uploadcore","up":"uptobox","upa":"upafile","vb":"vidbux","vd":"vidbull","vk1":"vk","vk2":"vk","vz":"videozed","vzed":"videozed","za":"zalaa"}
    return lista[id]

def server_link(id):
    lista = {"180":"http://www.180upload.com/%s","bf":"http://www.bayfiles.net/file/%s","bill":"http://billionuploads.com/%s","bit":"http://my.bitcasa.com/#/folders/%s","bs":"http://bitshare.com/?f=%s","cra":"http://www.cramit.in/%s","dir":"%s","dir1":"%s","doc":"%s","dp":"http://www.depositfiles.com/files/%s","dv":"http://www.donevideo.com/%s","epic":"http://epicshare.net/%s","fb":"http://www.filebox.com/%s","ff":"http://www.filefactory.com/file/%s","fk":"http://www.freakshare.com/files/%s","gor":"http://gorillavid.in/embed-cnx-%s-600x360.html","hf":"http://hotfile.com/dl/%s","hk":"http://www.hulkshare.com/%s","ifvm":"http://videomega.tv/iframe.php?ref=%s&width=970&height=200","jb":"http://www.jumbofiles.com/%s","megr":"http://megarelease.org/%s","mf":"http://www.mediafire.com/?%s","mig":"http://mightyupload.com/%s","moo":"http://mooshare.biz/%s","mov":"http://movreel.com/%s","pic":"%s","pla":"http://played.to/%s","pow":"http://powvideo.net/%s","pt":"http://www.putlocker.com/file/%s","ra":"http://www.rapidgator.net/file/%s","uc":"http://www.uploadcore.com/%s","up":"http://www.uptobox.com/%s","upa":"http://upafile.com/%s","vb":"http://www.vidbux.com/%s","vd":"http://www.vidbull.com/%s","vk1":"http://vk.com/video_ext.php?%s","vk2":"http://vk.com/video_ext.php?%s","vz":"http://videozed.net/%s","vzed":"http://videozed.net/%s","za":"http://www.zalaa.com/%s"}
    return lista[id]

def html2symbol(text):
    lista = {'&#32;':' ', '&#33;':'!', '&#34;':'"', '&quot;':'"','&#35;':'#', '&#36;':'$', '&#37;':'%', '&#38;':'&', '&amp;':'&','&#39;':'\'', '&#40;':'(', '&#41;':')', '&#42;':'*', '&#43;':'+', '&#44;':',', '&#45;':'-', '&#46;':'.', '&#47;':'/', '&#48;':'0', '&#49;':'1', '&#50;':'2', '&#51;':'3', '&#52;':'4', '&#53;':'5', '&#54;':'6', '&#55;':'7', '&#56;':'8', '&#57;':'9', '&#58;':':', '&#59;':';', '&#60;':'<', '&lt;':'<','&#61;':'=', '&#62;':'>', '&gt;':'>','&#63;':'?', '&#64;':'@', '&#65;':'A', '&#66;':'B', '&#67;':'C', '&#68;':'D', '&#69;':'E', '&#70;':'F', '&#71;':'G', '&#72;':'H', '&#73;':'I', '&#74;':'J', '&#75;':'K', '&#76;':'L', '&#77;':'M', '&#78;':'N', '&#79;':'O', '&#80;':'P', '&#81;':'Q', '&#82;':'R', '&#83;':'S', '&#84;':'T', '&#85;':'U', '&#86;':'V', '&#87;':'W', '&#88;':'X', '&#89;':'Y', '&#90;':'Z', '&#91;':'[', '&#92;':'\\', '&#93;':']', '&#94;':'^', '&#95;':'_', '&#96;':'`', '&#97;':'a', '&#98;':'b', '&#99;':'c', '&#100;':'d', '&#101;':'e', '&#102;':'f', '&#103;':'g', '&#104;':'h', '&#105;':'i', '&#106;':'j', '&#107;':'k', '&#108;':'l', '&#109;':'m', '&#110;':'n', '&#111;':'o', '&#112;':'p', '&#113;':'q', '&#114;':'r', '&#115;':'s', '&#116;':'t', '&#117;':'u', '&#118;':'v', '&#119;':'w', '&#120;':'x', '&#121;':'y', '&#122;':'z', '&#123;':'{', '&#124;':'|', '&#125;':'}', '&#126;':'~', '&#160;':'', '&nbsp;':'','&#161;':'¡', '&iexcl;':'¡','&#162;':'¢', '&cent;':'¢','&#163;':'£', '&pound;':'£','&#164;':'¤', '&curren;':'¤','&#165;':'¥', '&yen;':'¥','&#166;':'¦', '&brvbar;':'¦','&#167;':'§', '&sect;':'§','&#168;':'¨', '&uml;':'¨','&#169;':'©', '&copy;':'©','&#170;':'ª', '&ordf;':'ª','&#171;':'«', '&laquo;':'«','&#172;':'¬', '&not;':'¬','&#173;':'­', '&shy;':'­','&#174;':'®', '&reg;':'®','&#175;':'¯', '&macr;':'¯','&#176;':'°', '&deg;':'°','&#177;':'±', '&plusmn;':'±','&#178;':'²', '&sup2;':'²','&#179;':'³', '&sup3;':'³','&#180;':'´', '&acute;':'´','&#181;':'µ', '&micro;':'µ','&#182;':'¶', '&para;':'¶','&#183;':'·', '&middot;':'·','&#184;':'¸', '&cedil;':'¸','&#185;':'¹', '&sup1;':'¹','&#186;':'º', '&ordm;':'º','&#187;':'»', '&raquo;':'»','&#188;':'¼', '&frac14;':'¼','&#189;':'½', '&frac12;':'½','&#190;':'¾', '&frac34;':'¾','&#191;':'¿', '&iquest;':'¿','&#192;':'À', '&Agrave;':'À','&#193;':'Á', '&Aacute;':'Á','&#194;':'Â', '&Acirc;':'Â','&#195;':'Ã', '&Atilde;':'Ã','&#196;':'Ä', '&Auml;':'Ä','&#197;':'Å', '&Aring;':'Å','&#198;':'Æ', '&AElig;':'Æ','&#199;':'Ç', '&Ccedil;':'Ç','&#200;':'È', '&Egrave;':'È','&#201;':'É', '&Eacute;':'É','&#202;':'Ê', '&Ecirc;':'Ê','&#203;':'Ë', '&Euml;':'Ë','&#204;':'Ì', '&Igrave;':'Ì','&#205;':'Í', '&Iacute;':'Í','&#206;':'Î', '&Icirc;':'Î','&#207;':'Ï', '&Iuml;':'Ï','&#208;':'Ð', '&ETH;':'Ð','&#209;':'Ñ', '&Ntilde;':'Ñ','&#210;':'Ò', '&Ograve;':'Ò','&#211;':'Ó', '&Oacute;':'Ó','&#212;':'Ô', '&Ocirc;':'Ô','&#213;':'Õ', '&Otilde;':'Õ','&#214;':'Ö', '&Ouml;':'Ö','&#215;':'×', '&times;':'×','&#216;':'Ø', '&Oslash;':'Ø','&#217;':'Ù', '&Ugrave;':'Ù','&#218;':'Ú', '&Uacute;':'Ú','&#219;':'Û', '&Ucirc;':'Û','&#220;':'Ü', '&Uuml;':'Ü','&#221;':'Ý', '&Yacute;':'Ý','&#222;':'Þ', '&THORN;':'Þ','&#223;':'ß', '&szlig;':'ß','&#224;':'à', '&agrave;':'à','&#225;':'á', '&aacute;':'á','&#226;':'â', '&acirc;':'â','&#227;':'ã', '&atilde;':'ã','&#228;':'ä', '&auml;':'ä','&#229;':'å', '&aring;':'å','&#230;':'æ', '&aelig;':'æ','&#231;':'ç', '&ccedil;':'ç','&#232;':'è', '&egrave;':'è','&#233;':'é', '&eacute;':'é','&#234;':'ê', '&ecirc;':'ê','&#235;':'ë', '&euml;':'ë','&#236;':'ì', '&igrave;':'ì','&#237;':'í', '&iacute;':'í','&#238;':'î', '&icirc;':'î','&#239;':'ï', '&iuml;':'ï','&#240;':'ð', '&eth;':'ð','&#241;':'ñ', '&ntilde;':'ñ','&#242;':'ò', '&ograve;':'ò','&#243;':'ó', '&oacute;':'ó','&#244;':'ô', '&ocirc;':'ô','&#245;':'õ', '&otilde;':'õ','&#246;':'ö', '&ouml;':'ö','&#247;':'÷', '&divide;':'÷','&#248;':'ø', '&oslash;':'ø','&#249;':'ù', '&ugrave;':'ù','&#250;':'ú', '&uacute;':'ú','&#251;':'û', '&ucirc;':'û','&#252;':'ü', '&uuml;':'ü','&#253;':'ý', '&yacute;':'ý','&#254;':'þ', '&thorn;':'þ','&#255;':'ÿ', '&yuml;':'ÿ','&#338;':'Œ', '&#339;':'œ', '&#352;':'Š', '&#353;':'š', '&#376;':'Ÿ', '&#402;':'ƒ', '&#8211;':'–', '&#8212;':'—', '&#8216;':'‘', '&#8217;':'’', '&#8218;':'‚', '&#8220;':'“', '&#8221;':'”', '&#8222;':'„', '&#8224;':'†', '&#8225;':'‡', '&#8226;':'•', '&#8230;':'…', '&#8240;':'‰', '&#8364;':'€', '&euro;':'€','&#8482;':'™'}

    text = text.replace('&#0','&#')
    matches = re.compile("(&[^;]+;)",re.DOTALL).findall(text)
    for tosymbol in matches:
        text = text.replace(tosymbol,lista[tosymbol])
    return text