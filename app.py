from flask import Flask, render_template, request, url_for, redirect, session
from bson import ObjectId
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('bv')
records = db.user
libros_r=db.libros
autores_r=db.autores
comentarios_r=db.comentarios
categoria_r=db.categoria

queryuser=[{'$count':'Contar'}]
totales_autor=autores_r.aggregate(queryuser)

for total_autor in totales_autor:  
     print (totales_autor)
     
querylibro=[{'$count':'Contarlibros'}]
totales_libro=libros_r.aggregate(querylibro)
for total_libro in totales_libro:  
     print (total_libro)

querycoment=[{'$count':'ContarComentarios'}]
totales_comentarios=comentarios_r.aggregate(querycoment)
for total_comentario in totales_comentarios:
    print(total_comentario)
todoscate_l=categoria_r.find()

title="PROYECTO BV"
@app.route('/')
def main():
    return render_template('index.html', t=title)

@app.route("/insertuser", methods=['post', 'get'])
def index():
    message = ''
   
    if request.method == "POST":
        nombre = request.form.get("txtnombre")
        apellido = request.form.get("txtapellido")
        email= request.form.get("txtmail")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")
        tipo = request.form.get("cbxtipo")
        
        
        email_found = records.find_one({"email": email})
        
        if email_found:
            message = 'Este correo ya existe en la base de datos'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'La contraseña no es igual'
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
    message = 'INGRESE DATOS'
   
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
        
        isbn_found = libros_r.find_one({"ISBN": isbn})
        if isbn_found:
            message = 'Este ISBN ya xiste en el registro'
            return render_template('libros.html', m=message,t_libro=total_libro)
        else:
            libros_input = {
             'ISBN': isbn,
             'Titulo':titulo,
             'Autor': autor,
             'Descripcion':descripcion,
             'Editorial': editorial,
             'Tipo': tipo_libro,
             'Categoría': categoria,
             'Numpaginas': numpaginas,
             'Fechapublicacion': fechapubli,
             'Archivo': archivo_pdf,
             'Estado': '1',
             'Contador': '1',
             'Miniatura': miniatura_jpg,
             'EDICION': edicion
            }
       
            libros_r.insert_one(libros_input)
   
        message = 'Datos ingresados correctamente'   
    return render_template('libros.html',m=message,t_libro=total_libro,todoscate=todoscate_l)

@app.route("/insertautores", methods=['post', 'get'])
def inautores():
    message = ''
    
    if request.method == "POST":
        nombre = request.form.get("txtnombre")
        apellido = request.form.get("txtapellido")
        direccion= request.form.get("txtdireccion")
        mail = request.form.get("txtmail")
        telefono = request.form.get("txttelefono")
        
        nombre_found = autores_r.find_one({"nombre": nombre, "apellido":apellido})
        if nombre_found:
            message = 'Este autores ya xiste en el registro'
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
   
        message = 'Datos ingresados correctamente'   
    return render_template('autores.html',message=message)

@app.route("/insertcategorias", methods=['post', 'get'])
def incategorias():
    message = ''
    
    if request.method == "POST":
        nombre = request.form.get("txtnombre")
        
        
        nombre_found = categoria_r.find_one({"nombre": nombre})
        if nombre_found:
            message = 'Ya existe la categoria'
            return render_template('categoria.html', message=message, todoscate=todoscate_l)
        else:
            categoria_input = {
             'nombre': nombre,
            
             
            }
       
            categoria_r.insert_one(categoria_input)
   
        message = 'Datos ingresados correctamente'   
    return render_template('categoria.html',message=message, todoscate=todoscate_l)

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Por favor ingrese correo y contraseña'
    
    if "email" in session:
        return redirect(url_for("logged_in"))
    
    if request.method == "POST":
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
       
        email_found = records.find_one({"email": email})
        
        
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
                
                
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Contraseña Invalida'
                return render_template('adminlogin.html', message=message)
        
        else:
            message = 'Correo no valido'
            return render_template('adminlogin.html', message=message)
    return render_template('adminlogin.html', message=message)


#actualizar registros
@app.route("/updatelibros")
def update ():
	id=request.values.get("_id")
	task=libros_r.find({"_id":ObjectId(id)})
	return render_template('editlibros.html',tasks=task,t=title)


@app.route("/actionlibro", methods=['POST'])
def actionlibro_db ():
    todoslibros_l=libros_r.find()
    titulo = request.values.get("txttitulo")
    autor= request.values.get("txtautor")
    descripcion = request.values.get("txtdescripcion")
    editorial = request.values.get("txteditorial")
    tipo_libro = request.values.get("cbxtipo")
    categoria = request.values.get("cbxcategoria")
    numpaginas = request.values.get("txtnumpaginas")
    fechapubli = request.values.get("txtfechapubli")
    archivo_pdf = request.values.get("txtarchivo_pdf")
    miniatura_jpg = request.values.get("txtminiatura_jpg")
    edicion = request.values.get("txtedicion")
       
    id=request.values.get("_id")
    
    libros_r.update_one({"_id":ObjectId(id)},
        {'$set':{ 
        'Titulo':titulo,
        'Autor': autor,
        'Descripcion':descripcion,
        'Editorial': editorial,
        'Tipo': tipo_libro,
        'Categoría': categoria,
        'Numpaginas': numpaginas,
        'Fechapublicacion': fechapubli,
        'Archivo': archivo_pdf,
       
        'Miniatura': miniatura_jpg,
        'EDICION': edicion
        }
        })
    return redirect("/verlibros")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("index.html")
    else:
        return render_template('index.html')

 
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('home.html', email=email,total_autor=total_autor,t_libro=total_libro,c=total_comentario)
    else:
        return redirect(url_for("login"))



@app.route('/novedades')
def novedades_ing():
    libros_l=libros_r.find().limit(10)
    if "email" in session:
        email = session["email"]
        return render_template('novedades.html', email=email,todoslibros=libros_l)
    else:
        return redirect(url_for("login"))
    
@app.route('/catalogo')
def catalogo_ing():
    libros_l=libros_r.find()
    if "email" in session:
        email = session["email"]
        return render_template('catalogo.html', email=email,todoslibros=libros_l)
    else:
        return redirect(url_for("login"))
    
@app.route('/verlibros')
def verlibros_bd():
    todoslibros_l=libros_r.find()
    if "email" in session:
        email = session["email"]
        return render_template('verlibros.html', email=email,todoslibros=todoslibros_l,todoscate=todoscate_l)
    else:
        return redirect(url_for("login"))

@app.route('/verautores')
def verautores_bd():
    todosautores_l=autores_r.find()
    if "email" in session:
        email = session["email"]
        return render_template('verautores.html', email=email,todosautores=todosautores_l)
    else:
        return redirect(url_for("login"))
    
@app.route('/vistas')
def vistas_bd():
    id=request.values.get("_id")
    task=libros_r.find({"_id":ObjectId(id)})
    if "email" in session:
        email = session["email"]
        return render_template('vistas.html', email=email,tasks=task,t=title)
    else:
        return redirect(url_for("login"))  
@app.route("/updateautores")
def update_autor ():
    id=request.values.get("_id")
    task=autores_r.find({"_id":ObjectId(id)})
    if "email" in session:
        email = session["email"]
        return render_template('editautores.html', email=email,tasks=task,t=title)
    else:
         return redirect(url_for("login"))
@app.route("/actionautor", methods=['POST'])
def actionautor_db ():
    
    nombre = request.values.get("txtnombre")
    apellido = request.values.get("txtapellido")
    direccion= request.values.get("txtdireccion")
    mail = request.values.get("txtmail")
    telefono = request.values.get("txttelefono")
       
    id=request.values.get("_id")
    
    autores_r.update_one({"_id":ObjectId(id)},
        {'$set':{ 
        'nombre': nombre,
        'apellido':apellido,
        'direccion': direccion,
        'mail':mail,
        'telefono': telefono
        }
        })
    return redirect("/verautores")

@app.route('/elimlibro')
def elimlibro_bd():
    todoslibros_l=libros_r.find()
    if "email" in session:
        email = session["email"]
        key=request.values.get("_id")
        print(key)
        libros_r.delete_one({"_id":ObjectId(key)})
        return render_template('verlibros.html', email=email,todoslibros=todoslibros_l)
    else:
        return redirect(url_for("login"))
    
@app.route('/buscar', methods=['GET'])
def buscar_ing():
    categoria=request.values.get("txtbuscar")
    
    todoslibros_l=libros_r.find({"Categoría":categoria})
    
   
    return render_template('catalogo.html',todoslibros=todoslibros_l)
@app.route('/home')
def adminhome():
    if "email" in session:
        email = session["email"]
        return render_template('home.html', email=email,total_autor=total_autor,t_libro=total_libro,c=total_comentario)
    else:
        return redirect(url_for("login"))
#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)
