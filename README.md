# Nový web obce Most pri Bratislave

Návrh nového, prehľadného webu obce Most pri Bratislave. Web obsahuje všetok obsah doterajšieho webu, len je usporiadaný podľa toho, čo ľudia potrebujú vybaviť.

## Čo web obsahuje

- **Úvodná stránka:** vyhľadávanie, rýchle odkazy „Čo potrebujete vybaviť?“, aktuality, úradná tabuľa, podujatia, harmonogram odpadu a príbeh mohyly M. R. Štefánika.
- **Šesť hlavných sekcií namiesto ~110 položiek v menu:** Úrad a služby · Odpady · Samospráva · Úradná tabuľa · Aktuality · Život v obci (+ Kontakt).
- **128 stránok, 39 aktualít a 15 podujatí** prenesených z pôvodného webu (vrátane matriky, VZN, zmlúv, faktúr, harmonogramov atď.).
- **Živý stav úradu:** v hlavičke je vidieť, či má úrad práve otvorené alebo kedy otvára.
- **Upozornenie v hornej lište** (napr. uzávierky ciest) s dátumom, do kedy sa má zobrazovať.
- **Fulltextové vyhľadávanie** (Pagefind) bez externých služieb.
- **Nahlásenie problému:** formulár pripraví e-mail priamo na zodpovedný referát.
- **Filtrovanie dokumentov** na úradnej tabuli, v zmluvách, faktúrach a ďalších zoznamoch.
- **Prístupnosť (WCAG 2.1 AA)** podľa vyhlášky 78/2020 Z. z.: kontrast, ovládanie klávesnicou, skip-link, sémantika.
- **Bez sledovania a cookies tretích strán:** písma a ikony sú súčasťou webu.
- **Mobilná verzia** je navrhnutá ako rovnocenná s počítačovou.

## Technické riešenie

| Časť | Riešenie |
| --- | --- |
| Generátor webu | [Astro 5](https://astro.build) (statický web, rýchly a bezpečný, bez databázy) |
| Obsah | Markdown súbory v `src/content/` (stránky a aktuality) |
| Administrácia | [Sveltia CMS](https://github.com/sveltia/sveltia-cms) na adrese `/admin/` (editor v prehliadači, bez programovania) |
| Vyhľadávanie | Pagefind (index sa vytvorí pri zostavení) |
| Hosting | GitHub Pages zadarmo, alebo ľubovoľný webhosting (stačí nahrať priečinok `dist/`) |

### Spustenie na počítači

```bash
npm install
npm run dev        # vývojový server na http://localhost:4321
npm run build      # zostavenie do priečinka dist/ (vrátane vyhľadávania)
npm run preview    # náhľad zostaveného webu
```

### Štruktúra

```
src/
  content/pages/<sekcia>/…   stránky webu (Markdown)
  content/news/…             aktuality
  data/site.ts               údaje obce, stránkové hodiny, menu, rýchle odkazy, kontakty
  data/alerts.json           upozornenie v hornej lište
  data/events.json           podujatia
  pages/                     šablóny stránok
  styles/global.css          dizajn (farby podľa erbu obce)
public/admin/                administrácia (Sveltia CMS)
tools/import/import.py       import obsahu z pôvodného webu
```

### Nasadenie

1. Repozitár je na GitHube a v nastaveniach je zapnuté **Settings → Pages → Source: GitHub Actions**.
2. Každá zmena v `main` (aj z administrácie) web automaticky zostaví a zverejní (`.github/workflows/deploy.yml`). Web sa navyše zostavuje každý deň, aby sa obnovili podujatia a skryli staré upozornenia.
3. **Vlastná doména obce:** v workflow nastavte `BASE_PATH: /` a `SITE_URL: https://www.mostpribratislave.sk`, pridajte súbor `public/CNAME` s doménou a u registrátora nasmerujte DNS na GitHub Pages.

### Administrácia pre obecný úrad

1. V `public/admin/config.yml` doplňte `repo: vlastník/názov-repozitára`.
2. Zamestnanci sa prihlasujú GitHub účtom, ktorý má prístup do repozitára. Prihlasovanie cez GitHub vyžaduje jednorazové nastavenie OAuth (návod v dokumentácii Sveltia CMS, napr. bezplatný Cloudflare Worker `sveltia-cms-auth`).
3. Na adrese `/admin/` potom môžu písať aktuality, upravovať stránky, nahrávať obrázky a meniť upozornenie v hornej lište.

## Čo treba doriešiť pred ostrým spustením

- **Dokumenty (PDF) a úradná tabuľa** zatiaľ odkazujú na súbory na pôvodnom portáli ModerneObce. Pred ukončením zmluvy s ModerneObce treba dokumenty stiahnuť a preniesť (importér je na to pripravený) alebo ponechať úradnú tabuľu na špecializovanom systéme.
- **Zákonné zverejňovanie** (zmluvy, faktúry, objednávky, úradná tabuľa) musí mať zaručený dátum zverejnenia a archív. Možnosti: samostatná kolekcia v administrácii alebo napojenie na existujúci systém obce.
- **Podnety občanov:** doterajší systém podnetov (1 600+ vyriešených) je služba ModerneObce. Nový web ich zatiaľ rieši e-mailom. Ak to obec bude chcieť, dá sa napojiť formulárová služba.
- **Presmerovania** zo starých adries: mapa starých a nových URL je v `src/data/redirects.json`.
- Vyhlásenie o ochrane osobných údajov a o prístupnosti treba doplniť o údaje obce.

## Automatická synchronizácia so starým webom

Kým obec používa pôvodný web, nový web si **každú noc sám prevezme** nové aktuality, podujatia a zmeny na stránkach (`tools/import/sync.sh`, spúšťa sa v `.github/workflows/deploy.yml`). Ručne sa dá spustiť v záložke **Actions → Zostavenie a nasadenie webu → Run workflow**.

Po prechode na nový web (úrad píše priamo v administrácii) treba krok „Synchronizácia obsahu“ z workflow odstrániť, inak by prepisoval stránky.

## Import obsahu

Obsah bol stiahnutý z pôvodného webu 10. 11. 2026. Import sa dá zopakovať (napr. tesne pred spustením):

```bash
./tools/import/sync.sh   # potrebuje: pip install -r requirements.txt
```

Mapovanie starých stránok do novej štruktúry je na začiatku skriptu.
