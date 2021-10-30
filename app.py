import re
import time
from flask import Flask, render_template, request, redirect, sessions, url_for, flash, session
import os  
from sqlite3 import Error
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import escape

from formularios import formPedido

app=Flask(__name__)
app.secret_key = os.urandom(24)

global nombre_usuario

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/perfil")
def perfil():

    if "username" in session:
        my_var = session.get('nombre', None)        
        direccion_correo = session.get('email', None)
        return render_template("profile.html", name=my_var, email=direccion_correo)
    else:
        flash ("Acción no permitida")
        return render_template("error.html")

@app.route("/sausuario")
def sausuario():
    return render_template("sausuario.html")

@app.route("/samenu")
def samenu():
    return render_template("samenu.html")

@app.route("/ausuario")
def ausuario():
    return render_template("ausuario.html")

@app.route("/amenu")
def amenu():
    return render_template("amenu.html")

@app.route('/acerca')
def about():
    return render_template("about.html")

@app.route('/menu')
def menu():
    return render_template("recipe.html")

@app.route('/comentarios')
def commint():
    return render_template("blog.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['id_user']
        password = request.form['password']
        
        try:
            with sqlite3.connect("restaurant.db") as con:
                cur = con.cursor() #manipula la conexión a la bd
                query = cur.execute("SELECT password,nombre_completo,email,rol from usuario where id_usuario = ?", [username]).fetchone()
                rol = query[3]
                nombre_usuario = query[1]
                correo = query[2]
                session['nombre'] = nombre_usuario
                session['email'] = correo
                
                if query != None:
                    if check_password_hash(query[0],password):
                        session["username"] = username
                        if rol == 1:
                            return render_template("sausuario.html")
                        elif rol == 2:
                            return render_template("ausuario.html")
                        return render_template("sesion.html", name=nombre_usuario) 
                    else:
                        return "Contraseña incorrecta!"
                else:
                    return "Usuario no existe!"
        except Error:
            print(Error)
            con.rollback()
            return 'No se pudo iniciar sesión'

    if 'username' in session:                
        documento_usuario = session.get('username', None)
        with sqlite3.connect("restaurant.db") as con:
            cur = con.cursor()
            query = cur.execute("SELECT password,nombre_completo,email from usuario where id_usuario = ?", [documento_usuario]).fetchone()
            nombre_usuario = query[1]
            correo = query[2]
            session['nombre'] = nombre_usuario
            session['email'] = correo
            my_var = session.get('nombre', None)
            return render_template("sesion.html", name=nombre_usuario)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    if 'username' in session:
        session.clear() 
        return render_template("index.html")



@app.route("/register", methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        
        id_user = request.form['id_user']
        name = request.form['nombre_completo']      
        email = request.form['email']
        country = request.form['pais']
        adress = request.form['direccion']
        phone = request.form['telefono']        
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        if pass1 == pass2:
            hashclave = generate_password_hash(pass1)

            try:
                with sqlite3.connect("restaurant.db") as con:
                    print("Se conectó")
                    cur = con.cursor() # manipula la conexión a la bd
                    cur.execute("INSERT INTO Usuario(id_usuario,nombre_completo,email,pais,direccion_residencia,telefono,password) values(?,?,?,?,?,?,?)", (id_user,name,email,country,adress,phone,hashclave))
                    con.commit()  
                    return render_template("login.html")
            except Error:
                print(Error)
                con.rollback()
            return 'No se pudo guardar'

        else: 
            return 'La contraseña no coincide'
      
    return render_template("register.html")



@app.route("/pedido/save", methods=['POST'])
def pedido_save():
    
    plato1 = 15000
    plato2 = 17000
    plato3 = 18000
    plato4 = 20000
    plato5 = 20000
    if "username" in session:
        if request.method == 'POST':
            plato = request.form.get('platoos')
            if plato == 'ASADO EN BISTEC':
                precio_pedido = plato1
            elif plato == 'SOLOMILLO':
                precio_pedido = plato2
            elif plato == 'LOMITOS DE RES':
                precio_pedido = plato3
            elif plato == 'ESTOFADO DE RES':
                precio_pedido = plato4
            elif plato == 'CARNE ASADA':
                precio_pedido = plato5

            adress = request.form['Adress']
            phone = request.form['Phone']
            fecha = time.strftime("%H:%M:%S")
            documento_usuario = session.get('username', None)
              
            try:
                with sqlite3.connect("restaurant.db") as con:
                    cur = con.cursor() #manipular la conexión a la bd
                    cur.execute("INSERT INTO pedido (platos, precio_pedido, direccion_domicilio, telefono, fecha_pedido, id_usuario) VALUES (?,?,?,?,?,?)", (plato, precio_pedido, adress, phone, fecha, documento_usuario))
                    con.commit() #Confirmar la transacción                    
                    return render_template("volver.html")
                    # return render_template("sesion.html", row = row, name=my_var)
                    
            except Error:
                print(Error)
            return "No se pudo realizar su pedido"
    else:
        flash ("Acción no permitida")
        return render_template("error.html")



@app.route("/platos/list", methods=["GET","POST"])
def platos_list():
    my_var = session.get('nombre', None)
    if "username" in session:
        try:
            with sqlite3.connect("restaurant.db") as con:
                con.row_factory = sqlite3.Row #convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT * FROM plato")
                row = cur.fetchall()

                return render_template("sesion.html", row = row, name=my_var)
            
        except Error:
            print(Error)
            return "No Existen Platos"
    else:
        flash ("Acción no permitida")
        return render_template("error.html")


@app.route("/perfil/update", methods = ['POST'])
def usuario_update():
    
    if "username" in session:  
        documento_usuario = session.get('username', None)

        nombre = request.form['nombre_completo']      
        email = request.form['email']
        country = request.form['pais']
        adress = request.form['direccion']
        phone = request.form['telefono'] 

        print(nombre)
        print(email)
        print(country)
        print(adress)
        print(phone)

        if request.method == "POST":
            
            try:
                with sqlite3.connect("restaurant.db") as con:
                    cur = con.cursor()
                    cur.execute("UPDATE usuario  SET nombre_completo = ?, email = ?, pais = ?, direccion_residencia = ?, telefono = ? WHERE id_usuario = ?;", [
                                nombre, email, country, adress, phone, documento_usuario])
                    con.commit()
                    return render_template("volver.html")

            except Error:
                print(Error)
                con.rollback()
    else:
        flash ("Acción no permitida")
        return render_template("error.html")


@app.route("/perfil/admin")
def admin():

    if "username" in session:
        my_var = session.get('nombre', None)        
        direccion_correo = session.get('email', None)
        return render_template("profile.html", name=my_var, email=direccion_correo)
    else:
        flash ("Acción no permitida")
        return render_template("error.html")

# ----------------------------------------------------------------------------------

@app.route("/platos/list/admin", methods=["GET","POST"])
def platos_list_admin():
    
    if "username" in session:
        try:
            with sqlite3.connect("restaurant.db") as con:
                con.row_factory = sqlite3.Row #convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT * FROM plato")
                row = cur.fetchall()

                return render_template("amenu.html", row = row)
            
        except Error:
            print(Error)
            return "No Existen Platos"
    else:
        flash ("Acción no permitida")
        return render_template("error.html")


@app.route("/user/list/admin", methods=["GET","POST"])
def user_list_admin():
    
    if "username" in session:
        try:
            with sqlite3.connect("restaurant.db") as con:
                con.row_factory = sqlite3.Row #convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT * FROM usuario")
                row = cur.fetchall()

                return render_template("ausuario.html", row = row)
            
        except Error:
            print(Error)
            return "No Existen Platos"
    else:
        flash ("Acción no permitida")
        return render_template("error.html")


@app.route("/platos/add/admin", methods = ['GET', 'POST'])
def platos_add_admin():

    if "username" in session:
        
        name_plato = request.form['nombre_plato']
        price_plato = request.form['precio_plato']

        print(name_plato)
        print(price_plato)

        try:
            with sqlite3.connect("restaurant.db") as con:
                cur = con.cursor() # manipula la conexión a la bd
                cur.execute("INSERT INTO plato(nombre_plato,precio_plato) values(?,?)", (name_plato,price_plato))
                con.commit()  
                return redirect("/amenu")
        except Error:
            print(Error)
            con.rollback()
            return 'No se pudo guardar'
      
    else:
        flash ("Acción no permitida")
        return render_template("error.html")





if __name__ == '__main__':
    app.run(debug=True, port=8000)