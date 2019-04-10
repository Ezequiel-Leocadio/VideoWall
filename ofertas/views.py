import json
from django.db.models import Max
from  django.contrib import  messages
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from datetime import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Oferta, IntensOferta
from produtos.models import Produto
from produtos.forms import ProdutoImagemForm
from django.views import View
from .forms import ItemOfertaForm
from tvs.models import Tv
from telas.models import Tela

def list_oferta(request):
    # codigo = request.GET.get('codigo', None)
    # nome = request.GET.get('nome',None)
    # datainicio = request.GET.get('data-inicio', None)
    # datafim = request.GET.get('data-fim', None)
    tv = request.GET.get('tv', None)

    # data = {}
    # data['codigo'] = codigo
    # data['nome'] = nome
    # if datainicio:
    #     datainicio2 = datetime.strptime(datainicio, '%d/%m/%Y')
    #     datainicio3 = datainicio2.strftime('%Y-%m-%d')
    #     data['datainicio'] = datainicio3
    # else:
    #     data['datainicio'] = '1990-01-01'
    # if datafim:
    #     datafim2 = datetime.strptime(datafim, '%d/%m/%Y')
    #     datafim3 = datafim2.strftime('%Y-%m-%d')
    #     data['datafim'] = datafim3
    # else:
    #     data['datafim'] = '9999-12-31'

    if tv:
        telas_list = Tela.objects.filter(
            tipo__contains='2oferta',
            tv_id=tv
        )


    else:
        telas_list = Tela.objects.filter(tipo='2oferta')

    paginator = Paginator(telas_list, 10)  # Lista 25  por pagina

    page = request.GET.get('page')
    telas = paginator.get_page(page)
    context = {
        'telas':telas,
        'tvs': Tv.objects.all()

    }
    return render(request, 'ofertas/lista.html',context)

class EditOferta(View):
    def get(self, request, oferta):
        data = {}
        oferta = Oferta.objects.get(idOferta=oferta)
        tela = Tela.objects.get(oferta_id=oferta)
        data['tela'] = tela
        data['form_item'] = ItemOfertaForm()
        data['codigo'] = oferta.codigo
        data['nome'] = oferta.nome
        data['datainicio'] = oferta.datainicio.strftime('%d-%m-%Y %H:%M')
        data['datafim'] = oferta.datafim.strftime('%d-%m-%Y %H:%M')
        data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
        data['oferta'] = oferta
        data['itens'] = oferta.intensoferta_set.all()
        data['tv_tela'] = int(tela.tv_id)
        data['tvs'] = Tv.objects.all()
        data['tempo'] = tela.tempoexibicao
        data['produtos'] = Produto.objects.all()

        for tam in range(int(6)):
            item = str('item_0')+str(tam)
            if IntensOferta.objects.filter(oferta_id=oferta.idOferta, ordem=tam):
                data[item] = IntensOferta.objects.get(oferta_id=oferta.idOferta, ordem=tam)
            else:
                pass


        return render(
            request, 'ofertas/inserir.html', data)

class NovaOferta(View):
    def get(self, request):
        data = {}
        data['tvs'] = Tv.objects.all()
        return render(request, 'ofertas/inserir.html',data)

    def post(self, request):
        data = {}
        data['form_item'] = ItemOfertaForm()
        data['data-inicio'] = datetime.strptime(request.POST['data-inicio'], '%d/%m/%Y %H:%M')
        data['data-fim'] = datetime.strptime(request.POST['data-fim'], '%d/%m/%Y %H:%M')
        data['nome'] = request.POST['nome']

        #Busca o Maior Código No Banco
        data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
        if data['max']:
            pass
        else:
            data['max'] = 1

        data['oferta_id'] = request.POST['oferta_id']

        if data['oferta_id']:
            oferta = Oferta.objects.get(idOferta=data['oferta_id'])
            oferta.nome = data['nome']
            oferta.datainicio = datetime.strptime(request.POST['data-inicio'], '%d/%m/%Y %H:%M')
            oferta.datafim = datetime.strptime(request.POST['data-fim'], '%d/%m/%Y %H:%M')
            oferta.save()

            tela = Tela.objects.get(oferta_id=data['oferta_id'])
            tela.tempoexibicao = request.POST['tela-tempo']
            tela.tv_id = request.POST['tela-tv']
            tela.save()

            values = request.POST.getlist('codigo[]')
            #files = request.FILES.getlist('imagem')
            #files1 = request.FILES.getlist('imagem1')


            tam = int(len(values))

            for valor in range(tam):
                produto = int(valor)
                if values[produto] == '':
                    pass
                else:
                    values2 = values[produto].split('--')
                    produto_id2 = Produto.objects.get(codigo=values2[0])
                    item_novo_editar = IntensOferta.objects.filter(ordem=produto).update(
                        produto_id=produto_id2.idProduto
                    )
                    if not item_novo_editar:
                        item = IntensOferta.objects.create(
                        produto_id=produto_id2.idProduto, oferta_id=oferta.idOferta, ordem=produto)

                    produto2 = get_object_or_404(Produto, pk=produto_id2.idProduto)
                    form = ProdutoImagemForm(request.POST or None, request.FILES or None, instance=produto2)
                    teste = 'imagem0'
                    item = str('imagem') + str(produto)
                    if item in request.FILES:
                        if form.is_valid():
                            produto2.imagem = request.FILES[item]
                            form.save()


            messages.success(request, 'Oferta Editada Com Sucesso')
        else:
            oferta = Oferta.objects.create(
                codigo=int(data['max']+1),
                nome=data['nome'],
                datainicio=data['data-inicio'],
                datafim=data['data-fim']
            )

            tela = Tela.objects.create(
                nome='oferta',
                tempoexibicao= request.POST['tela-tempo'],
                tipo='2oferta',
                tv_id=request.POST['tela-tv'],
                oferta_id=oferta.idOferta
            )


            values = request.POST.getlist('codigo[]')
            files = request.FILES.getlist('imagem')

            tam = int(len(values))

            for valor in range(tam):
                produto = int(valor)
                if values[produto] == '':
                    pass
                else:
                    values2 = values[produto].split('--')
                    produto_id = Produto.objects.get(codigo=values2[0])
                    item = IntensOferta.objects.create(
                    produto_id=produto_id.idProduto, oferta_id=oferta.idOferta,ordem=produto)

                    produto2 = get_object_or_404(Produto, pk= produto_id.idProduto)
                    form = ProdutoImagemForm(request.POST or None, request.FILES or None, instance=produto2)

                    item = str('imagem') + str(produto)
                    if item in request.FILES:
                        if form.is_valid():
                            produto2.imagem = request.FILES[item]
                            form.save()



            #data_json = json.dumps(files)
            messages.success(request, 'Oferta Inserida Com Sucesso, Código: '+ str(oferta.codigo))

        itens = oferta.intensoferta_set.all()
        data['codigo'] = oferta.codigo
        data['datainicio'] = oferta.datainicio.strftime('%d-%m-%Y %H:%M')
        data['datafim'] = oferta.datafim.strftime('%d-%m-%Y %H:%M')
        data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
        data['oferta'] = oferta
        data['itens'] = itens
        data['produtos'] = Produto.objects.all()
        data['tv_tela'] = int(tela.tv_id)
        data['tvs'] = Tv.objects.all()
        data['tempo'] = tela.tempoexibicao

        data['tvs'] = Tv.objects.all()
        for tam in range(int(6)):
            item = str('item_0') + str(tam)
            if IntensOferta.objects.filter(oferta_id=oferta.idOferta, ordem=tam):
                data[item] = IntensOferta.objects.get(oferta_id=oferta.idOferta, ordem=tam)
            else:
                pass

        return render(request, 'ofertas/inserir.html', data)

class NovoItemOferta(View):
    def get(self, request, pk):
        pass

    def post(self, request, oferta):
        data = {}
        item = IntensOferta.objects.filter(produto_id=request.POST['produto_id'], oferta_id=oferta)

        if item:
            data['max'] = 'sim'
            oferta = Oferta.objects.get(idOferta=oferta)
            data['form_item'] = ItemOfertaForm()
            data['codigo'] = oferta.codigo
            data['nome'] = oferta.nome
            data['datainicio'] = oferta.datainicio
            data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
            data['oferta'] = oferta
            data['itens'] = oferta.intensoferta_set.all()
            data['produtos'] = Produto.objects.all()


            messages.error(request,"Erro Item Já Existe")
        else:
            data['max'] = 'nao'
            idProduto = request.POST["produto_id"]
            produto = get_object_or_404(Produto, pk=idProduto)
            form = ProdutoImagemForm(request.POST or None, request.FILES or None, instance=produto)

            if form.is_valid():
                produto.imagem = form.cleaned_data["imagem"]
                form.save()

            item = IntensOferta.objects.create(
            produto_id=request.POST['produto_id'], oferta_id=oferta)

            data['item'] = item
            data['form_item'] = ItemOfertaForm()
            data['codigo'] = item.oferta.codigo
            data['nome'] = item.oferta.nome
            #data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
            data['datainicio'] = item.oferta.datainicio.strftime('%d-%m-%Y %H:%M')
            data['datafim'] = item.oferta.datafim.strftime('%d-%m-%Y %H:%M')
            data['oferta'] = item.oferta
            data['itens'] = item.oferta.intensoferta_set.all()
            data['produtos'] = Produto.objects.all()

            messages.success(request, "Item Inserido Com Sucesso")

        return render(
            request, 'ofertas/inserir.html', data)

class DeleteItemPedido(View):
    def get(self, request, item):
        item_oferta = IntensOferta.objects.get(idIntensOferta=item)
        return render(
            request, 'ofertas/confirma-delete.html', {'item_oferta': item_oferta})

    def post(self, request, item):
        item_oferta = IntensOferta.objects.get(idIntensOferta=item)
        oferta_id = item_oferta.oferta.idOferta
        item_oferta.delete()
        return redirect('editar-oferta', oferta=oferta_id)

class DeleteOferta(View):
    def get(self, request):
        pass

    def post(self, request):
        oferta_id = request.POST['IdExcluir']
        tela = Tela.objects.get(oferta_id=oferta_id)
        tela.delete()
        
        oferta = Oferta.objects.get(idOferta=oferta_id)
        oferta.delete()
        messages.success(request, "Oferta Excluirda Com Sucesso")
        return redirect('list_oferta')



def lista_produtos_auto_ajax(request):
    if request.is_ajax:
        search = request.POST.get('start', '')

        doctores = Produto.objects.filter(codigo__icontains=search)

        results = []
        for doctor in doctores:
            doctor_json = {}
            doctor_json['label'] =str(doctor.codigo) + str(' -- '+doctor.descricaoexibicao)
            doctor_json['value'] = str(doctor.codigo) + str(' -- '+doctor.descricaoexibicao)
            results.append(doctor_json)

        data_json = json.dumps(results)

    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)