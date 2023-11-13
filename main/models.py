from django.db import models
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey, ChainedManyToManyField
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from django.contrib import messages


class Company(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Compañía'
        verbose_name_plural = 'Compañías'

    def __str__(self):
        return str(self.nombre)


class Clasificacion_maquina(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Clasificación máquina'

    def __str__(self):
        return str(self.nombre)


class Conductor(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, null=True, blank=True)
    nombre = models.CharField(max_length=45, null=True)
    ap_paterno = models.CharField(max_length=45, null=True)
    ap_materno = models.CharField(max_length=45, null=True)
    num_licencia = models.CharField(max_length=12, null=True, blank=True)
    venc_lic = models.DateField(null=True, blank=True)
    observaciones_cond = models.TextField(max_length=1000, null=True, blank=True, default="Ninguna")
    foto = models.FileField(upload_to='profile', null=True, blank=True)

    class Meta:
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'

    def __str__(self):
        nombre = self.nombre
        nombre = nombre.split(" ")
        return nombre[0] + " " + str(self.ap_paterno) + " " + str(self.ap_materno)

    def get_absolute_url(self):
        return reverse('conductor_detail', args=[str(self.id)])


year_dropdown = []
for y in range(1950, (datetime.datetime.now().year + 1)):
    year_dropdown.append((str(y), str(y)))

TIPO_MAQUINA_CHOICES = (
    ('1', 'AMERICANO'),
    ('2', 'EUROPEO'),
)


class Maquina(models.Model):
    nombre = models.CharField(max_length=45)
    clasificacion = models.ForeignKey(Clasificacion_maquina, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    marca = models.CharField(max_length=45, null=True, blank=True)
    modelo = models.CharField(max_length=45, null=True, blank=True)
    ano = models.CharField(max_length=5, choices=year_dropdown, default=datetime.datetime.now().year, null=True,
                           blank=True)
    numero_motor = models.CharField(max_length=45, null=True, blank=True)
    numero_chasis = models.CharField(max_length=45, null=True, blank=True)
    bin = models.CharField(max_length=45, null=True, blank=True)
    patente = models.CharField(max_length=10, null=True, blank=True)
    conductor = models.ManyToManyField(Conductor, blank=True)
    kilometraje = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    hodometro = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    tiene_bomba = models.BooleanField(default=False, choices=((True, "Si"), (False, "No")))
    hodometro_bomba = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    venc_patente = models.DateField(null=True, blank=True)  # vencimiento patente
    costo_patente = models.IntegerField(null=True, blank=True)  # costo patente
    soap_costo = models.IntegerField(null=True, blank=True)  # seguro obligatorio
    venc_rev_tec = models.DateField(null=True, blank=True)  # vencimiento revicion tecnica
    costo_rev_tec = models.IntegerField(null=True, blank=True)  # costo revision tecnica
    costo_seg_auto = models.IntegerField(null=True, blank=True)  # costo seguro automotriz
    venc_seg_auto = models.DateField(null=True, blank=True)
    prueba = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    procedencia_maquina = models.CharField(max_length=1, choices=TIPO_MAQUINA_CHOICES, default=1)

    class Meta:
        verbose_name = 'Maquina'
        verbose_name_plural = 'Maquinas'

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse('maquina_detail', args=[str(self.id)])


# class Detalle_Maquina(models.Model):
#     maquina = models.ForeignKey(Maquina)
#     venc_patente = models.DateField()       #vencimiento patente
#     costo_patente = models.IntegerField()   #costo patente
#     soap_costo = models.IntegerField()      #seguro obligatorio
#     venc_rev_tec = models.DateField()       #vencimiento revicion tecnica
#     costo_rev_tec = models.IntegerField()   #costo revision tecnica
#     costo_seg_auto = models.IntegerField()  #costo seguro automotriz
#     venc_seg_auto = models.DateField(null=True)


TIPO_USER_CHOICES = (
    ('0', 'Teniente de máquina'),
    ('1', 'OBAC'),
    ('2', 'Inspector general de máquina'),
    ('3', 'Comandante')
)


class UsuarioComp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_USER_CHOICES)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Usuario Compañía'

    def __str__(self):
        return str(self.user)

    def get_tipo(self):
        return self.tipo


class Servicentro(models.Model):
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Servicentro'
        verbose_name_plural = 'Servicentros'

    def __str__(self):
        return self.nombre + " - " + self.direccion


class Taller(models.Model):
    tipo = models.CharField(max_length=45)
    razon_social = models.CharField(max_length=45)
    rut = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    contacto = models.CharField(max_length=45, null=True, blank=True)
    tel_contacto = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=60, null=True, blank=True)
    correo = models.EmailField(max_length=45, null=True, blank=True)

    class Meta:
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'

    def __str__(self):
        return str(self.razon_social)


class Componente(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=100)

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

    def __str__(self):
        return str(self.nombre)


class Division(models.Model):
    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'División'
        verbose_name_plural = 'Divisiones'

    def __str__(self):
        return str(self.nombre)


class TipoMantencion(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=100)

    class Meta:
        verbose_name = 'Tipo Mantención'

    def __str__(self):
        return str(self.nombre)


class Subdivision(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Subdivisión'
        verbose_name_plural = 'Subdivisiones'

    def __str__(self):
        return str(self.nombre)


class ServicioMantencion(models.Model):
    division = models.ForeignKey(Division, null=True, on_delete=models.CASCADE)
    subdivision = ChainedForeignKey(Subdivision, chained_field="division", chained_model_field="division",
                                    related_name='%(class)s_requests_created', null=True, on_delete=models.CASCADE)
    # tipo_mantencion = models.ForeignKey(TipoMantencion)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=75, null=True, blank=True)

    class Meta:
        verbose_name = 'Servicio Mantención'

    def __str__(self):
        return str(self.nombre)


class Clave(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True, choices=((True, "Si"), (False, "No")))

    class Meta:
        verbose_name = 'Clave'
        verbose_name_plural = 'Claves'

    def __str__(self):
        return str(self.nombre) + ' - ' + str(self.descripcion)


class Bitacora(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    maquina = ChainedForeignKey(Maquina, chained_field="company", chained_model_field="company",
                                related_name='%(class)s_requests_created', on_delete=models.CASCADE)
    conductor = ChainedForeignKey(Conductor, chained_field="maquina", chained_model_field="maquina", null=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100, null=True)
    fecha = models.DateField(auto_now=False, auto_now_add=False, null=True)
    hora_salida = models.TimeField(null=True)
    hora_llegada = models.TimeField(null=True)
    clave = models.ForeignKey(Clave, null=True, on_delete=models.CASCADE)
    kilometraje_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    kilometraje_llegada = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    hodometro_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    hodometro_llegada = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ho_bomba_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    ho_bomba_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    observciones = models.TextField(max_length=300, null=True)

    class Meta:
        verbose_name = 'Bitacora'

    def __str__(self):
        return str(self.id) + ' - ' + str(self.company) + ' - ' + str(self.maquina) + ' - ' + str(
            self.fecha) + ' - ' + str(self.clave)

    def get_absolute_url(self):
        return reverse('bitacora_detail', args=[str(self.id)])


class Mantencion(models.Model):
    fecha = models.DateField()
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    maquina = ChainedForeignKey(Maquina, chained_field="company", chained_model_field="company",
                                related_name='%(class)s_requests_created', on_delete=models.CASCADE)
    ki_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ho_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ki_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ho_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ho_bomba_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    ho_bomba_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    hora_salida = models.TimeField(null=True)
    hora_llegada = models.TimeField(null=True)
    cod_man = models.CharField(max_length=45)  # orden de trabajo
    observacion = models.TextField(max_length=200)
    num_factura = models.IntegerField(default=0, blank=True)
    valor = models.IntegerField(blank=True, default=0)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    responsable = ChainedForeignKey(Conductor, chained_field="maquina", chained_model_field="maquina", null=True,
                                    on_delete=models.CASCADE)
    servicio = models.ForeignKey(Bitacora, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Mantención'
        verbose_name_plural = 'Mantenciones'

    def __str__(self):
        return str(self.maquina) + '-' + str(self.cod_man)

    def get_absolute_url(self):
        return reverse('mantencion_detail', args=[str(self.id)])


class DetalleMantencion(models.Model):
    mantencion = models.ForeignKey(Mantencion, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, null=True, on_delete=models.CASCADE)
    subdivision = ChainedForeignKey(Subdivision, chained_field="division", chained_model_field="division", null=True,
                                    related_name='%(class)s_requests_created', on_delete=models.CASCADE)
    tipo_mantencion = models.ForeignKey(TipoMantencion, default=1, null=True, on_delete=models.CASCADE)
    servicio = ChainedForeignKey(ServicioMantencion, chained_field="subdivision", chained_model_field="subdivision",
                                 null=True, blank=True, related_name='%(class)s_requests_created',
                                 on_delete=models.CASCADE)
    des_detalle = models.TextField(max_length=200, null=True, blank=True)
    hodometro_prox_man = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Detalle Mantención'

    def __str__(self):
        return str(self.servicio)


class RepuestoDetalleMantencion(models.Model):
    mantencion = models.ForeignKey(Mantencion, on_delete=models.CASCADE)
    detalle_mantencion = ChainedForeignKey(DetalleMantencion, chained_field="mantencion",
                                           chained_model_field="mantencion", on_delete=models.CASCADE)
    repuesto = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        verbose_name = 'Repuesto Detalle'

    def __str__(self):
        return str(self.repuesto)


class CargaCombustible(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    maquina = ChainedForeignKey(Maquina, chained_field="company", chained_model_field="company",
                                related_name='%(class)s_requests_created', on_delete=models.CASCADE)
    litros = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    servicentro = models.ForeignKey(Servicentro, on_delete=models.CASCADE)
    km_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    hm_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    km_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    hm_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True)
    ho_bomba_salida = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    ho_bomba_regreso = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    hora_salida = models.TimeField(null=True)
    hora_llegada = models.TimeField(null=True)
    valor = models.IntegerField()
    tarjeta_tct = models.IntegerField()
    conductor = ChainedForeignKey(Conductor, chained_field="maquina", chained_model_field="maquina", null=True,
                                  blank=True, on_delete=models.CASCADE)
    obac = models.CharField(max_length=45, null=True, blank=True)
    fecha = models.DateField(null=True)
    servicio = models.ForeignKey(Bitacora, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Carga Combustible'
        verbose_name_plural = 'Cargas Combustible'

    def __str__(self):
        return str(self.maquina)

    def get_absolute_url(self):
        return reverse('combustible_detail', args=[str(self.id)])
