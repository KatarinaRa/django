from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .decorators import profesor_required
from django.contrib.auth import login,authenticate
from .forms import LoginForm,PredmetForm,StudentForm,ProfesorForm,UpisiForm

from app1.models import Korisnici, Predmeti, Upisi

# Views for ADMIN

@staff_member_required
def predmeti(request):
    lista_predmeta = Predmeti.objects.all()
    return render(request, 'predmeti.html',{'predmeti':lista_predmeta})

@staff_member_required
def add_predmet(request):
    if request.method == 'GET':
        form = PredmetForm()
        return render(request, 'add_predmet.html', {'form':form})
    elif request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predmeti')
        else:
            return HttpResponseNotAllowed()
        
@staff_member_required
def delete_predmet(request,predmet_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    if 'yes' in request.POST:
        predmet.delete()
    return redirect('predmeti')

    

@staff_member_required
def delete_predmetconf(request, predmet_id):
    if request.method == 'GET':
        return render(request, 'delete_predmetconf.html', {"data":predmet_id})
    return HttpResponseNotAllowed()

@staff_member_required
def edit_predmet(request,predmet_id):
    predmet = Predmeti.objects.get(id= predmet_id)
    
    if request.method=="GET":
        data = PredmetForm(instance=predmet)
        return render(request,'edit_predmet.html',{'form':data})
    elif request.method=="POST":
        data = PredmetForm(request.POST, instance=predmet)
        if data.is_valid():
            predmet.save()
            return redirect('predmeti')
    else:
        return HttpResponse("Something went wrong!")

@staff_member_required
def get_students(request):
    lista_studenata = Korisnici.objects.filter(uloga='STUDENT')
    return render(request, 'studenti.html',{'studenti':lista_studenata})

@staff_member_required
def add_students(request):
    if request.method == 'GET':
        form = StudentForm()
        return render (request, 'add_students.html',{'form': form})
    elif request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studenti')
        else:
            return render(request, 'add_students.html', {'form': form})

@staff_member_required       
def edit_students(request, student_id):           
    student = Korisnici.objects.get(id=student_id)
    
    if request.method == 'GET':
        data = StudentForm(instance=student)
        return render(request, 'edit_students.html', {'form': data})
    elif request.method == 'POST':
        data = StudentForm(request.POST, instance=student)
        if data.is_valid():
            student.save()
            return redirect('studenti')
    else:
        return render(request, 'edit_students.html')

def get_profesors(request):
    lista_profesora = Korisnici.objects.filter(uloga='PROFESOR')
    return render(request, 'profesori.html',{'profesori':lista_profesora})

def add_profesors(request):
    if request.method == 'GET':
        form = ProfesorForm()
        return render(request,'add_profesors.html',{'form':form})
    elif request.method == 'POST':
        form=ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profesors')
        else:
            return render(request,'add_profesors.html',{'form': form})

def edit_profesors(request,profesor_id):
    profesor = Korisnici.objects.get(id = profesor_id)

    if request.method == 'GET':
        data = ProfesorForm(instance = profesor)
        return render(request,'edit_profesors.html',{'form':data})
    elif request.method == 'POST':
        data = PredmetForm(request.POST, instance=profesor)
        if data.is_valid():
            data.save()
            return redirect('profesors')
        else:
            return render(request, 'edit_profesors.html',{'form':data})

def studenti_po_predmetu(request, predmet_id):
    upisi = Upisi.objects.filter(predmeti_id=predmet_id)
    return render(request, 'studenti_predmet.html', {'upisi':upisi})


#views for profesors  
@profesor_required
def predmeti_po_profesoru(request):
    predmeti = Predmeti.objects.filter(nositelj=request.user)
    return render(request, 'predmeti_profesor.html',{'predmeti': predmeti})

@profesor_required
def edit_status(request, upis_id):
    upis = Upisi.objects.get(id=upis_id)
    if request.method == 'GET':
        data = UpisiForm(instance=upis)
        return render(request, 'edit_status.html', {'form': data})
    elif request.method == 'POST':
        data = UpisiForm(request.POST, instance=upis)
        if data.is_valid():
            upis.save()
            return redirect('predmet_profesor')
    else:
        return render(request, 'edit_status.html',{'form': data})
    
@staff_member_required
def upisni_list_admin(request,student_id):
    korisnik = Korisnici.objects.get(id=student_id)
    if request.method == "GET":
        upisi = Upisi.objects.filter(korisnici=korisnik)
        sviPredmeti = Predmeti.objects.all()
        predmeti = [p for p in sviPredmeti if not upisi.filter(predmeti=p)]
        return render(request, 'upisni_list.html', {'upisi': upisi, 'predmeti': predmeti, 'student': korisnik})
    
    if request.method == "POST":
        data = request.POST
        if data.get("upisi"):
            predmet_id = data.get("upisi")
            predmet = Predmeti.objects.get(id=predmet_id)
            if predmet.sem_redovni in [5, 6] and check(korisnik):
                return HttpResponse("Ne moze se upisati predmet sa 3. godine")
            upis = Upisi(korisnici=korisnik, predmeti=predmet, status='UPISAN')
            upis.save()
            return redirect('upisni_list',student_id=student_id)
        
        if data.get("ispisi"):
            upis_id = data.get("ispisi")
            upis = Upisi.objects.get(id=upis_id)
            if upis.status in [Upisi.POLOZEN, Upisi.IZGUBIO_POTPIS]:
                return HttpResponse("Predmet se ne moze ispisati")
            upis.delete()
            return redirect('upisni_list',student_id=student_id)
        
        if data.get("polozen"):
            upis_id = data.get("polozen")
            upis = Upisi.objects.get(id=upis_id)
            upis.status = Upisi.POLOZEN
            upis.save()
            return redirect('upisni_list',student_id=student_id)


#views for students
@login_required
def upisni_list(request):
    korisnik = Korisnici.objects.get(id=request.user.id)
    if request.method == "GET":
        upisi = Upisi.objects.filter(korisnici=korisnik)
        sviPredmeti = Predmeti.objects.all()
        predmeti = [p for p in sviPredmeti if not upisi.filter(predmeti=p)]
        return render(request, 'upisni_list.html', {'upisi': upisi, 'predmeti': predmeti, 'student': korisnik})
    
    if request.method == "POST":
        data = request.POST
        if data.get("upisi"):
            predmet_id = data.get("upisi")
            predmet = Predmeti.objects.get(id=predmet_id)
            if predmet.sem_redovni in [5, 6] and check(korisnik):
                return HttpResponse("Ne moze se upisati predmet sa 3. godine")
            upis = Upisi(korisnici=korisnik, predmeti=predmet, status='UPISAN')
            upis.save()
            return redirect('upisni_list')
        
        if data.get("ispisi"):
            upis_id = data.get("ispisi")
            upis = Upisi.objects.get(id=upis_id)
            if upis.status in [Upisi.POLOZEN, Upisi.IZGUBIO_POTPIS]:
                return HttpResponse("Predmet se ne moze ispisati")
            upis.delete()
            return redirect('upisni_list')
        
        if data.get("polozen"):
            upis_id = data.get("polozen")
            upis = Upisi.objects.get(id=upis_id)
            upis.status = Upisi.POLOZEN
            upis.save()
            return redirect('upisni_list')
        
def check(korisnik):
    predsem1 = Predmeti.objects.filter(sem_redovni=1)
    predsem2 = Predmeti.objects.filter(sem_redovni=2)
    upisi = Upisi.objects.filter(korisnici=korisnik)

    
    if not all(Upisi.objects.filter(korisnici=korisnik, predmeti=p) for p in predsem1):
        return True

    
    if not all(Upisi.objects.filter(korisnici=korisnik, predmeti=p) for p in predsem2):
        return True
    
    if any(u.predmeti.sem_redovni in [1, 2] and u.status != 'POLOZEN' for u in upisi):
        return True

    return False

#OTHER
def home(request):
    return render(request,'home.html')


def logIn(request):
    error = False
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password = password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})

#prikazati imena svih predmeta koji imaju preko x bodova
@login_required
def filtriranje(request):
    predmeti = Predmeti.objects.all()
    bodovi = None

    if request.method == 'POST':
        bodovi = int(request.POST.get('bodovi'))

    filtrirani_predmeti = []

    for predmet in predmeti:
        if bodovi is not None and predmet.bodovi > bodovi:
            filtrirani_predmeti.append(predmet)

    context = {
        'predmeti': filtrirani_predmeti,
        'bodovi': bodovi
    }

    return render(request, 'filtiranje.html', context)
 

#prikazati imena svih predmeta koji pripadaju semestru x
@login_required
def filtriranje1(request):
    if request.method == 'POST':
        semestar = int(request.POST.get('semestar'))
        predmeti = Predmeti.objects.filter(sem_redovni=semestar) | Predmeti.objects.filter(sem_izvanredni=semestar)  
    else:
        predmeti = Predmeti.objects.all()

    data = {
        'predmeti':predmeti
    }
    return render(request, 'filtriranje1.html', data)

#prikazati imena predmeta koji imaju preko x bodova i pripadaju semestru x

def prikazi_predmete(request):
    predmeti = Predmeti.objects.all()
    minimalni_bodovi = None
    semestar = None

    if request.method == 'POST':
        minimalni_bodovi = int(request.POST.get('minimalni_bodovi'))
        semestar = int(request.POST.get('semestar'))

    filtrirani_predmeti = []

    for predmet in predmeti:
        if minimalni_bodovi is not None and semestar is not None:
            if predmet.bodovi > minimalni_bodovi and (predmet.sem_redovni == semestar or predmet.sem_izvanredni == semestar):
                filtrirani_predmeti.append(predmet)
        else:
            filtrirani_predmeti.append(predmet)

    context = {
        'predmeti': filtrirani_predmeti,
        'minimalni_bodovi': minimalni_bodovi,
        'semestar': semestar
    }

    return render(request, 'prikaz_predmeta.html', context)

                    
                
            





