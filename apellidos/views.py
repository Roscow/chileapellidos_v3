from django.shortcuts import render, redirect
from .models import Persona, Apellido, Region, RegionApellido, Direccion , EstadoBase
import random
from django.db.models import Q
from django.views import View
import unicodedata
import re
import json
from django.http import HttpResponse
import math
from datetime import datetime, timedelta
from django.db import connection
import requests
from dotenv import load_dotenv
import os
from django.core.mail import EmailMessage

load_dotenv()



def remover_tildes(cadena):
    # Usar la librería unicodedata para normalizar la cadena y eliminar los caracteres acentuados
    cadena_sin_tildes = ''.join((c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn'))
    return cadena_sin_tildes

def reemplazar_tildes(cadena):
    # Usar una expresión regular para encontrar caracteres con tilde
    cadena_sin_tildes = re.sub(r'[áéíóúÁÉÍÓÚ]', lambda x: remover_tildes(x.group()), cadena)
    return cadena_sin_tildes

def invertir_queryset(queryset):
    # Convierte el queryset en una lista y luego inviértela
    lista_invertida = list(reversed(list(queryset)))
    return lista_invertida

def obtener_origen_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"  # Asegúrate de tener la URL correcta según la documentación de OpenAI
    clave_api = os.getenv("CLAVE_API_AI")  # Reemplaza con tu clave API de OpenAI
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {clave_api}",
    }
    data = {
        "model": "gpt-3.5-turbo",  # Modelo específico de ChatGPT
        "messages": [{"role": "system", "content": "de donde viene el apellido "}, {"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error en la solicitud: {response.status_code} - {response.text}"

def obtener_relevancia_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"  # Asegúrate de tener la URL correcta según la documentación de OpenAI
    clave_api = os.getenv("CLAVE_API_AI")  # Reemplaza con tu clave API de OpenAI
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {clave_api}",
    }
    data = {
        "model": "gpt-3.5-turbo",  # Modelo específico de ChatGPT
        "messages": [{"role": "system", "content": "que importancia tiene el siguiente apellido en chile "}, {"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error en la solicitud: {response.status_code} - {response.text}"

def index(request):
    #ultimos_30_estados = EstadoBase.objects.all().order_by('fecha')[:30]
    ultimos_30_estados = EstadoBase.objects.all().order_by('-fecha')[:30]

    estado_mas_reciente = ultimos_30_estados[0]
    porcentaje_mujeres = round((estado_mas_reciente.cuenta_mujeres* 100)/estado_mas_reciente.cuenta_personas , 1)
    porcentaje_hombres = round((estado_mas_reciente.cuenta_hombres* 100)/estado_mas_reciente.cuenta_personas , 1)
    style_hombres =  (f"width:{porcentaje_hombres}%;")   
    style_mujeres =  (f"width:{porcentaje_mujeres}%;")   
    listado_etario = list()
    listado_etario.append(estado_mas_reciente.etario1)
    listado_etario.append(estado_mas_reciente.etario2)
    listado_etario.append(estado_mas_reciente.etario3)
    listado_etario.append(estado_mas_reciente.etario4)
    listado_etario.append(estado_mas_reciente.etario5)
    listado_etario.append(estado_mas_reciente.etario6)
    listado_etario.append(estado_mas_reciente.etario7)
    listado_etario.append(estado_mas_reciente.etario8)
    listas_encabezados = list()
    listas_encabezados.append('19-29')
    listas_encabezados.append('30-39')
    listas_encabezados.append('40-49')
    listas_encabezados.append('50-59')
    listas_encabezados.append('60-69')
    listas_encabezados.append('70-79')
    listas_encabezados.append('80-89')
    listas_encabezados.append('90+')
    regiones_orden_geografico = (15,1,2,3,4,5,13,6,7,16,8,9,14,10,11,12,17)
    detalle_regiones = list()   
    for i in regiones_orden_geografico:
        region_obj = Region.objects.get(id=i)
        romano = region_obj.numero
        nombre = region_obj.nombre
        if(i==1):
            porcentaje = round((estado_mas_reciente.habitantes_region1* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region1, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==2):
            porcentaje = round((estado_mas_reciente.habitantes_region2* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region2, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==3):
            porcentaje = round((estado_mas_reciente.habitantes_region3* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region3, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==4):
            porcentaje = round((estado_mas_reciente.habitantes_region4* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region4, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==5):
            porcentaje = round((estado_mas_reciente.habitantes_region5* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region5, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==6):
            porcentaje = round((estado_mas_reciente.habitantes_region6* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region6, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==7):
            porcentaje = round((estado_mas_reciente.habitantes_region7* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region7, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==8):
            porcentaje = round((estado_mas_reciente.habitantes_region8* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region8, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==9):
            porcentaje = round((estado_mas_reciente.habitantes_region9* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region9, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==10):
            porcentaje = round((estado_mas_reciente.habitantes_region10* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region10, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==11):
            porcentaje = round((estado_mas_reciente.habitantes_region11* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region11, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==12):
            porcentaje = round((estado_mas_reciente.habitantes_region12* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region12, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==13):
            porcentaje = round((estado_mas_reciente.habitantes_region13* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region13, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==14):
            porcentaje = round((estado_mas_reciente.habitantes_region14* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region14, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==15):
            porcentaje = round((estado_mas_reciente.habitantes_region15* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region15, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==16):
            porcentaje = round((estado_mas_reciente.habitantes_region16* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region16, porcentaje ,(f"width:{porcentaje}%;")  )
        if(i==17):
            porcentaje = round((estado_mas_reciente.habitantes_region17* 100)/ estado_mas_reciente.cuenta_personas, 1)
            tupla =(romano, nombre, estado_mas_reciente.habitantes_region17, porcentaje ,(f"width:{porcentaje}%;")  )
        detalle_regiones.append(tupla)
    #para grafico de datos 
    listado_cuenta = list()
    listado_dias =list()
    lista_cuenta_apellidos = list()
    lista_invertida = invertir_queryset(ultimos_30_estados)
    for e in lista_invertida:
        listado_cuenta.append(e.dif_personas)
        lista_cuenta_apellidos.append(e.dif_apellidos)
        listado_dias.append(e.fecha.strftime('%d-%m'))
    context = {
        'estado_mas_reciente':estado_mas_reciente,
        'style_hombres':style_hombres,
        'style_mujeres':style_mujeres,
        'porcentaje_mujeres':porcentaje_mujeres,
        'porcentaje_hombres':porcentaje_hombres,
        'listado_etario_json':json.dumps(listado_etario),
        'lista_encabezados_json':json.dumps(listas_encabezados),
        'detalle_regiones':detalle_regiones,
        'fechas_ultimos_30_dias_json': json.dumps(listado_dias),
        'cuentas_ultimos_30_dias_json': json.dumps(listado_cuenta),
        'cuentas_apellidos_ultimos_30_dias_json': json.dumps(lista_cuenta_apellidos)
        }
    return render(request, 'apellidos/index.html', context)

def calcular_edad(fecha_nacimiento):
    hoy = datetime.now().date()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def detalle_apellido(request):
    if 'apellido_p' in request.GET:
        try:
            apellido_p = request.GET['apellido_p']
            apellido_p = apellido_p.lower()
            apellido_p = apellido_p.capitalize()
            apellido_p = apellido_p.strip()
            apellido_p = reemplazar_tildes(apellido_p)

            total_personas = Persona.objects.all().count()  #esto deberia estar en una tabla para no calcularlo con cada consulta 
            apellido_obj = Apellido.objects.get(apellido=apellido_p)
            apellido_obj.cuenta_busqueda = int(apellido_obj.cuenta_busqueda) + 1
            apellido_obj.save()
            if apellido_obj.descripcion is None:
                descripcion = obtener_origen_openai(apellido_p)
                descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido_p)
                apellido_obj.descripcion = descripcion
                apellido_obj.save()
            total_apellido = int(apellido_obj.cuenta)
            porcentaje_apellido = round( (total_apellido*100)/total_personas  , 5)
            regiones_orden_geografico = (15,1,2,3,4,5,13,6,7,16,8,9,14,10,11,12,17)
            detalle_regiones=list()
            edad_promedio = round(apellido_obj.edad_promedio)
            #obtener datos guardados
            contador_region = RegionApellido.objects.filter(apellido=apellido_obj)
            for i in regiones_orden_geografico:
                    region_obj = Region.objects.get(id=i)
                    romano = region_obj.numero
                    nombre = region_obj.nombre
                    #region_apellido = RegionApellido.objects.filter(region=region_obj,apellido=apellido_obj)
                    region_apellido_elemento = contador_region.get(region=region_obj.id)
                    region_apellido = region_apellido_elemento
                    contador_r = region_apellido.cuenta
                    porcentaje = int(contador_r* 100)/(total_apellido)
                    style_width=(f"width:{porcentaje}%;")
                    tupla = (romano, nombre, contador_r, porcentaje,style_width)
                    detalle_regiones.append(tupla)
            porcentaje_mujeres = round( (int(apellido_obj.mujeres) * 100) / int(apellido_obj.cuenta) , 2)
            porcentaje_hombres= round( (int(apellido_obj.hombres) * 100) / int(apellido_obj.cuenta), 2)
            style_mujeres = (f"width:{porcentaje_mujeres}%;")
            style_hombres = (f"width:{porcentaje_hombres}%;")     
            listado_etario = list()
            listado_etario.append(apellido_obj.etario1)
            listado_etario.append(apellido_obj.etario2)
            listado_etario.append(apellido_obj.etario3)
            listado_etario.append(apellido_obj.etario4)
            listado_etario.append(apellido_obj.etario5)
            listado_etario.append(apellido_obj.etario6)
            listado_etario.append(apellido_obj.etario7)
            listado_etario.append(apellido_obj.etario8)
            listas_encabezados = list()
            listas_encabezados.append('19-29')
            listas_encabezados.append('30-39')
            listas_encabezados.append('40-49')
            listas_encabezados.append('50-59')
            listas_encabezados.append('60-69')
            listas_encabezados.append('70-79')
            listas_encabezados.append('80-89')
            listas_encabezados.append('90+')
            context = {
                'apellido':apellido_obj, 
                'detalle_regiones':detalle_regiones,
                'porcentaje_apellido':porcentaje_apellido, 
                'style_mujeres':style_mujeres, 
                'style_hombres':style_hombres,
                'porcentaje_hombres':porcentaje_hombres,
                'porcentaje_mujeres':porcentaje_mujeres,
                'listado_etario_json':json.dumps(listado_etario),
                'lista_encabezados_json':json.dumps(listas_encabezados),
                'edad_promedio':edad_promedio,
                }
            return render(request, 'apellidos/detalle_apellido.html',context)
        except Exception as e:
            context = {'error':e}
            return render(request, 'apellidos/error.html',context)
        
#ranking de cantidad de personas ascendentes
def ranking_cantidad_asc(request,pagina):
    try:
        titulo = 'Cuenta de personas'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('cuenta')[inicio:fin]
        contador =0
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido, round(e.cuenta))
            lista_elementos.append(tupla)
        caracteristica='Total personas'
        ranking_actual_desc = 'ranking_cantidad_desc'
        ranking_actual_asc = 'ranking_cantidad_asc'
        ranking_actual='ranking_cantidad_asc'
        #style_desc='bg-white text-primary'
        style_asc= 'bg-dark text-light border-dark'
        style_desc = 'bg-white text-dark border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'apellidos':apellidos, 
            'style_desc':style_desc,
            'lista_elementos':lista_elementos, 
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'style_asc':style_asc  
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)

#ranking de cantidad de personas descendente
def ranking_cantidad_desc(request,pagina):
    try:
        titulo = 'Cuenta de personas'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('-cuenta')[inicio:fin]
        contador = inicio
        caracteristica='Total personas'
        ranking_actual_desc = 'ranking_cantidad_desc'
        ranking_actual_asc = 'ranking_cantidad_asc'
        ranking_actual='ranking_cantidad_desc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido, round(e.cuenta))
            lista_elementos.append(tupla)
        style_asc='bg-white text-dark border-dark'
        style_desc = 'bg-dark text-light border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'ranking_actual':ranking_actual,
            'apellidos':apellidos, 
            'style_asc':style_asc,
            'lista_elementos':lista_elementos, 
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo ,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas ,
            'style_desc':style_desc
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)

#ranking de promedio edad ascendente
def ranking_promedio_edad_asc(request,pagina):
    try:
        titulo = 'Edad Promedio'
        descripcion = 'Mostrando los datos ordenados segun la edad promedio de las personas con el apellido'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('edad_promedio')[inicio:fin]
        contador = inicio
        caracteristica='Edad Promedio'
        ranking_actual_desc = 'ranking_promedio_edad_desc'
        ranking_actual_asc = 'ranking_promedio_edad_asc'
        ranking_actual='ranking_promedio_edad_asc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido, round(e.edad_promedio))
            lista_elementos.append(tupla)
        #style_desc='bg-white text-primary'
        style_asc= 'bg-dark text-light border-dark'
        style_desc = 'bg-white text-dark border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'apellidos':apellidos, 
            'style_desc':style_desc,
            'style_asc':style_asc,
            'lista_elementos':lista_elementos, 
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas  ,
            'descripcion':descripcion
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)

#ranking de promedio edad descendente
def ranking_promedio_edad_desc(request,pagina):
    try:
        titulo = 'Edad Promedio'
        descripcion = 'Mostrando los datos ordenados segun la edad promedio de las personas con el apellido'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('-edad_promedio')[inicio:fin]
        contador = inicio
        caracteristica='Edad Promedio'
        ranking_actual_desc = 'ranking_promedio_edad_desc'
        ranking_actual_asc = 'ranking_promedio_edad_asc'
        ranking_actual='ranking_promedio_edad_desc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido,  round(e.edad_promedio))
            lista_elementos.append(tupla)
        style_asc='bg-white text-dark border-dark'
        style_desc = 'bg-dark text-light border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'apellidos':apellidos, 
            'style_asc':style_asc,
            'lista_elementos':lista_elementos,
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'style_desc':style_desc,
            'descripcion':descripcion   
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)
    
#buscar datos en tiempo real sobre la combinacion de dos apellidos 
def combinar(request):
    if request.method == 'POST':
        try:
            captcha_response = request.POST.get('g-recaptcha-response', '')
            captcha_data = {
                'secret': os.getenv("SECRET_KEY_CAPTCHA"),
                'response': captcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            result = response.json()
            if result['success']:
                #realizar proceso en tiempo real
                regiones_orden_geografico = (15,1,2,3,4,5,13,6,7,16,8,9,14,10,11,12,17)
                apellido1_req = request.POST.get('apellido1', '')
                apellido1_req = apellido1_req.lower()
                apellido1_req = apellido1_req.capitalize()
                apellido2_req = request.POST.get('apellido2', '')
                apellido2_req = apellido2_req.lower()
                apellido2_req = apellido2_req.capitalize()
                apellido1_obj = Apellido.objects.get(apellido=apellido1_req)
                apellido1_obj.cuenta_busqueda = int(apellido1_obj.cuenta_busqueda) + 1
                apellido1_obj.save()
                apellido2_obj = Apellido.objects.get(apellido=apellido2_req) 
                apellido2_obj.cuenta_busqueda = int(apellido2_obj.cuenta_busqueda) + 1
                apellido2_obj.save()
                #descripcion apellido1
                if apellido1_obj.descripcion is None:
                    descripcion = obtener_origen_openai(apellido1_req)
                    descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido1_req)
                    apellido1_obj.descripcion = descripcion
                    apellido1_obj.save()      
                #descripcion apellido2
                if apellido2_obj.descripcion is None:
                    descripcion = obtener_origen_openai(apellido2_req)
                    descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido2_req)
                    apellido2_obj.descripcion = descripcion
                    apellido2_obj.save() 
                personas_list = Persona.objects.filter(apellido1=apellido1_obj, apellido2=apellido2_obj)
                total_personas_apellido = len(personas_list)
                total_general_personas = Persona.objects.all().count()
                porcentaje_apellido = round((total_personas_apellido*100)/total_general_personas, 5)
                mujeres =0
                hombres =0
                edad_suma=0
                lista_regiones = list()
                detalle_regiones = list()
                etario1=etario2=etario3=etario4=etario5=etario6=etario7=etario8=etario9=0
                for p in personas_list:
                    if(p.genero == 'F'):
                        mujeres = mujeres+1 
                    else:
                        hombres = hombres+1
                    edad = calcular_edad(p.fecha_nacimiento_aprox)
                    edad_suma = edad + edad_suma
                    #etario 1
                    if(edad>= 18 and edad<=29 ):
                        etario1 = etario1+1
                    #etario 2
                    if(edad>= 30 and edad<=39 ):
                        etario2 = etario2+1     
                    #etario 3
                    if(edad>= 40 and edad<=49 ):
                        etario3 = etario3+1     
                    #etario 4
                    if(edad>= 50 and edad<=59 ):
                        etario4 = etario4+1
                    #etario 5
                    if(edad>= 60 and edad<=69 ):
                        etario5 = etario5+1
                    #etario 6
                    if(edad>= 70 and edad<=79 ):
                        etario6 = etario6+1  
                    #etario 7
                    if(edad>= 80 and edad<=89 ):
                        etario7 = etario7+1
                    #etario 8
                    if(edad>= 90 ):
                        etario8 = etario8+1
                    #etario 9
                    if(edad< 18 ):
                        etario9 = etario9+1
                    #region = Direccion.objects.raw(f'SELECT obtener_region_desde_direccion({p.run});')
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT obtener_region_desde_direccion({p.run});")
                        region = cursor.fetchone()[0]  # Suponiendo que la función devuelve un único valor
                        lista_regiones.append(int(region))
                
                for i in regiones_orden_geografico:
                        region_obj = Region.objects.get(id=i)
                        romano = region_obj.numero
                        nombre = region_obj.nombre
                        cuenta = lista_regiones.count(i)
                        porcentaje = round((cuenta*100)/total_personas_apellido)
                        style_width=(f"width:{porcentaje}%;")
                        tupla = (romano, nombre, cuenta, porcentaje, style_width)
                        detalle_regiones.append(tupla)

                porcentaje_hombre = round((hombres*100)/total_personas_apellido)
                porcentaje_mujer  = round((mujeres*100)/total_personas_apellido)
                promedio_edad = round(edad_suma/total_personas_apellido)
                style_mujeres = (f"width:{porcentaje_mujer}%;")
                style_hombres = (f"width:{porcentaje_hombre}%;") 
                listado_etario = list()
                listado_etario.append(etario1)
                listado_etario.append(etario2) 
                listado_etario.append(etario3) 
                listado_etario.append(etario4) 
                listado_etario.append(etario5) 
                listado_etario.append(etario6) 
                listado_etario.append(etario7) 
                listado_etario.append(etario8)
                listas_encabezados = list()
                listas_encabezados.append('19-29')
                listas_encabezados.append('30-39')
                listas_encabezados.append('40-49')
                listas_encabezados.append('50-59')
                listas_encabezados.append('60-69')
                listas_encabezados.append('70-79')
                listas_encabezados.append('80-89')
                listas_encabezados.append('90+')
                #distribucion regional 

                context = {
                    'apellido1':apellido1_obj, 
                    'apellido2':apellido2_obj,
                    'total_personas':total_personas_apellido,
                    'porcentaje_apellido':porcentaje_apellido,
                    'mujeres':mujeres,
                    'hombres':hombres,
                    'porcentaje_hombre':porcentaje_hombre,
                    'porcentaje_mujer':porcentaje_mujer,
                    'style_mujeres':style_mujeres,
                    'style_hombres':style_hombres,
                    'promedio_edad':promedio_edad,
                    'listado_etario_json':json.dumps(listado_etario),
                    'lista_encabezados_json':json.dumps(listas_encabezados),
                    'detalle_regiones':detalle_regiones
                }
                return render(request, 'apellidos/detalle_combinacion.html', context)
            else:
                context = {'error':'captcha incorrecto'}
                return render(request, 'apellidos/error.html', context)        
        except Exception as e:
            context = {'error':e}
            return render(request, 'apellidos/error.html', context)
    else:
        context = {}
        return render(request, 'apellidos/combinar.html', context)
    
#mostrar informacion de dos apellidos y determinar bajo ciertos criterios cual es mas relevante
def comparar(request):
    error="no se encontraron resultados del apellido. "
    if request.method == 'POST':
        try:
            captcha_response = request.POST.get('g-recaptcha-response', '')
            captcha_data = {
                'secret': os.getenv("SECRET_KEY_CAPTCHA"),
                'response': captcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            result = response.json()
            if result['success']:
                total_general_personas = Persona.objects.all().count()
                apellido1_req = request.POST.get('apellido1', '')
                apellido1_req = apellido1_req.lower()
                apellido1_req = apellido1_req.capitalize()
                apellido2_req = request.POST.get('apellido2', '')
                apellido2_req = apellido2_req.lower()
                apellido2_req = apellido2_req.capitalize()
                apellido1_obj = Apellido.objects.get(apellido=apellido1_req)
                apellido1_obj.cuenta_busqueda = int(apellido1_obj.cuenta_busqueda) + 1
                apellido1_obj.save()
                apellido2_obj = Apellido.objects.get(apellido=apellido2_req)
                apellido2_obj.cuenta_busqueda = int(apellido2_obj.cuenta_busqueda) + 1
                apellido2_obj.save()
                porcentaje_apellido1 = round((apellido1_obj.cuenta*100) /  total_general_personas ,5  ) 
                porcentaje_apellido2 = round((apellido2_obj.cuenta*100) /  total_general_personas ,5 )  
                apellido1_porcentaje_mujer = round ((apellido1_obj.mujeres*100)/apellido1_obj.cuenta , 1)
                apellido1_porcentaje_hombre =round ((apellido1_obj.hombres*100)/apellido1_obj.cuenta , 1)
                apellido2_porcentaje_mujer = round ((apellido2_obj.mujeres*100)/apellido2_obj.cuenta , 1)
                apellido2_porcentaje_hombre =round ((apellido2_obj.hombres*100)/apellido2_obj.cuenta , 1)
                style1_mujeres = (f"width:{apellido1_porcentaje_mujer}%;")
                style1_hombres = (f"width:{apellido1_porcentaje_hombre}%;")
                style2_mujeres = (f"width:{apellido2_porcentaje_mujer}%;")
                style2_hombres = (f"width:{apellido2_porcentaje_hombre}%;")
                #descripcion
                if apellido1_obj.descripcion is None:
                    descripcion = obtener_origen_openai(apellido1_req)
                    descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido1_req)
                    apellido1_obj.descripcion = descripcion
                    apellido1_obj.save()      
                #descripcion apellido2
                if apellido2_obj.descripcion is None:
                    descripcion = obtener_origen_openai(apellido2_req)
                    descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido2_req)
                    apellido2_obj.descripcion = descripcion
                    apellido2_obj.save() 
                #histogramas 
                listas_encabezados = list()
                listas_encabezados.append('19-29')
                listas_encabezados.append('30-39')
                listas_encabezados.append('40-49')
                listas_encabezados.append('50-59')
                listas_encabezados.append('60-69')
                listas_encabezados.append('70-79')
                listas_encabezados.append('80-89')
                listas_encabezados.append('90+')
                listado_etario1 = list()
                listado_etario1.append(apellido1_obj.etario1)
                listado_etario1.append(apellido1_obj.etario2)
                listado_etario1.append(apellido1_obj.etario3)
                listado_etario1.append(apellido1_obj.etario4)
                listado_etario1.append(apellido1_obj.etario5)
                listado_etario1.append(apellido1_obj.etario6)
                listado_etario1.append(apellido1_obj.etario7)
                listado_etario1.append(apellido1_obj.etario8)
                listado_etario2 = list()
                listado_etario2.append(apellido2_obj.etario1)
                listado_etario2.append(apellido2_obj.etario2)
                listado_etario2.append(apellido2_obj.etario3)
                listado_etario2.append(apellido2_obj.etario4)
                listado_etario2.append(apellido2_obj.etario5)
                listado_etario2.append(apellido2_obj.etario6)
                listado_etario2.append(apellido2_obj.etario7)
                listado_etario2.append(apellido2_obj.etario8)
                #distribucion regional
                regiones_orden_geografico = (15,1,2,3,4,5,13,6,7,16,8,9,14,10,11,12,17)
                contador_region1 = RegionApellido.objects.filter(apellido=apellido1_obj)
                contador_region2 = RegionApellido.objects.filter(apellido=apellido2_obj)
                detalle_regiones3=list()
                for i in regiones_orden_geografico:
                    region_obj = Region.objects.get(id=i)
                    romano = region_obj.numero
                    nombre = region_obj.nombre
                    #apellido1
                    region_apellido_elemento1 = contador_region1.get(region=region_obj.id)
                    region_apellido1 = region_apellido_elemento1
                    contador_r1 = region_apellido1.cuenta
                    porcentaje1 = int(contador_r1* 100)/(apellido1_obj.cuenta)
                    style_width1=(f"width:{porcentaje1}%;")
                    #apellido2
                    region_apellido_elemento2 = contador_region2.get(region=region_obj.id)
                    region_apellido2 = region_apellido_elemento2
                    contador_r2 = region_apellido2.cuenta
                    porcentaje2 = int(contador_r2* 100)/(apellido2_obj.cuenta)
                    style_width2=(f"width:{porcentaje2}%;")
                    #armar tupla
                    tupla = (romano, nombre, porcentaje1, style_width1, porcentaje2, style_width2)
                    detalle_regiones3.append(tupla)   
                
                context = {
                    'apellido1_obj':apellido1_obj,
                    'apellido2_obj':apellido2_obj,
                    'porcentaje_apellido1':porcentaje_apellido1,
                    'porcentaje_apellido2':porcentaje_apellido2,
                    'apellido1_porcentaje_mujer':apellido1_porcentaje_mujer,
                    'apellido1_porcentaje_hombre':apellido1_porcentaje_hombre,
                    'apellido2_porcentaje_mujer':apellido2_porcentaje_mujer,
                    'apellido2_porcentaje_hombre':apellido2_porcentaje_hombre,
                    'style1_mujeres':style1_mujeres,
                    'style1_hombres':style1_hombres,
                    'style2_mujeres':style2_mujeres,
                    'style2_hombres':style2_hombres,
                    'listado_etario1_json':json.dumps(listado_etario1),
                    'listado_etario2_json':json.dumps(listado_etario2),
                    'lista_encabezados_json':json.dumps(listas_encabezados),
                    'detalle_regiones3':detalle_regiones3
                    }
                return render(request, 'apellidos/detalle_comparacion.html', context)
            else:
                context = {'error':'captcha incorrecto'}
                return render(request, 'apellidos/error.html', context)   
        except Exception as e:
            error = error + ' ' + str(e)
            context = {'error':error}
            return render(request, 'apellidos/error.html', context)
    else:
        context = {}
        return render(request, 'apellidos/comparar.html', context)
    
#ranking de promedio edad ascendente
def ranking_dif_genero_asc(request,pagina):
    try:
        titulo = 'Diferencia entre generos'
        descripcion = 'Se muestran los datos ordenados segun la diferencia porcentual existente entre la cantidad de hombres y mujeres'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('dif_genero')[inicio:fin]
        contador = inicio
        caracteristica='Diferencia entre genero (%)'
        ranking_actual_desc = 'ranking_dif_genero_desc'
        ranking_actual_asc = 'ranking_dif_genero_asc'
        ranking_actual='ranking_dif_genero_asc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido, e.dif_genero)
            lista_elementos.append(tupla)
        #style_desc='bg-white text-primary'
        style_asc= 'bg-dark text-light border-dark'
        style_desc = 'bg-white text-dark border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'apellidos':apellidos, 
            'style_desc':style_desc,
            'style_asc':style_asc,
            'lista_elementos':lista_elementos, 
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'descripcion':descripcion  
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)

#ranking de promedio edad descendente
def ranking_dif_genero_desc(request,pagina):
    try:
        titulo = 'Diferencia entre generos'
        descripcion = 'Se muestran los datos ordenados segun la diferencia porcentual existente entre la cantidad de hombres y mujeres'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        total_apellidos = Apellido.objects.all().count()
        apellidos = Apellido.objects.all().order_by('-dif_genero')[inicio:fin]
        contador = inicio
        caracteristica='Diferencia entre generos (%)'
        ranking_actual_desc = 'ranking_dif_genero_desc'
        ranking_actual_asc = 'ranking_dif_genero_asc'
        ranking_actual='ranking_dif_genero_desc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido,  e.dif_genero )
            lista_elementos.append(tupla)
        style_asc='bg-white text-dark border-dark'
        style_desc = 'bg-dark text-light border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        context= { 
            'apellidos':apellidos, 
            'style_asc':style_asc,
            'lista_elementos':lista_elementos,
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'style_desc':style_desc ,
            'descripcion':descripcion  
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)
  

def error_404(request, exception):
    return render(request, 'apellidos/error.html', status=404)

def error_500(request):
    return render(request, 'apellidos/error.html', status=500)

def ranking_mas_buscados_desc(request,pagina):
    try:
        titulo = 'Por veces buscado'
        descripcion = 'Mostrando los datos ordenados segun la cantidad de veces que se buscó'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        #apellidos = Apellido.objects.all().order_by('-cuenta_busqueda')[inicio:fin]
        apellidos = Apellido.objects.exclude(cuenta_busqueda=0).order_by('-cuenta_busqueda')[inicio:fin]
        apellidos_todos = Apellido.objects.exclude(cuenta_busqueda=0).count()
        total_apellidos = apellidos_todos
        contador = inicio
        caracteristica='Busquedas'
        ranking_actual_desc = 'ranking_mas_buscados_desc'
        ranking_actual_asc = 'ranking_mas_buscados_asc'
        ranking_actual='ranking_mas_buscados_desc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido,  round(e.cuenta_busqueda))
            lista_elementos.append(tupla)
        style_asc='bg-white text-dark border-dark'
        style_desc = 'bg-dark text-light border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if((pagina>=3 and pagina<=(total_paginas-2))) :
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        if(total_paginas<5):
            lista_paginas= list()
            for i in range(total_paginas):
                lista_paginas.append(i+1)
        context= { 
            'apellidos':apellidos, 
            'style_asc':style_asc,
            'lista_elementos':lista_elementos,
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'style_desc':style_desc,
            'descripcion':descripcion   
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)


def ranking_mas_buscados_asc(request,pagina):
    try:
        titulo = 'Por veces buscado'
        descripcion = 'Mostrando los datos ordenados segun la cantidad de veces que se buscó'
        num_elementos = 150
        lista_elementos=list()
        inicio = (num_elementos * (pagina -1))
        fin = num_elementos * pagina 
        #apellidos = Apellido.objects.all().order_by('-cuenta_busqueda')[inicio:fin]
        apellidos = Apellido.objects.exclude(cuenta_busqueda=0).order_by('cuenta_busqueda')[inicio:fin]
        apellidos_todos = Apellido.objects.exclude(cuenta_busqueda=0).count()
        total_apellidos = apellidos_todos
        contador = inicio
        caracteristica='Busquedas'
        ranking_actual_desc = 'ranking_mas_buscados_desc'
        ranking_actual_asc = 'ranking_mas_buscados_asc'
        ranking_actual='ranking_mas_buscados_asc'
        for e in apellidos:
            contador=contador+1
            tupla=(contador, e.apellido,  round(e.cuenta_busqueda))
            lista_elementos.append(tupla)
        style_asc='bg-white text-dark border-dark'
        style_desc = 'bg-dark text-light border-dark'
        #sobre paginacion 
        total_paginas =  math.ceil(total_apellidos/num_elementos)
        pagina_prev = pagina-1
        pagina_next = pagina+1
        lista_paginas = list()
        if(pagina>=3 and pagina<=(total_paginas-2)):
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
        if(pagina==2):
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
        if(pagina==1):
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
            lista_paginas.append(pagina+2)
            lista_paginas.append(pagina+3)
            lista_paginas.append(pagina+4)
        if(pagina==total_paginas):
            lista_paginas.append(pagina-4)
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
        if(pagina==(total_paginas-1)):
            lista_paginas.append(pagina-3)
            lista_paginas.append(pagina-2)
            lista_paginas.append(pagina-1)
            lista_paginas.append(pagina)
            lista_paginas.append(pagina+1)
        if(total_paginas<5):
            lista_paginas= list()
            for i in range(total_paginas):
                lista_paginas.append(i+1)
        context= { 
            'apellidos':apellidos, 
            'style_asc':style_asc,
            'lista_elementos':lista_elementos,
            'caracteristica':caracteristica, 
            'ranking_actual_desc':ranking_actual_desc, 
            'ranking_actual_asc':ranking_actual_asc,
            'ranking_actual':ranking_actual,
            'titulo':titulo,
            'pagina_actual':pagina,
            'total_paginas':total_paginas,
            'pagina_next':pagina_next,
            'pagina_prev':pagina_prev,
            'lista_paginas':lista_paginas,
            'style_desc':style_desc,
            'descripcion':descripcion   
            }
        return render(request, 'apellidos/ranking.html', context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html', context)
 
def detalle_apellido2(request,apellido):
    try:
        apellido_p = apellido
        apellido_p = apellido_p.lower()
        apellido_p = apellido_p.capitalize()
        apellido_p = apellido_p.strip()
        total_personas = Persona.objects.all().count()  #esto deberia estar en una tabla para no calcularlo con cada consulta 
        apellido_obj = Apellido.objects.get(apellido=apellido_p)
        apellido_obj.cuenta_busqueda = int(apellido_obj.cuenta_busqueda) + 1
        apellido_obj.save()
        if apellido_obj.descripcion is None:
            descripcion = obtener_origen_openai(apellido_p)
            descripcion = descripcion + ' ' + obtener_relevancia_openai(apellido_p)
            apellido_obj.descripcion = descripcion
            apellido_obj.save()
        total_apellido = int(apellido_obj.cuenta)
        porcentaje_apellido = round( (total_apellido*100)/total_personas  , 5)
        regiones_orden_geografico = (15,1,2,3,4,5,13,6,7,16,8,9,14,10,11,12,17)
        detalle_regiones=list()
        edad_promedio = round(apellido_obj.edad_promedio)
        #obtener datos guardados
        contador_region = RegionApellido.objects.filter(apellido=apellido_obj)
        for i in regiones_orden_geografico:
                region_obj = Region.objects.get(id=i)
                romano = region_obj.numero
                nombre = region_obj.nombre
                #region_apellido = RegionApellido.objects.filter(region=region_obj,apellido=apellido_obj)
                region_apellido_elemento = contador_region.get(region=region_obj.id)
                region_apellido = region_apellido_elemento
                contador_r = region_apellido.cuenta
                porcentaje = int(contador_r* 100)/(total_apellido)
                style_width=(f"width:{porcentaje}%;")
                tupla = (romano, nombre, contador_r, porcentaje,style_width)
                detalle_regiones.append(tupla)
        porcentaje_mujeres = round( (int(apellido_obj.mujeres) * 100) / int(apellido_obj.cuenta) , 2)
        porcentaje_hombres= round( (int(apellido_obj.hombres) * 100) / int(apellido_obj.cuenta), 2)
        style_mujeres = (f"width:{porcentaje_mujeres}%;")
        style_hombres = (f"width:{porcentaje_hombres}%;")     
        listado_etario = list()
        listado_etario.append(apellido_obj.etario1)
        listado_etario.append(apellido_obj.etario2)
        listado_etario.append(apellido_obj.etario3)
        listado_etario.append(apellido_obj.etario4)
        listado_etario.append(apellido_obj.etario5)
        listado_etario.append(apellido_obj.etario6)
        listado_etario.append(apellido_obj.etario7)
        listado_etario.append(apellido_obj.etario8)
        listas_encabezados = list()
        listas_encabezados.append('19-29')
        listas_encabezados.append('30-39')
        listas_encabezados.append('40-49')
        listas_encabezados.append('50-59')
        listas_encabezados.append('60-69')
        listas_encabezados.append('70-79')
        listas_encabezados.append('80-89')
        listas_encabezados.append('90+')
        context = {
            'apellido':apellido_obj, 
            'detalle_regiones':detalle_regiones,
            'porcentaje_apellido':porcentaje_apellido, 
            'style_mujeres':style_mujeres, 
            'style_hombres':style_hombres,
            'porcentaje_hombres':porcentaje_hombres,
            'porcentaje_mujeres':porcentaje_mujeres,
            'listado_etario_json':json.dumps(listado_etario),
            'lista_encabezados_json':json.dumps(listas_encabezados),
            'edad_promedio':edad_promedio,
            }
        return render(request, 'apellidos/detalle_apellido.html',context)
    except Exception as e:
        context = {'error':e}
        return render(request, 'apellidos/error.html',context)

def solicitud_revision(request):  
    if request.method == 'POST':
        try:
            apellido = request.POST.get('input_apellido', '')            
            mensaje = request.POST.get('mensaje','')
            send_email(apellido,mensaje)
            return redirect('index')
        except Exception as e:
            context = {'error':e}
            return render(request, 'apellidos/error.html', context)

#creacion del correo
def send_email(apellido, mensaje):
    email = EmailMessage(
        subject=f'Solicitud de revision en: {apellido}',
        body=f'Se ha solicitado revisar los datos del apelliedo {apellido}. Mensaje: {mensaje}',
        from_email='nicolas.valdeslobos@gmail.com',
        to=['nicolas.valdes@live.com'],
    )   
    email.send()

