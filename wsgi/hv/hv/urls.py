# -*- coding: utf-8 -*-

from settings import desarrollando
from postman.views import ConversationView
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('geoservicios.views',
	url('^$', 'inicio'),

	url('^buscar/$', 'buscar'),
	url('^(?P<vista>nuevos|mejores)-servicios/$', 'destacados'),

	url('^sesionarme/$', 'sesionar_usr'),
	url('^cierre-sesion/$', 'cerrar_sesion'),
	url('^registrarme/$', 'registrar_usr'),

	url('^perfil/(?P<usr>[a-zA-Z0-9_]+)/$', 'ver_perfil'),
	url('^configuracion/$', 'configurar_cta'),
	url('^borrar-cta/$', 'borrar_cta'),
	url('^lengua/$', 'cambiar_idioma'),
	url('^recuperar-cuenta/clave=(?P<clave>[a-zA-Z0-9-_\+]+)&correo=(?P<correo>[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)$', 'recuperar_pw'),
	url('^recuperar-cuenta/$', 'recuperar_pw'),

	url('^categoria/(?P<cat>[a-zA-Z0-9-]+)/$', 'ver_categoria'),
	url('^categoria/(?P<cat>[a-zA-Z0-9-]+)/(?P<subcat>[a-zA-Z0-9-+]+)/$', 'ver_subcategoria'),
	url('^categoria/(?P<cat>[a-zA-Z0-9-]+)/[a-zA-Z0-9-+]+/(?P<serv>[a-zA-Z0-9-+]+)/$', 'ver_servicio'),
	# xPENSAR: ¿es seguro incluir el ' ya q los gringos lo usan mucho...?
	# NOTA: servicio es el nombre "uerelizado" osea en forma de url, osea sin vainas raras solo simbolos basicos de una url
	#url('^cuadroHonor/$', 'ver_cuadro_honor'),

	url('^enlistar-usuario/(?P<usr>[a-zA-Z0-9_]+)/$', 'enlistar_usuario'),
	url('^lista-solicitudes-servicio/$', 'lista_solicitudes_servicio'),
	url('^crear-servicio/$', 'crear_servicio'),
	url('^traducir-servicio/$', 'traducir_servicio'),
	url('^comprando/$', 'proceso_compra'),
	url('^facturas/$', 'facturados'),

	url('^sugerencia/$', 'sugerir'),
	url('^oportunidades-(?P<tipo>inversion|empleo)/$', 'mostrar_oportunidad'),
	url('^contacto/$', 'contactar_empresa'),

	url(r'^discusion/(?P<thread_id>[\d]+)/(?P<obj_cola>[\d]+)/$', ConversationView.as_view(template_name='postman/discusion.html'), name='view_conversation'),
	url(r'^discusion/(?P<thread_id>[\d]+)/(?P<obj_cola>[\d]+)/(?P<msj>[\d]+)/$', ConversationView.as_view(template_name='postman/discusion.html'), name='view_conversation'),
	(r'^mensajeria/', include('postman.urls', namespace='postman', app_name='postman')),

	url('^admin/', include(admin.site.urls)),
	url(r'^googlea6116be28450736e.html/$', TemplateView.as_view(template_name="googlea6116be28450736e.html")),
	url('^robots.txt/$', TemplateView.as_view(template_name="robots.txt")),
	#url('googlea6116be28450736e.html', )

	# xHACER:  url('^borrar/(?P<id_tlmsj>\\d+)/$', 'borrar'),
)

if desarrollando:
	from django.conf.urls.static import static
	from settings import STATIC_ROOT, STATIC_URL, MEDIA_URL, MEDIA_ROOT
	urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)

# xHACER: se pueden eliminar lo q no es una vista y pasar a funciones/form que simplementen procesen, x ejm:
	# enlistar-usuario
	# sugerir
	# idioma
	# sesionar_usr
	# cerrar sesion
	# registrar_usr
	# borrar_cta
