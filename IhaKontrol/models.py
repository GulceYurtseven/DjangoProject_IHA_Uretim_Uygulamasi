#models.py database de olması gereken tabloların tutlduğu yer
from django.contrib.auth.models import User
from django.db import models
#Takımların bulunduğu tablo
class Team(models.Model):
    PART_TYPES = [
        ("Kanat", "Kanat Takımı"),
        ("Gövde", "Gövde Takımı"),
        ("Kuyruk", "Kuyruk Takımı"),
        ("Aviyonik","Aviyonik Takımı"),
        ("Montaj", "Montaj Takımı"),
    ]  #Her takım kendi alanında parça ürettiği için part_type yazıldı

    name = models.CharField(max_length=80)
    default_part_type = models.CharField(max_length=80, choices=PART_TYPES, null=True, blank=True)
    def __str__(self):
        return self.name

#Pesonellerin ve hangi takıma ait olduklarını tutan tablo
#Bir takımda birden fazla personel olabilir.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.team}"

#Uçakların tutulduğu tablo
class Aircraft(models.Model):
    AIRCRAFT_CHOICES = [
        ("TB2", "tb2"),
        ("TB3", "tb3"),
        ("AKINCI", "akıncı"),
        ("KIZILELMA", "kızılelma"),
    ]

    name = models.CharField(max_length=20, choices=AIRCRAFT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

#Uçak parçalarının tutulduğu tablo
class Part(models.Model):
    PART_CHOICES = [
        ("KANAT", "Kanat"),
        ("GOVDE", "Gövde"),
        ("KUYRUK", "Kuyruk"),
        ("AVIYONIK", "Aviyonik"),
    ]
    # Her parçanın bir uçağa ait olduğunu belirle.
    name = models.CharField(max_length=20, choices=PART_CHOICES)
    # Her parça ilgili uçağa ait (Her parça uçağa özeldir TB2 kanadı TB3 kanadına takılamaz) bu nedenle foreign key ile ilgili uçak tutuluyor
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)  # Parçanın stok durumu
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True) #Parçayı hangi takım ürettiği

    def __str__(self):
        return f"{self.get_name_display()} - {self.aircraft}"

#Montaj takımının bütün uyumlu parçaları birleştirerek 1 uçak üretmesi gerekmektedir. Üretilen uaçkalrın tutulduğu tablo
class Aircraft_produced(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE) #Üretilen uçak
    parts_used = models.ManyToManyField(Part)  # Üretilen uçakta kullanılan parçalar

    def __str__(self):
        return f"{self.aircraft} Montajı"

