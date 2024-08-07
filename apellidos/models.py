from django.db import models
from django.utils import timezone



class AfiliacionSalud(models.Model):
    ultima_actualizacion = models.DateField(blank=True, null=True)
    run = models.ForeignKey('Persona', models.DO_NOTHING, db_column='run', to_field='run')
    isapre = models.ForeignKey('Isapre', models.DO_NOTHING, db_column='isapre')

    class Meta:
        managed = False
        db_table = 'afiliacion_salud'


class Afp(models.Model):
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'afp'


class Apellido(models.Model):
    apellido = models.CharField(max_length=100)
    ultima_actualizacion = models.DateField(blank=True, null=True)
    cuenta = models.IntegerField(blank=True, null=True)
    hombres = models.IntegerField(blank=True, null=True)
    mujeres = models.IntegerField(blank=True, null=True)
    etario1 = models.IntegerField(blank=True, null=True)
    etario2 = models.IntegerField(blank=True, null=True)
    etario3 = models.IntegerField(blank=True, null=True)
    etario4 = models.IntegerField(blank=True, null=True)
    etario5 = models.IntegerField(blank=True, null=True)
    etario6 = models.IntegerField(blank=True, null=True)
    etario7 = models.IntegerField(blank=True, null=True)
    etario8 = models.IntegerField(blank=True, null=True)
    etario9 = models.IntegerField(blank=True, null=True)
    edad_promedio = models.FloatField(blank=True, null=True)
    posc_ranking_cuenta = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=5000, blank=True, null=True)
    dif_genero = models.FloatField(blank=True, null=True)
    cuenta_busqueda = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.apellido

    class Meta:
        managed = False
        db_table = 'apellido'


class Bancario(models.Model):
    ultima_actualizacion = models.DateField(blank=True, null=True)
    run = models.ForeignKey('Persona', models.DO_NOTHING, db_column='run', to_field='run')
    banco = models.ForeignKey('Banco', models.DO_NOTHING, db_column='banco')

    class Meta:
        managed = False
        db_table = 'bancario'


class Banco(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'banco'


class Comuna(models.Model):
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='provincia')
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'comuna'


class Contacto(models.Model):
    run = models.ForeignKey('Persona', models.DO_NOTHING, db_column='run', to_field='run')
    contacto = models.CharField(max_length=200)
    tipo_contacto = models.ForeignKey('TipoContacto', models.DO_NOTHING, db_column='tipo_contacto')
    fecha_modificacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacto'
        unique_together = (('contacto', 'run'),)


class Direccion(models.Model):
    run = models.ForeignKey('Persona', models.DO_NOTHING, db_column='run', to_field='run')
    calle = models.CharField(max_length=100, blank=True, null=True)
    numeracion = models.CharField(max_length=10, blank=True, null=True)
    depto = models.CharField(max_length=10, blank=True, null=True)
    comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comuna')
    direccion_completa = models.CharField(max_length=200, blank=True, null=True)
    ultima_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direccion'


class Isapre(models.Model):
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'isapre'


class Persona(models.Model):
    nombre_completo = models.CharField(max_length=80)
    run = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)
    dv = models.CharField(max_length=1, blank=True, null=True)
    genero = models.CharField(max_length=1, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    apellido1 = models.CharField(max_length=100, blank=True, null=True)
    apellido2 = models.CharField(max_length=100, blank=True, null=True)
    ultima_actualizacion = models.DateField(blank=True, null=True)
    nombres = models.CharField(max_length=300, blank=True, null=True)
    fecha_nacimiento_aprox = models.DateField(blank=True, null=True)
    fallecido = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona'


class Provincia(models.Model):
    region = models.ForeignKey('Region', models.DO_NOTHING, db_column='region')
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'provincia'


class Region(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'region'


class RegionApellido(models.Model):
    region = models.ForeignKey(Region, models.DO_NOTHING, db_column='region')
    apellido = models.ForeignKey(Apellido, models.DO_NOTHING, db_column='apellido')
    cuenta = models.IntegerField(blank=True, null=True)
    ultima_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_apellido'
        unique_together = (('region', 'apellido'),)


class TipoContacto(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_contacto'


class EstadoBase(models.Model):
    fecha = models.DateField(blank=True, null=True)
    cuenta_personas = models.IntegerField(blank=True, null=True)
    cuenta_apellidos = models.IntegerField(blank=True, null=True)
    cuenta_mujeres = models.IntegerField(blank=True, null=True)
    cuenta_hombres = models.IntegerField(blank=True, null=True)
    habitantes_region1 = models.IntegerField(blank=True, null=True)
    habitantes_region2 = models.IntegerField(blank=True, null=True)
    habitantes_region3 = models.IntegerField(blank=True, null=True)
    habitantes_region4 = models.IntegerField(blank=True, null=True)
    habitantes_region5 = models.IntegerField(blank=True, null=True)
    habitantes_region6 = models.IntegerField(blank=True, null=True)
    habitantes_region7 = models.IntegerField(blank=True, null=True)
    habitantes_region8 = models.IntegerField(blank=True, null=True)
    habitantes_region9 = models.IntegerField(blank=True, null=True)
    habitantes_region10 = models.IntegerField(blank=True, null=True)
    habitantes_region11 = models.IntegerField(blank=True, null=True)
    habitantes_region12 = models.IntegerField(blank=True, null=True)
    habitantes_region13 = models.IntegerField(blank=True, null=True)
    habitantes_region14 = models.IntegerField(blank=True, null=True)
    habitantes_region15 = models.IntegerField(blank=True, null=True)
    habitantes_region16 = models.IntegerField(blank=True, null=True)
    habitantes_region17 = models.IntegerField(blank=True, null=True)
    etario1 = models.FloatField(blank=True, null=True)
    etario2 = models.FloatField(blank=True, null=True)
    etario3 = models.FloatField(blank=True, null=True)
    etario4 = models.FloatField(blank=True, null=True)
    etario5 = models.FloatField(blank=True, null=True)
    etario6 = models.FloatField(blank=True, null=True)
    etario7 = models.FloatField(blank=True, null=True)
    etario8 = models.FloatField(blank=True, null=True)
    etario9 = models.FloatField(blank=True, null=True)
    dif_personas =  models.IntegerField(blank=True, null=True)
    dif_apellidos =  models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_base'


class Comentario(models.Model):
    usuario = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200)
    cuerpo = models.CharField(max_length=1000)
    apellido = models.ForeignKey(Apellido, models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comentario'

    def __str__(self):
        return f"{self.titulo} por {self.usuario}"