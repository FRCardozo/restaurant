import re
from flask import Flask, render_template, request, redirect, sessions, url_for, flash, session
import os  
from sqlite3 import Error
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import escape

app=Flask(__name__)
app.secret_key = os.urandom(24)

global nombre_usuario

@app.route("/")
def main():
    return render_template("index.html")

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
        username = escape(request.form['id_user'])
        password = escape(request.form['password'])
        
        try:
            with sqlite3.connect("restaurant.db") as con:
                cur = con.cursor() #manipula la conexión a la bd
                query = cur.execute("SELECT password,nombre_completo from usuario where id_usuario = ?", [username]).fetchone()
                nombre_usuario = query[1]
                session['nombre'] = nombre_usuario
                
                if query != None:
                    if check_password_hash(query[0],password):
                        session["username"] = username
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
        return render_template("sesion.html")
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

        print(id_user)
        print(pass1)
        print(pass2)

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





@app.route("/estudiante/list", methods=["GET","POST"])
def estudiante_list():
    my_var = session.get('nombre', None)
    if "username" in session:
        try:
            with sqlite3.connect("restaurant.db") as con:
                con.row_factory = sqlite3.Row #convierte la respuesta de la BD en un diccionario
                cur = con.cursor()
                cur.execute("SELECT * FROM plato")
                row = cur.fetchall()

                # query = cur.execute("SELECT password,nombre_completo from usuario where id_usuario = ?", [my_var]).fetchone()
                # nombre_ = query[1]

                return render_template("sesion.html", row = row, name=my_var)
            
        except Error:
            print(Error)
            return "No Existen Platos"
    else:
        flash ("Acción no permitida")
        return render_template("error.html")






if __name__ == '__main__':
    app.run(debug=True, port=8000)