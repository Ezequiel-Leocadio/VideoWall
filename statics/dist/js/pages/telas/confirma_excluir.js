$(document).ready(function() {

    $('.confirma-excluir').click(function(){
        /*  recupera o id do objeto que invocou esta rotina e popula os
            campos de 'id' (oculto), descrição e prioridade. A data é
            preenchida diretamente no gabarito. */
        let values = this.id.split('-');
        $('.IdExcluir').prop('value', values[1]);
        $('.DescricaoExcluir').html( values[2]);



        $('#confirma-exluir').modal('toggle');
    })// click()

})// function()
