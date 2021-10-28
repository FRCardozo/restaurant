function guardarEst(){
    document.getElementById("formulario").action="/estudiante/save";
}

function consultarEst(){
    document.getElementById("formulario").action="/estudiante/get";
}

function listarEst(){
    document.getElementById("formulario").action="/estudiante/list";
}

function eliminarEst(){
    document.getElementById("formulario").action="/estudiante/delete";
}

function actualizarEst(){
    document.getElementById("formulario").action="/estudiante/update";
}

function consultarLogin(){
    document.getElementById("formsLogin").action="/login/get";
}

function insertar(){
    document.getElementById("formsLogin").action="/login/save";
}

function mostrarContrasena(){
    var tipo = document.getElementById("password");
      if(tipo.type == "password"){
          tipo.type = "text";
      }else{
          tipo.type = "password";
      }
}

function logout(){
    document.getElementById("formulario").action="/logout";
}