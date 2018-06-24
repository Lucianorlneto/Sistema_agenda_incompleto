from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'myapp'

urlpatterns = [
    url(r'^$', views.indexView, name="index"),
    url(r'^cadastro/$', views.cadastro_view, name="cadastro"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^fichas/criar$', views.criarFichaView, name="criar_ficha"),
    url(r'^fichas/listar$', views.listarFichasView, name="listar_fichas"),
    url(r'^fichas/(?P<ficha_id>[0-9]+)$', views.visualizarFichaView, name="visualizar_ficha"),
    url(r'^fichas/editar/(?P<ficha_id>[0-9]+)$', views.editarFichaView, name="editar_ficha"),
    url(r'^fichas/update/(?P<ficha_id>[0-9]+)$', views.updateFichaView, name="update_ficha"),
    url(r'^fichas/apagar/(?P<ficha_id>[0-9]+)$', views.apagarFichaView, name="apagar_ficha"),
    url(r'^agenda$', views.agendaView, name="agenda"),
    url(r'^agenda/marcar$', views.marcarSessoesView, name="marcar_sessoes"),
    url(r'^agenda/editar/(?P<horario_id>[0-9]+)$', views.editarHorarioView, name="editar_horario"),
    url(r'^agenda/update/(?P<horario_id>[0-9]+)$', views.updateHorarioView, name="update_horario"),
    url(r'^agenda/apagar/(?P<horario_id>[0-9]+)$', views.apagarHorarioView, name="apagar_horario"),
    url(r'^teste$', views.testeView, name="pagina de teste"),

]