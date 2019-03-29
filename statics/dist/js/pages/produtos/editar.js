$(document).ready(function() {

    $('.editar-produto').click(function(){
        /*  recupera o id do objeto que invocou esta rotina e popula os
            campos de 'id' (oculto), descrição e prioridade. A data é
            preenchida diretamente no gabarito. */
        let values = this.id.split('-');
        $('#editarProdutoId').prop('value', values[1]);
        $('#editarprodutoCodigo').prop('value', values[2]);
        $('#editarProdutoDescricao').prop('value', values[3]);
        $('#editarProdutoTipo').prop('value', values[4]);
        $('#editarProdutoValor').prop('value', values[5]);

        $('#editarProduto').modal('toggle');
    })// click()

})// function()
