# Pflanzenbewaesserung

## Einführung

Dieses repo beinhaltet den backend-code für das Projekt "PlantDrop". Es stellt die nötigen Funktionalitäten da, um verschiedene Sensoren mithilfe eines Raspberry Pi zu steuern. In diesem Fall sind die Sensoren für die automatische Bewässerung von Pflanzen gedacht. Daher ist das backend auf diese Sensoren ausgelegt. Das passende Frontend finded ihr in [diesem Repository](https://github.com/FemRene/Plantify).

## Funktionen

- [x] **Steuerung der Pumpe per PWM**<br/>
- [x] **PH-Wertemessung**<br/> 
- [x] **Temperatur & Luftfeuchtigkeitmessung**<br/> 
- [x] **Lichtmessung**<br/> 
- [x] **Luftqualitätsmessung**<br/>
- [x] **Wasserstand**<br/> 
- [x] **API An- & Abfragen**<br/> 
- [x] **Aktuelle Messwerte**<br/>  

## Voraussetzungen

# Hardware
**Raspberry Pi 2 und neuer**
**Lichtsensor**
**PH-Sensor**
**Pumpe**
**Feuchtigkeitssensor**
**Temperaturseonsor**

Die Hardware kann auf eigene bedürfnisse angepassst werden. Dazu muss jedoch der Code ebenso angepasst werden!

# Software
[**Raspberry Pi OS (Lite)**](https://www.raspberrypi.com/software/operating-systems/)
**Python3** 
[**Python 3.11+**](https://www.python.org/downloads/windows/)<br/>
[**Pip**](https://pypi.org/project/pip/) <br/>
[**Python Pakete**](https://github.com/Chautoo/Pflanzenbewaesserung/blob/backend/requirements.txt)

## Installation und Ausführung

**1. Repository klonen & zu Verzeichniss Springen**
   ```bash
   git clone https://github.com/Chautoo/Pflanzenbewaesserung.git
   cd Pflanzenbewaesserung
   `````````
**2. Ausführen des Codes**
```bash
   sudo python3 main.py
   `````````
**3. Code automatisch ausführen (systemd)**
Zuerst muss die datei unter dem folgendem Pfad angelegt werden. 
```bash
   sudo nano /etc/systemd/system/Plantdrop_backend.service
   `````````
Kopiere in dieses Verzeichnis die Plantdrop_backend.service.example und speichere sie. 
Starte und lege die Datei in den Autostart mit folgendem Befehl.
```bash
   sudo systemctl enable Plantdrop_backend.service && sudo systemctl start Plantdrop_backend.service
   `````````

## Credits

Folgende Mitglieder haben dieses Projekt realisert:

[Chauto (Anakin)](https://github.com/Chautoo)

[FemRene (Rene)](https://github.com/FemRene)

## Unterstützt und gefördert durch 

![srhHeader](https://github.com/user-attachments/assets/7592aeef-c2d3-40f3-b446-e0a64a8f632e)
