from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Part, Aircraft, Aircraft_produced
from django.contrib.auth.decorators import login_required

# personel girişi
def login_view(request):
    print("Login fonksiyonu çalıştı")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print("Giren kullanıcı", username, password) #konsolda kontrol etmek için yazdım
                user_team = request.user.profile.team
                return redirect("dashboard")  # Giriş başarılıysa dashboard’a yönlendir
            else:
                messages.error(request, "Hatalı giriş!")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

#personel çıkışı
def logout_view(request):
    print("Logout fonksiyonu çalıştı")
    logout(request)
    return redirect("login")

#Login Required Django'da belirli görünümleri korumanıza ve yalnızca kimliği doğrulanmış kullanıcıların bunlara erişebilmesini sağlamanıza olanak tanıyan temel bir özelliğidir
#bu nedenle giriş yaptıktan sonraki işlemlerde login required kullandım
@login_required
def dashboard(request):
    print("Dashboard fonksiyonu çalıştı")
    #Personelin takımını al
    user_team = request.user.profile.team.name

    if user_team != "Montaj":
        parts = Part.objects.all()
        aircrafts = Aircraft.objects.all()
    else:
        parts = Part.objects.filter(name=user_team)
        aircrafts = None
    #dashboar.html e gerekli verileri gönderdim böylece giriş yapan personel verileri ekrande görebildi.
    return render(request, "dashboard.html", {"parts": parts, "aircrafts": aircrafts, "team": user_team})

#-----------------------------------------------------------------------

#Takımların kendi parçalarını üretme, listeleme ve geri dönüşüme gönderme işlemleri olmalı (CRUD) Not: geri dönüşüm ‘delete’ anlamındadır.
#Parça üretme
@login_required
def stock_change(request):
    print("Stock Change fonksiyonu çalıştı")
    #Personelin takımını al
    user_team = request.user.profile.team
    #Takıma uygun olan parça türünü al (kanat,gövde,aviyonik,kuyruk) modelde belirtilen, takımlara uygun parça türleri
    #Takımlar kendi sorumluluğundan başka parça üretemez. (Örn: Aviyonik takımı kuyruk üretemez.)
    part_type = user_team.default_part_type

    if request.method == "POST":
        aircraft_id = request.POST.get('aircraft')  #Formdan seçilen uçağın ID'si al
        #Seçilen uçağa ait bilgiyi al
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
            print(f"Uçak bulundu: {aircraft.name}")

            #Parça oluştur veya mevcutsa al
            part, created = Part.objects.get_or_create(
                name=part_type,
                aircraft=aircraft,
                team=user_team,
                defaults={'stock': 0}
            )
            #Stok sayısını artır
            part.stock += 1
            try:
                part.save()
                print(f"Yeni Stok Durumu: {part.stock}")
            except Exception as e:
                print(f"Veritabanına kaydetme hatası: {e}")
                messages.error(request, f"Veritabanına kaydedilemedi: {e}")
                return redirect('dashboard')

            #Eğer database e kaydedildiyse başarı mesajı
            messages.success(request, f"{aircraft.name} için {part.get_name_display()} üretildi. Yeni stok: {part.stock}")

        except Aircraft.DoesNotExist:
            messages.error(request, "Geçersiz uçak seçimi.")
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f"Bir hata oluştu: {str(e)}")
            return redirect('dashboard')

    aircrafts = Aircraft.objects.all() #Eğer get isteği varsa uçakları databaseden çek
    part_choices = [part_type] #Takımın parçasına göre uygun parça türü

    #dashboard.html e verileri gönderme.
    return render(request, 'dashboard.html', {'aircrafts': aircrafts, 'part_choices': part_choices})

#Parça listeleme
@login_required
def list_team_parts(request):
    user_team = request.user.profile.team #Personelin takımı
    parts = Part.objects.filter(team=user_team) #Takımına ait parçaları listele
    #Verileri team_parts.html e gönder
    return render(request, "team_parts.html", {"parts": parts, "team": user_team})

#Perça geri dönüştürme
@login_required
def recycle_part(request, part_id):
    user_team = request.user.profile.team #Personelin takımını al

    try:
        part = Part.objects.get(id=part_id, team=user_team) #Personelin takımına ait parçayı getir

        if part.stock > 1:
            part.stock -= 1  #Stoktan 1 düş
            part.save()

    except Part.DoesNotExist:
        messages.error(request, "Geri dönüşüme göndermek istediğiniz parça bulunamadı.")
    #Personeli takımın parça listesine yönlendir
    return redirect("list_team_parts")

#----------------------------------------------------------------------

#Uçak üretme (Montaj takımının bütün uyumlu parçaları birleştirerek 1 uçak üretmesi gerekmektedir.)
@login_required
def aircraft_assemble(request):
    print("Uçak montajı başlatıldı")
    user_team = request.user.profile.team #Personelin takımını al

    if user_team.name == "Montaj": #Sadece montaj takımı uraç üretebilir
        if request.method == "POST":
            aircraft_id = request.POST.get('aircraft')

            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
                #Uçak için tüm gerekli parçalar için bi liste
                required_part_types = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]
                #Her parça tipi için stok kontrolü yap
                missing_parts = []
                available_parts = []

                for part_type in required_part_types:
                    part = Part.objects.filter(
                        aircraft=aircraft,
                        name=part_type,
                        stock__gt=0 #Stok 0'dan büyük olmalı
                    ).first()

                    if part:
                        available_parts.append(part) #Eksik olmayan parçaları listeye ekle
                    else:
                        missing_parts.append(part_type) #Eksik parçaları listeye ekle

                #Eksik parça var mı kontrol et personele eksik parçaları bildirir.(Envanterde eksik parça olduğunda uyarı vermelidir (Örn: Akıncı için gövde parçası eksik))
                if missing_parts:
                    missing_parts_display = [
                        dict(Part.PART_CHOICES).get(part, part) for part in missing_parts
                    ]
                    messages.error(request, f"Üretim için gerekli parçalar eksik: {', '.join(missing_parts_display)}")
                    return redirect('aircraft_assemble')

                #Tüm parçalar mevcutsa üretim gerçekleşir
                #1 uçakta kullanılan parça başka uçakta kullanılamaz, stok sayısından azaltılmalıdır.
                for part in available_parts:
                    part.stock -= 1
                    part.save()

                # Yeni üretilen uçağı database e kaydet
                #Uçaklar için bütün parçaları oluşturup monte ettikten sonra kullanılan parçaların sayısını ve hangi uçakta kullanıldığının bilgisi tutulmalıdır.
                aircraft_produced = Aircraft_produced.objects.create(aircraft=aircraft)
                aircraft_produced.parts_used.set(available_parts)
                aircraft_produced.save()

                messages.success(request, f"{aircraft.name} başarıyla üretildi!")

            except Aircraft.DoesNotExist:
                messages.error(request, "Seçilen uçak bulunamadı.")
                return redirect('aircraft_assemble')

            except Exception as e:
                messages.error(request, f"Bir hata oluştu: {str(e)}")
                return redirect('aircraft_assemble')

        aircrafts = Aircraft.objects.all()#Eğer get isteği varsa uçakları databaseden çek
        #Verileri aircraft_assemble.html e gönder
        return render(request, 'aircraft_assemble.html', {'aircrafts': aircrafts})

    else:
        messages.error(request, "Bu işlem için yetkiniz yok!")
        return redirect('dashboard')

#Montaj takımı üretilen uçakları listeleyebilir.
@login_required
def list_aircraft(request):
    user_team = request.user.profile.team #Personelin takımını al
    if user_team.name == "Montaj": #Personelin takımı montaj ise
        aircrafts = Aircraft_produced.objects.all()
        print("Üretilen uçaklar:", aircrafts) #Debug için
        #Verileri aircraft_list.html e gönder
        return render(request, "aircraft_list.html", {"aircrafts": aircrafts})
    else:
        messages.error(request, "Bu sayfaya erişim izniniz yok.")
        return redirect("dashboard")