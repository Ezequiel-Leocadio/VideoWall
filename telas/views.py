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
import os
import glob
from django.conf import settings

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
        #Verifica se o input de Tela de Tabela esta preenchido se estiver ira atualizar
        if data['tela_id']:
            #Atualizar A tela de Tebela
            try:
                tela = Tela.objects.get(idTela=data['tela_id'])
                tela.nome = data['nome1']
                tela.tempoexibicao = data['tempo']
                tela.tv_id = data['tela_tv']
                tela.save()
            except Exception as erro:
                messages.error(request,'Erro ao Editar tabela')
            ##Fim atualizar a tela de Tabela
            #Atualizar itens na tela de Tabela
            try:
                values = request.POST.getlist('codigo[]')
                tam = int(len(values))

                for valor in range(tam):
                    produto = int(valor)
                    if values[produto] == '':
                        pass
                    else:
                        values2 = values[produto].split('--')
                        produto_id2 = Produto.objects.get(codigo=values2[0])
                        item_novo_editar = IntensTela.objects.filter(tela_id=tela.idTela,ordem=produto).update(
                            produto_id=produto_id2
                        )
                        if not item_novo_editar:
                            item = IntensTela.objects.create(
                                produto_id=produto_id2.idProduto, tela_id=tela.idTela, ordem=produto)
            except Exception as erro:
                messages.error(request,'Erro ao Atualizar itens na Tabela '+str(erro))
            ##Fim atualizar itens na Tabela
            data['nome'] = tela.nome
            data['tv_tela'] = int(tela.tv_id)
            data['tela_id'] = tela.idTela
            data['tela'] = tela
            #Loop Para preencher as variaves de itens de item00 até item21, 22 itens
            for tam in range(int(22)):
                item = str('item_0') + str(tam)
                if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                    data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
                else:
                    pass
            ##Fim Loop de itens
            messages.success(request, "Tela Editada Com Sucesso")
        else:
            #Inserir Tela de Tabela
            try:
                tela = Tela.objects.create(
                    nome=data['nome1'],
                    tempoexibicao=data['tempo'],
                    tipo='1tabela',
                    tv_id=data['tela_tv']
                )
            except Exception as erro:
                messages.error(request,'Erro ao Criar Tabela '+str(erro))
            ##Fim Inseri tela de Tabela
            #Inseri itens na tela de Tabela
            try:
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
            except Exception as erro:
                messages.error(request,'Erroa ao Inserir itens na Tabela '+str(erro))
            ##Fim Inseri itens na tela de Tabela
            messages.success(request, "Tela Inserida Com Sucesso")

            # idTela = tela.idTela
            # telav = get_object_or_404(Tela, pk=idTela)
            # form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

            # if form.is_valid():
            #     telav.video = form.cleaned_data["video"]
            #     form.save()

            itens = tela.intenstela_set.all()

            data['tv_tela'] = int(tela.tv_id)
            data['tipo_tela'] = tela.tipo
            data['tela'] = tela
            data['itens'] = itens
            data['nome'] = tela.nome
            # data['video'] = telav.video
            data['tela_id'] = tela.idTela
            #Loop Para preencher as variaves de itens de item00 até item21, 22 itens
            for tam in range(int(22)):
                item = str('item_') + str(tam)
                if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                    data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
                else:
                    pass
            ##Fim Loop de itens



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
        #Loop Para preencher as variaves de itens de item00 até item21, 22 itens
        for tam in range(int(22)):
            item = str('item_') + str(tam)
            if IntensTela.objects.filter(tela_id=tela.idTela, ordem=tam):
                data[item] = IntensTela.objects.get(tela_id=tela.idTela, ordem=tam)
            else:
                  pass
        ##Fim Loop de itens
        return render(
            request, 'telas/inserir.html',data )


class DeleteTela(View):
    def get(self, request):
       pass

    def post(self, request):
        try:
            tela_id = request.POST['IdExcluir']
            tela = Tela.objects.get(idTela=tela_id)
            nome_video_nome = tela.video.name
            tipo = tela.tipo
            tela.delete()

            if tipo == '3video':
                try:
                    path = settings.BASE_DIR + "\\media\\videos"
                    dir = os.listdir(path)

                    nome_video_array = nome_video_nome.split('/')
                    nome_video = nome_video_array[1]

                    for file in dir:
                        if file == str(nome_video):
                            os.remove(os.path.join(path, file))
                except Exception as erro:
                    messages.error(request, "Erro ao apagar Video antigo " + str(erro))

                messages.success(request, "Video Excluido Com Sucesso")
                return redirect('list_video')
            else:
                messages.success(request, "Tabela Excluida Com Sucesso")
                return redirect('list_tela')
        except Exception as erro:
            messages.erro(request,"Erro ao Deletar Tela "+ str(erro))



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

        #Verifica se o input de id da tela esta preenchido se estiver e so atualizar o video
        if data['tela_id']:
            #Primeiro Atualizar a tela de video
            try:
                tela = Tela.objects.get(idTela=data['tela_id'])
                tela.nome ='video'
                tela.tempoexibicao = data['tempo']
                tela.tv_id = data['tela_tv']
                tela.save()
            except Exception as erro:
                messages.error(request,'Erro ao atualizar Tela de Video'+str(erro))

            data['tv_tela'] = int(tela.tv_id)
            data['tela_id'] = tela.idTela
            data['tela'] = tela
            ##Fim Atualizar Tela de Video
            #Segundo Apagar o Video antigo
            idTela = tela.idTela
            telav = get_object_or_404(Tela, pk=idTela)
            form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

            try:
                path = settings.BASE_DIR+"\\media\\videos"
                dir = os.listdir(path)

                nome_video_nome = tela.video.name
                nome_video_array = nome_video_nome.split('/')
                nome_video = nome_video_array[1]

                for file in dir:
                    if file == str(nome_video):
                       os.remove(os.path.join(path,file))
            except Exception as erro:
                messages.error(request,"Erro ao apagar Video antigo "+str(erro))
            ##Fim Apagar Video Antigo
            #Terceiro Atualizar Video na Tela
            try:
                if form.is_valid():
                    telav.video = form.cleaned_data["video"]
                    form.save()
            except Exception as erro:
                messages.error(request,'Erro ao Atualizar Video da Tela '+str(erro))
            ##Fim Atulizar Video na Tela
            data['video'] = telav.video
            messages.success(request, "Video Editada Com Sucesso")
        else:

            try:
                #Verifica se Existe Video na TV
                #tela_video = Tela.objects.filter(tv_id=data['tela_tv'], tipo='3video')

                #if tela_video:
                    #messages.error(request,'Erro Já Existe Um Video para essa TV')
                #else:
                # Se a tela de Video não Existe na TV , Primeiro Inserir Tela De Video

                tela = Tela.objects.create(
                    nome='video',
                    tempoexibicao=data['tempo'],
                    tipo='3video',
                    tv_id=data['tela_tv']
                )
                ##Fim Inserir Tela de Video
                #Segundo Inseri Video na Tela
                try:
                    idTela = tela.idTela
                    telav = get_object_or_404(Tela, pk=idTela)
                    form = TelaVideoForm(request.POST or None, request.FILES or None, instance=telav)

                    if form.is_valid():
                        telav.video = form.cleaned_data["video"]
                        form.save()
                except Exception as erro:
                    messages.error(request, 'Erro ao Inserir video na Tela ' + str(erro))
                ##Fim Inserir Video na Tela
                messages.success(request, "Video Inserida Com Sucesso")

                data['tv_tela'] = int(tela.tv_id)
                data['tela'] = telav
                data['video'] = tela.video
                data['tela_id'] = tela.idTela
                data['video'] = telav.video
            except Exception as erro:
                messages.error(request,'Erro ao Inserir Tela '+str(erro))

        data['tvs'] = Tv.objects.all()

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
