$(document).ready(function() {
     var valor = $("#tela-tipo").val();

    if(valor == 'oferta'){

         $("#oferta").show();
     } else {

         $("#oferta").hide();
     }

    if(valor == 'video'){

         $("#video").show();
     } else {

         $("#video").hide();
     }


})// function()


function exibir_ocultar(val) {
    var valor = $("#tela-tipo").val();

    if(valor == 'oferta'){

         $("#oferta").show();
     } else {

         $("#oferta").hide();
     }


     if(valor == 'video'){

         $("#video").show();
     } else {

         $("#video").hide();
     }
};