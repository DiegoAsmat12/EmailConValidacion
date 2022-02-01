from email_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, Markup
import re

EXP_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, email, created_at, updated_at):
        self.email = email
        self.created_at =created_at
        self.updated_at = updated_at
    
    @classmethod
    def registrarEmail(cls, email):
        query = '''
                    INSERT INTO emails(email, created_at, updated_at)
                    VALUES (%(email)s, NOW(), NOW());
                '''
        resultado = connectToMySQL("esquema_email").query_db(query,email)

        return resultado

    @classmethod
    def obtenerEmails(cls):
        query = '''
                    SELECT * FROM emails;
                '''
        resultado = connectToMySQL("esquema_email").query_db(query)
        listaEmail = []

        for email in resultado:
            listaEmail.append(cls(email["email"], email["created_at"], email["updated_at"]))
        return listaEmail

    @classmethod
    def obtenerEmail(cls,email):
        query = '''
                    SELECT * FROM emails
                    WHERE emails.email = %(email)s;
                '''
    
        resultado = connectToMySQL("esquema_email").query_db(query,email)
        emailObtenido=None
        if len(resultado)>0:
            emailObtenido = cls(resultado[0]["email"], resultado[0]["created_at"], resultado[0]["updated_at"])
        return emailObtenido

    @classmethod
    def eliminarEmail(cls,email):
        query = '''
                    DELETE FROM emails WHERE emails.email = %(email)s
                '''
        resultado = connectToMySQL("esquema_email").query_db(query,email)
        return resultado

    @staticmethod
    def validarEmail(email):
        isValid = True
        emailAComparar = Email.obtenerEmail(email)
        if(not EXP_EMAIL.match(email["email"])):
            flash(Markup("<h1>FLASH!!!</h1><p>El email proporcionado no es valido.</p>"), "email")
            isValid = False
        elif(emailAComparar!= None):
            flash(Markup("<h1>FLASH!!!</h1><p>El email proporcionado ya existe.</p>"),"email")
            isValid = False
        return isValid