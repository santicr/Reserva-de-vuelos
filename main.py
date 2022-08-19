from flask import Flask, request, g, redirect, url_for, render_template, flash, session #Importa las librerías que usaré
from itertools import islice #Sirve para empezar una lista a partir de x numero hasta y numero
app = Flask(__name__) #Crea una variable app para hacer mas corto el Flask name
app.secret_key = 'any random string' #Esto es para session, validar el usuario y que no se repita
@app.route('/') #Es el main por lo que no tiene una direccion
def pagPrincipal(): #Función para renderizar el index.html
    return render_template('index.html') #Busca el archivo en templates y lo enlaza con la funcion pagPrincipal

@app.route('/inicia') #La direccion a la que sedirige es a /inicia
def iniciarSesion(): #Esta función es para el inicio de sesion que se ve renderizado en /inicia
    return render_template('iniciasesion.html') #Busca el archivo en template y lo enlaza a esta función

#los metodos get y post es para obtener los datos del form
@app.route('/inicia2',methods=['GET','POST']) #Esta función ejecuta la operación de autenticación de usuario
def iniciaSesion2():
    """
    Inicia sesion comprobando que el usuario y la contraseña esten en usuarios.txt
    """
    nombre = request.form['Usuario1'] #Coge el valor de Usuario1 de html, este es para validar en el archivo txt
    contraseña= request.form['Contraseña1'] #Coge el valor de Contraseña1 de html
    usuarioB = request.form['Usuario1'] #Coge el valor de Usuario1 de html, este sirve para validar en session
    archivo = open("usuarios.txt", mode='r') #Abre el archivo usuarios.txt con modo de lectura
    session['username'] = request.form['Usuario1'] #Valida el usuario
    for i in archivo: #Coge cada linea del archivo
        x = i.split() #Convierte cada linea del archivo en una lista
        if(nombre == x[0] and contraseña == x[1]): #Verifica que el usuario y la contraseña esten registrados
            archivo.close() #Cierra el archivo para no hacer mas cambios
            return redirect(url_for('perfilPrincipal',nombre=nombre)) #Redirige al perfil del usuario
    archivo.close() #En caso de que no funcione cierra el archivo
    return redirect(url_for('pagPrincipal')) #En caso que lo anterior no funcionara redirige a la pagina principal

@app.route('/crear') #Crea una ruta para crear el usuario
def crearUsuario(): #Esta funcion enlaza html con python para enlazar la función con la página
    return render_template('crearusuario.html') #Renderiza la página web para asignarle la página a la función


@app.route('/crear2',methods=['GET','POST']) #Crea la ruta para crear el usuario, obtiene los datos del form
def crearUsuario2(): #Esta función hace las operaciones para crear el usuario
    """
    En esta parte obtiene los valores del html y los mete en el archivo usuarios.txt,
    comprueba que el usuario no exista por cada linea, si existe entonces se redirige a la misma pagina
    con un mensaje diciendo que ya existe, cuando retorna entonces se termina la función.
    Si el usuario no existe entonces los agrega y se redirige a la pagina principal.
    """
    nombre=request.form['Nombre'] #Obtiene el valor de "Nombre" que esta en el form de html
    apellido=request.form['Apellido'] #Obtiene el valor de "Apellido" que esta en el form de html
    apellido2=request.form['Apellido2'] #Obtiene el valor de "Apellido2" que esta en el form de html
    usuario=request.form['Usuario'] #Obtiene el valor de "Usuario" que esta en el form de html
    contraseña=request.form['Contraseña'] #Obtiene el valor de "Contraseña" que esta en el form de html
    aeropuerto=request.form['seleccion'] #Obtiene el valor de "Seleccion" que esta en el form de html
    archivo = open('usuarios.txt','r+') #Abre el archivo usuarios.txt con modo de lectura y escritura
    for lineas in archivo: #Coge cada linea del archivo
        split = lineas.split() #Cada linea la transforma en una lista
        if (usuario == split[0]): #Si el usuario ya esta registrado entonces...
            archivo.close() #Se cierra el archivo
            msj = "El usuario ya existe!" #Crea un mensaje diciendo que el usuario ya existe
            return redirect(url_for('crearUsuario',msj=msj)) #Se redirige a la misma pagina y termina la funcion
            break #Se rompe el ciclo del for
            archivo.close() #En caso que pase algo se cierra de nuevo
    archivo.write(usuario + ' ') #Agrega el usuario de esa persona
    archivo.write(contraseña + ' ') #Agrega la contraseña de esa persona
    archivo.write(nombre + ' ') #Agrega el nombre de la persona
    archivo.write(apellido + ' ') #Agrega el apellido paterno
    archivo.write(apellido2 + ' ') #Agrega el apellido materno
    archivo.write(aeropuerto + "\n") #Agrega al aeropuerto favorito
    archivo.close() #Y por ultimo se cierra el archivo

    return redirect(url_for('pagPrincipal')) #Retorna a la pagina principal para iniciar sesion

@app.route('/perfil',methods=['GET','POST']) #Crea la ruta para el perfil, obtiene los datos del form
def perfil(): #Nombre de la función al referirse a esta página web
    """
    Esta página aunque el nombre de la función es perfil, es la página para reservar,
    no la del usuario.
    """
    valor = request.args.get('nombre') #Esto es para coger el valor de nombre del url ej. /perfil?nombre=x
    return (render_template('perfil.html',valor=valor)) # Enlaza la página de perfil.html con la función

@app.route('/perfil2',methods=['GET','POST']) #Esta es la ruta para hacer las operaciones, metodos para obtener los valores
def perfil2(): #Esta función es la de las operaciones de 'perfil'
    """
    Esta función es para reservar, considere que primero debemos ingresar los campos
    de nuestro perfil (usuario y contraseña) para poder reservar, esta también verifica
    que el usuario y la contraseña sean de el mismo perfil y sean correctas, en caso de que no
    manda un mensaje redirigiendose a la página diciendo que los datos son incorrectos, también
    se verifica que las reservas existan en el archivo de datosvuelos.txt, en caso de que no,
    no deja que este reserve.
    """
    ciudad1=request.form['ciudad1'] #Obtiene los valores de ciudad1
    ciudad2=request.form['ciudad2'] #Obtiene los valores de ciudad2 
    escalas=request.form['escalas'] #Obtiene los valores de escalas
    aerolinea=request.form['aero'] #Obtiene los valores de la aerolinea
    lista=[] #Crea una lista externa para introducir luego unos datos
    usuario5=request.form['usuario5'] #Obtiene el valor del campo usuario5
    contra=request.form['contra'] #Obtiene el valor de la contraseña del campo contra
    archivo=open('datosvuelos.txt','r+') #Abre el archivo datosvuelos.txt con modo de lectura y escritura
    archivo2=open('reservas.txt','a') #Abre el archivo reservas.txt con modo para agregar texto
    archivo3=open('usuarios.txt','r') #Abre el archivo usuarios.txt con modo de lectura
    for linea2 in archivo3: #Obtiene cada linea del archivo usuarios.txt
        split2 = linea2.split() #Cada linea la vuelve una lista
        if(usuario5==split2[0] and contra==split2[1]): #Verifica que el usuario y contraseña ingresados sean los mismos de usuarios.txt
            for linea in islice(archivo, 59, 3927): #Obtiene cada linea de datosvuelos.txt desde la línea 60 hasta la 3927
                split = linea.split() #Cada linea de datosvuelos.txt la convierte en una lista
                if ((split[0] == aerolinea) and (split[len(split)-7] == escalas) and (split[2] == ciudad1) and (split[4] == ciudad2)): #Si el valor ingresado es igual al valor de x caracter de la lista de datosvuelos.txt
                    archivo2.write(usuario5+' ') #Escribe primero el nombre de usuario en el archivo de reservas.txt para despues identificarlo
                    lista.append(split) #Agrega la lista (si existe) de datosvuelos.txt a la lista "lista"
                    for sublista in lista: #Coge cada sublista de esa lista porque "lista" es una lista que tiene listas
                        for palabra in sublista: #Coge cada palabra de esa sublista
                            archivo2.write(' '+palabra) #Como es un ciclo anexa toda la linea palabra por palabra a reservas.txt
                        archivo2.write('\n') #Cuando acaba de meter todo, entonces agrega un espacio para la siguiente linea que va a meter
                        return render_template('perfil.html',aerolinea=aerolinea, usuario5=usuario5, lista=lista, ciudad1=ciudad1, escalas=escalas) #Se redirige a la página para mostrar otros datos
    else: #Si la contraseña y el usuario no son correctos entonces...
        men="Los datos ingresados son incorrectos" #Crea un mensaje diciendo que los datos no son correctos
        return redirect(url_for('perfil',men=men)) #Se redirige a la pagina mostrando el mensaje en el url

    return render_template('perfil.html',aerolinea=aerolinea, usuariosIni=usuariosIni, lista=lista, ciudad1=ciudad1, escalas=escalas, tamLista=tamLista) #Por si se salta todas las líneas para que no haya error

@app.route('/') #Se dirige a la página principal
def volver(): #FUncion para enlazarlo
    """
    Esta función la hice para volver de una página a la principal
    """
    return redirect(url_for('pagPrincipal')) #Retorna a la función de la página principal


@app.route('/perfilPrincipal') #Esta es la página de cualquier perfil autenticado
def perfilPrincipal(): #Esta función enlaza el html con python
    """
    Esto crea la página de cada perfil, donde solo muestra
    los registros de los vuelos en una tabla y que se puede cerrar sesion.
    """
    nombre = request.args.get('nombre') #Obtiene el valor de nombre /perfilPrincipal?nombre=hola
    archivo = open('reservas.txt','r') #Abre el archivo de reservas.txt con modo de lectura
    lista=[] #Crea una lista para poder almacenar los datos del archivo aqui
    for linea in archivo: #Coge cada línea que contiene el archivo de reservas
        split = linea.split() #Cada linea la convierte en una lista
        if (nombre == split[0]): #Si el nombre es igual a la posición 1 de la lista creada
            lista.append(split) #Agrega la lista del archivo a la lista original


    return render_template('perfilprincipal.html',lista=lista) #Enlaza la pagina con la funcion

app.run(debug = True) #Esto sirve para ejecutar el programa sin necesidad de reiniciarlo