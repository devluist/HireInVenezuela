# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

# xPENSAR:
	# xq idioma es idiomas del usr, xq no hay una relacion entre servicios e idiomas xejm??


class Idioma(models.Model):
	"""Description: Almacena los idiomas que habla cada usuario"""
	codigo = models.CharField(max_length=5, primary_key=True, unique=True)

	def __unicode__(self):
		return "%s" % self.codigo


# xHACER:
	# Perfil deberia heredar de User?
	# xq quizas conviene usar sus metodos.. is_active, get_fullname, etc
	# o actualizar como se usa User (Abstract....)
class Perfil(models.Model):
	LISTA = (
		("M", "Mujer"),
		("H", "Hombre"),
		("D", "Sexodiverso"),
	)
	usuario = models.OneToOneField(User)
	idiomas = models.ManyToManyField(Idioma)
	nombre_completo = models.CharField(max_length=50, default="")
	# ci = models.CharField(max_length="30", default="")
	edad = models.IntegerField(default=0)
	vacacionando = models.BooleanField(default=False)
	eliminado = models.BooleanField(default=False)
	sexo = models.CharField(max_length=1, blank=True, null=True, choices=LISTA)
	es_venezolano = models.BooleanField(default=False)
	# foto = models.ImageField()

	def __unicode__(self):
		return "%s" % self.usuario


class Nivel(models.Model):
	""" El id te dice el nivel. El precio siempre sera en dolares dentro del sistema.
		NIVEL 0
		---------------
		Usr debe comprobar que existe, que esta activo y q es dinero sano, 4$ fijos


		NIVEL 1						  BENEFICIOS
		---------------				---------------
		experiencia > 10			hasta 10$
		f_ingreso > 1 mes			1 satelite x servicio (menos de 5$)


		NIVEL 2						  BENEFICIOS
		---------------				---------------
		promedio > 5				hasta 20$ ---> 50
		f_ingreso > 3 meses			3 satelite x servicio (q sumen menos de 5$) --> 25
		experiencia > 25


		NIVEL 3						  BENEFICIOS
		---------------				---------------
		promedio > 7				hasta 30$ ---> 100
		f_ingreso > 6 meses			3 satelite x servicio (q sumen menos de 10$) --> 50
		experiencia > 100


		** NIVEL 4					  BENEFICIOS
		---------------				---------------
		promedio > 8				hasta 500$
		f_ingreso > 6/9 m (750 Bs?)	5 satelite x servicio (q sumen menos de 250$)
		experiencia > 250
	"""
	numero = models.PositiveSmallIntegerField(primary_key=True)
	# requisitos
	promedio = models.PositiveSmallIntegerField()
	experiencia = models.PositiveSmallIntegerField()
	meses_laborando = models.PositiveSmallIntegerField()
	# beneficios
	precio_max = models.DecimalField(decimal_places=2, default=400.00, max_digits=5)
	max_satelites = models.PositiveSmallIntegerField()
	precio_max_sat = models.DecimalField(decimal_places=2, default=250.00, max_digits=5)

	def __unicode__(self):
		return "%d" % self.numero


class NivelUsuario(models.Model):
	usuario = models.ForeignKey(Perfil)
	nivel = models.ForeignKey(Nivel)

	def __unicode__(self):
		return "%s" % self.nivel


# class BusquedaEficiente(models.Model):
	# """Quizas seria buena idea crear una tabla con menos claves foraneas y menos columnas para que sea mas eficiente la busqueda"""


# class DatosExtraPerfil(models.Model):
	## ubicacion, tanto si es vzlano como si es extranjero
	# usuario = models.ForeignKey(Perfil, unique=True)
	# codigo_QR = models.CharField(max_length=250)
	# cuenta_paypal = models.CharField(max_length=250)
	# cuenta_mercadopago = models.CharField(max_length=250)

	# def __unicode__(self):
	# 	return "%s" % self.usuario


class UrlCategoria(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.CharField(max_length=75)
	padre = models.ForeignKey('self', blank=True, null=True, related_name="hijos")

	class Meta:
		unique_together = ('url', 'padre')

	def __unicode__(self):
		return "%s" % self.url


class Categoria(models.Model):
	nombre = models.CharField(max_length=75)
	descripcion = models.CharField(max_length=250)
	url = models.ForeignKey(UrlCategoria)
	idioma = models.CharField(max_length=5, default="es")

	def __unicode__(self):
		return "%s" % self.nombre


#class CuadroHonor(models.Model):
	# """Este es distinto a valoracion, y contador ya que este guarda una imagen mensual los otros no. Es un historial de los 30 puestos mejor valorados cada trimestre/semestre/año en un estado/pais. Donde
	# 0 = atencion, 1 = tiempo de entrega, 2 = calidad del producto, 3 = promedio, 4 = experiencia acumulada//ESTAS NO? 5 = precio justo, 6 = cantidad de medallas"""
	# # fecha = models.DateField()
	# usuario = models.ForeignKey(Perfil)
	# puntaje = models.PositiveSmallIntegerField()
	# tipo_puntaje = models.PositiveSmallIntegerField()

	# mes = models.PositiveSmallIntegerField()
	# anio = models.PositiveSmallIntegerField()

	# class Meta:
	# 	# unique_together = ( ('usuario', 'fecha'))
	# 	unique_together = ( ('usuario', 'mes', 'anio'))
	# 	ordering = ["tipo_puntaje", "-puntaje"]

	# def __unicode__(self):
	# 	return "%s" % self.usuario


# class ActividadExtras(models.Model):
	# """Cuantas veces se usa un determinado servicio satelite"""
	# servicio = models.ForeignKey(ServicioSatelite)
	# cantidad = models.BigIntegerField()

	# def __unicode__(self):
		# return "%d" % self.cantidad


# class Visitas(models.Model):
	# usuario = models.ForeignKey(Perfil, unique=True)
	# cantidad = models.BigIntegerField()
	# servicio = models.ForeignKey(UrlServicio)
	# pais del visitante

	# def __unicode__(self):
	# 	return "%d" % self.cantidad


class UrlServicio(models.Model):
	""" Precio es en dolares dentro del sistema, al usr le pido que ingrese por su cuenta cual debe ser el precio por dicho servicio en dolares igual, y yo lo multiplico en la vista al cambio en bolivares """
	url = models.CharField(max_length=100, primary_key=True, unique=True)
	subcategoria = models.ForeignKey(UrlCategoria)
	vendedor = models.ForeignKey(Perfil)
	precio = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

	def __unicode__(self):
		return "%s" % self.url


class ServicioVirtual(models.Model):
	"""Eliminado existe para no borrar estos datos para las facturas. El maximo valor del precio (PSI field) que toma para Django v1.7 es 32767
	El precio no esta aqui para poder evitar las preferencias por parte de los usr, asi soy yo el que impongo que valor se paga por cada dolar/peso/libra, etc
	Cada una de estas instancias representa una traduccion del mismo servicio, es decir siempre se crea una en español y luego se puede traducir
	La fecha la tienen los servicios para saber cuando se tradujo y sobre todo para poder traer los nuevos servicios (buqueda por fecha)"""
	url = models.ForeignKey(UrlServicio, related_name="obj_servicio")
	idioma = models.CharField(max_length=5, default="es")
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=250)
	activo = models.BooleanField(default=True)
	contrato = models.TextField()
	eliminado = models.BooleanField(default=False)
	imagen = models.ImageField(upload_to="alla", blank=True, null=True)  # imagen/video
	fecha_publicacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (("url", "idioma"))
		ordering = ["fecha_publicacion"]

	def __unicode__(self):
		return u"%s" % self.nombre


#class ServicioSatelite(models.Model):
	# """Es un servicio complementario, es decir, que acompaña al servicio principal por un costo extra. Eliminado existe para no borrar estos datos para las facturas"""
	# servicio = models.ForeignKey(UrlServicio)
	# descripcion = models.CharField(max_length=250)
	# precio = models.DecimalField(decimal_places=2, default=4.00, max_digits=5)
	# activo = models.BooleanField(default=True)
	# eliminado = models.BooleanField(default=False)

	# def __unicode__(self):
	# 	return "%s" % self.descripcion


class Factura(models.Model):
	"""Pago (para Django v1.7) puede manejar hasta..."""
	# xHACER: poner q la id sea una vaina codificada como los codigos de barra y no un int
	# verificar la cantidad maxima... cuanto es lo max q se puede facturar luego de q se usen Serv Satelite y eso...
	comprador = models.ForeignKey(Perfil)
	fecha = models.DateTimeField(auto_now_add=True)
	url_servicio = models.ForeignKey(UrlServicio)
	comprador_pago = models.DecimalField(decimal_places=2, default=0.00, max_digits=12)  # pago que hizo el comprador
	vendedor_recibe = models.DecimalField(decimal_places=2, default=0.00, max_digits=12)  # pago para el vendedor
	comision_empresa = models.DecimalField(decimal_places=2, default=0.00, max_digits=12)
	comision_paypal = models.DecimalField(decimal_places=2, default=0.00, max_digits=12)
	porcentaje_comision = models.PositiveSmallIntegerField(default=30)
	contrato = models.TextField()

	def __unicode__(self):
		return "%d" % self.id


class Cola(models.Model):
	# xHACER:
		# quizas estado deberian ser todos espera, hasta q salga de la cola, y cancelado seria una operacion q te resta ptos??
	ESTADO = (
		("E", "En espera (el vendedor debe aceptar la solicitud)"),
		("A", "En espera (pero aceptada la compra/venta)"),
		("C", "Cancelada")
	)
	estatus = models.CharField(max_length=1, blank=True, choices=ESTADO, default=0)
	comprador_cancela = models.BooleanField(default=False)
	vendedor_cancela = models.BooleanField(default=False)
	fecha = models.DateTimeField(auto_now_add=True)
	servicio = models.ForeignKey(ServicioVirtual)
	comprador = models.ForeignKey(Perfil, related_name='comprador_cola')
	vendedor = models.ForeignKey(Perfil, related_name='vendedor_cola')  # esto sale de:  servicio__usuario..... SI PERO CUANDO TENGO SOLO EL vendedor Y NO EL servicio??
	contrato = models.TextField()
	conversacion = models.PositiveIntegerField(null=True, blank=True)  # ya sea el id de la cola o la factura....  ESTO ESTA MAL AQUI! CUANDO BORRE DE COLA SE ELIMINA LA REFERENCIA A LA CONVERSACION----> PROHIBIR Q SE BORREN LOS MSJS PRE-FACTURACION
	# unique=True? null puede ser unique??
	# eliminada = models.BooleanField(default=False)

	class Meta:
		ordering = ["fecha"]

	def __unicode__(self):
		return u"%s" % self.servicio


class Intermediario(models.Model):
	"""Recibimos el dinero, mientras se confirma la transaccion. Si está en Intermediario, quiere decir que no se ha facturado hacia mi cuenta ni para la del vendedor (por eso lleva el id del objeto en Cola)"""
	clave_paypal = models.CharField(max_length=20, primary_key=True)  # payKey
	obj_cola = models.ForeignKey(Cola)
	comprador = models.ForeignKey(Perfil, related_name='comprador_intermediario')
	vendedor = models.ForeignKey(Perfil, related_name='vendedor_intermediario')

	def __unicode__(self):
		return u"%s" % self.vendedor


# class ExtrasFactura(models.Model):
	# factura = models.ForeignKey(Factura)
	# pago = models.PositiveIntegerField()
	# serv_extra = models.ForeignKey(ServicioSatelite)

	# def __unicode__(self):
		# return "%d" % self.pago


class Contador(models.Model):
	"""Es una copia modificable que va escalando (sumatoria). Cada mes se toma una "foto" promediada de lo que se almacena en esta tabla, para guardar el incremento/decremento del puntaje de un usuario. Esto para calcular posiciones en el cuadro de honor"""
	servicio = models.ForeignKey(ServicioVirtual)
	atencion = models.BigIntegerField()
	calidad = models.BigIntegerField()
	tiempo_entrega = models.BigIntegerField()
	experiencia = models.BigIntegerField()
	promedio = models.BigIntegerField()
	# class Meta:
		# unique_together = (('usuario', 'servicio'))

	class Meta:
		ordering = ["-promedio"]

	def __unicode__(self):
		return "%d" % self.promedio


# class Disponibilidad(models.Model):
	# """Permite que el usuario eleja cuantos usuarios puede atender en cuantos dias. Ejemplo: 3 clientes en 1 dia"""
	# servicio = models.OneToOneField(ServicioVirtual)
	# contador = models.PositiveSmallIntegerField(default=0)
	# maximo = models.PositiveSmallIntegerField(default=1)
	# num_dias = models.PositiveSmallIntegerField(default=7)

	# def __unicode__(self):
	# 	return "%d" % self.contador


class Valoracion(models.Model):
	"""Es la reseña de cada transaccion que hace cada extranjero a un venezolano"""
	evaluador = models.ForeignKey(Perfil)
	atencion = models.PositiveSmallIntegerField(default=0)
	tiempo_entrega = models.PositiveSmallIntegerField(default=0)
	calidad = models.PositiveSmallIntegerField(default=0)
	# precio = models.SmallIntegerField(default=0)
	promedio = models.PositiveSmallIntegerField(default=0)
	estafa = models.BooleanField(default=False)
	eliminada = models.BooleanField(default=False)
	servicio = models.ForeignKey(ServicioVirtual)

	class Meta:
		ordering = ["-promedio"]

	def __unicode__(self):
		return "%d" % self.promedio


class Sugerencia(models.Model):
	texto = models.TextField()
	asunto = models.CharField(max_length=150)
	usuario = models.ForeignKey(Perfil)

	def __unicode__(self):
		return "%s" % self.asunto
