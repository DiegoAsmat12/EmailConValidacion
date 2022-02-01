from flask import render_template, request, redirect
from email_app.modelos.modelo_email import Email
from email_app import app

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def registraEmail():
    email = {
        "email": request.form["email"]
    }
    if( Email.validarEmail(email) ):
        respuesta = Email.registrarEmail(email)
        if(type(respuesta) is bool and not respuesta):
            print("Algo salio mal, intente nuevamente")
            return redirect("/")
        return redirect("/results")
    return redirect("/")

@app.route("/results", methods=["GET"])
def mostrarEmails():
    emails = Email.obtenerEmails()
    return render_template("emails.html", emails=emails)

@app.route("/delete/<email>", methods=["POST"])
def eliminarEmail(email):
    emailAEliminar = {
        "email":email
    }
    resultado = Email.eliminarEmail(emailAEliminar)
    return redirect("/results")