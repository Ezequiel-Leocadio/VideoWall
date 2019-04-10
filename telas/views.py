from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.datetime_safe import datetime
from django.views import View
from tvs.models import Tv
from produtos.models import Produto
from ofertas.models import Oferta
from .models import Tela, IntensTela
from .forms import TelaForm, ItemTelaForm, TelaVideoForm

def list_tela(request):

    nome = request.GET.get('nome', None)
    tv = request.GET.get('tv', None)
    if nome or tv:
        telas_list = Tela.objects.filter(
            nome__contains=nome,
            tipo__contains='1tabela',

        )
        if tv:
            telas_list = Tela.objects.filter(
                nome__contains=nome,
                tipo__contains='1tabela',
                tv_id=tv
            )
    else:
        telas_list = Tela.objects.filter(tipo='1tabela')
    paginator = Paginator(telas_list, 10)  # Lista 25  por pagina

    page = request.GET.get('page')
    telas = paginator.get_page(page)
    context = {
        'telas':telas,
        'tvs': Tv.objects.all()
    }
    return render(request, 'telas/lista.html', context)



class NovaTela(View):
    def get(self, request):

        context = {

            'tipos':Tela.lista_tipo,
            'tvs': Tv.objects.all(),
            'ofertas': Oferta.objects.filter(datafim__gte=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
        return render(request, 'telas/inserir.html', context)

    def post(self, request):

        data = {}
        data['item_form'] = ItemTelaForm
        data['ofertas'] = Oferta.objects.filter(datafim__gte=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data['data']: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['tela_id'] = request.POST['tela_id']
        data['nome1'] = request.POST['tela-nome']
        data['tempo'] = request.POST['tela-tempo']
        data['tela_tv'] = request.POST['tela-tv']
        data['produtos'] = Produto.objects.all()

        if data['tela_id']:
            tela = Tela.objects.get(idTela=data['tela_id'])
            tela.nome = data['nome1']
            tela.tempoexibicao = data['tempo']
            tela.tv_id = data['tela_tv']
            tela.save()

            values = request.POST.getlist('codigo[]')
            tam = int(len(values))
            for valor in range(tam):
                produto = int(valor)
                if values[produto] == '':
                    pass
                else:
                    values2 = values[produto].split('--')
                    produto_id2 = Produto.objects.get(codigo=values2[0])
                    item_novo_editar = IntensTela.objects.filter(ordem=produto).update(
                        produto_id=produto_id2
                    )
                    if not item_novo_editar:
                        item = IntensTela.objects.create(
                            produto_id=produto_id2.idProduto, tela_id=tela.idTela, ordem=produto)

            data['nome'] = tela.nome
            data['tv_tela'] = int(tela.tv_id)
            data['tela_id'] = tela.idTela
            data['tela'] = tela
            for tam in range(int(22)):
                item = str('item_0') + str(tam)
                if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                    data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
                else:
                    pass

            messages.success(request, "Tela Editada Com Sucesso")
        else:

            tela = Tela.objects.create(
                nome=data['nome1'],
                tempoexibicao=data['tempo'],
                tipo='1tabela',
                tv_id=data['tela_tv']
            )

            values = request.POST.getlist('codigo[]')
            tam = int(len(values))
            for valor in range(tam):
                produto = int(valor)
                if values[produto] == '':
                    pass
                else:
                    values2 = values[produto].split('--')
                    produto_id = Produto.objects.get(codigo=values2[0])
                    item = IntensTela.objects.create(
                    produto_id=produto_id.idProduto, tela_id=tela.idTela,ordem=produto)


            messages.success(request, "Tela Inserida Com Sucesso")

            idTela = tela.idTela
            telav = get_object_or_404(Tela, pk=idTela)
            form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

            if form.is_valid():
                telav.video = form.cleaned_data["video"]
                form.save()

            itens = tela.intenstela_set.all()


            data['tv_tela'] = int(tela.tv_id)
            data['tipo_tela'] = tela.tipo
            data['tela'] = tela
            data['itens'] = itens
            data['nome'] = tela.nome
            data['video'] = telav.video
            data['tela_id'] = tela.idTela
            for tam in range(int(22)):
                item = str('item_0') + str(tam)
                if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                    data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
                else:
                    pass

        data['tvs'] = Tv.objects.all()
        data['tipos'] = Tela.lista_tipo



        return render(
            request, 'telas/inserir.html', data)


class EditTela(View):
    def get(self, request, tela):
        data = {}
        tela = Tela.objects.get(idTela=tela)

        data['form_item'] = ItemTelaForm
        data['tela_form'] = TelaForm
        data['nome'] = tela.nome
        data['tempo'] = tela.tempoexibicao
        data['tela'] = tela
        data['tvs'] = Tv.objects.all()
        data['ofertas'] = Oferta.objects.filter(datafim__gte=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data['tv_tela'] = tela.tv_id
        data['itens'] = tela.intenstela_set.all()
        data['produtos'] = Produto.objects.all()

        for tam in range(int(22)):
            item = str('item_0') + str(tam)
            if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
            else:
                pass


        return render(
            request, 'telas/inserir.html',data )

class NovoItemTela(View):
    def get(self, request, pk):
        pass

    def post(self, request, tela):
        data = {}
        item = IntensTela.objects.filter(produto_id=request.POST['produto_id'], tela_id=tela)

        if item:
            data['max'] = 'sim'
            tela = Tela.objects.get(idTela=tela)
            data['form_item'] = ItemTelaForm
            data['nome'] = tela.nome
            data['tempo'] = tela.tempoexibicao
            data['tvs'] = Tv.objects.all()
            data['tipos'] = Tela.lista_tipo
            data['tipo_tela'] = tela.tipo
            data['tv_tela'] = tela.tv_id
            data['tela'] = tela
            data['itens'] = tela.intenstela_set.all()
            data['produtos'] = Produto.objects.all()

            messages.error(request,"Erro Item Já Existe")
        else:
            data['max'] = 'nao'
            item = IntensTela.objects.create(
            produto_id=request.POST['produto_id'], tela_id=tela)

            data['item'] = item
            data['form_item'] = ItemTelaForm
            data['nome'] = item.tela.nome
            data['tempo'] = item.tela.tempoexibicao
            data['tvs'] = Tv.objects.all()
            data['tv_tela'] = item.tela.tv_id
            data['tipos'] = Tela.lista_tipo
            data['tipo_tela'] = item.tela.tipo
            data['tela'] = item.tela
            data['itens'] = item.tela.intenstela_set.all()
            data['produtos'] = Produto.objects.all()

            messages.success(request, "Item Inserido Com Sucesso")

        return render(
            request, 'telas/inserir.html', data)



class DeleteItemTela(View):
    def get(self, request, item):
        item_tela = IntensTela.objects.get(idIntensTela=item)
        return render(
            request, 'telas/confirma-delete.html', {'item_tela': item_tela})

    def post(self, request, item):
        item_tela = IntensTela.objects.get(idIntensTela=item)
        tela_id = item_tela.tela.idTela
        item_tela.delete()
        messages.success(request, "Item Excluido Com Sucesso")
        return redirect('editar-tela', tela=tela_id)


class DeleteTela(View):
    def get(self, request):
       pass

    def post(self, request):
        tela_id = request.POST['IdExcluir']
        tela = Tela.objects.get(idTela=tela_id)
        tipo = tela.tipo
        tela.delete()

        if tipo == '3video':
            messages.success(request, "Video Excluido Com Sucesso")
            return redirect('list_video')
        else:
            messages.success(request, "Tabela Excluida Com Sucesso")
            return redirect('list_tela')



def list_video(request):


    tv = request.GET.get('tv', None)
    if tv:
        telas_list = Tela.objects.filter(
            tipo__contains='3video',
            tv_id=tv
        )
    else:
        telas_list = Tela.objects.filter(tipo='3video')
    paginator = Paginator(telas_list, 10)  # Lista 25  por pagina

    page = request.GET.get('page')
    telas = paginator.get_page(page)
    context = {
        'telas':telas,
        'tvs': Tv.objects.all()
    }
    return render(request, 'videos/lista.html', context)




class NovoVideo(View):
    def get(self, request):

        context = {
            'tvs': Tv.objects.all(),
        }
        return render(request, 'videos/inserir.html', context)

    def post(self, request):

        data = {}
        data['item_form'] = ItemTelaForm
        data['tela_id'] = request.POST['tela_id']
        data['tempo'] = request.POST['tela-tempo']
        data['tela_tv'] = request.POST['tela-tv']

        if data['tela_id']:
            tela = Tela.objects.get(idTela=data['tela_id'])
            tela.nome ='video'
            tela.tempoexibicao = data['tempo']
            tela.tv_id = data['tela_tv']
            tela.save()

            data['tv_tela'] = int(tela.tv_id)
            data['tela_id'] = tela.idTela
            data['tela'] = tela
            data['video'] = tela.video


            messages.success(request, "Video Editada Com Sucesso")
        else:

            tela = Tela.objects.create(
                nome='video',
                tempoexibicao=data['tempo'],
                tipo='3video',
                tv_id=data['tela_tv']
            )


            messages.success(request, "Video Inserida Com Sucesso")

            idTela = tela.idTela
            telav = get_object_or_404(Tela, pk=idTela)
            form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

            if form.is_valid():
                telav.video = form.cleaned_data["video"]
                form.save()




            data['tv_tela'] = int(tela.tv_id)
            data['tela'] = telav
            data['video'] = tela.video
            data['tela_id'] = tela.idTela


        data['tvs'] = Tv.objects.all()
        data['video'] = tela.video


        return render(
            request, 'videos/inserir.html', data)



class EditVideo(View):
    def get(self, request, tela):
        data = {}
        tela = Tela.objects.get(idTela=tela)

        data['tela_form'] = TelaForm
        data['video'] = tela.video
        data['tempo'] = tela.tempoexibicao
        data['tela'] = tela
        data['tvs'] = Tv.objects.all()
        data['tv_tela'] = int(tela.tv_id)




        return render(
            request, 'videos/inserir.html',data)
