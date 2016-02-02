# -*- coding: utf-8 -*-

# projecto o django
from geoservicios.models import *
from geoservicios.formularios import *
from django.template import RequestContext
from django.http import HttpResponseRedirect  # , Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404  # , redirect
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.signing import TimestampSigner, BadSignature
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import translation

# python
from decimal import Decimal, getcontext
from os import mkdir, access, F_OK
from datetime import datetime  # , date
from hashlib import sha1
import re, urllib2, json
from hv.settings import ACCESO_API_PAYPAL, IDIOMAS_DISPONIBLES, COMISION_HV, COMISION_PAYPAL, URL_SITIO, MUESTRA_ERRORES_SMTP  # ,PRECIO_POR_DOLAR, ANIO_INICIO_CH

#----------------------------------------------------------
#---------------------  Inicializando  --------------------
#----------------------------------------------------------


##############################
###############  VARIABLES
##############################

getcontext().prec = 5

##############################
##############  FUNCIONES
##############################


# xHACER: esto no es mejor con iri_to_uri ??
def uerelizar(cad):  # que tiene forma de URL
	cad = cad.replace(" ", "-").replace(u"ñ", "n").replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u").lower()
	# [^a-zA-Z0-9-!()+]
	temp = re.findall("([^a-zA-Z0-9-])+", cad)
	for t in temp:
		cad = cad.replace(t, "")
	return cad


# xHACER: cargar en el index las categorias desde la BD y no estaticamente?
# ver archivo vista_traduccionCategoria.txt
def inicializar_categorias():
	if not UrlCategoria.objects.filter(id=1).exists():

		###############################################  Espanol

		c = UrlCategoria.objects.create(url="diseno-graficos-fotografia", padre=None)
		Categoria.objects.create(url=c, nombre=u"Diseño, Gráficos y Fotografía", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="historietas-caricaturas-personajes")
		Categoria.objects.create(nombre=u"Historietas, Caricaturas y Personajes", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="logos")
		Categoria.objects.create(nombre=u"Logos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="vectorizar")
		Categoria.objects.create(nombre=u"Vectorizar", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="estampados")
		Categoria.objects.create(nombre=u"Estampados para prendas", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="ilustracion")
		Categoria.objects.create(nombre=u"Ilustración", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="tarjetas")
		Categoria.objects.create(nombre=u"Tarjetas de...", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="portada-libros-paquetes")
		Categoria.objects.create(nombre=u"Portada de Libros y Paquetes", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="fotografia-edicion-fotografica")
		Categoria.objects.create(nombre=u"Fotografía y Edición Fotográfica", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="presentaciones-infografias")
		Categoria.objects.create(nombre=u"Presentaciones e Infografías", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="arquitectura-inmobiliario")
		Categoria.objects.create(nombre=u"Arquitectura y Diseño Inmobiliario", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="mobiliario-interiores")
		Categoria.objects.create(nombre=u"Mobiliario y Diseño de Interiores", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="modelado-2d-3d")
		Categoria.objects.create(nombre=u"Modelado 2D y 3D", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="transcripcion-traduccion-redaccion", padre=None)
		Categoria.objects.create(url=c, nombre=u"Transcripción, Traducción y Redacción", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="redaccion-escritura-creativa")
		Categoria.objects.create(nombre=u"Redacción y Escritura Creativa", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="traduccion")
		Categoria.objects.create(nombre=u"Traducción", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="transcripcion")
		Categoria.objects.create(nombre=u"Transcripción", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="contenido-sitios-web")
		Categoria.objects.create(nombre=u"Contenido para Sitios Web", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="resenas-criticas")
		Categoria.objects.create(nombre=u"Reseñas/Críticas", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="redaccion-discursos")
		Categoria.objects.create(nombre=u"Redacción de Discursos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="edicion-revision-escritos")
		Categoria.objects.create(nombre=u"Edición y Revisión de Escritos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="comunicado-prensa")
		Categoria.objects.create(nombre=u"Comunicado de Prensa", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="audio-musica", padre=None)
		Categoria.objects.create(url=c, nombre=u"Audio y Música", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="edicion-audio")
		Categoria.objects.create(nombre=u"Edición de Audio", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="produccion-musical")
		Categoria.objects.create(nombre=u"Producción Musical", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="composicion-canciones")
		Categoria.objects.create(nombre=u"Composición de canciones", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="lecciones-musica")
		Categoria.objects.create(nombre=u"Lecciones de Música", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="musica-rap")
		Categoria.objects.create(nombre=u"Música Rap", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="narracion-doblaje")
		Categoria.objects.create(nombre=u"Narración y Doblaje", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="efectos-sonido")
		Categoria.objects.create(nombre=u"Efectos de sonido", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="tonos-llamada-personalizados")
		Categoria.objects.create(nombre=u"Tonos de Llamada Personalizados", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="canciones-personalizadas-dedicatorias")
		Categoria.objects.create(nombre=u"Canciones Personalizadas y Dedicatorias", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="programacion-tecnologia", padre=None)
		Categoria.objects.create(url=c, nombre=u"Programación y Tecnología", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="python")
		Categoria.objects.create(nombre=u"Python", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="base-datos")
		Categoria.objects.create(nombre=u"Base de Datos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="ruby")
		Categoria.objects.create(nombre=u"Ruby", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="wordpress")
		Categoria.objects.create(nombre=u"WordPress", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="php")
		Categoria.objects.create(nombre=u"PHP", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="videojuegos")
		Categoria.objects.create(nombre=u"Videojuegos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="app-escritorio")
		Categoria.objects.create(nombre=u"Aplicaciones de Escritorio", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="diseno-web-arquitectura-informacion")
		Categoria.objects.create(nombre=u"Diseño Web y Arquitectura de la Información", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="javascript")
		Categoria.objects.create(nombre=u"JavaScript", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="c-c++")
		Categoria.objects.create(nombre=u"C/C++", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="java")
		Categoria.objects.create(nombre=u"Java", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="ios-android-moviles")
		Categoria.objects.create(nombre=u"iOS, Android y Móviles", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="pruebas-software-accesibilidad-usabilidad")
		Categoria.objects.create(nombre=u"Testing de Software, Accesibilidad y Usabilidad", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="comercio-electronico")
		Categoria.objects.create(nombre=u"Comercio Electrónico", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="conversion-recuperacion-archivos")
		Categoria.objects.create(nombre=u"Conversión y Recuperación de Archivos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="net")
		Categoria.objects.create(nombre=u".Net", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		# mercadeo/mercadotecnia
		c = UrlCategoria.objects.create(url="marketing-digital", padre=None)
		Categoria.objects.create(url=c, nombre=u"Marketing Digital", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="analisis-web")
		Categoria.objects.create(nombre=u"Análisis Web", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="menciones-blogs")
		Categoria.objects.create(nombre=u"Menciones en Blogs", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="paginas-fans")
		Categoria.objects.create(nombre=u"Páginas de Fans", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="seo")
		Categoria.objects.create(nombre=u"Optimización para Motores de Búsqueda (SEO)", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="marketing-redes-sociales")
		Categoria.objects.create(nombre=u"Marketing en Redes Sociales", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="generar-trafico-web")
		Categoria.objects.create(nombre=u"Generar Tráfico Web", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="marketing-videos")
		Categoria.objects.create(nombre=u"Marketing en Videos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="publicidad-propaganda", padre=None)
		Categoria.objects.create(url=c, nombre=u"Publicidad y Propaganda", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="tu-mensaje-en-con")
		Categoria.objects.create(nombre=u"Tu mensaje en/con...", descripcion="", url=u)
		# en mi cadera, con piedras/ tu mensaje sobre: arena,mi cadera, ¿sobre PIEDRAS? Sostener tu Letrero-->
		u = UrlCategoria.objects.create(padre=c, url="encabezados-anuncios")
		Categoria.objects.create(nombre=u"Encabezados y Anuncios", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="volantes-folletos-regalos-publicitarios")
		Categoria.objects.create(nombre=u"Volantes, Folletos y Regalos Publicitarios", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="anuncios-humanos")
		Categoria.objects.create(nombre=u"Anuncios Humanos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="comerciales")
		Categoria.objects.create(nombre=u"Comerciales", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="mascotas-modelos")
		Categoria.objects.create(nombre=u"Mascotas Modelos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="publicidad-exteriores")
		Categoria.objects.create(nombre=u"Publicidad en Exteriores", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="publicidad-radio")
		Categoria.objects.create(nombre=u"Publicidad para Radio", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="promocion-musical")
		Categoria.objects.create(nombre=u"Promoción Musical", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="publicidad-anuncios-web")
		Categoria.objects.create(nombre=u"Anuncios Web", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="negocios", padre=None)
		Categoria.objects.create(url=c, nombre=u"Negocios", descripcion="")
		# xHACER: Entrepreneurship!
		u = UrlCategoria.objects.create(padre=c, url="planes-negocios")
		Categoria.objects.create(nombre=u"Planes de Negocios", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consejos-carrera-profesional")
		Categoria.objects.create(nombre=u"Consejos para tu Carrera Profesional", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="estudio-mercado")
		Categoria.objects.create(nombre=u"Estudio de Mercado", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="curriculum-cartas-presentacion")
		Categoria.objects.create(nombre=u"Curriculum, Cartas de Presentación", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="presentacion-proyectos-ideas")
		Categoria.objects.create(nombre=u"Presentación para de Proyectos/Ideas", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="asistentecia-virtual")
		Categoria.objects.create(nombre=u"Asistentecia Virtual", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consejos-negocios")
		Categoria.objects.create(nombre=u"Consejos para Negocios", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="servicios-marca-registrada")
		Categoria.objects.create(nombre=u"Servicios para tu Marca Registrada", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consultoria-financiera")
		Categoria.objects.create(nombre=u"Consultoría Financiera", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consultoria-legal")
		Categoria.objects.create(nombre=u"Consultoría Legal", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="video-animacion", padre=None)
		Categoria.objects.create(url=c, nombre=u"Video y Animación", descripcion="")
		# xPENSAR:
			# deberia cambiar el esquema (q un servicio elija las categorias)??
			# comerciales puede estar en video y en publicidad??
		u = UrlCategoria.objects.create(padre=c, url="edicion-efectos-produccion")
		Categoria.objects.create(nombre=u"Edición, Efectos y Producción", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="animacion-2d-3d")
		Categoria.objects.create(nombre=u"Animación 2D y 3D", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="stop-motion")
		Categoria.objects.create(nombre=u"Stop Motion", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="intros")
		Categoria.objects.create(nombre=u"Intros", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="subtitulos")
		Categoria.objects.create(nombre=u"Subtitulado", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="narracion-doblaje")
		Categoria.objects.create(nombre=u"Doblaje", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="storyboarding")
		Categoria.objects.create(nombre=u"Storyboarding", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="diversion-entretenimiento", padre=None)
		Categoria.objects.create(url=c, nombre=u"Diversión y Entretenimiento", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="video-standup")
		Categoria.objects.create(nombre=u"Video StandUp", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="chistes-escritos")
		Categoria.objects.create(nombre=u"Chistes Escritos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="humor-grafico-memes")
		Categoria.objects.create(nombre=u"Chistes Gráficos/Memes", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="chistes-vivo")
		Categoria.objects.create(nombre=u"Chistes en Vivo", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="marionetas")
		Categoria.objects.create(nombre=u"Marionetas", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="discurso-gracioso-evento")
		Categoria.objects.create(nombre=u"Discurso Gracioso para Evento", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="personificacion-celebridades")
		Categoria.objects.create(nombre=u"Personificación de Celebridades", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="trucos-magia-malabarismo")
		Categoria.objects.create(nombre=u"Trucos de Magia y Malabarismo", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="estilo-vida", padre=None)
		Categoria.objects.create(url=c, nombre=u"Estilo de vida", descripcion="")
		u = UrlCategoria.objects.create(padre=c, url="cuidado-animales-mascotas")
		Categoria.objects.create(nombre=u"Cuidado de Animales y Mascotas", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consejos-relaciones")
		Categoria.objects.create(nombre=u"Consejos sobre Relaciones", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="maquillaje-estilo-belleza")
		Categoria.objects.create(nombre=u"Maquillaje, Estilo y Belleza", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="ejercicios-rutinas")
		Categoria.objects.create(nombre=u"Ejercicios y Rutinas (Entrenadores)", descripcion="", url=u)  # xHACER: peligro
		u = UrlCategoria.objects.create(padre=c, url="dietas-nutricionistas")
		Categoria.objects.create(nombre=u"Dietas y Perdida de Peso (Nutricionistas)", descripcion="", url=u)  # xHACER: peligro
		u = UrlCategoria.objects.create(padre=c, url="recetas-cocina")
		Categoria.objects.create(nombre=u"Recetas de Cocina", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="consejos-padres")
		Categoria.objects.create(nombre=u"Consejos para Padres", descripcion="", url=u)  # xHACER: peligro
		u = UrlCategoria.objects.create(padre=c, url="viajes")
		Categoria.objects.create(nombre=u"Concejos para Viajes", descripcion="", url=u)  # xHACER: peligro
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		c = UrlCategoria.objects.create(url="regalos", padre=None)
		Categoria.objects.create(url=c, nombre=u"Regalos", descripcion="")
		# <li><a href="#">Tarjetas Postales desde...</a></li>
		# <li><a href="#">Artesan&iacute;as Recicladas</a></li>
		# "Ideas para Joyería hechas a mano"		
		u = UrlCategoria.objects.create(padre=c, url="tarjetas-felicitaciones")
		Categoria.objects.create(nombre=u"Tarjetas de Felicitaciones", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="video-felicitaciones")
		Categoria.objects.create(nombre=u"Video Felicitaciones", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="ideas-regalos-divertidos-inesperados")
		Categoria.objects.create(nombre=u"Ideas para Regalos Divertidos/Inesperados", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="manualidades-artesanias")
		Categoria.objects.create(nombre=u"Ideas para Manualidades y Artesanías", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="regalos-nerdos")
		Categoria.objects.create(nombre=u"Ideas de Regalos para Nerdos", descripcion="", url=u)
		u = UrlCategoria.objects.create(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Otros", descripcion="", url=u)
		# termino


		###############################################  Ingles

		c = UrlCategoria.objects.get(url="diseno-graficos-fotografia", padre=None)
		Categoria.objects.create(url=c, nombre=u"Design, Graphics & Photography", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="historietas-caricaturas-personajes")
		Categoria.objects.create(nombre=u"Manga, Cartoon & Characters", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="logos")
		Categoria.objects.create(nombre=u"Logos", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="vectorizar")
		Categoria.objects.create(nombre=u"Vectorizar", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="estampados")
		Categoria.objects.create(nombre=u"Design of Prints for clothes", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="ilustracion")
		Categoria.objects.create(nombre=u"Ilustrations", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="tarjetas")
		Categoria.objects.create(nombre=u"Card Designs", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="portada-libros-paquetes")
		Categoria.objects.create(nombre=u"Book Cover & Packages", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="fotografia-edicion-fotografica")
		Categoria.objects.create(nombre=u"Photography & Photographic Edition", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="presentaciones-infografias")
		Categoria.objects.create(nombre=u"Presentations & Infographics", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="arquitectura-inmobiliario")
		Categoria.objects.create(nombre=u"Architecture & Housing Design", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="mobiliario-interiores")
		Categoria.objects.create(nombre=u"Furniture & Interior Design", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="modelado-2d-3d")
		Categoria.objects.create(nombre=u"2D & 3D Models", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="transcripcion-traduccion-redaccion", padre=None)
		Categoria.objects.create(url=c, nombre=u"Transcription, Translation & Drafting", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="redaccion-escritura-creativa")
		Categoria.objects.create(nombre=u"Drafting & Creative Writing", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="traduccion")
		Categoria.objects.create(nombre=u"Translation", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="transcripcion")
		Categoria.objects.create(nombre=u"Transcription", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="contenido-sitios-web")
		Categoria.objects.create(nombre=u"Content for Web Sites", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="resenas-criticas")
		Categoria.objects.create(nombre=u"Reviews & Critiques", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="redaccion-discursos")
		Categoria.objects.create(nombre=u"Speech Drafting", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="edicion-revision-escritos")
		Categoria.objects.create(nombre=u"Edition, Speelcheck & Proofreading", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="comunicado-prensa")
		Categoria.objects.create(nombre=u"Press Release", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="audio-musica", padre=None)
		Categoria.objects.create(url=c, nombre=u"Audio & Music", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="edicion-audio")
		Categoria.objects.create(nombre=u"Audio Edition", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="produccion-musical")
		Categoria.objects.create(nombre=u"Musical Production", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="composicion-canciones")
		Categoria.objects.create(nombre=u"Songwriters", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="lecciones-musica")
		Categoria.objects.create(nombre=u"Music Lessons", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="musica-rap")
		Categoria.objects.create(nombre=u"Rap Music", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="narracion-doblaje")
		Categoria.objects.create(nombre=u"Voice-Over & Dubbing", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="efectos-sonido")
		Categoria.objects.create(nombre=u"Sound Effects", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="tonos-llamada-personalizados")
		Categoria.objects.create(nombre=u"Custom Ringtones", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="canciones-personalizadas-dedicatorias")
		Categoria.objects.create(nombre=u"Custom Songs & Dedications", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="programacion-tecnologia", padre=None)
		Categoria.objects.create(url=c, nombre=u"Programming & Tecnology", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="python")
		Categoria.objects.create(nombre=u"Python", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="base-datos")
		Categoria.objects.create(nombre=u"Data Base", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="ruby")
		Categoria.objects.create(nombre=u"Ruby", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="wordpress")
		Categoria.objects.create(nombre=u"WordPress", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="php")
		Categoria.objects.create(nombre=u"PHP", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="videojuegos")
		Categoria.objects.create(nombre=u"Videogames", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="app-escritorio")
		Categoria.objects.create(nombre=u"Desktop Applications", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="diseno-web-arquitectura-informacion")
		Categoria.objects.create(nombre=u"Web Design & Information Architecture", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="javascript")
		Categoria.objects.create(nombre=u"JavaScript", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="c-c++")
		Categoria.objects.create(nombre=u"C/C++", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="java")
		Categoria.objects.create(nombre=u"Java", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="ios-android-moviles")
		Categoria.objects.create(nombre=u"iOS, Android & Mobile", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="pruebas-software-accesibilidad-usabilidad")
		Categoria.objects.create(nombre=u"Software Testing, Accesibility & Usability", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="comercio-electronico")
		Categoria.objects.create(nombre=u"eCommerce", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="conversion-recuperacion-archivos")
		Categoria.objects.create(nombre=u"File Convertion & Data Recovery", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="net")
		Categoria.objects.create(nombre=u".Net", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="marketing-digital", padre=None)
		Categoria.objects.create(url=c, nombre=u"Digital Marketing", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="analisis-web")
		Categoria.objects.create(nombre=u"Web Analytics", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="menciones-blogs")
		Categoria.objects.create(nombre=u"Blog Mentions", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="paginas-fans")
		Categoria.objects.create(nombre=u"FanPage", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="seo")
		Categoria.objects.create(nombre=u"Search Engine Optimization (SEO)", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="marketing-redes-sociales")
		Categoria.objects.create(nombre=u"Social Network Marketing", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="generar-trafico-web")
		Categoria.objects.create(nombre=u"Web Traffic", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="marketing-videos")
		Categoria.objects.create(nombre=u"Video Marketing", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="publicidad-propaganda", padre=None)
		Categoria.objects.create(url=c, nombre=u"Propaganda & Publicity", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="tu-mensaje-en-con")
		Categoria.objects.create(nombre=u"Your message in/with...", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="encabezados-anuncios")
		Categoria.objects.create(nombre=u"Ads & Headlines", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="volantes-folletos-regalos-publicitarios")
		Categoria.objects.create(nombre=u"Flyers, Handouts & Publicitary Gift Ideas", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="anuncios-humanos")
		Categoria.objects.create(nombre=u"Human Billboards", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="comerciales")
		Categoria.objects.create(nombre=u"Commercials", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="mascotas-modelos")
		Categoria.objects.create(nombre=u"Pet Models", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="publicidad-exteriores")
		Categoria.objects.create(nombre=u"Outdoor Advertising", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="publicidad-radio")
		Categoria.objects.create(nombre=u"Radio Publicity", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="promocion-musical")
		Categoria.objects.create(nombre=u"Music Promotion", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="publicidad-anuncios-web")
		Categoria.objects.create(nombre=u"Web Ads", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="negocios", padre=None)
		Categoria.objects.create(url=c, nombre=u"Business", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="planes-negocios")
		Categoria.objects.create(nombre=u"Business Plans", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consejos-carrera-profesional")
		Categoria.objects.create(nombre=u"Professional Career Advice", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="estudio-mercado")
		Categoria.objects.create(nombre=u"Market Research", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="curriculum-cartas-presentacion")
		Categoria.objects.create(nombre=u"Resume/Presentation Letters", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="presentacion-proyectos-ideas")
		Categoria.objects.create(nombre=u"Proyects or Ideas Presentations", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="asistentecia-virtual")
		Categoria.objects.create(nombre=u"Virtual Assistants", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consejos-negocios")
		Categoria.objects.create(nombre=u"Business Advice", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="servicios-marca-registrada")
		Categoria.objects.create(nombre=u"Brand & Trademark", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consultoria-financiera")
		Categoria.objects.create(nombre=u"Financial Advice", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consultoria-legal")
		Categoria.objects.create(nombre=u"Legal Advice", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="video-animacion", padre=None)
		Categoria.objects.create(url=c, nombre=u"Video & Animation", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="edicion-efectos-produccion")
		Categoria.objects.create(nombre=u"Edition, Effects & Production", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="animacion-2d-3d")
		Categoria.objects.create(nombre=u"2D & 3D Animation", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="stop-motion")
		Categoria.objects.create(nombre=u"Stop Motion", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="intros")
		Categoria.objects.create(nombre=u"Intros", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="subtitulos")
		Categoria.objects.create(nombre=u"Subtitle", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="narracion-doblaje")
		Categoria.objects.create(nombre=u"Voice-Over & Dubbing", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="storyboarding")
		Categoria.objects.create(nombre=u"Storyboarding", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="diversion-entretenimiento", padre=None)
		Categoria.objects.create(url=c, nombre=u"Fun & Entertainment", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="video-standup")
		Categoria.objects.create(nombre=u"StandUp Video", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="chistes-escritos")
		Categoria.objects.create(nombre=u"Written Jokes", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="humor-grafico-memes")
		Categoria.objects.create(nombre=u"Graphic Jokes/Memes", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="chistes-vivo")
		Categoria.objects.create(nombre=u"Live Jokes", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="marionetas")
		Categoria.objects.create(nombre=u"Puppets", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="discurso-gracioso-evento")
		Categoria.objects.create(nombre=u"Funny Speech for Event", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="personificacion-celebridades")
		Categoria.objects.create(nombre=u"Personification of Celebrities", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="trucos-magia-malabarismo")
		Categoria.objects.create(nombre=u"Magic Tricks & Jugglery", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="estilo-vida", padre=None)
		Categoria.objects.create(url=c, nombre=u"Life Style", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="cuidado-animales-mascotas")
		Categoria.objects.create(nombre=u"Animal Care & Pets", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consejos-relaciones")
		Categoria.objects.create(nombre=u"Relationship Advices", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="maquillaje-estilo-belleza")
		Categoria.objects.create(nombre=u"Makeup, Style & Beauty", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="ejercicios-rutinas")
		Categoria.objects.create(nombre=u"Exercise & Routines (Trainers)", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="dietas-nutricionistas")
		Categoria.objects.create(nombre=u"Diets & Lose Weight (Nutritionists)", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="recetas-cocina")
		Categoria.objects.create(nombre=u"Cooking Recipes", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="consejos-padres")
		Categoria.objects.create(nombre=u"Parent Advices", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="viajes")
		Categoria.objects.create(nombre=u"Traveling", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

		c = UrlCategoria.objects.get(url="regalos", padre=None)
		Categoria.objects.create(url=c, nombre=u"Gifts", descripcion="", idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="tarjetas-felicitaciones")
		Categoria.objects.create(nombre=u"Greeting Cards", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="video-felicitaciones")
		Categoria.objects.create(nombre=u"Greeting Videos", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="ideas-regalos-divertidos-inesperados")
		Categoria.objects.create(nombre=u"Ideas for Unexpected/Fun Gifts", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="manualidades-artesanias")
		Categoria.objects.create(nombre=u"Ideas for Crafts", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="regalos-nerdos")
		Categoria.objects.create(nombre=u"Ideas for Gift to Geeks", descripcion="", url=u, idioma="en")
		u = UrlCategoria.objects.get(padre=c, url="otros")
		Categoria.objects.create(nombre=u"Others", descripcion="", url=u, idioma="en")

	else:
		return "Ya existen en la BD"


def inicializar_idiomas():
	# xHACER: falta validar los q ya existen de una mejor manera, xq luego yo puedo querer meter mas niveles
	if not Idioma.objects.all().exists():
		for idioma in IDIOMAS_DISPONIBLES:
			Idioma.objects.create(codigo=idioma)
	else:
		return "Ya existen en la BD"


def inicializar_niveles():
	""" El precio sera en dolares hasta la version 1 de la plataforma """
	# xHACER: falta validar los q ya existen de una mejor manera, xq luego yo puedo querer meter mas niveles
	if not Nivel.objects.all().exists():
		Nivel.objects.create(numero=0, promedio=0, experiencia=0, meses_laborando=0, precio_max=4.00, max_satelites=0, precio_max_sat=0)
		Nivel.objects.create(numero=1, promedio=0, experiencia=10, meses_laborando=1, precio_max=10.00, max_satelites=1, precio_max_sat=10.00)
		Nivel.objects.create(numero=2, promedio=5, experiencia=25, meses_laborando=3, precio_max=20.00, max_satelites=3, precio_max_sat=50.00)
		Nivel.objects.create(numero=3, promedio=7, experiencia=100, meses_laborando=6, precio_max=50.00, max_satelites=5, precio_max_sat=100.00)
	else:
		return "Ya existen en la BD"


def datos_perfil_venezolano(perfil, idioma):
	# es distinto pedir cantidad de servicios por las urls que por los servicios...
	urls = UrlServicio.objects.filter(vendedor=perfil)
	servis = ServicioVirtual.objects.filter(url__in=urls, eliminado=False, )
	cant_servicios = servis.count()
	facturas = Factura.objects.filter(url_servicio__vendedor=perfil)
	n_facturas = facturas.count()
	lista_servis = []
	# visitas = Visitas.objects.filter(usuario=perfil).count()
	ganancias = 0
	try:
		for s in servis:
			c = Cola.objects.filter(servicio=s)
			pedidos = c.filter(estatus="E").count()
			cancelados = c.filter(estatus="C").count()
			facturados = Factura.objects.filter(url_servicio=s.url).count()
			lista_servis.append([s, pedidos, facturados, cancelados])
		lista_servis.sort(key=lambda x: x[1], reverse=True)
		for f in facturas:
			ganancias += f.vendedor_recibe
		valores = Contador.objects.get(servicio__url__vendedor=perfil)
		prom = valores.promedio / valores.experiencia
		te = valores.tiempo_entrega / valores.experiencia
		exp = valores.experiencia
		atencion = valores.atencion / valores.experiencia
		calidad = valores.calidad / valores.experiencia
	except:
		prom, te, exp, atencion, calidad = 0, 0, 0, 0, 0
	nivel_usr = NivelUsuario.objects.get(usuario=perfil)
	# u_extras = get_object_or_404(DatosExtraPerfil, usuario__iexact=usuario)
	LISTA_SUBCATEGORIAS = []
	CATEGORIAS = Categoria.objects.filter(url__padre=None, idioma=idioma)
	for i, cat in enumerate(CATEGORIAS):
		LISTA_SUBCATEGORIAS.append([i, Categoria.objects.filter(url__padre=cat.url, idioma=idioma)])
	datos = {
		'vacacionando': "Si" if perfil.vacacionando else "No, Trabajando",
		'prom': prom,
		'tiempo_entrega': te,
		'perfil': perfil,
		'atencion': atencion,
		'calidad': calidad,
		'exp': exp,
		'categorias': CATEGORIAS,
		'lista_subcat': LISTA_SUBCATEGORIAS,
		'ganancias': ganancias,
		# xHACER:
			# el precio debe variar si el usr elije un precio menor al maximo
		"precio_max": nivel_usr.nivel.precio_max,
		'nivel': nivel_usr.nivel.numero,
		'lista_servis': lista_servis,
		'n_servicios': cant_servicios,
		'n_compradores': n_facturas,
		# 'visitas': visitas,
		# 'n_servicios_progreso': x_comprar,
		# 'n_servicios_cancelados': cancelada,
		"pag_activa": idioma + "/perfil.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	return datos


def reembolsar(obj_encola):
	inter = Intermediario.objects.get(obj_cola=obj_encola)
	datos_paypal = {
		"currencyCode": "USD",
		"payKey": inter.clave_paypal,
		"requestEnvelope": {
			"errorLanguage": "en_US",
			"detailLevel": "ReturnAll"
		}
	}
	datos_paypal = json.dumps(datos_paypal)
	try:
		peticion = urllib2.Request(url=ACCESO_API_PAYPAL["URL_REFUND"], data=datos_paypal, headers=ACCESO_API_PAYPAL["HEADERS_API"])
		com_paypal = urllib2.urlopen(peticion, timeout=30)
	except urllib2.URLError, motivo:
		# xHACER: reenviar a una pagina luego de un error en el reembolso (inicio, perfil ?)
		return 0
		# xHACER: terminar q pasa si no conecta con el servidor
	resp_paypal = com_paypal.read()
	com_paypal.close()
	resp_paypal = json.JSONDecoder().decode(resp_paypal)
	if resp_paypal["responseEnvelope"]["ack"] == "Success" and resp_paypal['refundInfoList']['refundInfo'][0]["refundStatus"] == "REFUNDED":
		inter.delete()
		obj_encola.delete()
		return 1
	return 0


def pagar_vendedores(obj_encola):
	inter = Intermediario.objects.get(obj_cola=obj_encola)
	datos_paypal = {
		"payKey": inter.clave_paypal,
		"requestEnvelope": {
			"errorLanguage": "en_US",
			"detailLevel": "ReturnAll"
		}
	}
	datos_paypal = json.dumps(datos_paypal)
	try:
		peticion = urllib2.Request(url=ACCESO_API_PAYPAL["URL_EXECUTE"], data=datos_paypal, headers=ACCESO_API_PAYPAL["HEADERS_API"])
		com_paypal = urllib2.urlopen(peticion, timeout=30)
	except urllib2.URLError, motivo:
		# xHACER: reenviar a una pagina luego de un error (inicio, perfil ?)
		return 0
		# xHACER: terminar q pasa si no conecta con el servidor
	resp_paypal = com_paypal.read()
	com_paypal.close()
	resp_paypal = json.JSONDecoder().decode(resp_paypal)
	if resp_paypal["responseEnvelope"]["ack"] == "Success" and resp_paypal["paymentExecStatus"] == "COMPLETED":
		inter.delete()
		obj_encola.delete()
		return 1
	return 0


# xHACER:
# def pagar_bs():
	# if request.user.is_authenticated():
	# 	p = get_object_or_404(Perfil, usuario=request.user)
		
	# return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


##############################
################  Clases
##############################


# class PrecioInjusto(Exception):
	# """Falta hacer q no se requiera el e.value sino simplemente con e se pueda decir cual es el error una vez se use en el except"""
	# def __init__(self, value):
	# 	self.value = value
	# 	if value > 500:
	# 		self = u"No se puede sobrepasar el precio techo para ofrecer Servicios de 500 $"
	# 	elif value < 5:
	# 		self = u"No se puede sobrepasar el precio piso para ofrecer Servicios de 5 $"
	# def __unicode__(self):
	# 	return "%s" % self.value


##############################
################  Vistas
##############################


def cambiar_idioma(request):
	if request.POST["language"] in IDIOMAS_DISPONIBLES:
		idioma = request.POST["language"]
		translation.activate(idioma)
		request.session[translation.LANGUAGE_SESSION_KEY] = idioma
	else:
		idioma = request.LANGUAGE_CODE
	datos = {
		"pag_activa": idioma + "/index.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil'] = p
		datos['perfil_logueado'] = p
		datos['logueado'] = True
	return HttpResponseRedirect('/', datos)


def mostrar_oportunidad(request, tipo):
	idioma = request.LANGUAGE_CODE
	datos = {
		"tipo_oport": tipo,
		"pag_activa": idioma + "/oportunidades.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil_logueado'] = p
		datos['logueado'] = True
		return render(request, 'base.html', datos)
	else:
		return render(request, 'base.html', datos)


def recuperar_pw(request, clave="", correo=""):
	# xHACER:
		# usar los correos verdaderos del admin
		# traducir los msjs
		# hay una vista q hace esto.. password_change()
	if not request.user.is_authenticated():
		idioma = request.LANGUAGE_CODE
		if request.method == "GET" and clave and correo:
			enigma = TimestampSigner("c4mb13-d3-v1d4-3l" + str(datetime(2014, 12, 31)), salt="j0d3t3-h@ck3r")
			datos = {
				"pag_activa": idioma + "/recuperar-pw.html",
				"cambiar_contra": True,
				"correo_usr": correo,
				"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			}
			try:
				clave = enigma.unsign(correo+":"+clave.replace("+",":"), max_age = 86400)  # 86400 segundos = un dia
				# luego le actualiza la clave y se le asigna al usuario esta nueva clave y se muestra el mensaje correspondiente (buscar en POST)
			except BadSignature:
				datos["mensaje"] = "Error: clave incorrecta"
			except SignatureExpired:
				datos["mensaje"] = "Error: la clave expiro. Debes solicitar una nueva URL para acceder"
		else:
			datos = {
				"pag_activa": idioma + "/recuperar-pw.html",
				"cambiar_contra": False,
				"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			}
		if request.method == "POST":
			correo = request.POST.get("correo", "")
			pw = request.POST.get("pw", "")
			correo_usr = request.POST.get("correo_usr", "")
			datos = {
				"pag_activa": idioma + "/index.html",
				"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			}
			if correo:
				try:
					receptor = User.objects.get(email=correo)
				except ObjectDoesNotExist:
					# try:
					# 	receptor = User.objects.get(username=datos_usr)
					# except ObjectDoesNotExist:
					receptor = ""
					datos["mensaje"] = 'Error: Ingrese su correo'
				if receptor:
					enigma = TimestampSigner("c4mb13-d3-v1d4-3l" + str(datetime(2014, 12, 31)), salt="j0d3t3-h@ck3r")
					contra = enigma.sign(correo).split(":")
					asunto = {
						"es": "Restablecer acceso a cuenta buy-2venezuela.com. Tienes menos de 1 dia",
						"en": ""
					}[idioma]
					msj = {
						"es": u"Ud. ha notificado imposibilidad para acceder a <b>buy-2venezuela.com<b><br><br>Ingrese a la siguiente URL para <a href='buy-2venezuela.com/recuperar-cuenta/clave=" + contra[1] + "+" + contra[2] + "&correo=" + correo + "' />recuperar su cuenta</a>",
						"en": ""
					}[idioma]
					from hv.settings import EMAIL_HOST_USER
					try:
						send_mail(asunto, msj, EMAIL_HOST_USER, [receptor.email], fail_silently=MUESTRA_ERRORES_SMTP)
					except BadHeaderError:
						datos["mensaje"] = 'Error: Cabecera del correo invalida.'
					else:
						datos["mensaje"] = u"Ha sido enviado un correo con las instrucciones para recuperar el acceso a su cuenta buy-2venezuela.com. La URL estará activa durante un dia solamente"
			elif pw:
				try:
					u = User.objects.get(email=correo_usr)
					u.set_password(pw)
					u.save()
				except ObjectDoesNotExist:
					datos["mensaje"] = u"Error: no se pudo actualizar su contraseña"
					datos["pag_activa"] = idioma + "/recuperar-pw.html"
				else:
					datos["mensaje"] = u"Su contraseña se ha actualizado correctamente. Ya puede iniciar sesión con su nombre de usuario y nueva contraseña"
		return render(request, 'base.html', datos)
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def buscar(request):
	# xHACER:  limpiar variables
		# GET y cadena de busqueda
		# limitar el tamaño de la cadena q recibe??
		# la validacion del paginador puede ir en el form
		# ordernar por valoracion y por nivel de los usrs
	idioma = request.LANGUAGE_CODE
	if request.method == "GET":
		formbuscar = FormBuscar(request.GET)
		if formbuscar.is_valid():
			consulta = formbuscar.cleaned_data["consulta"]  # request.GET["c"]
			usrs = Perfil.objects.filter(usuario__username__icontains=consulta, eliminado=False)
			servis = ServicioVirtual.objects.filter(activo=True, url__vendedor__eliminado=False, nombre__icontains=consulta, eliminado=False)
			for s in servis:
				try:
					s.nivel = NivelUsuario.objects.get(usuario=s.url.vendedor)
					s.valoraciones = Contador.objects.get(servicio=s)
				except:
					pass
			paginador = Paginator(servis, 20)
			n_pagina = request.GET.get("pagina")
			try:
				servis = paginador.page(n_pagina)
			except PageNotAnInteger:
				servis = paginador.page(1)
			except EmptyPage:
				servis = paginador.page(paginador.num_pages)

			datos = {
				'lista_usuarios': usrs,
				'lista_servicios': servis,
				'rango': paginador.page_range,
				'consulta': consulta,
				'pag_activa': idioma + "/busqueda.html",
				'idiomas_disponibles': IDIOMAS_DISPONIBLES,
			}
		if request.user.is_authenticated():
			p = get_object_or_404(Perfil, usuario=request.user)
			datos['perfil'] = p
			datos['perfil_logueado'] = p
			datos['logueado'] = True
		return render(request, 'base.html', datos)
	datos = {
		"formbuscar": FormBuscar(),
		"pag_activa": idioma + "/busqueda.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	return HttpResponseRedirect(reverse('/', datos))


def destacados(request, vista):
	# xHACER:
		# que el usr pueda decir de todos los idiomas plz...
	idioma = request.LANGUAGE_CODE
	if request.method == "GET":
		if vista == "mejores":
			lista = Contador.objects.filter(servicio__eliminado=False, servicio__activo=True, servicio__idioma=idioma)
			servis = ServicioVirtual.objects.filter(id__in=lista)

		if vista == "nuevos":
			servis = ServicioVirtual.objects.filter(activo=True, eliminado=False, url__vendedor__eliminado=False, idioma=idioma)

		for s in servis:
			try:
				s.nivel = NivelUsuario.objects.get(usuario=s.url.vendedor)
				s.valoraciones = Contador.objects.get(servicio=s)
			except:
				pass
		paginador = Paginator(servis, 20)
		n_pagina = request.GET.get("pagina")
		try:
			servis = paginador.page(n_pagina)
		except PageNotAnInteger:
			servis = paginador.page(1)
		except EmptyPage:
			servis = paginador.page(paginador.num_pages)

		datos = {
			'lista_servicios': servis,
			'rango': paginador.page_range,
			'vista': vista,
			'pag_activa': idioma + "/destacados.html",
			'idiomas_disponibles': IDIOMAS_DISPONIBLES,
		}
		if request.user.is_authenticated():
			p = get_object_or_404(Perfil, usuario=request.user)
			datos['perfil'] = p
			datos['perfil_logueado'] = p
			datos['logueado'] = True
		return render(request, 'base.html', datos)
	datos = {
		"pag_activa": idioma + "/destacados.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	return HttpResponseRedirect(reverse('/', datos))


def inicio(request):
	# val = request.META
	# ip_cabecera = request.META["REMOTE_ADDR"]  # remote_host, server_name
	# xDEPURAR:
	# y el http_referer en q lo puedo usar??
	idioma = request.LANGUAGE_CODE
	servis = ServicioVirtual.objects.filter(activo=True, idioma=idioma, url__vendedor__eliminado=False).order_by("-fecha_publicacion")[:8]
	for s in servis:
		try:
			s.valoraciones = Contador.objects.get(servicio=s)
			s.nivel = NivelUsuario.objects.get(usuario=s.url.vendedor)
		except:
			pass
	datos = {
		'nuevos_geos': servis,
		'idioma': idioma,
		# 'servicios_valorados': Valoracion.objects.all()[:8],
		# 'LANGUAGES': settings.LANGUAGES,
		'idiomas_disponibles': IDIOMAS_DISPONIBLES,
		# 'val': val,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil'] = p
		datos['perfil_logueado'] = p
		datos['logueado'] = True
	datos["pag_activa"] = idioma + "/index.html"
	return render(request, "base.html", datos)


def sesionar_usr(request):
	# xHACER:
		# usar is_activeen vez de eliminado para validar q no vuelvan a entrar
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))
	else:
		idioma = request.LANGUAGE_CODE
		datos = {
			"pag_activa": idioma + "/index.html",
			"idiomas_disponibles": IDIOMAS_DISPONIBLES,
		}
		try:
			# xHACER: estos Post estan filtrados!
			usuario = authenticate(username = request.POST['usuario'], password = request.POST['pw'])
			# xHACER:
				# esto es como deberia hacerse?:
				# user = authenticate(username=username, password=password)
				# if user is not None:
		except KeyError:
			datos["mensaje"] = 'Rellene todos los campos'
			return render(request, 'base.html', datos)
		if usuario is not None:
			if usuario.is_active:
				login(request, usuario)
			else:
				datos["mensaje"] = 'El usuario ha sido eliminado'
				return render(request, 'base.html', datos, RequestContext(request))
		else:
			datos["mensaje"] = 'Ingrese los datos correctamente'
			return render(request, 'base.html', datos)
		return HttpResponseRedirect(reverse('geoservicios.views.ver_perfil', args=[usuario]))


def cerrar_sesion(request):
	# xHACER:   # idioma = request.LANGUAGE_CODE
	logout(request)
	return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def sugerir(request):
	if request.user.is_authenticated():
		usr = request.user
		usr = Perfil.objects.get(usuario=usr)
		asunto = request.POST['asunto']
		txt = request.POST['txt']
		# xHACER:  deberia validar q no sean chimbos los datos
		Sugerencia.objects.create(texto=txt, asunto= asunto, usuario=usr)
	return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def proceso_compra(request):
	if request.user.is_authenticated():
		id_cola = request.POST.get("serv-cola")
		idioma = request.LANGUAGE_CODE
		p = Perfil.objects.get(usuario__username=request.user)
		serv_cola = get_object_or_404(Cola, id=id_cola)
		if p == serv_cola.comprador or p == serv_cola.vendedor:
			msj = ""
			if request.POST.get("ac"):
				pass  # xHACER:
			elif request.POST.get("exito"):
				precio_serv = serv_cola.servicio.url.precio
				comision_emp = precio_serv * COMISION_HV / 100
				comision_pay = (precio_serv * COMISION_PAYPAL["ganancia"] / 100) + COMISION_PAYPAL["neto"]
				pal_vendedor = precio_serv - (precio_serv * COMISION_PAYPAL["ganancia"] / 100) - COMISION_PAYPAL["neto"] - (precio_serv * COMISION_HV / 100)
				bien = pagar_vendedores(serv_cola)
				if bien:
					Factura.objects.create(comprador=serv_cola.comprador, url_servicio=serv_cola.servicio.url, comprador_pago=precio_serv, vendedor_recibe=pal_vendedor, comision_empresa=comision_emp, comision_paypal=comision_pay, contrato=serv_cola.contrato)
				else:
					datos = {
						"msj": "Hubo un error en el procesamiento del pago. Por favor vuelva a intetarlo, si persiste el error contacte a nuestro personal.",
						'pag_activa': idioma + "/index.html",
						'idiomas_disponibles': IDIOMAS_DISPONIBLES
					}
					if request.user.is_authenticated():
						p = get_object_or_404(Perfil, usuario__username = request.user)
						datos['logueado'] = True
						if perfil != p:
							datos['perfil_logueado'] = p
						else:
							datos['perfil_propio'] = True
					# u_extras = get_object_or_404(DatosExtraPerfil, usuario__iexact=usuario)
					return render(request, 'base.html', datos)
				# xHACER: falta guardar la conversacion en un lugar q no se borre y sirva de referencia
				# PAGAR al trabajador en Bs..
				return HttpResponseRedirect(reverse('geoservicios.views.ver_perfil', args=[p,]))  # xHACER: no se ve un mensaje diciendo q todo salio bien
			elif request.POST.get("mutuo-cancel"):
				if p == serv_cola.comprador:
					Cola.objects.filter(id=serv_cola.id).update(comprador_cancela=True)
					serv_cola.comprador_cancela = True
					msj = "1"
				elif p == serv_cola.vendedor:
					Cola.objects.filter(id=serv_cola.id).update(vendedor_cancela=True)
					serv_cola.vendedor_cancela = True
					msj = "2"
				if serv_cola.comprador_cancela and serv_cola.vendedor_cancela:
					bien = reembolsar(serv_cola)
					datos = {
						'perfil': p,
						'logueado': True,
						'perfil_logueado': p,
						"pag_activa": idioma + "/index.html",
						"idiomas_disponibles": IDIOMAS_DISPONIBLES,
					}
					if bien:
						Cola.objects.filter(id=serv_cola.id).update(estatus="C")
						datos["mensaje"] = "Se ha reembolsado todo el dinero exitosamente."
					else:
						datos["mensaje"] = "Debido a un error no se ha podido reembolsar el dinero. Por favor intentelo nuevamente."
						if p == serv_cola.comprador:
							Cola.objects.filter(id=serv_cola.id).update(comprador_cancela=False)
						elif p == serv_cola.vendedor:
							Cola.objects.filter(id=serv_cola.id).update(vendedor_cancela=False)
					return render(request, 'base.html', datos)
			conversa = str(request.POST.get('conversa'))
			return HttpResponseRedirect('/discusion/'+conversa+'/'+str(serv_cola.id)+'/'+msj+'/')
	return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


# xHACER:  validar q no pasa nada si hago sql-injection
def registrar_usr(request):
	try:
		idioma = request.LANGUAGE_CODE
		datos = {
			"pag_activa": idioma + "/index.html",
			"idiomas_disponibles": IDIOMAS_DISPONIBLES,
		}
		if not re.match('^[a-zA-Z0-9_]+$', request.POST['usuario']):
			datos["mensaje"] = 'El nombre de usuario solo puede contener letras, numeros y _'
			return render(request, 'base.html', datos)
		if not re.match('^[a-zA-Z][a-zA-Z0-9_\.-]*[@][a-zA-Z0-9_\.]+[.][a-zA-Z0-9_]+$', request.POST['correo']):
			datos["mensaje"] = 'Ingrese un correo valido'
			return render(request, 'base.html', datos)

		usr = request.POST['usuario'].lower()
		if User.objects.filter(username__iexact = usr):
			datos["mensaje"] = 'El usuario ya existe'
			return render(request, 'base.html', datos)
		u = User.objects.create_user(
			usr,
			request.POST['correo'],
			request.POST['pw'],
		)
		u.save()

		p = Perfil.objects.create(
			usuario = u,
			# ubicado_en = '',
		)
		vzlano = request.POST.get("vzlano", None)
		if vzlano:
			p.es_venezolano = True
		p.save()
		if vzlano:
			p.idiomas.add(Idioma.objects.get(codigo="es"))

		NivelUsuario.objects.create(usuario=p, nivel=Nivel.objects.get(numero=0))
		usr = authenticate(username= usr, password = request.POST['pw'])
		login(request, usr)
		return HttpResponseRedirect(reverse('geoservicios.views.ver_perfil', args=[usr]))
	except KeyError:
		datos["mensaje"] = 'Rellene todos los campos'
		return render(request, 'base.html', datos)


def ver_categoria(request, cat):
	# xHACER:  usar un paginador, validar cat, usar el promedio para ordenar las cat
	idioma = request.LANGUAGE_CODE
	cat = get_object_or_404(UrlCategoria, url=cat)
	cat.nombre = str(Categoria.objects.get(url=cat, idioma=idioma))

	urlsubcategorias = UrlCategoria.objects.filter(padre=cat)
	subcategorias = Categoria.objects.filter(url__in=urlsubcategorias, idioma=idioma)

	urls = UrlServicio.objects.filter(subcategoria__in=urlsubcategorias, vendedor__eliminado=False)
	lista_servs = ServicioVirtual.objects.filter(activo=True, idioma=idioma, url__in=urls)
	# xHACER: esta idea se puede mejorar, creando un solo objeto con los datos de ambos (urls y lista_servs)
	for i, serv in enumerate(lista_servs):
		lista_servs[i].vendedor = urls[i].vendedor
		lista_servs[i].precio = urls[i].precio
		try:
			lista_servs[i].nivel = NivelUsuario.objects.get(usuario=serv.url.vendedor)
			lista_servs[i].valoraciones = Contador.objects.get(servicio=serv)
		except:
			pass

	paginador = Paginator(lista_servs, 20)
	n_pagina = request.GET.get("pagina")
	try:
		lista_servs = paginador.page(n_pagina)
	except PageNotAnInteger:
		lista_servs = paginador.page(1)
	except EmptyPage:
		lista_servs = paginador.page(paginador.num_pages)
	datos = {
		'categoria': cat,
		'servicios': lista_servs,
		'rango': paginador.page_range,
		'subcategorias': subcategorias,
		"pag_activa": idioma + "/categoria.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil'] = p
		datos['perfil_logueado'] = p
		datos['logueado'] = True
		return render(request, 'base.html', datos)
	else:
		return render(request, 'base.html', datos)


def ver_subcategoria(request, cat, subcat):
	# xHACER:  usar un paginador, limpiar subcat,
	idioma = request.LANGUAGE_CODE
	cat = get_object_or_404(UrlCategoria, url=cat)
	cat.nombre = str(Categoria.objects.get(url=cat, idioma=idioma))
	cat.urlsubcategoria = UrlCategoria.objects.get(url=subcat, padre=cat)  # existen varias url "otros", debo delimitar
	cat.subcategoria = str(Categoria.objects.get(url=cat.urlsubcategoria, idioma=idioma))

	urlsubcategorias = UrlCategoria.objects.filter(padre=cat)
	subcategorias = Categoria.objects.filter(url__in=urlsubcategorias, idioma=idioma)

	urls = UrlServicio.objects.filter(subcategoria=cat.urlsubcategoria, vendedor__eliminado=False)
	lista_servs = ServicioVirtual.objects.filter(activo=True, idioma=idioma, url__in=urls)
	for i, serv in enumerate(lista_servs):
		lista_servs[i].vendedor = urls[i].vendedor
		lista_servs[i].precio = urls[i].precio
		try:
			lista_servs[i].valoraciones = Contador.objects.get(servicio=serv)
			lista_servs[i].nivel = NivelUsuario.objects.get(usuario=serv.url.vendedor)
		except:
			pass

	paginador = Paginator(lista_servs, 20)
	n_pagina = request.GET.get("pagina")
	try:
		lista_servs = paginador.page(n_pagina)
	except PageNotAnInteger:
		lista_servs = paginador.page(1)
	except EmptyPage:
		lista_servs = paginador.page(paginador.num_pages)
	datos = {
		'categoria': cat,
		'servicios': lista_servs,
		'rango': paginador.page_range,
		'subcategorias': subcategorias,
		"pag_activa": idioma + "/categoria.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil'] = p
		datos['perfil_logueado'] = p
		datos['logueado'] = True
		return render(request, 'base.html', datos)
	else:
		return render(request, 'base.html', datos)


def ver_servicio(request, cat, serv):
	# xHACER:  limpiar subcat, xq meti todo en ver_servicio (modular eliminar, editar, traducir)
	cat = get_object_or_404(UrlCategoria, url=cat)
	url = get_object_or_404(UrlServicio, url=serv)
	idioma = request.LANGUAGE_CODE
	band = True
	if request.method == "POST":
		try:
			if request.POST.get("traduccion_servicio", None):
				serv = ServicioVirtual.objects.get(url=url, idioma=request.POST["traduccion_servicio"])
				band = False
			elif request.POST.get("editar", None):
				idioma_serv = request.POST["idioma_serv"]
				cont = ""
				n_clausulas = request.POST.get("Nclausulas", None)  # modificado! n_clausulas = int(request.POST.get('Nclausulas', 1))
				if n_clausulas is not None:
					n_clausulas = int(n_clausulas)
					for k in range(n_clausulas):
						n = 'clausula-' + str(k)
						if request.POST[n] != "":
							cont += request.POST[n] + "<br>"
					cont = cont[: len(cont) - 4]  # le quito el ultimo <br>
				ServicioVirtual.objects.filter(url=url, idioma=idioma_serv).update(nombre=request.POST["nomb"], descripcion=request.POST["descrip"], contrato=cont)
				if idioma_serv != idioma:
					serv = ServicioVirtual.objects.get(url=url, idioma=idioma_serv)
					band = False
			elif request.POST.get("eliminar", None):
				idioma_serv = request.POST["idioma_serv"]
				eliminado = ServicioVirtual.objects.filter(url=url, idioma=idioma_serv).update(activo=False, eliminado=True)
				perfil = get_object_or_404(Perfil, usuario__username = request.user)
				datos = datos_perfil_venezolano(perfil, idioma)
				if eliminado == 1:
					datos["mensaje"] = "Servicio eliminado satisfactoriamente"
				else:
					datos["mensaje"] = "Hubo un error al eliminar el Servicio: %s" % serv
				datos['logueado'] = True
				datos['perfil_propio'] = True
				return render(request, 'base.html', datos)
		except:
			pass
	if band:  # xHACER: como predeterminar al idioma de la pag de una mejor manera?
		serv = ServicioVirtual.objects.get(url=url, idioma=idioma)
	cat.nombre = str(Categoria.objects.get(url=cat, idioma=idioma))
	cat.urlsubcategoria = serv.url.subcategoria
	cat.subcategoria = str(Categoria.objects.get(url=serv.url.subcategoria, idioma=idioma))
	idiomas_servicio = []
	for servis in ServicioVirtual.objects.filter(url=url, activo=True, eliminado=False):
		idiomas_servicio.append(servis.idioma)
	data = {}
	if serv.url.vendedor.eliminado:
		data["mensaje"] = "Lo sentimos, el usuario ha cancelado su cuenta"
	elif serv.eliminado:
		data["mensaje"] = "Lo sentimos, el usuario ha cancelado el servicio o esta de vacaciones"
	if data:
		return render(request, 'base.html', data)
	try:
		val = Contador.objects.get(servicio=serv)
		te = val.tiempo_entrega / val.experiencia
		exp = val.experiencia
		atencion = val.atencion / val.experiencia
		calidad = val.calidad / val.experiencia
	except:
		te, exp, atencion, calidad = 0, 0, 0, 0

	contrato = ""
	if serv.contrato != "":
		contrato = serv.contrato.split("<br>")

	#extras = ServicioSatelite.objects.filter(servicio=serv)
	datos = {
		"pag_activa": idioma + "/servicio.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
		'exp': exp,
		'te': te,
		'calidad': calidad,
		'atencion': atencion,
		'idiomas_servicio': idiomas_servicio,
		'servicio': serv,
		'contrato': contrato,
		'categoria': cat,
		#'servs_satelite': extras,
	}
	msj = request.GET.get("mensaje", None)  # xHACER: request.POST.get("mensaje", None)
	if msj == "error":
		datos["mensaje"] = u"Hubo un error al intentar la operación. Puedes intentarlo nuevamente. Si el error persiste por favor contacta a nuestro personal."
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil'] = p
		datos['logueado'] = True
		datos['perfil_logueado'] = p
		return render(request, 'base.html', datos)
	else:
		return render(request, 'base.html', datos)


def ver_perfil(request, usr):
	# xHACER:  tiempo estimado de entrega por cada servicio, x semana
	# numero de impresiones de anuncios en las busquedas
	# cant de usuarios atendidos por servicio
	# cant de servicios rechazados mutuamente
	idioma = request.LANGUAGE_CODE
	try:
		perfil = get_object_or_404(Perfil, usuario__username=usr, eliminado=False)
	except:
		data = {}
		data["mensaje"] = "Este usuario ha borrado su cuenta o no existe"
		data["pag_activa"] = idioma + "/index.html"
		data["idiomas_disponibles"] = IDIOMAS_DISPONIBLES
		return render(request, 'base.html', data)
	if perfil.es_venezolano:
		datos = datos_perfil_venezolano(perfil, idioma)

	else:  # no es venezolano
		datos = {}
		id_sc = request.GET.get("c", None)  # este valor aparece en la URL de error de paypal
		# if not id_sc:
		# 	id_sc = request.POST.get("ident", None)
		msj = request.GET.get("mensaje", None)
		if msj and id_sc:
			if msj == "bien":
				datos["mensaje"] = u"Perfecto! Muchas gracias por apoyar el desarrollo de Venezuela. Ahora solo debes esperar un poquito a que el Vendedor acepte tu solicitud y discutan como se entregará tu Servicio Virtual."  #  Recuerda visitar tu perfil y cuando el usuario te envie el archivo calificarlo para que compartas tu opinión con respecto al servicio
			if msj == "cancelado":
				actualizo = Cola.objects.filter(id=id_sc, estatus__in=["E","A"], comprador__usuario__username=request.user).update(estatus="C")
				if actualizo:
					reembolso = reembolsar(id_sc)
					if reembolso:
						datos["mensaje"] = u"Se ha cancelado la operación, puedes reintentarlo en cualquier momento. El dinero ha sido reembolsado."
					else:
						datos["mensaje"] = u"Hubo problemas para reembolsar el dinero porfavor recargue la página"
				else:
					datos["mensaje"] = u"No hay Servicios en Cola en nuestra Base de Datos."

		cola = Cola.objects.filter(estatus="E", comprador=perfil)
		aprobados = Cola.objects.filter(estatus="A", comprador=perfil)
		lista = []
		for item in cola:
			item.idioma = ServicioVirtual.objects.get(id=item.servicio.id).idioma
			if item.contrato != item.servicio.contrato:  # es un contrato distinto al contrato del servicio?
				# si lo es lo muestro, sino, es facil ubicar/recordar las clausulas
				item.contrato = item.contrato.split("<br>")
				item.contrato_mod = True
			else:
				item.contrato = []
			lista.append(item)
		facturas = Factura.objects.filter(comprador=perfil)
		n_facturas = facturas.count()
		invertido = 0
		if n_facturas > 0:
			for f in facturas:
				invertido += f.comprador_pago
			# valoraciones = Valoracion.objects.get(evaluador=perfil).count()  # xHACER: debo depurar q hacer luego de q se termina la operacion de compra
		CATEGORIAS = Categoria.objects.filter(url__padre=None, idioma=idioma)
		datos['perfil'] = perfil
		datos['invertido'] = invertido
		datos['n_compras'] = n_facturas
		datos['lista'] = lista
		datos['lista_aprobados'] = aprobados
		datos['categorias'] = CATEGORIAS
		# datos['n_valoraciones']: valoraciones
		datos['pag_activa'] = idioma + "/perfil.html"
		datos['idiomas_disponibles'] = IDIOMAS_DISPONIBLES

	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario__username = request.user)
		datos['logueado'] = True
		if perfil != p:
			datos['perfil_logueado'] = p
		else:
			datos['perfil_propio'] = True
	# u_extras = get_object_or_404(DatosExtraPerfil, usuario__iexact=usuario)
	return render(request, 'base.html', datos)


def traducir_servicio(request):
	# xHACER:
		# falta trabajar con los servicios satelite, precios segun pais
		# q el html, el select tenga un valor vacio que diga "Seleccionar idioma"
	if request.user.is_authenticated():
		# xDEPURAR:  crear un servicio fisico??
		url = request.POST["serv"]
		url_existe = UrlServicio.objects.filter(url=url).exists()
		if url_existe:
			url = UrlServicio.objects.get(url=url)
			idioma = request.POST["serv_traducido"]
			if url.obj_servicio.get().idioma != idioma:
				nomb = request.POST['nomb']
				usr = request.user
				p = Perfil.objects.get(usuario=usr)
				# xHACER:
					# limpiar todos los datos de entrada
					# revisar q no se traduzca al mismo idioma o devuelva un error
				descrip = request.POST['descrip']
				cont = ""
				n_clausulas = request.POST.get("Nclausulas", None)  # n_clausulas = int(request.POST.get('Nclausulas', 0))
				if n_clausulas is not None:
					n_clausulas = int(n_clausulas)
					for k in range(n_clausulas):
						n = 'clausula-' + str(k)
						if request.POST[n] != "":
							cont += request.POST[n] + "<br>"
					cont = cont[: len(cont) - 4]  # le quito el ultimo <br>
				s = ServicioVirtual.objects.create(url=url, idioma=idioma, nombre=nomb, descripcion=descrip, contrato=cont)  # , imagen=url.obj_servicio.get().imagen)
				Contador.objects.create(servicio=s, experiencia=0, atencion=0, calidad=0, promedio=0, tiempo_entrega=0)
			# xHACER: q tenga un else q mande un mensaje de error si es el mismo lenguaje al q quiere traducir
			return HttpResponseRedirect('/categoria/' + url.subcategoria.padre.url + "/" + url.subcategoria.url + "/" + url.url + "/")
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def crear_servicio(request):
	# xHACER:
		# q esta vista sea en realidad un formulario.. y q desde ver_perfil se llame,
		# esto pa validar q la url sea unica, ademas de otras cosas como los precios, etc
		# ó puedo usar ajax tambien
	if request.user.is_authenticated():
		# xDEPURAR:  crear un servicio fisico??
		usr = request.user
		p = Perfil.objects.get(usuario=usr)
		# xHACER:
			# si añade una categoria como tratarla?
			# limpiar todos los datos de entrada
		if request.method == 'POST':
			nomb = request.POST['nomb']
			url = uerelizar(nomb)
			# xHACER:
				# si tu eres un chino como coño traduces tu servicio a url??
				# el precio debe variar segun el nivel del usr
			descrip = request.POST['descrip']
			# if request.FILES:
			# 	usr_str = str(p)
			# 	if not access('Multimedia/images/' + usr_str, F_OK):
			# 		mkdir('Multimedia/images/' + usr_str)
			# 	with open('Multimedia/images/' + usr_str + '/name.png', 'wb+') as destination:
			# 		for chunk in request.FILES['img_serv'].chunks():
			# 			destination.write(chunk)
			cont = ""
			n_clausulas = request.POST.get("Nclausulas", None)  # n_clausulas = int(request.POST.get('Nclausulas', 0))  # modificado! 1
			if n_clausulas is not None:
				n_clausulas = int(n_clausulas)
				for k in range(n_clausulas):
					n = 'clausula-' + str(k)
					if request.POST[n] != "":
						cont += request.POST[n] + "<br>"
				cont = cont[: len(cont) - 4]  # le quito el ultimo <br>
			id_subc = int(request.POST['subc'])
			id_cat = int(request.POST['subcategoria'])
			LISTA_SUBCATEGORIAS = []
			CATEGORIAS = Categoria.objects.filter(url__padre=None, idioma=idioma)
			for i, cat in enumerate(CATEGORIAS):
				LISTA_SUBCATEGORIAS.append([i, Categoria.objects.filter(url__padre=cat.url, idioma=idioma)])
			subc = LISTA_SUBCATEGORIAS[id_cat][1][id_subc]
			try:
				precio = Decimal(request.POST['precio'])
				if precio > 500 or precio < 5:
					raise
				url_existe = UrlServicio.objects.filter(url=url).exists()
				if url_existe:
					u = UrlServicio.objects.get(url=url)
				else:
					u = UrlServicio.objects.create(url=url, subcategoria=subc.url, vendedor=p, precio=precio)
				# if request.FILES:
					# # xHACER:
					# 	# darle un nombre a la img yo
					# 	# meterlo en una carpeta del usr
					# 	# validar en la img: formato, peso, dimensiones??
					# img = request.FILES["img_serv"]
					# s = ServicioVirtual.objects.create(url=u, nombre=nomb, descripcion=descrip, contrato=cont, imagen=img)  # idioma no va xq el q crea los servicios es un venezolano
				# else:
				s = ServicioVirtual.objects.create(url=u, nombre=nomb, descripcion=descrip, contrato=cont)  # idioma no va xq el q crea los servicios es un venezolano
				Contador.objects.create(servicio=s, experiencia=0, atencion=0, calidad=0, promedio=0, tiempo_entrega=0)
			except BaseException, e:
				# xHACER:
					# que el except se porte bien dependiendo de cual sea el error
					# mostrar msj adecuadamente segun el error
				datos = datos_perfil_venezolano(p, request.LANGUAGE_CODE)
				if precio > 500:
					datos["mensaje"] = u"No se puede sobrepasar el precio techo (de 500 $) para ofrecer Servicios"
				elif precio < 5:
					datos["mensaje"] = u"No se puede sobrepasar el precio piso (de 5 $) para ofrecer Servicios"
				else:
					datos["mensaje"] = "Codigo de error: NXQPSA. Por Favor intentelo nuevamente y si persiste haganoslo saber y le atenderemos. Gracias!"  # No Xe Que PaSo Aqui  jajajaj
				if request.user.is_authenticated():
					perfil2 = get_object_or_404(Perfil, usuario__username = usr)
					datos['logueado'] = True
					if p != perfil2:
						datos['perfil_logueado'] = perfil2
					else:
						datos['perfil_propio'] = True
				return render(request, 'base.html', datos)
		return HttpResponseRedirect(reverse('geoservicios.views.ver_perfil', args=[usr]))
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


# def crear_complemento_servicio(request, servicio):
	# """este debe permanecer individual xq deberia ser capaz de procesar N numero de servicios extras"""
	# if request.user.is_authenticated():
	#   usr = request.user
	#   usr = Perfil.objects.get(usuario=usr)

	#   try:
	#       # xHACER:  sera q acepto servicio via get or post?? y ademas debo limpiar el dato!!
	#       serv = get_object_or_404(ServicioVirtual, id=servicio)
	#       nomb_complemento = request.POST['nomb-complemento']
	#       desc_complemento = request.POST['desc-complemento']
	#       precio_complemento = request.POST['precio-complemento']
	#       ServicioSatelite.objects.create(servicio_v=serv, usuario=usr, nombre=nomb_complemento, descripcion=desc_complemento, precio=precio_complemento)
	#   except:
	#       pass  # xHACER: q pasa si no se envia y q retorna al final
	#   return usr
	# else:
	#   return HttpResponseRedirect(reverse('geoservicios.views.sesionar_usr'))


def enlistar_usuario(request, usr):
	"""Enlistar solicitudes de servicio"""
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario__username=usr)
		idioma = request.POST.get("idioma_serv", request.LANGUAGE_CODE)
		url = request.POST["serv"]
		url = get_object_or_404(UrlServicio, url=url)
		serv = get_object_or_404(ServicioVirtual, url=url, idioma=idioma)
		if p == url.vendedor:
			# xHACER: quizas yo deba hacer mi propio redirect q envie datos POST
			datos = {
				'perfil': p,
				'perfil_logueado': p,
				'logueado': True,
				# 'lista': lista,
				"pag_activa": idioma + "/lista-solicitudes-servicio.html",
				"idiomas_disponibles": IDIOMAS_DISPONIBLES,
				"mensaje": "No puedes comprar tus propios servicios"
			}
			return render(request, 'base.html', datos)
		n_clausulas = request.POST.get("Nclausulas", None)
		if n_clausulas is not None:
			cont = ""
			n_clausulas = int(n_clausulas)
			for k in range(n_clausulas):
				n = 'clausula-' + str(k)
				if request.POST[n] != "":
					cont += request.POST[n] + "<br>"
			cont = cont[: len(cont) - 4]
			encola = Cola.objects.create(servicio=serv, estatus="E", comprador=p, vendedor=url.vendedor, contrato=cont)
		else:
			encola = Cola.objects.create(servicio=serv, estatus="E", comprador=p, vendedor=url.vendedor, contrato=serv.contrato)
		precio_serv = encola.servicio.url.precio
		comisiones = precio_serv - (precio_serv * COMISION_PAYPAL["ganancia"] / 100) - COMISION_PAYPAL["neto"] - (precio_serv * COMISION_HV / 100)
		datos_paypal = {
			# xHACER: falta enviar el precio de la comision para q se vea directo cuanto debe pagar
			"actionType": "PAY_PRIMARY",
			"currencyCode": "USD",
			"payKeyDuration": "P1D",  # XML Schema (especificamente Duration Data Type)
			"feesPayer": "SECONDARYONLY",
			"memo": u"Ud. adquirirá el servicio: " + unicode(serv),
			"receiverList": {
				"receiver": [{
					"amount": unicode(round(precio_serv,2)),
					"email": ACCESO_API_PAYPAL["CORREO_API"],
					"primary": True
				},{
					"amount": unicode(round(precio_serv-comisiones,2)),
					"email": unicode(url.vendedor.usuario.email) if not ACCESO_API_PAYPAL["CORREO_USR_API"] else ACCESO_API_PAYPAL["CORREO_USR_API"],
					"primary": False
				}]
			},
			"returnUrl": URL_SITIO + unicode(p) + "/?mensaje=bien&c=" + unicode(encola.id),
			"cancelUrl": URL_SITIO + unicode(p) + "/?mensaje=cancelado&c=" + unicode(encola.id),
			"requestEnvelope": {
				"errorLanguage": "en_US",
				"detailLevel": "ReturnAll"
			}
		}
		datos_paypal = json.dumps(datos_paypal)
		try:
			peticion = urllib2.Request(url=ACCESO_API_PAYPAL["URL_PAY"], data=datos_paypal, headers=ACCESO_API_PAYPAL["HEADERS_API"])
			com_paypal = urllib2.urlopen(peticion, timeout=360)
			resp_paypal = com_paypal.read()
			com_paypal.close()
			resp_paypal = json.JSONDecoder().decode(resp_paypal)
			if resp_paypal["responseEnvelope"]["ack"] == "Success":
				Intermediario.objects.create(clave_paypal=resp_paypal['payKey'], obj_cola=encola, comprador=encola.comprador, vendedor=encola.vendedor)
				return HttpResponseRedirect(ACCESO_API_PAYPAL["URL_GOPAY"] + resp_paypal['payKey'])
		except urllib2.URLError, motivo:
			pass
			# xHACER: terminar q pasa si no conecta con el servidor o si datos de paypal no vino como es
		Cola.objects.get(id=encola.id).delete()
		return HttpResponseRedirect("/categoria/" + unicode(url.subcategoria.padre) + "/" + unicode(url.subcategoria) + "/" + unicode(url) + "/?mensaje=error")
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


# si entro como vzlano/extranjero y quiero ver la lista de otro?
	# no se puede xq trabajo con el usr autenticado...

# es extranjero, entonces quiere ver que servicios a pedido
# es vendedor, entonces muestro sus clientes pidiendo servirles
def lista_solicitudes_servicio(request):
	"""Aceptar o rechazar solicitudes y mostrar la lista"""
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario__username=request.user)
		if p.es_venezolano:
			opc = request.POST.get("opc", None)
			msj_reembolso = None
			if opc:
				ident = request.POST["ident"]
				cola = get_object_or_404(Cola, id=ident, vendedor=p)
				if opc == "1":  # vendedor acepta el contrato
					from postman.models import Message
					from postman.api import pm_write  # xPENSAR: es buena idea importar aqui ?
					# este saludo es necesario para poder crear una conversacion y poder enviar a ambos usrs a que intercambien desde un enlace comun
					asunto_msj = "Estoy listo para empezar!"
					cuerpo_msj = "He aceptado realizar el Servicio Virtual " +str(cola.servicio)+ ", ¿pudiese aclararme que es exacmente lo que desea que realice? Al terminarlo me estaré comunicando con ud. con una primera version del Producto Virtual y luego puede presionar en \"Operacion Exitosa\" si esta le satisface. Gracias por preferirme!"
					asunto_resp = "Gracias por aceptar el pedido"
					cuerpo_resp = "Gracias de antemano y dentro de poco te envio la informacion necesaria."
					msj = pm_write(cola.vendedor.usuario, cola.comprador.usuario, asunto_msj, body=cuerpo_msj, skip_notification=False, auto_archive=False, auto_delete=False, auto_moderators=None, devuelve=True)
					resp = pm_write(cola.comprador.usuario, cola.vendedor.usuario, asunto_resp, body=cuerpo_resp, skip_notification=False, auto_archive=False, auto_delete=False, auto_moderators=None, devuelve=True)
					Message.objects.filter(id=msj.id).update(thread=resp)
					Message.objects.filter(id=resp.id).update(thread=resp)
					msj = Message.objects.get(id=msj.id)
					Cola.objects.filter(id=ident, vendedor=p).update(estatus="A", conversacion=msj.thread_id)
					# xHACER: validar q sea exactamente el servicio q quiero
				if opc == "2":  # vendedor rechaza la solicitud
					bien = reembolsar(cola)
					if bien:
						msj_reembolso = u"Se ha cancelado el servicio satisfactoriamente y se realizó el reembolso al comprador."
						Cola.objects.filter(id=ident, vendedor=p).update(estatus="C")
					else:
						msj_reembolso = u"Hubo un error al cancelar el servicio ya que no se pudo reembolsar el dinero al comprador."
			cola = Cola.objects.filter(estatus="E", vendedor=p)
			aprobados = Cola.objects.filter(estatus="A", vendedor=p)
			lista = []
			lista_aprobados = []
			for item in cola:
				serv_original = ServicioVirtual.objects.get(id=item.servicio.id)
				item.nombre = unicode(item.servicio)
				if item.contrato != serv_original.contrato:  # es un contrato distinto al contrato del servicio? (comparandolo con el del mismo idioma con el q el usuario lo contrato)
					# si lo es lo muestro, sino, es facil ubicar/recordar las clausulas
					item.contrato = item.contrato.split("<br>")
					item.contrato_mod = True
				else:
					item.contrato = []
				lista.append(item)
			for item in aprobados:
				serv_original = ServicioVirtual.objects.get(id=item.servicio.id)
				item.nombre = unicode(item.servicio)
				if item.contrato != serv_original.contrato:  # es un contrato distinto al contrato del servicio? (comparandolo con el del mismo idioma con el q el usuario lo contrato)
					# si lo es lo muestro, sino, es facil ubicar/recordar las clausulas
					item.contrato = item.contrato.split("<br>")
					item.contrato_mod = True
				else:
					item.contrato = []
				lista_aprobados.append(item)
			idioma = request.LANGUAGE_CODE
			datos = {
				'perfil': p,
				'perfil_logueado': p,
				'logueado': True,
				'aprobados': lista_aprobados,
				'lista': lista,
				'mensaje': msj_reembolso,
				"pag_activa": idioma + "/encolados.html",
				"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			}
			return render(request, 'base.html', datos)
	return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def facturados(request):
	if request.user.is_authenticated():
		p = Perfil.objects.get(usuario__username=request.user)
		facts = Factura.objects.filter(url_servicio__vendedor = p)
		for f in facts:
			f.contrato = f.contrato.split("<br>")

		datos = {
			"pag_activa": "es/facturados.html",  # todos los q venden son venezolanos por tanto español es el unico idioma
			"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			'perfil': p,
			'facts': facts,
			'logueado': True,
			'perfil_logueado': p,
		}
		return render(request, 'base.html', datos)
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


# xHACER:
	# falta pais estado ciudad por guardar
def configurar_cta(request):
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		idioma = request.LANGUAGE_CODE
		datos = {
			"pag_activa": idioma + "/config.html",
			"idiomas_disponibles": IDIOMAS_DISPONIBLES,
			'perfil': p,
			'logueado': True,
			'perfil_logueado': p,
		}
		try:
			if request.method == "POST":
				valores = [p.nombre_completo, p.edad, p.vacacionando, p.sexo, p.idiomas]
				for i, dat in enumerate(['nombre_completo', 'edad', 'vacacionando', 'sexo', 'lenguas']):
					if request.POST.get(dat, None):
						valores[i] = request.POST[dat]

				p.nombre_completo = valores[0]
				p.edad = valores[1]
				p.vacacionando = bool(int(valores[2]))  # el boleano llega es como una cadena de txt... "0" ó "1" no un entero
				p.sexo = valores[3]
				p.save()
				valores[4] = valores[4].split(",")
				if idioma not in valores[4]:
					valores[4].append(idioma)

				# xHACER:
					# esto creo q puede ser mas eficiente
				p.idiomas.clear()
				for leng in valores[4]:
					p.idiomas.add(Idioma.objects.get(codigo=leng))

				datos["idiomas_usr_habla"] = [idiomas_usr.codigo for idiomas_usr in p.idiomas.all()]
				datos["perfil"] = p
				datos["mensaje"] = "Se guardaron tus cambios!"
			else:
				datos["idiomas_usr_habla"] = idioma
		except KeyError, e:
			datos["mensaje"] = "Codigo de error: NXQPT. Por Favor intentelo nuevamente y si persiste haganoslo saber y le atenderemos. Gracias!"  # No Xe Que PaSo Tampoco  jajajaj
		return render(request, 'base.html', datos)
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def borrar_cta(request):
	"""Actualmente conservo Valoracion para saber si el q se fue era bueno en lo que hace, ServiciosVirtuales/Setelite para tener control de las facturas hechas"""
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		idioma = request.LANGUAGE_CODE
		datos = {
			"pag_activa": idioma + "/index.html",
			"idiomas_disponibles": IDIOMAS_DISPONIBLES
		}
		try:
			p.eliminado = True
			p.save()
			if ServicioVirtual.objects.filter(url__vendedor=p):
				ServicioVirtual.objects.filter(url__vendedor=p).update(eliminado=True)
			# ServicioSatelite.objects.filter(servicio=s).update(eliminado=True)
			Cola.objects.filter(comprador=p).delete()
			# Contador.objects.filter(servicio__url__vendedor=p).delete()  # este pudiese ser, q mande a sacar el promedio con lo q tiene el contador hasta ahora, y luego elimina
			# Disponibilidad.objects.filter(servicio__vendedor=p).delete()
			logout(request)
			datos["mensaje"] = "Su cuenta ha sido cerrada. Puedes volver cuando quieras, Te extrañaremos!  =("

		except BaseException, e:
			datos["mensaje"] = "Codigo de error: NXQEPD. Por Favor intentelo nuevamente y si persiste haganoslo saber y le atenderemos. Gracias!"  # No Xe Que Esta Pasando Dios mio  jajajaj

		return render(request, 'base.html', datos)
	else:
		return HttpResponseRedirect(reverse('geoservicios.views.inicio'))


def contactar_empresa(request):
	idioma = request.LANGUAGE_CODE
	datos = {
		"pag_activa": idioma + "/contacto.html",
		"idiomas_disponibles": IDIOMAS_DISPONIBLES,
	}
	if request.user.is_authenticated():
		p = get_object_or_404(Perfil, usuario=request.user)
		datos['perfil_logueado'] = p
		datos['logueado'] = True
		return render(request, 'base.html', datos)
	else:
		return render(request, 'base.html', datos)
