from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class formEstudiante( FlaskForm ):
    documento = StringField( 'Documento', validators=[DataRequired( message='No dejar vacío, completar' )],render_kw={"placeholder": "Identificación"} )
    nombre = StringField( 'Nombre', validators=[DataRequired( message='No dejar vacío, completar' )],render_kw={"placeholder": "Nombres"} )
    ciclo = SelectField('Ciclo', choices=[('Python'), ('Java'), ( 'Web')])
    sexo = StringField( 'Sexo', validators=[DataRequired( message='No dejar vacío, completar' )],render_kw={"placeholder": "M/F"} )
    estado = BooleanField( 'Estado')
    enviar = SubmitField( 'Enviar',render_kw={"onmouseover": "guardarEst()","class":"form_boton"} )
    consultar = SubmitField( 'Consultar', render_kw={"onmouseover": "consultarEst()","class":"form_boton"})
    listar = SubmitField( 'Listar', render_kw={"onmouseover": "listarEst()", "class":"form_boton"})
    eliminar = SubmitField( 'Eliminar', render_kw={"onmouseover": "eliminarEst()", "class":"form_boton"})
    actualizar = SubmitField( 'Actualizar', render_kw={"onmouseover": "actualizarEst()","class":"form_boton"})
    

class formlogin(FlaskForm):
    usuario = StringField( 'Usuario', validators=[DataRequired( message='No dejar vacío, completar' )],render_kw={"placeholder": "Usuario"} )
    clave = PasswordField( 'Clave', validators=[DataRequired( message='No dejar vacío, completar' )],render_kw={"placeholder": "Contraseña", "id":"password"} )
    login = SubmitField( 'Login', render_kw={"onmouseover": "consultarLogin()", "class":"form_botonL"})
    insertar = SubmitField( 'Insertar', render_kw={"onmouseover": "insertar()", "class":"form_botonL"})
  