from datetime import timedelta
from django.utils.datetime_safe import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Tv
from telas.models import Tela, IntensTela


def list_tv(request):
    tvs_list = Tv.objects.all()
    paginator = Paginator(tvs_list, 10)  # Lista 25  por pagina

    page = request.GET.get('page')
    tvs = paginator.get_page(page)
    hoje = datetime.now()

    context = {
        'tvs' : tvs,
        'hoje': hoje
    }
    return render(request, 'tvs/lista.html', context)


def list_tabela(request):
    tv = request.GET.get('tv', None)
    if tv:
        tvs = Tv.objects.filter(idTv=tv)
        #SQL select from clientes nome LIKE %nome%
       #clientes = clientes.filter(nome=termo_busca)
    else:
        tvs = Tv.objects.all()

    telas = Tela.objects.filter(tv_id=tv).order_by('tipo')

    paginator = Paginator(telas, 1)  # Lista 25  por pagina

    page = request.GET.get('page')
    telas = paginator.get_page(page)

    data = {}
    data['tvs'] = tvs
    data['telas'] = telas
    data['tv_tv'] = tv
    data['tv_page'] = page
    data['total_page'] = telas.paginator.num_pages
    for tela3 in telas:
        tempotela_bd = tela3.tempoexibicao
        if tela3.tipo == 'tabela':
            itensTela = tela3.intenstela_set.all()
            pagina1 = Paginator(itensTela, 22)
            data['itens_tabela'] = pagina1.get_page(1)

        if tela3.tipo == 'oferta':

            itensTela = tela3.oferta.intensoferta_set.count


            data['totl_item_oferta'] = itensTela


    tempotela_minutos = int(tempotela_bd[:2])
    tempotela_segundos = int(tempotela_bd[3:5])
    hoje = datetime.now()
    dt_futura = hoje + timedelta(minutes=tempotela_minutos, seconds=tempotela_segundos)



    tvedit = Tv.objects.get(idTv=tv)
    tvedit.status = dt_futura
    tvedit.save()


    #data['itensoferta'] = telas.oferta.intensoferta_set.all()


    return render(request, 'tvs/lista-tabela.html', data)