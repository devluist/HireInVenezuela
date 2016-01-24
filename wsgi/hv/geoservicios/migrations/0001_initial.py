# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=75)),
                ('descripcion', models.CharField(max_length=250)),
                ('idioma', models.CharField(default=b'es', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Cola',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estatus', models.CharField(default=0, max_length=1, blank=True, choices=[(b'E', b'En espera (el vendedor debe aceptar la solicitud)'), (b'A', b'En espera (pero aceptada la compra/venta)'), (b'C', b'Cancelada')])),
                ('comprador_cancela', models.BooleanField(default=False)),
                ('vendedor_cancela', models.BooleanField(default=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('contrato', models.TextField()),
                ('conversacion', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Contador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atencion', models.BigIntegerField()),
                ('calidad', models.BigIntegerField()),
                ('tiempo_entrega', models.BigIntegerField()),
                ('experiencia', models.BigIntegerField()),
                ('promedio', models.BigIntegerField()),
            ],
            options={
                'ordering': ['-promedio'],
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('comprador_pago', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('vendedor_recibe', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('comision_empresa', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('comision_paypal', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('porcentaje_comision', models.PositiveSmallIntegerField(default=30)),
                ('contrato', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Idioma',
            fields=[
                ('codigo', models.CharField(max_length=5, unique=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Intermediario',
            fields=[
                ('clave_paypal', models.CharField(max_length=20, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('numero', models.PositiveSmallIntegerField(serialize=False, primary_key=True)),
                ('promedio', models.PositiveSmallIntegerField()),
                ('experiencia', models.PositiveSmallIntegerField()),
                ('meses_laborando', models.PositiveSmallIntegerField()),
                ('precio_max', models.DecimalField(default=400.0, max_digits=5, decimal_places=2)),
                ('max_satelites', models.PositiveSmallIntegerField()),
                ('precio_max_sat', models.DecimalField(default=250.0, max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='NivelUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nivel', models.ForeignKey(to='geoservicios.Nivel')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_completo', models.CharField(default=b'', max_length=50)),
                ('edad', models.IntegerField(default=0)),
                ('vacacionando', models.BooleanField(default=False)),
                ('eliminado', models.BooleanField(default=False)),
                ('sexo', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Mujer'), (b'H', b'Hombre'), (b'D', b'Sexodiverso')])),
                ('es_venezolano', models.BooleanField(default=False)),
                ('idiomas', models.ManyToManyField(to='geoservicios.Idioma')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServicioVirtual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idioma', models.CharField(default=b'es', max_length=5)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=250)),
                ('activo', models.BooleanField(default=True)),
                ('contrato', models.TextField()),
                ('eliminado', models.BooleanField(default=False)),
                ('imagen', models.ImageField(null=True, upload_to=b'alla', blank=True)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['fecha_publicacion'],
            },
        ),
        migrations.CreateModel(
            name='Sugerencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField()),
                ('asunto', models.CharField(max_length=150)),
                ('usuario', models.ForeignKey(to='geoservicios.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='UrlCategoria',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.CharField(max_length=75)),
                ('padre', models.ForeignKey(related_name='hijos', blank=True, to='geoservicios.UrlCategoria', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlServicio',
            fields=[
                ('url', models.CharField(max_length=100, unique=True, serialize=False, primary_key=True)),
                ('precio', models.DecimalField(default=5.0, max_digits=5, decimal_places=2)),
                ('subcategoria', models.ForeignKey(to='geoservicios.UrlCategoria')),
                ('vendedor', models.ForeignKey(to='geoservicios.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atencion', models.PositiveSmallIntegerField(default=0)),
                ('tiempo_entrega', models.PositiveSmallIntegerField(default=0)),
                ('calidad', models.PositiveSmallIntegerField(default=0)),
                ('promedio', models.PositiveSmallIntegerField(default=0)),
                ('estafa', models.BooleanField(default=False)),
                ('eliminada', models.BooleanField(default=False)),
                ('evaluador', models.ForeignKey(to='geoservicios.Perfil')),
                ('servicio', models.ForeignKey(to='geoservicios.ServicioVirtual')),
            ],
            options={
                'ordering': ['-promedio'],
            },
        ),
        migrations.AddField(
            model_name='serviciovirtual',
            name='url',
            field=models.ForeignKey(related_name='obj_servicio', to='geoservicios.UrlServicio'),
        ),
        migrations.AddField(
            model_name='nivelusuario',
            name='usuario',
            field=models.ForeignKey(to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='intermediario',
            name='comprador',
            field=models.ForeignKey(related_name='comprador_intermediario', to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='intermediario',
            name='obj_cola',
            field=models.ForeignKey(to='geoservicios.Cola'),
        ),
        migrations.AddField(
            model_name='intermediario',
            name='vendedor',
            field=models.ForeignKey(related_name='vendedor_intermediario', to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='factura',
            name='comprador',
            field=models.ForeignKey(to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='factura',
            name='url_servicio',
            field=models.ForeignKey(to='geoservicios.UrlServicio'),
        ),
        migrations.AddField(
            model_name='contador',
            name='servicio',
            field=models.ForeignKey(to='geoservicios.ServicioVirtual'),
        ),
        migrations.AddField(
            model_name='cola',
            name='comprador',
            field=models.ForeignKey(related_name='comprador_cola', to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='cola',
            name='servicio',
            field=models.ForeignKey(to='geoservicios.ServicioVirtual'),
        ),
        migrations.AddField(
            model_name='cola',
            name='vendedor',
            field=models.ForeignKey(related_name='vendedor_cola', to='geoservicios.Perfil'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='url',
            field=models.ForeignKey(to='geoservicios.UrlCategoria'),
        ),
        migrations.AlterUniqueTogether(
            name='urlcategoria',
            unique_together=set([('url', 'padre')]),
        ),
        migrations.AlterUniqueTogether(
            name='serviciovirtual',
            unique_together=set([('url', 'idioma')]),
        ),
    ]
