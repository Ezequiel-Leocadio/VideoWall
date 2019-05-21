import json
from django.db.models import Max
from django.contrib import messages
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
import os
import glob
from django.conf import settings

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
        data['tvs'] = Tv.objects.all()
        #Busca o Maior Código No Banco
        data['max'] = Oferta.objects.all().aggregate(Max('codigo'))['codigo__max']
        if data['max']:
            pass
        else:
            data['max'] = 1

        data['oferta_id'] = request.POST['oferta_id']

        if data['oferta_id']:
            try:
                oferta = Oferta.objects.get(idOferta=data['oferta_id'])
                oferta.nome = data['nome']
                oferta.datainicio = datetime.strptime(request.POST['data-inicio'], '%d/%m/%Y %H:%M')
                oferta.datafim = datetime.strptime(request.POST['data-fim'], '%d/%m/%Y %H:%M')
                oferta.save()
            except Exception as erro:
                messages.error(request,'Erro ao editar oferta '+str(erro))

            try:
                tela = Tela.objects.get(oferta_id=data['oferta_id'])
                tela.tempoexibicao = request.POST['tela-tempo']
                tela.tv_id = request.POST['tela-tv']
                tela.save()
            except Exception as erro:
                messages.error(request,'Erro ao editar tela '+str(erro))

            try:
                values = request.POST.getlist('codigo[]')
                #files = request.FILES.getlist('imagem')
                #files1 = request.FILES.getlist('imagem1')

                tam = int(len(values))

                for valor in range(tam):
                    produto = int(valor)
                    values3 = values[produto].split('--')
                    if (values[produto] == '') or (len(values3) <= 1):
                        IntensOferta.objects.filter(oferta_id=oferta.idOferta, ordem=produto).delete()
                    else:
                        values2 = values[produto].split('--')

                        produto_id2 = Produto.objects.get(codigo=values2[0])
                        item_novo_editar = IntensOferta.objects.filter(oferta_id=oferta.idOferta,ordem=produto).update(
                            produto_id=produto_id2.idProduto
                        )
                        if not item_novo_editar:
                            item = IntensOferta.objects.create(
                            produto_id=produto_id2.idProduto, oferta_id=oferta.idOferta, ordem=produto)

                        produto2 = get_object_or_404(Produto, pk=produto_id2.idProduto)
                        form = ProdutoImagemForm(request.POST or None, request.FILES or None, instance=produto2)
                        teste = 'imagem0'
                        item = str('imagem') + str(produto)
                        try:
                            if item in request.FILES:
                                path = settings.BASE_DIR + "\\media\\produtos"
                                dir = os.listdir(path)
                                files = glob.glob('*.txt')

                                nome_imagem_nome = produto2.imagem.name
                                nome_imagem_array = nome_imagem_nome.split('/')
                                nome_imagem = nome_imagem_array[1]

                                for file in dir:
                                    if file == str(nome_imagem):
                                        os.remove(os.path.join(path, file))
                            else:
                                pass
                        except Exception as erro:
                            messages.error(request, "Erro ao apagar Imagem antiga " + str(erro))

                        if item in request.FILES:
                            if form.is_valid():
                                produto2.imagem = request.FILES[item]
                                form.save()


                data['datainicio'] = oferta.datainicio.strftime('%d-%m-%Y %H:%M')
                data['datafim'] = oferta.datafim.strftime('%d-%m-%Y %H:%M')
                data['tv_tela'] = int(tela.tv_id)
                data['tempo'] = tela.tempoexibicao
                data['oferta'] = oferta
                for tam in range(int(6)):
                    item = str('item_0') + str(tam)
                    if IntensOferta.objects.filter(oferta_id=oferta.idOferta, ordem=tam):
                        data[item] = IntensOferta.objects.get(oferta_id=oferta.idOferta, ordem=tam)
                    else:
                        pass

                messages.success(request, 'Oferta Editada Com Sucesso ')
            except Exception as erro:
                messages.error(request,'Erro ao Inserir Itens e Imagens na Oferta '+str(teste_values))

        else:
            try:
                tela_oferta = Tela.objects.filter(tv_id=request.POST['tela-tv'], tipo='2oferta')
                if tela_oferta:
                    messages.error(request,'Erro Ja Existe uma Oferta para essa TV')
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
                    for tam in range(int(6)):
                        item = str('item_0') + str(tam)
                        if IntensOferta.objects.filter(oferta_id=oferta.idOferta, ordem=tam):
                            data[item] = IntensOferta.objects.get(oferta_id=oferta.idOferta, ordem=tam)
                        else:
                            pass
            except Exception as erro:
                messages.error(request, 'Erro ao Inserir Oferta '+str(erro))
        return render(request, 'ofertas/inserir.html', data)


class DeleteOferta(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            oferta_id = request.POST['IdExcluir']
            tela = Tela.objects.get(oferta_id=oferta_id)
            tela.delete()

            oferta = Oferta.objects.get(idOferta=oferta_id)
            oferta.delete()
            messages.success(request, "Oferta Excluirda Com Sucesso")
        except Exception as erro:
            messages.error(request,'Erro ao excluir oferta '+str(erro))
        return redirect('list_oferta')



def lista_produtos_auto_ajax(request):
    try:
        if request.is_ajax:
            search = request.POST.get('start', '')

            produtos = Produto.objects.filter(codigo__icontains=search) or Produto.objects.filter(descricaoexibicao__icontains=search)

            results = []
            for produto in produtos:
                produto_json = {}
                produto_json['label'] =str(produto.codigo) + str(' -- '+produto.descricaoexibicao)
                produto_json['value'] = str(produto.codigo) + str(' -- '+produto.descricaoexibicao)
                results.append(produto_json)

            data_json = json.dumps(results)

        else:
            data_json = 'fail'
    except Exception as erro:
        messages.error(request, 'Erro ao listar Produtos '+str(erro))
        data_json = 'Erro ao listar Produtos '+str(erro)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)