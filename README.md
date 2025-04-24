# Rijbewijs Notificatie Bot

Een Python-script dat automatisch controleert op beschikbare momenten voor het aanvragen of ophalen van je rijbewijs bij de gemeente Zoetermeer. 
Als er een nieuw moment beschikbaar is die eerder is dan het laatst gecontroleerde moment, krijg je direct een melding via Discord.

## Functies

- Controleert automatisch op aanvraag- en ophaalmomenten
- Stuurt meldingen via Discord Webhooks
- Werkt op zowel Windows als Ubuntu
- Gebruikt Selenium met Chromium of ChromeDriver
- Eenvoudige installatie via requirements.txt
  
## Installatie

#### TIP: Maak een [python virtual environment](https://docs.python.org/3/library/venv.html) aan zodat de requirements zijn geïsoleerd van de rest van je systeem.

### Windows

Download en installeer Python 3.8.10 van python.org

Open een terminal (CMD of PowerShell)

Clone de repository:
```
git clone https://github.com/Deanddj/RijbewijsBot.git
```

Ga naar de projectmap:

``` 
cd RijbewijsBot
```

Installeer de vereiste pakketten:
```
pip install -r requirements.txt
```

Voer het script uit:
```
python rijbewijs_aanvraag.py
python rijbewijs_ophaal.py
```
### _Vergeet niet je eigen '.env'-bestand aan te maken, zie '.env.example'!_

### Ubuntu (of andere Linux distro's)

Installeer Git en Python 3.8.10 (via apt of pyenv):

Met apt:
```
sudo apt update sudo apt install git python3.8 python3.8-venv python3-pip
```

Of gebruik pyenv als je meerdere versies wilt beheren.

Clone de repository:
```
git clone https://github.com/Deanddj/RijbewijsBot.git
```

Ga naar de projectmap:
```
cd RijbewijsBot
```

Installeer de vereiste pakketten:
```
pip install -r requirements.txt
```

Voer het script uit:
```
python3.8 rijbewijs_aanvraag.py
python3.8 rijbewijs_ophaal.py
```
### _Vergeet niet je eigen '.env'-bestand aan te maken, zie '.env.example'!_

### Automatisch via Ubuntu:
Je kunt dit script ook automatisch laten draaien op een VPS of eigen server die 24/7 online is. 
Zo ben jij er als eerste bij wanneer iemand anders een afspraak annuleert.

Open crontab:
```
crontab -e
```

Voeg toe (dit voert het script elke 5 minuten uit):
```
*/5 * * * * /volledig/pad/naar/linux_start.sh
```

## Vereisten

- [Python 3.8](https://www.python.org/downloads/release/python-3810/) of hoger
- chromium-browser (Ubuntu) of Google Chrome (Windows)
- [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) (in de map van het script)
- werkende [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL’s
#### LET OP: De chromedriver en browser moeten dezelfde versie zijn.

## Hulp nodig?

Stel je vraag via de Issues-tab op GitHub of stuur een pull request als je iets wil bijdragen.

## Licentie

MIT – Vrij te gebruiken, aanpassen en verspreiden. Credits geven is altijd welkom.

### Let op: ik ben niet aansprakelijk voor verkeerd gebruik van dit script, zoals het overmatig belasten van overheidswebsites door het te vaak te laten draaien. Gebruik dit script op een verantwoorde manier.
