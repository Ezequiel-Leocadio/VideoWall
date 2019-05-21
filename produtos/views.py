import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tvs, Produto
from django.contrib import messages
import csv, io
from .forms import ProdutoForm, ProdutoImagemForm, ProdutoUpload
from django.contrib.auth.decorators import permission_required
from django.db import transaction
import os
import glob
from django.conf import settings

def list_produtos(request):
    form = ProdutoForm(request.POST, request.FILES)

    codigo = request.GET.get('codigo', None)
    valor = request.GET.get('valor', None)
    tipo = request.GET.get('tipo', None)
    descricaoex = request.GET.get('descricaoex', None)
    descricaoim = request.GET.get('descricaoim', None)

    if codigo or valor or tipo or descricaoex or descricaoim:
        produtos_list = Produto.objects.filter(
            codigo__icontains=codigo,
            valor__icontains=valor,
            tipoproduto__icontains=tipo,
            descricaoexibicao__icontains=descricaoex,
            descricaoimportcao__icontains=descricaoim,
        ).order_by('descricaoimportcao')
    else:
        produtos_list = Produto.objects.all().order_by('descricaoimportcao')

    paginator = Paginator(produtos_list, 10)  # Lista 25  por pagina

    page = request.GET.get('page')
    produtos = paginator.get_page(page)

    context = {
        'produtos':produtos,
        'form':form
    }
    return render(request, 'produtos/lista.html', context)

def inserir_produtos(request):

    tvs = Tvs.objects.all()
    return render(request, 'produtos/inserir.html', {'tvs':tvs})



def editar_produtos2(request):
    form = ProdutoForm(request.POST, request.FILES)

    idProduto = request.POST["idProduto"]
    editado = Produto.objects.filter(idProduto=idProduto).update(
        codigo=request.POST["codigoProduto"],
        tipoproduto=request.POST["tipoProduto"],
        valor=str(request.POST["valorProduto"]).replace(',', '.'),
        descricaoexibicao=request.POST["descricaoProduto"],
        imagem=request.FILES["imagem"],
    )
    if not editado:
        messages.error(request, "Erro ao Editaro")

    messages.success(request, 'Salvo Com Sucesso')

    context = {
        'form': form,
    }
    return redirect('list_produtos')

def editar(request):
    produto = get_object_or_404(Produto, pk=request.POST['idProduto'])
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    if form.is_valid():
        try:
            produto.imagem = form.cleaned_data["imagem"]
            form.save()
            messages.success(request, 'Salvo Com Sucesso')
        except Exception as erro:
            messages.error(request,'Erro ao editar produto '+str(erro))

        return redirect('list_produtos')

    context = {
        'form': form
    }

    return redirect('list_produtos')

def editar_produtos(request,id):
    produto = get_object_or_404(Produto, pk=id)
    nome_imagem_nome = produto.imagem.name
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    if form.is_valid():
        try:
            try:
                path = settings.BASE_DIR + "\\media\\produtos"
                dir = os.listdir(path)
                nome_imagem_array = nome_imagem_nome.split('/')
                nome_imagem = nome_imagem_array[1]

                for file in dir:
                    if file == str(nome_imagem):
                        os.remove(os.path.join(path, file))

            except Exception as erro:
                messages.error(request, "Erro ao apagar Imagem antiga " + str(nome_imagem_nome))

            produto.imagem = form.cleaned_data["imagem"]
            produto.descricaoexibicao = form.cleaned_data["descricaoexibicao"]
            produto.tipoproduto = form.cleaned_data["tipoproduto"]
            produto.valor = form.cleaned_data["valor"]
            produto.codigo = form.cleaned_data["codigo"]
            form.save()

            messages.success(request, 'Salvo Com Sucesso')
            return redirect('list_produtos')
        except Exception as erro:
            messages.error(request,'Erro ao editar Produto '+ str(erro))

    context = {
   'form': form,
    'produto':produto
    }

    return render(request, 'produtos/editar2.html', context)



def list_tabela(request):
    pesquisa = request.GET.get('pesquisa', None)
    if pesquisa:
        products = Tvs.objects.filter(description__contains =pesquisa)
        #SQL select from clientes nome LIKE %nome%
       #clientes = clientes.filter(nome=termo_busca)
    else:
        products = Tvs.objects.all()
    return render(request, 'produtos/lista-tabela.html', {'products':products})

def list_tabela2(request):
    pesquisa = request.GET.get('pesquisa', None)
    if pesquisa:
        products = Tvs.objects.filter(description__contains =pesquisa)
        #SQL select from clientes nome LIKE %nome%
       #clientes = clientes.filter(nome=termo_busca)
    else:
        products = Tvs.objects.all()
    return render(request, 'produtos/tabela2.html', {'products':products})


class NewsCreateView(CreateView):
    model = Produto
    fields = '__all__'

    def form_valid(self, form):
       # self.object = form.save()
        return render(self.request, 'produtos/news_create_success.html', {'news': self.object})

#@permission_required('admin.can_add_log_entry')


def produto_upload2(request):
    template = "produtos/inserir.html"

    form = ProdutoUpload(request.POST or None, request.FILES or None,)
    data = {}
    data2 = {}
    tipoproduto = ''
    codigo = ''
    valor = {}
    descricao = ''
    io_string = ''
    transaction.set_autocommit(False)
    if form.is_valid():
        data = request.FILES['file'].read()
        data2 =data.splitlines()
        produtos = Produto.objects.all()
        for item in data2:
            data3 = str(item).split('b')
            data_item = str(data3[1])
            tipoproduto = int(data_item[3:4])
            codigo = int(data_item[4:10])
            valor1 = str(data_item[10:14])
            valor2 = str(data_item[14:16])
            valor = float(valor1+'.'+valor2)
            descricao = data_item[19:69]

            created = Produto.objects.filter(codigo=codigo).update(
                tipoproduto=tipoproduto,
                valor=valor,
                descricaoimportcao=descricao,
            )
            if not created:
                Produto.objects.create(
                    tipoproduto=tipoproduto,
                    codigo=codigo,
                    valor=valor,
                    descricaoimportcao=descricao,
                    descricaoexibicao=descricao
                )
        transaction.commit()

    messages.success(request, "Upload Efetuado Com Sucesso "+str(codigo))
    return render(request, template)

def produto_upload(request):
    template = "produtos/inserir.html"
    try:

        prompt = {
           # 'order': "Order of csv should be first_name, last_name, email, ip_address, message"
        }
        if request.method == "GET":
            return render(request, template, prompt)

        csv_file = request.FILES['file']

        if (not csv_file.name.endswith('.TXT')) or (not csv_file.name.endswith('.txt')):
            messages.error(request, "O Arquivo não corresponde ao formato .txt")

        data_set = csv_file.read().decode('ISO-8859-1')
        io_string = io.StringIO(data_set)

        for column in csv.reader(io_string):
            linha = ''.join(str(e) for e in column)
            tipoproduto = int(linha[2:3])
            codigo = int(linha[3:9])
            valor = float(linha[9:13]+'.'+linha[13:15])
            descricao = linha[18:68]

            created = Produto.objects.filter(codigo=codigo).update(
                tipoproduto=tipoproduto,
                valor=valor,
                descricaoimportcao=descricao,
            )
            if not created:
                Produto.objects.create(
                    tipoproduto=tipoproduto,
                    codigo=codigo,
                    valor=valor,
                    descricaoimportcao=descricao,
                    descricaoexibicao=descricao
                )
    except Exception as erro:
        messages.error(request,'Erro ao Realizar Upload de arquivo '+str(erro))
    context = {}
    messages.success(request, "Upload Efetuado Com Sucesso")
    return render(request, template, context)