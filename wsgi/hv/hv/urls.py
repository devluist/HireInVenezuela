# -*- coding: utf-8 -*-

""" hv URL Configuration
	The `urlpatterns` list routes URLs to views. For more information please see:
		https://docs.djangoproject.com/en/1.8/topics/http/urls/
	Examples:
	Function views
		1. Add an import:  from my_app import views
		2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
	Class-based views
		1. Add an import:  from other_app.views import Home
		2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
	Including another URLconf
		1. Add an import:  from blog import urls as blog_urls
		2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

# xHACER: las siguientes dos lineas son temporales, solo dunrante desarrollo
# from django.conf import settings
from django.conf.urls.static import static
from postman.views import ConversationView

from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = patterns('geoservicios.views',
	## Examples:
	## url(r'^$', 'hv.views.home', name='home'),
	## url(r'^blog/', include('blog.urls')),
	url('^$', 'inicio'),

	url('^buscar/$', 'buscar'),
	url('^(?P<vista>nuevos)-servicios/$', 'destacados'),
	url('^(?P<vista>mejores)-servicios/$', 'destacados'),

	url('^sesionarme/$', 'sesionar_usr'),
	url('^cierre-sesion/$', 'cerrar_sesion'),
	url('^registrarme/$', 'registrar_usr'),

	url('^perfil/(?P<usr>[a-zA-Z0-9_]+)/$', 'ver_perfil'),
	url('^configuracion/$', 'configurar_cta'),
	url('^borrar-cta/$', 'borrar_cta'),
	url('^lengua/$', 'idioma'),
	url('^recuperar-cuenta/clave=(?P<clave>[a-zA-Z0-9-_\+]+)&correo=(?P<correo>[a-zA-Z0-9-_]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)$', 'recuperar_pw'),
	url('^recuperar-cuenta/$', 'recuperar_pw'),

	url('^categoria/(?P<cat>[a-zA-Z-]+)/$', 'ver_categoria'),
	url('^categoria/(?P<cat>[a-zA-Z-]+)/(?P<subcat>[a-zA-Z-\+\.]+)/$', 'ver_subcategoria'),
	url('^categoria/(?P<cat>[a-zA-Z-]+)/[a-zA-Z-+]+/(?P<serv>[0-9a-zA-Z-_()!\.,\']+)/$', 'ver_servicio'),
	#url('^cuadroHonor/$', 'ver_cuadro_honor'),

	url('^enlistar-usuario/(?P<usr>[a-zA-Z0-9_]+)/$', 'enlistar_usuario'),
	url('^lista-solicitudes-servicio/$', 'lista_solicitudes_servicio'),
	url('^crear-servicio/$', 'crear_servicio'),
	url('^traducir-servicio/$', 'traducir_servicio'),
	url('^comprando/$', 'proceso_compra'),
	url('^facturas/$', 'facturados'),

	url('^sugerencia/$', 'sugerir'),
	url('^contacto/$', 'contactar_empresa'),

	url(r'^discusion/(?P<thread_id>[\d]+)/(?P<obj_cola>[\d]+)/$', ConversationView.as_view(template_name='es/discusion.html'), name='view_conversation'),
	url(r'^discusion/(?P<thread_id>[\d]+)/(?P<obj_cola>[\d]+)/(?P<msj>[\d]+)/$', ConversationView.as_view(template_name='es/discusion.html'), name='view_conversation'),
	(r'^mensajeria/', include('postman.urls', namespace='postman', app_name='postman')),

	url('^admin/', include(admin.site.urls)),

	# xHACER:  url('^borrar/(?P<id_tlmsj>\\d+)/$', 'borrar'),
) # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # xHACER: temporal, solo dunrante desarrollo

# xHACER: se pueden eliminar lo q no es una vista y pasar a funciones/form que simplementen procesen, x ejm:
	# enlistar-usuario
	# sugerir
	# idioma
	# sesionar_usr
	# cerrar sesion
	# registrar_usr
	# borrar_cta
