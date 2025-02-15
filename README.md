# DjangoProject_IHA_Uretim_Uygulamasi

Bu proje, bir IHA fabrikasında takımların parça üretimi, envanter yönetimi ve montaj süreçlerini takip etmek için geliştirilmiş bir web uygulamasıdır. Pycharm ortamında Django ve Python kullanılarak geliştirilen sistem, her takımın yalnızca kendi alanındaki parçaları üretebilmesini, envanter kontrolü yapabilmesini ve montaj ekibinin tam uçak montajını gerçekleştirmesini sağlar.

## 1. Fonksiyonalite

   ### 1.1 Personel Girişi

   Kullanıcılar sisteme kendi kimlik bilgileriyle giriş yapar.

   Kullanıcı, sistemde tanımlı olan takım bilgisine sahiptir.

   Yalnızca doğrulanmış kullanıcılar sisteme erişim sağlayabilir.

   ### 1.2 Takımlar ve Personel

   Takımlar: Kanat, Gövde, Kuyruk, Aviyonik ve Montaj olmak üzere beş ana takım bulunmaktadır.

   Takımlar yalnızca kendi alanlarındaki parçaları üretebilir (Kanat Takımı yalnızca kanat üretebilir vb.).

   ### 1.3 Parça Yönetimi

   Parça Ekleme: Takımlar, sadece kendi sorumluluk alanlarındaki parçaları üretebilir.

   Parça Listeleme: Takımlar, ürettikleri parçaları listeleyebilir.

   Parça Geri Dönüşüm: Bir parça geri dönüşüme gönderildiğinde stoktan düşürülür.

   ### 1.4 Montaj Takımı ve Uçak Üretimi

   Montaj takımı, tüm uyumlu parçaları birleştirerek uçak üretir.

   Her parça, yalnızca ait olduğu uçakta kullanılabilir (TB2 kanadı, TB3'e takılamaz).

   Montaj ekibi, üretilen uçakları listeleyebilir.

   ### 1.5 Envanter Kontrolü

   Eksik parça olduğunda sistem uyarı verir (Örneğin"Akıncı için gövde parçası eksik").

   Kullanılan parçalar stoktan düşürülür ve hangi uçakta kullanıldığı bilgisi tutulur.

## 2. Teknolojiler

   ### 2.1 Backend:
     Django (Model-View-Template (MVT) mimarisini kullanır),

     Django Rest Framework,
   
     PostgreSQL,

     Django Models (ORM (Object-Relational Mapping) kullanarak veritabanı tablolarını Python koduyla tanımlar),
   
     Django Authentication,

     Django Messages Framework,

     Django URL Mapping,

     Veritabanı İşlemleri (ORM - Django QuerySet) :Django ORM (Object-Relational Mapping), SQL sorguları yazmadan veritabanı ile etkileşim kurmayı sağlar 

   ### 2.2 Frontend:
     Html

     Tailwind CSS

     Django Template Language (DTL)(Dinamik içerik göstermek ve backend’den gelen verileri şablonda kullanmak için tercih edilir)

## 4. Ekran Görüntüleri

### Personel Giriş Sayfası
![image](https://github.com/user-attachments/assets/9cc8a1b2-8119-44e7-838a-196f3718cd77)

### Takım Dashboard Sayfası

Giriş yapan personelin bulunduğu takıma göre dashboard yüklenir. Örneğin Kanat Takımı için:
![image](https://github.com/user-attachments/assets/2fc616c2-0660-4ab8-800c-42f7bb1daafc)
Takımlar istenilen uçak için parça üretebilir. 
![image](https://github.com/user-attachments/assets/d5367a35-ca7b-41fc-835d-81bba099a4dd)

### Envanter Listesi
![image](https://github.com/user-attachments/assets/402e1874-ec4c-46f5-b772-eb39f83fd3fa)
Geri Dönüştürme İşlemi
![image](https://github.com/user-attachments/assets/92529d59-9b29-4600-bb82-17a4258b90b4)

### Montaj Takımı için Dashboard Sayfası
![image](https://github.com/user-attachments/assets/7476b67e-2a8a-45c6-9696-e1e66647824d)

### Montaj Takımı Uçak Üretme Sayfası

Eğer parça eksik ise uyarı veriliyor.
![image](https://github.com/user-attachments/assets/8609b846-ca57-49ac-9461-fa0dcb77f972)
Eğer parçalar eksik değilse uçak üretilir.
![image](https://github.com/user-attachments/assets/6214d446-4286-4271-bb35-fa8ec2e43a0f)
Tüm uçaklar ve üretilmesi için gerekli parçaları stok sayısıyla birlikte montaj takımına gösterilir
![image](https://github.com/user-attachments/assets/69cbfec8-f5f3-499f-b1e7-bc4acbfd18ab)

### Uçak Listesi

Montaj takımı tüm uçakları ve uçakların parçalarını listeleyebilir
![image](https://github.com/user-attachments/assets/096e0980-dea8-4519-94d9-d364c1f72b58)
