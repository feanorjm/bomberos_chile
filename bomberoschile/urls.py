from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from bomberoschile.views import login_view, logout_view
from main.views import *

urlpatterns = [
                  path('grappelli/', include('grappelli.urls')), # grappelli URLS
                  path('admin/', admin.site.urls),
                  path('chaining/', include('smart_selects.urls')),
                  path('index/', bitacora_list, name='bitacora_list'),
                  path('', bitacora_list, name='bitacora_list'),
                  # path(r'^index/$', index_view,name='index_view'),
                  path('login/', login_view, name='login_view'),
                  path('logout/', logout_view, name='logout_view'),
                  # BITACORA
                  path('bitacora/add/', bitacora_create_view, name='bitacora_create_view'),
                  path('bitacora/', bitacora_list, name='bitacora_list'),
                  path('bitacora/detalle/<str:pk>/', bitacora_detail, name='bitacora_detail'),
                  path('bitacora/editar/<str:pk>/', bitacora_update, name='bitacora_update'),
                  path('bitacora/eliminar/<str:pk>/', bitacora_delete, name='bitacora_delete'),
                  # MANTENCIONES
                  # path(r'^mantencion/add/$', mantencion_create, name='mantencion_create'),
                  path('mantencion/add/', mantencion_create_view, name='mantencion_create_view'),
                  path('mantencion/add/nuevo', mantencion_form_view, name='mantencion_form_view'),
                  path('mantencion/add/detalle', detalle_mantencion_form_view, name='detalle_mantencion_form_view'),
                  path('mantencion/add/repuesto', repuesto_detalle_mantencion_form_view,
                       name='repuesto_detalle_mantencion_form_view'),
                  # path(r'^mantencion/add_detalle/$', mantencion_add_detalle, name='mantencion_add_detalle'),
                  # path(r'^mantencion/add_repuesto/$', mantencion_add_repuesto, name='mantencion_add_repuesto'),
                  path('mantenciones/', mantencion_list, name='mantencion_list'),
                  path('mantencion/detalle/<str:pk>/', mantencion_detail, name='mantencion_detail'),
                  path('mantencion/eliminar/<str:pk>/', mantencion_delete, name='mantencion_delete'),
                  path('mantencion/editar/<str:pk>/', mantencion_update, name='mantencion_update'),
                  # MAQUINA
                  path('maquina/detalle/<str:pk>/', maquina_detail, name='maquina_detail'),
                  path('maquinas/', maquina_list, name='maquina_list'),
                  path('maquina/add/', maquina_create, name='maquina_create'),
                  path('maquina/editar/<str:pk>/', maquina_update, name='maquina_update'),
                  path('maquina/eliminar/<str:pk>/', maquina_delete, name='maquina_delete'),
                  path('get_maquina_conductores/', get_maquina_conductores, name='get_maquina_conductores'),
                  path('get_parametros_maquina/', get_parametros_maquina, name='get_parametros_maquina'),

                  # CONDUCTORES
                  path('conductores/', conductor_list, name='conductor_list'),
                  path('conductor/detalle/<str:pk>/', conductor_detail, name='conductor_detail'),
                  path('conductor/add/', conductor_create, name='conductor_create'),
                  path('conductor/editar/<str:pk>/', conductor_update, name='conductor_update'),
                  path('conductor/eliminar/<str:pk>/', conductor_delete, name='conductor_delete'),

                  # COMBUSTIBLE
                  path('combustible/add/', combustible_create, name='combustible_create'),
                  path('carga-combustible/', combustible_list, name='combustible_list'),
                  path('carga-combustible/eliminar/<str:pk>/', combustible_delete, name='combustible_delete'),
                  path('carga-combustible/detalle/<str:pk>/', combustible_detail, name='combustible_detail'),
                  path('carga-combustible/editar/<str:pk>/', combustible_update, name='combustible_update'),

                  # DASHBOARD
                  path('dashboard/', dashboard_list_view, name='dashboard_list_view'),

                  # REPORTES
                  path('reporte/parte-combustible/', reporte_combustible_list_view,
                       name='reporte_combustible_list_view'),
                  path('reporte/maquinistas/', reporte_maquinistas_list_view, name='reporte_maquinistas_list_view'),
                  path('reporte/servicios/', reporte_servicios_list_view, name='reporte_servicios_list_view'),
                  path('reporte/mantenciones/', reporte_mantenciones_list_view, name='reporte_mantenciones_list_view'),
                  path('reporte/talleres/', reporte_talleres_list_view, name='reporte_talleres_list_view'),
                  path('get_maquinas_company/', get_maquinas_company, name='get_maquinas_company'),

                  # UTIL
                  path('get_all_conductores/', get_all_conductores, name='get_all_conductores'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
