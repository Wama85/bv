from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('bv')
records = db.user
libros_r=db.libros
autores_r=db.autores
@app.route('/')
def main():
    return render_template('index.html')
@app.route("/insertuser", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        nombre = request.form.get("txtnombre")
        apellido = request.form.get("txtapellido")
        email= request.form.get("txtmail")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")
        tipo = request.form.get("cbxtipo")
        
        nombre_found = records.find_one({"nombre": nombre})
        email_found = records.find_one({"email": email})
        if nombre_found:
            message = 'html:There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'html:This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'html:Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'nombre': nombre, 'apellido':apellido, 'email': email, 'tipo':tipo, 'password': hashed}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('catalogo.html', email=new_email)
    return render_template('usuarios.html')

@app.route("/insertlibros", methods=['post', 'get'])
def inlibros():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        isbn = request.form.get("txtisbn")
        titulo = request.form.get("txttitulo")
        autor= request.form.get("txtautor")
        descripcion = request.form.get("txtdescripcion")
        editorial = request.form.get("txteditorial")
        tipo_libro = request.form.get("cbxtipo")
        categoria = request.form.get("cbxcategoria")
        numpaginas = request.form.get("txtnumpaginas")
        fechapubli = request.form.get("txtfechapubli")
        archivo_pdf = request.form.get("txtarchivo_pdf")
        
        miniatura_jpg = request.form.get("txtminiatura_jpg")
        edicion = request.form.get("txtedicion")
        
        isbn_found = records.find_one({"isbn": isbn})
        if isbn_found:
            message = 'html:Este ISBN ya xiste en el registro'
            return render_template('libros.html', message=message)
        else:
            libros_input = {
             'isbn': isbn,
             'titulo':titulo,
             'autor': autor,
             'descripcion':descripcion,
             'editorial': editorial,
             'tipo_libro': tipo_libro,
             'categoria': categoria,
             'numpaginas': numpaginas,
             'fechapubli': fechapubli,
             'archivo': archivo_pdf,
             'estado': '1',
             'cantador': '1',
             'miniatura_jpg': miniatura_jpg,
             'edicion': edicion
            }
       
            libros_r.insert_one(libros_input)
   
        message = 'html:Datos ingresados correctamente'   
    return render_template('libros.html',message=message)

@app.route("/insertautores", methods=['post', 'get'])
def inautores():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        nombre = request.form.get("txtnombre")
        apellido = request.form.get("txtapellido")
        direccion= request.form.get("txtdireccion")
        mail = request.form.get("txtmail")
        telefono = request.form.get("txttelefono")
       
        
     
        
        nombre_found = records.find_one({"nombre": nombre, "apellido":apellido})
        if nombre_found:
            message = 'html:Este autores ya xiste en el registro'
            return render_template('autores.html', message=message)
        else:
            autores_input = {
             'nombre': nombre,
             'apellido':apellido,
             'direccion': direccion,
             'mail':mail,
             'telefono': telefono
             
            }
       
            autores_r.insert_one(autores_input)
   
        message = 'html:Datos ingresados correctamente'   
    return render_template('autores.html',message=message)

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'html:Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
    
       
        email_found = records.find_one({"email": email})
        if records.find_one({"tipo": "ADMIN"}):
            return render_template('home.html')
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('adminlogin.html', message=message)
        else:
            message = 'Email not found'
            return render_template('adminlogin.html', message=message)
    return render_template('adminlogin.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("index.html")
    else:
        return render_template('index.html')
@app.route('/catalogo')
def catalogo():
 if "email" in session:
     session.pop("email", None)
     return render_template("catalogo.html")
 else:
     return render_template('signout.html')
 
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('catalogo.html', email=email)
    else:
        return redirect(url_for("login"))
    
@app.route('/home')
def adminhome():
    if "email" in session:
        email = session["email"]
        return render_template('home.html', email=email)
    else:
        return redirect(url_for("login"))
#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)
