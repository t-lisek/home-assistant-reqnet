# REQNET API Reference

Source: https://portal.inprax.pl/REQNET/OpisyAPI_REQNET?ID_TYPU=9

---

## API

**Description:** Funkcja zwraca podstawowe informacje o urządzeniu np. MAC , status podłączenia do WIFI oraz MQTT, numer wersji oprogramowania dla modułu WIFI oraz płyty itp.

**Parameters:**
```
brak
```

**Result:**
```
{
 "APIResult": true,
 "MAC": "CC:50:E3:CD:CB:CB",
 "Status": "true",
 "MQTTStatus": false,
 "WIFIStatus": "false",
 "WIFISSID": "",
 "APSSID": "reqnetCC:50:E3:CD:CB:CB",
 "UpdateFirmwareStatus": 0,
 "Mode": 1,
 "UpdateToVersion": 0,
 "RecuperatorSoftwareVersion": "6.26",
 "APIVersion": 19,
 "AvailableHeapSize": 17208,
 "TotalProgramSize": 2445312,
 "ProgramSize": 698080,
 "DeviceType": 8,
 "WIFIIP": "192.168.7.1",
 "WIFISignalStrength": 5,
 "LogMode": 0
}
APIResult - wynik wykonania , true - prawidłowy , false - nieprawidłowy
MAC - MAC urządzenia (modułu WIFI)
Status - status urządzenia , true - włączony , false - wyłączony
MQTTStatus status podłączenia do brokera MQTT , tru - połączony, false - nie połączony
WIFIStatus status podłączenia urządzenia do sieci domowej/firmowe , true - połączony, false - nie połączony
WIFISSID nazwa sieci WIFI
APPSSID nazwa sieci (widoczność urządzenia) w momencie braku podłączenia do sieci WiFi domowej/firmowej
UpdateFirmwareStatus wartość wykorzystywana wewnętrznie
Mode tryb pracy modułu Wifi
UpdateToVersion wartość wykorzystywana wewnętrznie
RecuperatorSoftwareVersion wersja oprogramowania sprzętowego
APIVersion wersja modułu Wifi
AvailableHeapSize wartość wykorzystywana wewnętrznie
TotalProgramSize wartość wykorzystywana wewnętrznie
ProgramSize wartość wykorzystywana wewnętrznie
DeviceType typ urządzenia (model)
WIFIIP adres IP urządzenia
WIFISignalStrength siła sygnału w sakli od 1-6
LogMode wartość wykorzystywana wewnętrznie
```

**HTTP:** `GET /API/RunFunction?name=API`

---

## AutomaticMode

**Description:** Włącza tryb inteligentny w urządzeniu

**Parameters:**
```
brak
```

**Result:**
```
{ AutomaticModeResult : true, Message : ""}
AutomaticModeResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=AutomaticMode`

---

## BlinkDiode

**Description:** Funkcja pozwala na uruchomienie mrugania diodą (wykorzystywane np. przy aktualizacji modułu Wifi).

**Parameters:**
```
active - 1 włącz, 0 - wyłącz
```

**Result:**
```
{ BlinkDiodeResult: true, Message : ""}
BlinkDiodeResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=BlinkDiode`

---

## ChangeAdditionalBrokerConfiguration

**Description:** Konfiguracja dodatkowego brokera MQTT

**Parameters:**
```
MQTT_ADDITIONAL_BROKER_ADDRESS - adres dodatkowego brokera MQTT
MQTT_ADDITIONAL_BROKER_PORT - port dodatkowego brokera MQTT
MQTT_ADDITIONAL_BROKER_USER - użytkownik brokera
MQTT_ADDITIONAL_BROKER_PASSWORD - hasło brokera
```

**Result:**
```
{"ChangeAdditionalBrokerConfigurationResult":true,"Message":""}

ChangeAdditionalBrokerConfigurationResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ChangeAdditionalBrokerConfiguration`

---

## ChangeConfiguration

**Description:** Funkcja pozwala na zmianę konfiguracji sieci WIFI i podłączenie do istniejącej sieci (sieć domowa, firmowa) lub uruchomienie urządzenia w trybie HotSpot.
Po wywołaniu funkcji urządzenie wgrywa odpowiednią konfigurację i uruchamia się w odpowiednim trybie (może to potrwać od 30-60 sekund)

**Parameters:**
```
Client_SSID - identyfikator sieci WIFI jeśli chcemy się podłączyć do istniejącej sieci
Client_PASS - hasło do sieci WIFI
```

**Result:**
```
{ ChangeConfigurationResult : true, Message : ""}
ChangeConfigurationResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ChangeConfiguration`

---

## ChangeTheStatusOfTheDevice

**Description:** Funkcja pozwalająca zmienić status urządzenia (włączyć, wyłączyć)

**Parameters:**
```
state - status urządzenia 1 - aktywny, 0 - nieaktywny
device - numer urządzenia od 1-13
```

**Result:**
```
{ ChangeTheStatusOfTheDeviceResult : true, Message : ""}
ChangeTheStatusOfTheDeviceResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ChangeTheStatusOfTheDevice`

---

## ChangeWifiPass

**Description:** Funkcja pozwala zmienić hasło dla trybu HotSpot (sieć REQNET) - domyślnie jest to 00000000

**Parameters:**
```
AP_PASS - hasło do sieci Reqnet
```

**Result:**
```
uzupełnić
```

**HTTP:** `GET /API/RunFunction?name=ChangeWifiPass`

---

## ConfigurationForTemporaryWorkModes

**Description:** Funkcja pozwala ustawić niezbędne współczynniki dla trybów nadrzędnych np. kominek, oczyszczanie itp. Aby zmienić któryś ze współczynników nie trzeba w parametrach podać wszystkich wystarczy ten który chcemy zmienić, reszta pozostanie bez zmian.

**Parameters:**
```
Wszystkie współczynniki podaje się jako % w stosunku do maksymalnej wydajności urządzenia w m3/h.
factorforthefastheating - współczynnik wydajności dla funkcji szybkiego grzania 
factorforthefastcooling - współczynnik wydajności dla funkcji szybkiego chłodzenia 
factorfortheholiday - współczynnik wydajności dla funkcji URLOP 
factorfortheventilation- współczynnik wydajności dla funkcji PRZEWIETRZANIE 
factorforthecleaning - współczynnik wydajności dla funkcji CZYSZCZENIE 
factorforthefireplace - współczynnik wydajności dla funkcji KOMINEK 
factorforthealarmcontrolpanel - współczynnik wydajności dla współpracy z centralka alarmową 
factorfortheventilationhood- współczynnik wydajności dla współpracy z okapem (nawiew) 
factorfortheextractorhood- współczynnik wydajności dla współpracy z okapem (wywiew) 
factorfortheopenwindow - współczynnik wydajności dla współpracy z kontaktronem otwartego okna 
factorforthehypertension - współczynnik nadciśnienia nawiewu względem wyciągu (o ile procent wartości nawiewu ma być zmniejszony i ustawiony wyciąg) domyślna wartość to 30% 
temp1 - Temperatura zabezpieczenia przed wychłodzeniem nr 1 (odnosi się do algorytmu obsługi błędu nr 9) 
temp2 - Temperatura zabezpieczenia przed wychłodzeniem nr 2 (odnosi się do algorytmu obsługi błędu nr 9)
```

**Result:**
```
{ ConfigurationForTemporaryWorkModesResult: true, Message : ""}
ConfigurationForTemporaryWorkModesResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ConfigurationForTemporaryWorkModes`

---

## CurrentWorkParameters

**Description:** Funkcja zwraca bieżące parametry pracy urządzenia

**Parameters:**
```
brak
```

**Result:**
```
{"CurrentWorkParametersResult":true,"Values":[1,300,22.2,90,90,100,100,43,500,0,8,0,0,0,0,4,80,80,25,100,80,100,20,70,30,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22.5,22.3,22.2,22.5,0.0,0.0,0.0,0.0,30,40,24,25,22,0,3,2,0,0,0,0,20,25,0,0,0,0,12,13,89,540,530,0,87,95,41,7,13,30,29,0,0,0,0,0,60000,12936]}
CurrentWorkParametersResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
Znaczenie poszczególnych wartości w Values w kolejności :
1.Status urządzenia - 1 - włączone , 0 - wyłączone
2.Maksymalna wartość nawiewu wyrażona w m3/h
3.Aktualna temperatura wyrażona w °C
4.Aktualna wartość nawiewu wyrażona w m3/h
5.Aktualna wartość wyciągu wyrażona w m3/h
6.Aktualna ustawiona wartość nawiewu w trybie ręcznym wyrażona w m3/h
7.Aktualna ustawiona wartość wyciągu w trybie ręcznym wyrażona w m3/h
8.Aktualna wilgotność powietrza
9.Aktualna wartość stężenia CO2 wyrażona w ppm
10.Status funkcji harmonogram - 1 - aktywna, 0 - nieaktywna
11.Aktualny tryb pracy urządzenia :
1 - szybkie grzanie
2 - szybkie chłodzenie
3 - urlop 
4 - przewietrzanie
5 - oczyszczanie
6 - kominek 
8 - tryb ręczny
9 - tryb inteligentny
10 - tryb pomiaru wydajności
12.Funkcja nadrzędna pozostały czas do zakończenia minuty
13.Funkcja nadrzędna pozostały czas do zakończenia sekundy
14.Status funkcji uruchomionej równoległe (grzanie, chłodzenie) :
0 - nieaktywna
1 - grzanie
2 - chłodzenie
15.Ilość dni w trybie urlop pozostałych do jego zakończenia
16.Model urządzenia - wartości w zakresie od 1-9
17.Współczynnik wydajności dla funkcji Szybkie grzanie wyrażony w % do maksymalnej wydajności
18.Współczynnik wydajności dla funkcji Szybkie wyrażony w % do maksymalnej wydajności
19.Współczynnik wydajności dla funkcji Urlop wyrażony w % do maksymalnej wydajności
20.Współczynnik wydajności dla funkcji Przewietrzanie wyrażony w % do maksymalnej wydajności
21.Współczynnik wydajności dla funkcji Oczyszczanie wyrażony w % do maksymalne
```

**HTTP:** `GET /API/RunFunction?name=CurrentWorkParameters`

---

## DeleteErrorLog

**Description:** Funkcja pozwalająca usunąć dziennik błędów urządzenia

**Parameters:**
```
brak
```

**Result:**
```
{ DeleteErrorLogResult : true, Message : ""}
DeleteErrorLogResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=DeleteErrorLog`

---

## DeleteSchedulePositions

**Description:** Funkcja pozwalająca usunąć wszystkie pozycje zdefiniowane w harmonogramie.

**Parameters:**
```
brak
```

**Result:**
```
{ DeleteSchedulePositionsResult: true, Message : ""}
DeleteSchedulePositionsResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=DeleteSchedulePositions`

---

## GetTemperatures

**Description:** Funkcja zwracająca temp. z wszystkich czujników

**Parameters:**
```
brak
```

**Result:**
```
{"GetTemperaturesResult":true,"Intake":"23.4","Launcher":"23.4","Supply":"23.1","Extract":"23.4","HeaterCooler":"0.0","HeaterCoolerActive":0,"GWC":"0.0","GWCActive":0,"Room":"0.0","RoomTempActive":0,"Additional":"0.0","AdditionalTempActive":0}

GetTemperaturesResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
Intake - temperatur na czerpni wyrażona w °C
Launcher- temperatur na wyrzutni wyrażona w °C
Supply- temperatur nawiewu wyrażona w °C
Extract - temperatur wyciągu wyrażona w °C
HeaterCooler - temperatura na czujniku kanałowym za nagrzewnicą/chłodnicą wyrażona w °C
GWC - temperatur GWC wyrażona w °C
Room - temperatura z czujnika pokojowego wyrażona w °C
Additional - temperatura z czujnika dodatkowego wyrażona w °C
AdditionalTempActive - status dodatkowego czujnika (podłączony 1 , nie podłączony 0)
RoomTempActive - status dodatkowego czujnika pokojowego (podłączony 1, nie podłączony 0)
GWCActive- status czujnika GWC (podłączony 1, nie podłączony 0)
```

**HTTP:** `GET /API/RunFunction?name=GetTemperatures`

---

## GetTheListOfDevicesWithStatus

**Description:** Funkcja zwracająca statusy urządzeń od 1-13

**Parameters:**
```
brak
```

**Result:**
```
{"GetTheListOfDevicesWithStatusResult":true,"DeviceStatus1":0,"DeviceStatus2":0,"DeviceStatus3":0,"DeviceStatus4":0,"DeviceStatus5":0,"DeviceStatus6":0,"DeviceStatus7":0,"DeviceStatus8":0,"DeviceStatus9":0,"DeviceStatus10":0,"DeviceStatus11":0,"DeviceStatus12":0,"DeviceStatus13":0}

GetTheListOfDevicesWithStatusResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
DeviceStatus1 - status urządzenia 1 (1 - aktywne, 0 - nieaktywne)
DeviceStatus2 - status urządzenia 2 (1 - aktywne, 0 - nieaktywne)
DeviceStatus3 - status urządzenia 3 (1 - aktywne, 0 - nieaktywne)
DeviceStatus4 - status urządzenia 4 (1 - aktywne, 0 - nieaktywne)
DeviceStatus5 - status urządzenia 5 (1 - aktywne, 0 - nieaktywne)
DeviceStatus6 - status urządzenia 6 (1 - aktywne, 0 - nieaktywne)
DeviceStatus7 - status urządzenia 7 (1 - aktywne, 0 - nieaktywne)
DeviceStatus8 - status urządzenia 8 (1 - aktywne, 0 - nieaktywne)
DeviceStatus9 - status urządzenia 9 (1 - aktywne, 0 - nieaktywne)
DeviceStatus10 - status urządzenia 10 (1 - aktywne, 0 - nieaktywne)
DeviceStatus11 - status urządzenia 11 (1 - aktywne, 0 - nieaktywne)
DeviceStatus12 - status urządzenia 12 (1 - aktywne, 0 - nieaktywne)
DeviceStatus13 - status urządzenia 13 (1 - aktywne, 0 - nieaktywne)
```

**HTTP:** `GET /API/RunFunction?name=GetTheListOfDevicesWithStatus`

---

## GetTheListOfMessages

**Description:** Funkcja zwraca dziennik błędów (maksymalnie 15 pozycji)

**Parameters:**
```
brak
```

**Result:**
```
{"GetTheListOfMessagesResult":true,"Bytes":8,"Rows":1,"0":[14,16,7,11,3,20]}
GetTheListOfMessagesResult- wynik wywołania metody
Bytes - ilość bajtów informacyjnie
Rows - ilość pozycji
"0" : numer wiersza od 0-14
[14 - kod błędu ,16 - godzina ,7 - minuta ,11 - dzień ,3 - miesiąc ,20 -rok]
```

**HTTP:** `GET /API/RunFunction?name=GetTheListOfMessages`

---

## GetTheListOfSchedules

**Description:** Funkcja zwracająca listę stref czasowych zaprogramowanych w harmonogramie.

**Parameters:**
```
brak
```

**Result:**
```
{"GetTheListOfSchedulesResult":true,"Bytes":10,"Rows":1,"0":[1,5,8,0,16,0,300,22]}
GetTheListOfSchedulesResult- wynik wywołania metody
Bytes - ilość bajtów
Rows - ilość pozycji
"0": numer strefy czasowej
[
1 - początkowy dzień tygodnia 1 = pon, 2 = wt. itd do 7= niedziela 
5 - końcowy dzień tygodnia 1 = pon, 2 = wt. itd do 7= niedziela ,
8 - godz. rozpoczęcia
0 - minuta rozpoczęcia,
16 - godzina zakończenia ,
0 - minuta zakończenia ,
300 - wydajność w m3/h,
22 - temperatura komfortu wyrażona w °C
]
```

**HTTP:** `GET /API/RunFunction?name=GetTheListOfSchedules`

---

## GetWorkParameters

**Description:** Funkcja zwraca zaawansowane ustawienia urządzenia

**Parameters:**
```
brak
```

**Result:**
```
{"GetWorkParametersResult":true,"Values":[300,3,10,4,3,2,1,0,200,300,400,500,600,700,800,0,2,2,2,7,10,25,5,7,20,3,5,15,20,40,100,50,15,25,5,2,25,5,2,0,22,300,10,90,170,14,10]}
GetWorkParametersResult - wynik wywołania metody
Values - macierz za ze zwrotką parametrów w kolejności :
0-nastawa poziomu CO2 (wartość w ppm od 500 do 900ppm )
1 -poziom czułości CO2 zakres od 10-50 ppm
2 -histereza_CO2 - różnica między poziomem załączenia i wyłączenia dla każdego z siedmiu progów wydajności/stężeń CO2 w trybie auto 
(zakres od 10-200 ppm)
3 - pierwszy poziom czułości (zakres od 0-200 ppm)
4 - drugi poziom czułości (zakres od 0-200 ppm)
5 - trzeci poziom czułości (zakres od 0-200 ppm)
6 - czwarty poziom czułości (zakres od 0-200 ppm)
7 - piąty poziom czułości (zakres od 0-200 ppm)
8 - współczynnik delta 1 progu 
9 - współczynnik delta 2 progu
10 - współczynnik delta 3 progu
11 - współczynnik delta 4 progu
12 - współczynnik delta 5 progu
13 - współczynnik delta 6 progu
14 - współczynnik delta 7 progu
15- aktywacja funkcji higro (0 - nieaktywna, 1 - aktywna)
16 - czułość funkcji HIGRO (zakres 1-3)
17 - wartość czasu podawaną w godzinach do obliczeń średniej wartości wilgotności z tego właśnie okresu. Wysyłając 3 ustawiamy, że parametr liczy 
średnią wilgotność z ostatnich 3
godzin. Zakres nastaw: od 1 do 6
18 - różnica między poziomem załączenia i wyłączenia dla każdego
z trzech progów wilgotności w trybie auto (wartość w % - wysyłając 3 ustawiamy
histerezę równą 3%). Dozwolone wartości: od 3 do 10
19- współczynnik korekcyjny 1 progu wilgotności dla niskiej czułości
20- współczynnik korekcyjny 2 progu wilgotności dla niskiej czułości
21- współczynnik korekcyjny 3 progu wilgotności dla niskiej czułości
22- współczynnik korekcyjny 1 progu wilgotności dla średniej czułości
23- współczynnik korekcyjny 2 progu wilgotności dla średniej czułości
24- współczynnik korekcyjny 3 progu wilgotności dla średniej czułości
25-współczynnik korekcyjny 1 progu wi
```

**HTTP:** `GET /API/RunFunction?name=GetWorkParameters`

---

## MacAddress

**Description:** Funkcja zwracająca MAC adres urządzenia (modułu Wifi)

**Parameters:**
```
brak
```

**Result:**
```
{"MacAddressResult":true,"MAC":"CC:50:E3:CD:CB:CB"}
MacAddressResult- wynik wywołania metody
MAC - MAC adres urządzenia
```

**HTTP:** `GET /API/RunFunction?name=MacAddress`

---

## ManualMode

**Description:** Funkcja pozwala na przełączenie urządzenia w tryb ręczny , w którym użytkownik może zadecydować wydajności urządzenia

**Parameters:**
```
airflowvalue - zadana wartość nawiewu 
valueofairextraction- zadana wartość wyciagu
```

**Result:**
```
{ ManualModeResult: true, Message : ""}
ManualModeResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ManualMode`

---

## ReplaceFilters

**Description:** Funkcja resetująca licznik wymiany filtrów (ustawiająca odliczanie na nowo)

**Parameters:**
```
brak
```

**Result:**
```
{ ReplaceFiltersResult: true, Message : ""}
ReplaceFiltersResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=ReplaceFilters`

---

## SetByPassMode

**Description:** Funkcja pozwala na przestawienie ByPassu na jeden z 3 trybów otwarty, zamknięty i automatyczny

**Parameters:**
```
mode - tryb ByPass'u :
0 - zamknięty
1 - otwarty
2 - automatyczny
```

**Result:**
```
{ SetByPassModeResult : true, Message : ""}
SetByPassModeResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetByPassMode`

---

## SetComfortTemperature

**Description:** Funkcja pozwala na zmianę temperatury komfortu

**Parameters:**
```
temperature - temperatura komfortu w zakresie od 10-35 stopni
```

**Result:**
```
{ SetComfortTemperatureResult: true, Message : ""}
SetComfortTemperatureResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetComfortTemperature`

---

## SetDateTime

**Description:** Funkcja pozwala na zmianę daty i czasu w urządzeniu. Data i czas muszą zostać ustawione dla prawidłowego działania większości funkcji np. wietrzenie, oczyszczanie, wymiana filtrów itp.

**Parameters:**
```
hour - godzina (0-23)
min - minuta (0-59)
sec - sekunda (0-59)
year - rok (dwie cyfry dla 2019 - 19)
month - miesiąc (1-12)
day - dzień (1-31)
weekday - dzień tygodnia :
1-poniedziałek
2-wtorek
3-środa
4-czwartek
5-piątek
6-sobota
7-niedziela
```

**Result:**
```
{ SetDateTimeResult: true, Message : ""}
SetDateTimeResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetDateTime`

---

## SetFiltersParameters

**Description:** Funkcja pozwala ustawić parametry związane z wymianą filtrów

**Parameters:**
```
daysbefore - liczba opisująca na ile dni przed ostateczną wymianą ma się pokazać alert "niedługo należy wymienić filtry" 
messagefrequency- liczba opisująca co ile dni ma się pokazać alert "wymień filtry" -> do tej wartości przeładowuje się licznik filtrów
```

**Result:**
```
{ SetFiltersParametersResult: true, Message : ""}
SetFiltersParametersResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetFiltersParameters`

---

## SetGWCMode

**Description:** Funkcja steruje przekaźnikiem podającym napięcie 230V AC do nagrzewnicy wstępnej. Wysłanie "1" powoduje załączenie grzałki aż do chwili zmiany wartości
na "0".

**Parameters:**
```
mode - tryb pracy nagrzewnicy 1- włącza , 0 - wyłącza
```

**Result:**
```
{ SetGWCModeResult: true, Message : ""}
SetGWCModeResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetGWCMode`

---

## SetPinCode

**Description:** Funkcja pozwala na ustawienie kodu PIN dla połączenia zdalnego (wymagane do zdalnego połączenia dla instalatora lub serwisanta) - w innym przypadku nie da się zdalnie sterować urządzeniem

**Parameters:**
```
pin - 6 cyfrowy PIN
```

**Result:**
```
{ SetPinCodeResult : true, Message : ""}
SetPinCodeResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetPinCode`

---

## SetSchedule

**Description:** Funkcja pozwala na dodanie nowej lub edycję istniejącej strefy czasowej w harmonogramie. Przy edycji ważny jest podanie prawidłowego numeru strefy czasowej.

**Parameters:**
```
number - numer strefy czasowej (przy dodawaniu można wpisać 255 wtedy zostanie nadany kolejny numer - pierwszy wolny)
startweekday - początek strefy dzień tygodnia (zakres od 1 do 7 -> poniedziałek , wtorek itd.)
endweekday - koniec strefy dzień tygodnia (zakres od 1 do 7)
starthour - początek strefy - godzina (zakres od 0 do 23)
startmin - początek strefy - minuta (zakres od 0 do 59)
endhour - koniec strefy - godzina (zakres od 0 do 23)
endmin - koniec strefy - minuta (zakres od 0 do 59)
efficiencyvalue - wydajność dla danej strefy czasowej 
[m3/h] ; zakres od 50 do maksymalnej wydajności)
comforttemperature - temperatura komfortu dla danej strefy wyrażona w °C
```

**Result:**
```
{ SetScheduleResult: true, Message : ""}
SetScheduleResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=SetSchedule`

---

## StatusDevice

**Description:** Funkcja zwraca podstawowe informacje o urządzeniu np. MAC , status podłączenia do WIFI oraz MQTT, numer wersji oprogramowania dla modułu WIFI oraz płyty itp.

**Parameters:**
```
brak
```

**Result:**
```
{
 "StatusDeviceResult":true,
 "Status":1,
 "Version":112,
 "DeviceType":1,
 "MAC":"EE:EE:EE:EE:EE:EE",
 "WIFISSID":"SiecWiFi",
 "APSSID":"reqnetEE:EE:EE:EE:EE:EE",
 "APIVersion":112,
 "RecuperatorSoftwareVersion":"9.25",
 "WIFISignalStrength":5,
 "WIFIIP":"192.168.1.101",
 "WifiSignalStrengthDescription":"excellent (-43 dBm)",
 "WifiChannel":"1",
 "REQNET_WIFI_IP_TO_CHECK":"",
 "REQNET_WIFI_ENABLED":"1"
}
StatusDeviceResult - wynik wykonania , true - prawidłowy , false - nieprawidłowy
Status - 0 - rozłączony, 1 - połączony, 2 - aktualizacja modułu WiFi, 3 - aktualizacja oprogramowania sprzętowego
Version - wersja modułu WiFi
DeviceType - typ urządzenia (model)
MAC - MAC urządzenia (modułu WIFI)
WIFISSID - nazwa sieci WIFI
APPSSID - nazwa sieci (widoczność urządzenia) w momencie braku podłączenia do sieci WiFi domowej/firmowej
APIVersion - wersja modułu Wifi
RecuperatorSoftwareVersion - wersja oprogramowania sprzętowego
WIFISignalStrength - siła sygnału w skali od 1-6
WIFIIP - adres IP urządzenia
WIFISignalStrengthDescription - siła sygnału - opis
WifiChannel - kanał sieci WiFi
REQNET_WIFI_IP_TO_CHECK - ustawienie statyscznego IP - jeżeli moduł WiFi jest podłączony do sieci i ma przydzielone podany adres IP - moduł nie rozłącza sie niezależnie od tego czy jest dostęp do internetu / brokera MQTT czy nie
REQNET_WIFI_ENABLED - wartość wykorzystywana wewnętrznie
```

**HTTP:** `GET /API/RunFunction?name=StatusDevice`

---

## TurnOff

**Description:** Wyłącza urządzenie (wprowadza w stan czuwania) - funkcja która go wybudza to TurnOn

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffResult : true, Message : ""}
TurnOffResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOff`

---

## TurnOffAiring

**Description:** Wyłącza funkcję wietrzenia

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffAiringResult : true, Message : ""}
TurnOffAiringResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffAiring`

---

## TurnOffCleaning

**Description:** Wyłącza funkcję oczyszczania powietrza

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffCleaningResult : true, Message : ""}
TurnOffCleaningResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffCleaning`

---

## TurnOffCooling

**Description:** Wyłącza funkcję chłodzenia

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffCoolingResult : true, Message : ""}
TurnOffCoolingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffCooling`

---

## TurnOffFastCooling

**Description:** Wyłącza funkcję szybkiego chłodzenia

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffFastCoolingResult : true, Message : ""}
TurnOffFastCoolingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffFastCooling`

---

## TurnOffFastHeating

**Description:** Wyłącza funkcję szybkiego grzania

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffFastHeatingResult : true, Message : ""}
TurnOffFastHeatingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffFastHeating`

---

## TurnOffFireplace

**Description:** Wyłącza funkcję kominek

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffFireplaceResult: true, Message : ""}
TurnOffFireplaceResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffFireplace`

---

## TurnOffHeating

**Description:** Wyłącza funkcję grzania

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffHeatingResult : true, Message : ""}
TurnOffHeatingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffHeating`

---

## TurnOffHoliday

**Description:** Wyłącza funkcję urlop

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOffHolidayResult: true, Message : ""}
TurnOffHolidayResult- wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOffHoliday`

---

## TurnOffSchedule

**Description:** Funkcja wyłącza harmonogram

**Parameters:**
```
brak
```

**Result:**
```
{
 "TurnOffScheduleResult": true
}
```

**HTTP:** `GET /API/RunFunction?name=TurnOffSchedule`

---

## TurnOn

**Description:** Włącza urządzenie ze stanu czuwania

**Parameters:**
```
brak
```

**Result:**
```
{ TurnOnResult : true, Message : ""}
```

**HTTP:** `GET /API/RunFunction?name=TurnOn`

---

## TurnOnAiring

**Description:** Włącza funkcję wietrzenia

**Parameters:**
```
time - czas na jaki ma być funkcją włączona
```

**Result:**
```
{ TurnOnAiringResult : true, Message : ""}
TurnOnAiringResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnAiring`

---

## TurnOnCleaning

**Description:** Włącza funkcję oczyszczania powietrza

**Parameters:**
```
time - czas na jaki ma być funkcją włączona
```

**Result:**
```
{ TurnOnCleaningResult : true, Message : ""}
TurnOnCleaningResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnCleaning`

---

## TurnOnCooling

**Description:** Włącza funkcję chłodzenia ( o ile dostępne jest i skonfigurowane urządzenie)

**Parameters:**
```
comforttemperature - temperatur komfortu do jakiej funkcja ma dążyć (10-35)
```

**Result:**
```
{ TurnOnCoolingResult : true, Message : ""}
TurnOnCoolingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnCooling`

---

## TurnOnFastCooling

**Description:** Włącza funkcję szybkiego chłodzenia

**Parameters:**
```
time - czas na jaki ma być funkcją włączona
```

**Result:**
```
{ TurnOnFastCoolingResult : true, Message : ""}
TurnOnFastCoolingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnFastCooling`

---

## TurnOnFastHeating

**Description:** Włącza funkcję szybkiego grzania

**Parameters:**
```
time - czas na jaki ma być funkcją włączona
```

**Result:**
```
{ TurnOnFastHeatingResult : true, Message : ""}
TurnOnFastHeatingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnFastHeating`

---

## TurnOnFireplace

**Description:** Włącza funkcję kominek na podany czas

**Parameters:**
```
time - czas na jaki ma być funkcją włączona (5-95)
```

**Result:**
```
{ TurnOnFireplaceResult : true, Message : ""}
TurnOnFireplaceResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnFireplace`

---

## TurnOnHeating

**Description:** Włącza funkcję grzania ( o ile dostępne jest i skonfigurowane urządzenie)

**Parameters:**
```
comforttemperature - temperatur komfortu do jakiej funkcja ma dążyć (10-35)
```

**Result:**
```
{ TurnOnHeatingResult : true, Message : ""}
TurnOnHeatingResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnHeating`

---

## TurnOnHoliday

**Description:** Włącza funkcję urlop

**Parameters:**
```
days - dni na ile funkcja urlop ma zostać załączona (0-255)
```

**Result:**
```
{ TurnOnHolidayResult : true, Message : ""}
TTurnOnHolidayResult - wynik wywołania metody
Message - informacja o błędzie lub niepoprawnej wartości
```

**HTTP:** `GET /API/RunFunction?name=TurnOnHoliday`

---

## TurnOnSchedule

**Description:** Funkcja włącza harmonogram

**Parameters:**
```
brak
```

**Result:**
```
{
 "TurnOnScheduleResult": true
}
```

**HTTP:** `GET /API/RunFunction?name=TurnOnSchedule`

---

