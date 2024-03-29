# Biblios django
from django.http      import HttpResponse
from django.shortcuts import render,redirect
from django.template  import Template,Context
from django.http      import JsonResponse

# Importamos funciones
from web_server.funciones.conexion_db          import conexion_peticion
from web_server.funciones.datos_home           import datos_default_home
from web_server.funciones.validacion_identidad import validacion_de_identidad,validacion_hash
from web_server.funciones.sha256               import hasheo_dato

# Pagina de prueba login como plantilla
def home(request):
    return render(request, 'login.html',{'advertencia':'Inicia Sesion','color':'gray'})

# Validación de usuario
def login(request):
    # Parametros por defecto de la session

    request.session['usuario'] = request.session.get('usuario', '');
    request.session['hash']    = request.session.get('hash', '');

    # Validamos
    validacion_es_true = validacion_de_identidad(request, conexion_peticion);

    if (validacion_es_true and request.method == "POST"):
        # Creamos un hash de Sesion (siempre será igual)
        hash    = hasheo_dato(request.POST.get('usuario'),request.POST.get('contraseña'));

        # Guardamos los datos en la session
        request.session['usuario'] = request.POST.get('usuario');
        request.session['hash']    = hash;

        # Traemos los datos de la DB
        usuario      = request.session['usuario'];
        datos        = datos_default_home(usuario);
        datos['max']   = max(datos['valor']) + 0.05 * max(datos['valor']);
        datos['min']   = min(datos['valor']) - 0.05 * max(datos['valor']);
        datos['uni']   = datos['magnitud_fisica'][0];

        # Creamos el contexto de datos
        context = {
            'usuario'   : request.POST.get('usuario'),
            'hash'      : hash,
            'datos'     : datos,
        }
        return render(request,'landing.html',context);
    elif (validacion_es_true and request.method == "GET"):

        # Traemos los datos de la DB
        usuario        = request.session['usuario'];
        datos          = datos_default_home(usuario);
        datos['max']   = max(datos['valor']) + 0.05 * max(datos['valor']);
        datos['min']   = min(datos['valor']) - 0.05 * max(datos['valor']);
        datos['uni']   = datos['magnitud_fisica'][0];

        # Creamos el contexto de datos
        context = {
            'usuario'   : request.session['usuario'],
            'hash'      : request.session['hash'],
            'datos'     : datos,
        }

        return render(request,'landing.html',context);
    else:
        #raise ValueError(request.session['usuario'])
        return render(request, 'login.html', {'advertencia':'Contraseña o usuario Incorrecto','color':'red'})

# Funcion de logout
def logout(request):
    # Reseteamos los datos de la sesion
    request.session['usuario'] = '';
    request.session['hash']    = '';

    # Cargamos la pagina de login
    return render(request, 'login.html', {'advertencia':'Inicia Sesion','color':'gray'})

# Endpoint que alimenta gráficos en la página
def datos(request,nodos,magnitudFisica):

    # Traemos los datos de la DB
    usuario = request.session['usuario'];

    datos = datos_default_home(usuario, nodo = nodos, magnitud = magnitudFisica);
    # Estructura de los datos que hay que mandar
    """
    data = {
        "x"     : [1,2,3,4,5,6,7],
        "y"     : [65, 59, 80, 81, 26, 55, 40],
        "y_min" : 1,
        "y_max" : 90
    }
    """
    return JsonResponse(datos)

# Página orientada a la visualización de los datos
def dashboard(request):
    # Parametros por defecto de la session

    request.session['usuario'] = request.session.get('usuario', '');
    request.session['hash']    = request.session.get('hash', '');

    # Validamos
    validacion_es_true = validacion_de_identidad(request, conexion_peticion);

    if (validacion_es_true and request.method == "GET"):

        # Traemos los datos de la DB
        usuario      = request.session['usuario'];
        datos        = datos_default_home(usuario);
        datos['max']   = max(datos['valor']);
        datos['min']   = min(datos['valor']);
        datos['uni']   = datos['magnitud_fisica'][0];

        # Creamos el contexto de datos
        context = {
            'usuario'   : request.session['usuario'],
            'hash'      : request.session['hash'],
            'datos'     : datos,
        }

        return render(request,'dashboard.html',context);
    else:
        #raise ValueError(request.session['usuario'])
        return render(request, 'login.html', {'advertencia':'Contraseña o usuario Incorrecto','color':'red'});