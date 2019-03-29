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
    tipo = request.GET.get('tipo', None)
    tv = request.GET.get('tv', None)
    if nome or tipo or tv:
        telas_list = Tela.objects.filter(
            nome__contains=nome,
            tipo__contains=tipo,

        )
        if tv:
            telas_list = Tela.objects.filter(
                nome__contains=nome,
                tipo__contains=tipo,
                tv_id=tv
            )
    else:
        telas_list = Tela.objects.all()
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
        data['tipo'] = request.POST['tela-tipo']
        data['oferta_tela'] = request.POST['tela-oferta']
        data['tela_tv'] = request.POST['tela-tv']
        data['produtos'] = Produto.objects.all()

        if data['tela_id']:
            tela = Tela.objects.get(idTela=data['tela_id'])
            tela.nome = data['nome1']
            tela.tempoexibicao = data['tempo']
            tela.tipo = data['tipo']
            if data['tipo'] == 'oferta':
                tela.oferta_id = data['oferta_tela']
            elif data['tipo'] == 'video':
                pass
            tela.tv_id = data['tela_tv']
            tela.save()

            messages.success(request, "Tela Editada Com Sucesso")
        else:
            tela_oferta_video = Tela.objects.filter(tv_id=data['tela_tv'], tipo=data['tipo'])

            if tela_oferta_video:
                if data['tipo'] == 'oferta':
                    messages.error(request, 'Erro Já Existe Uma Oferta Para Essa TV')
                elif data['tipo'] == 'video':
                    messages.error(request, 'Erro Já Existe Um Video Para Essa TV')
            else:
                tela = Tela.objects.create(
                    nome=data['nome1'],
                    tempoexibicao=data['tempo'],
                    tipo=data['tipo'],
                    tv_id=data['tela_tv'],
                    oferta_id=data['oferta_tela']
                )

                messages.success(request, "Tela Inserida Com Sucesso")

                idTela = tela.idTela
                telav = get_object_or_404(Tela, pk=idTela)
                form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

                if form.is_valid():
                    telav.video = form.cleaned_data["video"]
                    form.save()

                itens = tela.intenstela_set.all()
                if data['tipo'] == 'oferta':
                    data['oferta_tela'] = int(tela.oferta_id)

                data['tv_tela'] = int(tela.tv_id)
                data['tipo_tela'] = tela.tipo
                data['tela'] = tela
                data['itens'] = itens
                data['nome'] = tela.nome
                data['video'] = telav.video

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
        data['video'] = tela.video
        data['tempo'] = tela.tempoexibicao
        data['tela'] = tela
        data['tvs'] = Tv.objects.all()
        data['ofertas'] = Oferta.objects.filter(datafim__gte=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data['oferta_tela'] = tela.oferta_id
        data['tipos']=Tela.lista_tipo
        data['tipo_tela'] = tela.tipo
        data['tv_tela'] = tela.tv_id
        data['itens'] = tela.intenstela_set.all()
        data['produtos'] = Produto.objects.all()


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
        tela.delete()
        messages.success(request, "Tela Excluirda Com Sucesso")
        return redirect('list_tela')