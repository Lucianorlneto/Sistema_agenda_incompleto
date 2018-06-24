from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm
from .models import *
from django.views import generic
from django.shortcuts import redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth.models import Group
from datetime import *
from django.http import Http404

# Create your views here.

def indexView(request):
    if request.user.is_authenticated:
        print(request.user.groups.values_list('name', flat=True))
        print(request.user.groups.filter(name='clinico').count())
        print(request.user.is_authenticated )
    return render(request, "myapp/index.html")

def cadastro_view(request):
    title = "Cadastro"
    if request.user.is_staff:
        staffForm = StaffUserRegisterForm(request.POST or None)
    else:
        form = UserRegisterForm(request.POST or None)
    usuarioform = UsuarioForm(request.POST or None)
    print(request.user.is_staff)
    for field in usuarioform:
        print(field.name)
    if request.user.is_staff:
        if staffForm.is_valid() and usuarioform.is_valid():
            user = staffForm.save(commit=False)

            password = staffForm.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            grupo = staffForm.cleaned_data.get("groups")
            print("eh staff")
            print(grupo)
            user.groups.add(grupo)
            usuario = usuarioform.save(commit=False)
            usuario.user = user
            usuario.save()

          
    else:
        if form.is_valid() and usuarioform.is_valid():
            print("entrei no bang")
            user = form.save(commit=False)

            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            print("nao eh staff")
            user.groups.add(1)
            usuario = usuarioform.save(commit=False)
            usuario.user = user
            usuario.save()

            new_user = authenticate(username=usuario.user.username, password=password)
            login(request, new_user)
            return redirect('../')

    if request.user.is_staff:
        return render(request, "myapp/form.html", {"form":staffForm, "usuarioform":usuarioform, "title":title})
    else:
        return render(request, "myapp/form.html", {"form": form, "usuarioform": usuarioform, "title": title})

def login_view(request):
    title = "Login"
    fields = ['username', 'password']
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('../')

    return render(request, "myapp/form.html", {"form":form, "title":title, "fields":fields})

def logout_view(request):
    logout(request)
    #redirect
    return redirect("../")

def criarFichaView(request):
    title = "Ficha"
    form = FichaForm(request.POST or None)
    if form.is_valid():
        ficha = form.save(commit=False)
        ficha.clinico_id = request.user
        ficha.data_criacao = date.today()
        ficha.save()

    return render(request, "myapp/form.html", {"form":form, "title":title})

def listarFichasView(request):
    title = "Fichas"
    if request.user.groups.filter(name='clinico').count():
        fichas = Ficha.objects.filter(clinico_id=request.user)
    if request.user.groups.filter(name='paciente').count():
        fichas = Ficha.objects.filter(paciente_id=request.user)
    return render(request, "myapp/listar_fichas.html", {"fichas":fichas})


def visualizarFichaView(request, ficha_id):
    title = "Visualizar"
    ficha = Ficha.objects.get(id=ficha_id)
    fichaModel = Ficha._meta.get_fields()
    print(fichaModel)

    return render(request, "myapp/visualizar_ficha.html", {"title":title, "ficha":ficha, "fichaModel":fichaModel})

def editarFichaView(request, ficha_id):
    title = "Editar"
    if request.user.groups.filter(name='paciente').count():
        raise Http404
    else:
        ficha = Ficha.objects.get(id=ficha_id)

        return render(request, "myapp/editar_ficha.html", {"title":title, "ficha":ficha})

def updateFichaView(request, ficha_id):
    ficha = Ficha.objects.get(id=ficha_id)
    ficha.observacao = request.POST['observacao']
    ficha.save()
    return redirect("../listar")

def apagarFichaView(request, ficha_id):
    title = "Deletar Ficha"
    if request.user.groups.filter(name='paciente').count():
        raise Http404
    else:
        ficha = Ficha.objects.get(id=ficha_id)
        ficha.delete()

        return redirect("../listar")



def agendaView(request):
    title = "Agenda"
    horarios = Horario.objects.all()
    for horario in horarios:
        print(horario.dataHora)
    return render(request, "myapp/agenda.html", {"title":title, "horarios":horarios})

def editarHorarioView(request, horario_id):
    title = "Editar Horario"
    horario = Horario.objects.get(id=horario_id)
    if request.user.is_authenticated:
        if request.user.groups.filter(name='paciente').count():
            if horario.paciente_id == request.user:
                return render(request, "myapp/editar_horario.html", {"title": title, "horario": horario})
            else:
                raise Http404
        else:
            return render(request, "myapp/editar_horario.html", {"title": title, "horario": horario})
    else:
        raise Http404

def updateHorarioView(request, horario_id):
    horario = Horario.objects.get(id=horario_id)
    data = datetime.strptime(request.POST['data_inicial'], "%m/%d/%Y").date()
    hora = datetime.strptime(request.POST['hora'], "%H").time()

    print(data)
    print(hora)
    dataHora = datetime.combine(data, hora)
    horario.dataHora = dataHora
    horario.save()
    return redirect("/myapp/agenda")

def apagarHorarioView(request, horario_id):
    title = "Apagar Ficha"
    horario = Horario.objects.get(id=horario_id)
    if request.user.is_authenticated:
        if request.user.groups.filter(name='paciente').count():
            if horario.paciente_id == request.user:
                horario.delete()
            else:
                raise Http404
        else:
            horario.delete()
    else:
        raise Http404
    return redirect("/myapp/agenda")

def marcarSessoesView(request):
    title = "Marcar"
    if request.user.is_authenticated:
        if request.user.groups.filter(name='paciente').count():
            form = PacienteSessoesForm(request.POST or None)
        else:
            form = SessoesForm(request.POST or None)
    if form.is_valid():
        for field in form:
            print(form.cleaned_data.get(field.name))
        sessao = form.save(commit=False)
        if request.user.groups.filter(name='paciente').count():
            sessao.paciente_id = request.user
        i=0
        j=1
        d = form.cleaned_data.get('data_inicial')
        dias = form.cleaned_data.get('dias_semana')
        hora = time(int(form.cleaned_data.get('hora')))
        print(dias)
        while i<int(form.cleaned_data.get('numero_sessoes')):
            for weekday in form.cleaned_data.get('dias_semana'):
                print(int(weekday))
                days_ahead = int(weekday) - d.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7*j
                next = d + timedelta(days_ahead)
                print(next)
                i=i+1

                dataHora = datetime.combine(next, hora)
                print(dataHora)
                sessao.pk = None
                sessao.dataHora = dataHora
                sessao.save()
            j = j + 1



    return render(request, "myapp/form.html", {"title":title, "form":form})

def testeView(request):
    return render(request, "myapp/teste.html")

