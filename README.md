# ManualAkademiTrack - Manual STU Registration Tool

Manual Python scripts for STU (Selvstendige Terminoppgaver) attendance registration at Akademiet.

🇳🇴 **Norsk** | 🇺🇸 [English](#english)

---

## 🇳🇴 Norsk

### Om Prosjektet
ManualAkademiTrack er en manuell versjon av AkademiTrack som lar deg registrere STU-oppmøte ved hjelp av Python-skript. Dette er nyttig for utviklere eller de som ønsker mer kontroll over registreringsprosessen.

### Hovedfunksjoner
- **Manuell cookie-håndtering**: Administrer autentisering gjennom cookie-filer
- **Fleksibel tidsplanforespørsler**: Hent timeplandata for spesifikke datoperioder  
- **Manuell oppmøteregistrering**: Registrer oppmøte for spesifikke STU-økter
- **JSON-dataeksport**: Lagre timeplandata til filer for analyse

### Filer i Prosjektet
- `get.py` - Henter timeplandata fra iSkole API
- `get-big.py` - Utvidet versjon for cookie-administrasjon og større dataforespørsler
- `post.py` - Registrerer oppmøte for STU-økter

### Systemkrav
- **Python 3.7+** med følgende pakker:
  - `requests`
  - `selenium` (for cookie-innhenting)
  - `webdriver-manager`
- **Chrome-nettleser** (for Selenium)
- **Internett**: Stabil forbindelse
- **Tilgang**: Gyldig iSkole-konto ved Akademiet

### Installasjon
```bash
# Klon repositoriet
git clone https://github.com/CyberGutta/ManualAkademiTrack.git
cd ManualAkademiTrack

# Installer avhengigheter
pip install requests selenium webdriver-manager
```

### Bruksanvisning

#### Steg 1: Hent Cookies
```bash
python get-big.py
```
- Skriptet åpner en nettleser for innlogging
- Logg inn via Feide som vanlig
- Trykk Enter når du er ferdig pålogget
- Cookies lagres automatisk i `cookies.json` og `cookies.txt`

#### Steg 2: Hent Timeplandata
```bash
python get.py
```
- Henter timeplandata for spesifisert periode
- Endre `start_date` og `end_date` variabler etter behov
- Data kan lagres til JSON-fil for analyse

#### Steg 3: Registrer Oppmøte
```bash
python post.py
```
**Viktig**: Før du kjører post.py, må du oppdatere `item`-objektet med riktig data:

```python
item = {
    "Id": 1,
    "Fag": "PB3A STU",           # Ditt fag
    "Stkode": "PB",              # Din studiekode
    "KlTrinn": "3",              # Ditt klassetrinn
    "KlId": "A",                 # Din klasse-ID
    "KNavn": "STU",              # Kursnavn
    "GruppeNr": "$",             # Gruppenummer
    "Dato": "20250903",          # Dato (YYYYMMDD)
    "Timenr": 21609421,          # Time-ID fra timeplan
    "StartKl": "0900",           # Starttid
    "SluttKl": "0945",           # Sluttid
    # ... resten av dataene
}
```

**Slik finner du riktig data:**
1. Kjør `get.py` for å hente timeplandata
2. Finn din STU-økt i JSON-responsen
3. Kopier verdiene til `item`-objektet i `post.py`
4. Kjør `post.py` for å registrere oppmøte

### Feilsøking
- **"Authentication failed"**: Cookies er utløpt, kjør `get-big.py` på nytt
- **"Missing required cookies"**: Sjekk at `cookies.json` inneholder riktige cookies
- **"Request failed"**: Kontroller at timeplan-dataene er korrekte

### Sikkerhet
- Cookies lagres kun lokalt på din maskin
- Ingen data sendes til utviklerne
- Bruker offisiell iSkole API

---

## 🇺🇸 English

### About the Project
ManualAkademiTrack is a manual version of AkademiTrack that allows you to register STU attendance using Python scripts. This is useful for developers or those who want more control over the registration process.

### Key Features
- **Manual cookie management**: Handle authentication through cookie files
- **Flexible schedule requests**: Fetch schedule data for specific date ranges
- **Manual attendance registration**: Register attendance for specific STU sessions
- **JSON data export**: Save schedule data to files for analysis

### Project Files
- `get.py` - Fetches schedule data from iSkole API
- `get-big.py` - Extended version for cookie management and larger data requests
- `post.py` - Registers attendance for STU sessions

### System Requirements
- **Python 3.7+** with the following packages:
  - `requests`
  - `selenium` (for cookie extraction)
  - `webdriver-manager`
- **Chrome browser** (for Selenium)
- **Internet**: Stable connection
- **Access**: Valid iSkole account at Akademiet

### Installation
```bash
# Clone the repository
git clone https://github.com/CyberGutta/ManualAkademiTrack.git
cd ManualAkademiTrack

# Install dependencies
pip install requests selenium webdriver-manager
```

### Usage Instructions

#### Step 1: Extract Cookies
```bash
python get-big.py
```
- Script opens browser for login
- Login via Feide as usual
- Press Enter when logged in
- Cookies are automatically saved to `cookies.json` and `cookies.txt`

#### Step 2: Fetch Schedule Data
```bash
python get.py
```
- Fetches schedule data for specified period
- Modify `start_date` and `end_date` variables as needed
- Data can be saved to JSON file for analysis

#### Step 3: Register Attendance
```bash
python post.py
```
**Important**: Before running post.py, you must update the `item` object with correct data:

```python
item = {
    "Id": 1,
    "Fag": "PB3A STU",           # Your subject
    "Stkode": "PB",              # Your study code
    "KlTrinn": "3",              # Your class level
    "KlId": "A",                 # Your class ID
    "KNavn": "STU",              # Course name
    "GruppeNr": "$",             # Group number
    "Dato": "20250903",          # Date (YYYYMMDD)
    "Timenr": 21609421,          # Session ID from schedule
    "StartKl": "0900",           # Start time
    "SluttKl": "0945",           # End time
    # ... rest of the data
}
```

**How to find the correct data:**
1. Run `get.py` to fetch schedule data
2. Find your STU session in the JSON response
3. Copy the values to the `item` object in `post.py`
4. Run `post.py` to register attendance

### Troubleshooting
- **"Authentication failed"**: Cookies expired, run `get-big.py` again
- **"Missing required cookies"**: Check that `cookies.json` contains correct cookies
- **"Request failed"**: Verify that schedule data is correct

### Security
- Cookies stored only locally on your machine
- No data sent to developers
- Uses official iSkole API

---

## Contributors
- **CyberHansen** (Mathias Hansen) - Developer
- **CyberNilsen** (Andreas Nilsen) - Developer

## License
This project is provided as-is for educational and personal use. Please ensure compliance with your school's policies regarding automated tools.

## Disclaimer
This tool is designed to assist students with legitimate attendance registration. Users are responsible for ensuring their use complies with school policies and academic integrity standards.

## Related Projects
- [AkademiTrack](https://github.com/CyberGutta/AkademiTrack) - Automated desktop application
- [AkademietTrack Website](https://github.com/CyberGutta/AkademietTrack) - Official website

---

**Version**: 1.0.0  
**Last Updated**: January 2025
