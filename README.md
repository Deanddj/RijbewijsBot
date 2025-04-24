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

Installeer Python 3.8 of hoger [hier](https://www.python.org/downloads/release/python-3810/)

Clone deze repository: 
```
git clone https://github.com/Deanddj/RijbewijsBot.git
```

Ga naar de map: 
```
cd RijbewijsBot
```

Installeer de benodigde pakketten: 
```
pip install -r requirements.txt
```

Vul het .env bestand aan in de hoofdmap met je discord webhook(s)

## Gebruik 

### Windows:
```
python rijbewijs_aanvraag.py 
python rijbewijs_ophaal.py
```

### Ubuntu:
```
python3 rijbewijs_aanvraag.py 
python3 rijbewijs_ophaal.py
```

### Automatisch via Ubuntu:
Je kunt dit script ook automatisch laten uitvoeren op een VPS of eigen server die 24/7 aan staat.
Zo ben je de eerste die iemand anders afgezegde afspraak pakt.

Open crontab:
```
crontab -e
```

Voeg toe (dit voert het script elke 5 minuten uit):
```
*/5 * * * * /volledig/pad/naar/linux_start.sh
```
(Maak 'linux_start.sh' executable als het dat nog niet is)

## Vereisten

- Python 3.8.10 of hoger
- chromium-browser of Google Chrome
- chromedriver (in de map van het script)
- werkende Discord Webhook URL’s
#### LET OP: De chromedriver en browser moeten dezelfde versie zijn.

## Hulp nodig?

Stel je vraag via de Issues-tab op GitHub of stuur een pull request als je iets wil bijdragen.

## Licentie

MIT – Vrij te gebruiken, aanpassen en verspreiden. Credits geven is altijd welkom.

### Let op: ik ben niet aansprakelijk voor verkeerd gebruik van dit script, zoals het overmatig belasten van overheidswebsites door het te vaak te laten draaien. Gebruik dit script op een verantwoorde manier.
