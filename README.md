# URL Shortener
Een eenvoudige URL-verkorter gebouwd met **Flask** en **SQLite**.

## Functies

- Verkort lange URL's en sla ze op in een database.
- Redirect gebruikers naar de originele URL via de verkorte link.
- Caching om prestaties te verbeteren.
- Logt fouten en verzoeken naar een logfile: `url_shortener.log`.

## Installatie

1. **Clone de repository**

```bash
git clone https://github.com/Sirehtea/URL_Shortener.git
cd url-shortener
```

2. **Installeer requirements**

```bash
pip install -r requirements.txt
```

3. **Start applicatie**

```bash
python.exe .\main.py
```

4. **Surf naar**

    http://127.0.0.1:5000

## MapStructuur

```bash
URL_Shortener/
│── static/
│   ├── style.css
│── templates/
│   ├── index.html
│   ├── shorten.html
│   ├── not_found.html
│── main.py
│── README.md
│── requirements.txt
```