#!/usr/bin/env python3
"""Generera återstående policyanalysdokument — ALLA filer i en körning"""

import os

OUT = '/Users/quberon1/OD-policybas/kategorier'

def save(cat, filename, content):
    path = os.path.join(OUT, cat, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    size = len(content)
    if size < 2000:
        print(f"  VARNING: {filename} är kort ({size} bytes)")
    else:
        print(f"  OK: {filename} ({size} bytes)")

# =============================================
# SKATT-004: Fastighetsskatt
# =============================================
save('skatt', 'SKATT-004-fastighetsskatt.md', '''# Policyanalys: Fastighetsskatt i Sverige

## Metadata
- **Fråge-ID:** SKATT-004
- **Kategori:** Skattepolitik
- **Underkategori:** Fastighetsbeskattning, bostadsmarknad
- **Evidensnivå:** MEDIUM-HÖG
- **Politisk laddning:** HÖG (historisk — skapade Ny Demokrati 1991)
- **Opinionsgap:** JA — stark opinion mot, brett nationalekonomiskt stöd för
- **Närliggande frågor:** BOST-001, BOST-002, SKATT-001

---

## 1. Rationale & Målbild

### Varför agera?
Den svenska fastighetsskatten avskaffades 2008 och ersattes med en kommunal fastighetsavgift med tak. Avgiften har sedan dess urholkats kraftigt av inflation och stigande fastighetspriser. Nationalekonomer är nästan eniga: fastighetsskatt är en av de minst snedvridande skatterna eftersom mark är en fast faktor (kan inte flyttas utomlands). OECD, IMF, EU-kommissionen och Finanspolitiska rådet har alla rekommenderat Sverige att reformera fastighetsbeskattningen.

### Vad vill man uppnå?
1. Ökade kommunala skatteintäkter utan att höja inkomstskatten
2. Dämpad bostadsprisutveckling
3. Effektivare utnyttjande av bostadsbeståndet (motverka inlåsning)
4. Ökad rörlighet på bostadsmarknaden

### Problem med status quo
- Fastighetsavgiften är 8 874 kr/år (tak 2024) oavsett fastighetsvärde — en villa för 10 Mkr betalar samma som en för 2 Mkr
- Extremt gynnsamt för högbelånade i storstäder
- Subventionerar boende på bekostnad av annan konsumtion

---

## 2. Alternativ

| Alternativ | Beskrivning |
|------------|-------------|
| **BAU** | Kommunal fastighetsavgift med tak, ingen koppling till marknadsvärde |
| **A. Proportionell fastighetsskatt** | 0,5-1,0 % av taxeringsvärde, med högre tak |
| **B. Progressiv fastighetsskatt** | Högre skattesats för högre taxeringsvärden |
| **C. Markvärdesbeskattning** | Skatt enbart på markvärdet (ej byggnaden), enligt Henry George-principen |
| **D. Nedtrappat ränteavdrag + reformerad fastighetsavgift** | Paketlösning som kompenserar höjd avgift med sänkt ränteavdrag |

---

## 3. Evidensgenomgång

### Nationalekonomisk konsensus
OECD (2023), "Economic Surveys: Sweden":
> "Sweden should consider increasing recurrent property taxation by linking it to updated property values. Property taxes are among the least distortionary taxes and could help stabilise house prices."

Mirrlees Review (2011), den mest omfattande skatteöversynen i modern tid, rankar fastighetsskatt som den minst skadliga skatten för ekonomisk tillväxt, efter konsumtionsskatter.

### Svenska fastighetsbeskattningens urholkning
Englund (2011) och SOU 2020:60 visar att:
- Fastighetsavgiften har sjunkit från ~0,8 % av fastighetsvärde (2008) till ~0,1-0,2 %
- En återgång till 0,5 % skulle ge ~40-50 mdr kr i skatteintäkter
- Hushållens boendeutgifter har samtidigt sjunkit som andel av disponibel inkomst

### Beteendeeffekter och bostadspriser
- En fastighetsskatt kapitaliseras delvis i lägre bostadspriser (Oates, 1969)
- Vid 0,5 % skatt skulle bostadspriserna sannolikt sjunka med 5-15 % (Svensson, 2018)
- Kortsiktigt smärtsamt för belånade hushåll, långsiktigt fördelaktigt för förstagångsköpare

### Likviditetsproblemet
Detta är den verkliga politiska svårigheten:
- Äldre hushåll med låga inkomster men höga fastighetsvärden kan få likviditetsproblem
- Uppskovsmodeller finns: betala skatten först vid försäljning (som i Danmark)
- Kan kombineras med äldreskydd och inkomstprövat uppskov

---

## 4. Sammanvägd Bedömning

| Kriterium | BAU | A (Prop.) | B (Progressiv) | C (Markvärde) | D (Paket) |
|-----------|-----|-----------|----------------|---------------|-----------|
| Intäktspotential | LÅG | HÖG | MEDIUM-HÖG | MEDIUM | MEDIUM-HÖG |
| Ekonomisk effektivitet | MEDIUM | HÖG | MEDIUM-HÖG | HÖG | MEDIUM-HÖG |
| Progressivitet | LÅG | MEDIUM | HÖG | MEDIUM | MEDIUM |
| Likviditetsproblem | LÅGA | MEDIUM | MEDIUM-HÖG | MEDIUM | MEDIUM |
| Politisk genomförbarhet | HÖG | LÅG | LÅG | LÅG | MEDIUM |

### Rekommendation

**OD bör förespråka Alternativ D: en paketlösning med reformerad fastighetsskatt, nedtrappat ränteavdrag och starka äldreskydd.**

Motivering:
1. En ren fastighetsskatt är politiskt omöjlig — paketlösning skapar kompensation
2. Uppskovsmodeller löser likviditetsproblemet
3. Nedtrappning av ränteavdrag är komplementärt och minskar skuldsättningen
4. OD kan "äga" denna fråga som evidensdrivet parti — nationalekonomisk konsensus är överväldigande

### Osäkerheter
- Bostadsprisfall vid införande: storleken är osäker, men viss nedgång är sannolik
- Finansiell stabilitet: kraftigt prisfall kan utlösa bankförluster
- Övergångsregler: hur lång infasningstid?

---

## 5. Referenser

| Källa | Länk |
|-------|------|
| OECD Economic Surveys: Sweden (2023) | https://oecd.org |
| Mirrlees Review (2011), "Tax by Design" | https://ifs.org.uk |
| SOU 2020:60, Fastighetstaxering | https://regeringen.se |
| Englund (2011), "Swedish housing market" | SNS |
| Svensson (2018), "Fastighetsskatt och bostadspriser" | IFN |
| Finanspolitiska rådet, årsrapporter | https://fpr.se |

---

## 6. Preliminär OD-Position

**OD anser att fastighetsbeskattningen bör reformeras i linje med den nationalekonomiska konsensusen**, i ett paket med nedtrappat ränteavdrag och starka äldreskydd inklusive uppskovsränta. Partiet konstaterar att dagens fastighetsavgift är godtycklig, icke-progressiv och urholkad, och att en reform skulle gynna förstagångsköpare och hyresmarknaden.

*Preliminär position — medlemsbeslut krävs.*
''')

print("SKATT-004 skapad")

# SKATT-005: 3:12-regler
save('skatt', 'SKATT-005-3-12-regler.md', '''# Policyanalys: 3:12-reglerna — Reform av inkomstomvandling

## Metadata
- **Fråge-ID:** SKATT-005
- **Kategori:** Skattepolitik
- **Underkategori:** Fåmansbolag, inkomstomvandling
- **Evidensnivå:** HÖG
- **Politisk laddning:** HÖG (stark företagaropinion mot reformer)
- **Opinionsgap:** JA — företagare är emot skärpning, löntagare omedvetna

---

## 1. Rationale & Målbild

### Varför agera?
3:12-reglerna (fåmansbolagsreglerna) styr hur ägare till fåmansföretag beskattas på utdelning och kapitalvinst. Reglerna är resultatet av 1990 års skattereform och syftar till att förhindra att arbetsinkomster omvandlas till lägre beskattade kapitalinkomster. Kritiker menar att reglerna fortfarande tillåter omfattande inkomstomvandling: höginkomsttagare kan ta ut miljonbelopp till 20 % skatt istället för marginalskatt på ~57 %.

### Vad vill man uppnå?
1. Täppa till kryphål för inkomstomvandling
2. Öka skatteintäkter från höginkomsttagare
3. Bevara entreprenörskapsincitament

---

## 2. Alternativ

| Alternativ | Beskrivning |
|------------|-------------|
| **BAU** | Nuvarande regler med löneunderlag och schablonbelopp |
| **A. Sänkt löneuttagskrav** | Skärpa kravet på eget löneuttag för att få använda löneunderlagsregeln |
| **B. Enhetlig skattesats** | Samma skattesats för arbets- och kapitalinkomster över brytpunkt |
| **C. Striktare kvalifikationskrav** | Begränsa 3:12-reglerna till "aktiva entreprenörer" |

---

## 3. Evidensgenomgång

Alstadsæter & Jacob (2016) visar i svensk registerdata att höginkomsttagare i betydande utsträckning använder 3:12-reglerna för att minska sin skattebörda. SOU 2016:75 (3:12-utredningen) identifierade specifika kryphål och föreslog åtgärder. Edmark & Gordon (2021) uppskattar att inkomstomvandling via 3:12 kostar staten 5-10 mdr kr årligen.

### Effekter på entreprenörskap
- Riskkapitalister och serieentreprenörer är starkt beroende av 3:12-reglerna
- För strikt reglering kan minska entreprenörskap — elasticiteten är okänd
- Sverige har redan hög marginalskatt jämfört med konkurrentländer

---

## 4. Sammanvägd Bedömning

| Kriterium | BAU | A (Skärpt lönekrav) | B (Enhetlig skatt) | C (Kvalifikation) |
|-----------|-----|---------------------|--------------------|-------------------|
| Intäktspotential | LÅG | MEDIUM | HÖG | MEDIUM |
| Rättvisa | LÅG | MEDIUM-HÖG | HÖG | MEDIUM |
| Entreprenörskapsincitament | HÖG | MEDIUM | LÅG | MEDIUM |
| Administrativ komplexitet | MEDIUM | MEDIUM | HÖG | MEDIUM |
| Politisk genomförbarhet | HÖG | MEDIUM | LÅG | MEDIUM |

### Rekommendation

**OD föreslår att 3:12-reglerna reformeras i två steg: först höjda löneuttagskrav för stora fåmansbolag, därefter utredning av bredare kapitalbeskattningsreform.**

---

## 5. Referenser
- SOU 2016:75, 3:12-utredningen
- Alstadsæter & Jacob (2016), "Income shifting in Sweden"
- Edmark & Gordon (2021), IFAU

## 6. Preliminär OD-Position
**OD anser att 3:12-reglerna bör reformeras** för att minska möjligheten till inkomstomvandling, med bibehållet entreprenörsstöd för genuina riskkapitalinvesteringar.
''')

print("SKATT-005 skapad")

# SKATT-006 till SKATT-008 — kompakta versioner
save('skatt', 'SKATT-006-optimalt-skattetryck.md', '''# Policyanalys: Optimalt skattetryck i Sverige

## Metadata
- **Fråge-ID:** SKATT-006
- **Evidensnivå:** MEDIUM
- **Politisk laddning:** HÖG

## 1. Rationale
Sverige har bland OECD:s högsta skattetryck (~43 % av BNP). Frågan är om vi är nära, på, eller över Lafferkurvans topp — där ytterligare skattehöjningar minskar skatteintäkterna.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Oförändrat skattetryck |
| A | Höjt skattetryck för ökad välfärd |
| B | Sänkt skattetryck för ökad tillväxt |
| C | Skatteväxling (samma tryck, bättre struktur) |

## 3. Evidensgenomgång

Trabandt & Uhlig (2011) estimerar Lafferkurvor för 14 EU-länder och finner att Sveriges topp för arbetsinkomstskatter ligger vid ~62 % marginalskatt — Sverige ligger nära denna nivå. Holmlund & Söderström (2011) visar att marginalskatteförändringar har signifikanta men måttliga dynamiska effekter i Sverige. Finanspolitiska rådet har återkommande förordat skatteväxling snarare än nivåhöjningar.

### Dynamiska effekter
- 10 % höjd marginalskatt → 2-5 % minskat arbetsutbud (elasticitet 0,2-0,5)
- Effekterna är störst för kvinnor, äldre och höginkomsttagare
- Kapitalbeskattning har högre elasticitet än arbetsinkomstbeskattning

## 4. Rekommendation
**OD bör förespråka skatteväxling (Alternativ C):** oförändrat totaltryck men bättre struktur — lägre skatt på arbete och investeringar, högre på fastigheter, miljö och konsumtion.

## 5. Referenser
- Trabandt & Uhlig (2011), Journal of Monetary Economics
- Holmlund & Söderström (2011), IFAU
- Finanspolitiska rådet, årsrapporter
- OECD Revenue Statistics 2023

## 6. Preliminär OD-Position
**OD förespråkar skatteväxling** — samma totala skattetryck men med en effektivare skattemix baserad på evidens om minsta snedvridning.
''')

print("SKATT-006 skapad")

save('skatt', 'SKATT-007-progressiv-bolagsskatt.md', '''# Policyanalys: Progressiv bolagsskatt

## Metadata
- **Fråge-ID:** SKATT-007
- **Evidensnivå:** LÅG-MEDIUM
- **Politisk laddning:** MEDIUM

## 1. Rationale
Progressiv bolagsskatt (högre skattesats för större vinster) föreslås ibland som sätt att få storföretag att bidra mer. Sverige har idag 20,6 % platt bolagsskatt.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Platt 20,6 % bolagsskatt |
| A | Progressiv bolagsskatt (t.ex. 15-25 %) |
| B | OECD minimum tax (15 % globalt golv) |
| C | Omsättningsbaserad skatt istället för vinstbaserad |

## 3. Evidens
Bolagsskatt är bland de mest snedvridande skatterna (OECD, Mirrlees Review). Progressivitet i bolagsskatt är extremt ovanligt internationellt — inget OECD-land har det i betydande utsträckning. OECD:s globala minimiskatt (Pillar 2, 15 %) är en mer framkomlig väg. Devereux & Griffith visar att bolagsskatt främst bärs av arbetstagare via lägre löner, inte av kapitalägare.

## 4. Rekommendation
**OD avråder från progressiv bolagsskatt.** OECD:s minimum tax + effektivare kapitalinkomstbeskattning är bättre alternativ.

## 5. Referenser
- OECD (2022), Corporate Tax Statistics
- Devereux & Griffith, "Evaluating tax policy for location decisions"
- Mirrlees Review (2011)
- OECD Pillar 2, Global Minimum Tax

## 6. Preliminär OD-Position
**OD avvisar progressiv bolagsskatt** men stödjer OECD:s globala minimiskatt och anser att kapitalägare bör beskattas effektivt via personliga kapitalinkomster snarare än bolagsskattenivån.
''')

print("SKATT-007 skapad")

save('skatt', 'SKATT-008-rot-rut-avdrag.md', '''# Policyanalys: ROT- och RUT-avdragen

## Metadata
- **Fråge-ID:** SKATT-008
- **Evidensnivå:** MEDIUM-HÖG
- **Politisk laddning:** MEDIUM-HÖG

## 1. Rationale
ROT (renovering, ombyggnad, tillbyggnad) och RUT (rengöring, underhåll, tvätt) infördes 2007 för att minska svartarbete, öka sysselsättning och underlätta livspusslet. Kostnaden för staten är ~19 mdr kr/år (2023).

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | ROT 30 % av arbetskostnad, RUT 50 %, separata tak |
| A | Sänkta subventionsgrader (t.ex. RUT till 25 %) |
| B | Samlat tak för ROT+RUT |
| C | Avskaffa ROT, behåll RUT |
| D | Avskaffa båda |

## 3. Evidens
Skatteverkets och Riksrevisionens utvärderingar visar att ROT/RUT minskat svartarbete signifikant — särskilt RUT i hushållsnära tjänster. Konjunkturinstitutet (2022) uppskattar att ROT/RUT genererar 40-60 % tillbaka i skatteintäkter via ökad vit sysselsättning. Bennmarker et al. (2013) visar att RUT specifikt ökat arbetsutbudet bland kvinnor med högre inkomster. Kritiken handlar om dödviktseffekter (hade jobbet gjorts ändå?) och fördelningsprofil (gynnar höginkomsttagare).

## 4. Rekommendation
**OD föreslår behåll RUT oförändrat, sänk ROT-subventionen gradvis.** ROT har mer dödvikt (renoveringar hade skett ändå), medan RUT skapar nya jobb för lågutbildade.

## 5. Referenser
- Skatteverket, ROT/RUT-statistik
- Riksrevisionen (2020), ROT/RUT-utvärdering
- Konjunkturinstitutet (2022)
- Bennmarker et al. (2013), Labour Economics

## 6. Preliminär OD-Position
**OD behåller RUT-avdraget oförändrat** (positiv sysselsättningseffekt, minskar svartarbete) **men trappar ner ROT-avdraget** gradvis för att minska dödviktseffekten och frisläppa budgetutrymme.
''')

print("SKATT-008 skapad — ALLA SKATT KLARA")

# =============================================
# ARBETSMARKNAD 005-008
# =============================================
for arb_id, arb_title, arb_content in [
    ("ARB-005-kortare-arbetstid", "Kortare arbetstid (6-timmarsdag)", '''# Policyanalys: Kortare arbetstid

## Metadata
- **Fråge-ID:** ARB-005
- **Evidensnivå:** MEDIUM
- **Politisk laddning:** HÖG

## 1. Rationale
Förslag om lagstadgad arbetstidsförkortning (ofta 6-timmarsdag med bibehållen lön) förs fram med argument om ökat välmående, jämställdhet och produktivitet. Frågan har prövats i flera svenska försök.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Normalarbetstid 40 h/vecka, avtalsfrihet |
| A | Lagstadgad 35-timmarsvecka (Frankrike-modell) |
| B | Lagstadgad 30-timmarsvecka (6-timmarsdag) |
| C | Ökad flexibilitet (årsarbetstid, arbetstidsbanker) |

## 3. Evidens
Göteborgs stads försök på Svartedalens äldreboende (2015-2017) visade positiva effekter på personalens hälsa och minskad sjukfrånvaro (-10 %), men kostnaden ökade med ~20 % pga extrapersonal. Frankrikes 35-timmarsvecka (Aubry-lagarna 2000) gav små sysselsättningseffekter men ökade enhetsarbetskostnaderna. OECD (2018) visar att arbetstidsförkortningar sällan ökar produktiviteten per timme tillräckligt för att kompensera bortfallet. Bosch & Lehndorff visar att arbetstidsflexibilitet (Alternativ C) har bättre evidens än generell förkortning.

## 4. Rekommendation
**OD bör inte driva generell arbetstidsförkortning.** Evidensen stödjer flexibilitetsreformer och riktade försök i specifika sektorer, inte en generell lagstiftning. Kostnaden överstiger nyttorna.

## 5. Referenser
- Göteborgs stad, Svartedalsförsöket (2017)
- OECD Employment Outlook (2018)
- Estevão & Sá (2008), Economic Journal (Frankrike 35h)

## 6. Preliminär OD-Position
**OD avvisar lagstadgad generell arbetstidsförkortning** men stödjer ökad flexibilitet (årsarbetstid, arbetstidsbanker) och sektoriella försök med kortare arbetstid.
'''),
    ("ARB-006-anstallningsstod", "Anställningsstöd och subventionerade anställningar", '''# Policyanalys: Anställningsstöd mot långtidsarbetslöshet

## Metadata
- **Fråge-ID:** ARB-006
- **Evidensnivå:** MEDIUM-HÖG
- **Politisk laddning:** MEDIUM

## 1. Rationale
Sverige spenderar betydande belopp på anställningsstöd (nystartsjobb, instegsjobb, lönebidrag). Frågan är vilka stöd som är kostnadseffektiva och hur dödviktseffekter kan minimeras.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Nuvarande blandning av stöd |
| A | Utökat nystartsjobb (längre subvention) |
| B | Fokus på lönebidrag för funktionsnedsatta |
| C | Omfördela till utbildning/matchning istället för subvention |

## 3. Evidens
IFAU:s metastudier visar att nystartsjobb har positiva men måttliga effekter, med betydande dödviktseffekter (~40-60 % — jobben hade skapats ändå). Forslund et al. visar att lönebidrag för funktionsnedsatta är bland de mest effektiva programmen. Calmfors et al. rekommenderar profilering — matcha insats till individ.

## 4. Rekommendation
**OD föreslår behåll lönebidrag, minska nystartsjobbens omfattning, öka matchningsinsatser.**

## 5. Referenser
- IFAU (flera rapporter)
- Calmfors et al. (2002), SOU
- Forslund et al. (2013), IFAU

## 6. Preliminär OD-Position
**OD vill omfördela från breda anställningsstöd till riktade insatser** (lönebidrag, matchning, utbildning) baserat på evidens om kostnadseffektivitet.
'''),
    ("ARB-007-pensionsalder", "Höjd pensionsålder — effekter", '''# Policyanalys: Höjd Pensionsålder

## Metadata
- **Fråge-ID:** ARB-007
- **Evidensnivå:** MEDIUM-HÖG
- **Politisk laddning:** HÖG

## 1. Rationale
Sverige har beslutat om riktad höjning av pensionsåldern (LAS-ålder till 69 år, garantipensionsålder till 67 år). Frågan är om ytterligare höjningar behövs och vilka effekterna är på arbetsutbud och hälsa.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Redan beslutad höjning |
| A | Ytterligare höjning — pensionsålder 70 |
| B | Flexibel pensionsålder med kraftigare avtalsincitament |
| C | Differentierad pensionsålder per yrkesgrupp |

## 3. Evidens
Laun & Palme (2018) visar att höjd pensionsålder ökar arbetsutbudet signifikant med små negativa hälsoeffekter. Pensionsåldersutredningen (SOU 2022:28) rekommenderar successiva höjningar. OECD Pensions at a Glance visar att Sverige redan har hög faktisk pensionsålder (64,5 år).

## 4. Rekommendation
**OD stödjer successivt höjd pensionsålder kopplad till medellivslängd, med yrkesspecifika anpassningar.**

## 5. Referenser
- SOU 2022:28, Pensionsåldersutredningen
- Laun & Palme (2018), IFAU
- OECD Pensions at a Glance (2023)

## 6. Preliminär OD-Position
**OD stödjer fortsatt successiv höjning av pensionsåldern** i takt med ökad medellivslängd, med undantag för fysiskt tunga yrken.
'''),
    ("ARB-008-gig-ekonomi", "Plattformsarbete — reglering?", '''# Policyanalys: Reglering av plattformsarbete (gig-ekonomi)

## Metadata
- **Fråge-ID:** ARB-008
- **Evidensnivå:** MEDIUM
- **Politisk laddning:** MEDIUM

## 1. Rationale
Plattformsarbete (Foodora, Uber, Taskrunner) växer globalt men är fortfarande litet i Sverige (~1 % av sysselsatta). EU:s plattformsdirektiv från 2024 inför anställningspresumtion. Frågan är om Sverige behöver ytterligare nationell reglering.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Ingen särreglering, EU-direktivet implementeras |
| A | Anställningspresumtion i svensk lag |
| B | Tredje kategori (mellan anställd och egenföretagare) |
| C | Branschspecifika kollektivavtal |

## 3. Evidens
SOU 2022:23 (Tryggare plattformsarbete) föreslår förstärkt arbetsgivaransvar för plattformar. IFAU (2023) visar att gig-arbete i Sverige främst är extrainkomst för unga och studenter — inte huvudsaklig försörjning. Erfarenheter från Kalifornien (Prop 22) visar att anställningspresumtion kan minska flexibilitet.

## 4. Rekommendation
**OD föreslår branschspecifika kollektivavtal (Alternativ C) som första steg, och avvaktar EU-direktivets effekter innan ytterligare lagstiftning.**

## 5. Referenser
- SOU 2022:23
- IFAU (2023)
- EU Platform Work Directive (2024)

## 6. Preliminär OD-Position
**OD vill balansera flexibilitet och trygghet** — kollektivavtal före lagstiftning, men beredskap att lagstifta om plattformar missbrukar egenföretagarstatus.
''')
]:
    save('arbetsmarknad', arb_id, arb_content)

print("ARBETSMARKNAD 005-008 klara")

# =============================================
# UTBILDNING 007-008
# =============================================
# UTB-007 skapades separat ovan
save('utbildning', 'UTB-008-tidigare-skolplikt.md', '''# Policyanalys: Skolplikt från tidigare ålder

## Metadata
- **Fråge-ID:** UTB-008
- **Evidensnivå:** MEDIUM

## 1. Rationale
Sverige har skolplikt från 6 år (förskoleklass). Vissa förespråkar skolplikt från 5 eller till och med 3 år, med argument om tidig språkutveckling och integration. Andra betonar familjens autonomi och barns mognad.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Skolplikt från 6 år |
| A | Skolplikt från 5 år |
| B | Obligatorisk förskola från 3 år (språkplikt) |
| C | Frivillig förskola med riktade insatser |

## 3. Evidens
Fredriksson & Öckert (2013) visar att tidigare skolstart har positiva effekter på kognitiva färdigheter men små effekter på långsiktiga utfall. OECD (2022) visar att obligatorisk förskola (Frankrike från 3 år) ökar jämlikhet i språkutveckling. Kritiker pekar på att förskolan redan når >95 % av 3-5-åringar i Sverige — obligatoriet skulle främst träffa marginalgrupper.

## 4. Rekommendation
**OD föreslår obligatorisk språkförskola från 3 år för barn som inte når språkmål**, men inte generell skolpliktssänkning.

## 5. Referenser
- Fredriksson & Öckert (2013), IFAU
- OECD Education at a Glance (2022)
- Skolverket

## 6. Preliminär OD-Position
**OD stödjer riktad obligatorisk språkförskola** men inte generell sänkning av skolpliktsåldern.
''')

print("UTBILDNING 007-008 klara")

# =============================================
# MIGRATION 004-007
# =============================================
for mig_id, mig_content in [
    ("MIGR-004-ebo-systemet.md", '''# Policyanalys: EBO-systemet och segregation

## Metadata
- **Fråge-ID:** MIGR-004
- **Evidensnivå:** MEDIUM

## 1. Rationale
EBO (eget boende) innebär att asylsökande kan ordna eget boende istället för anläggningsboende (ABO). Systemet kritiseras för att driva segregation då nyanlända bosätter sig i redan utsatta områden.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | EBO med dagersättning |
| A | Avskaffa EBO — endast anläggningsboende |
| B | EBO med kommunalt veto |
| C | Statlig bosättningsstyrning för alla nyanlända |

## 3. Evidens
Andersson & Hammarstedt (2017) visar att EBO bidrar till koncentration av nyanlända i socioekonomiskt utsatta områden. SOU 2022:19 föreslår avskaffande av EBO. Boverket (2023) dokumenterar att 32 kommuner redan har infört socialtjänstrelaterade EBO-begränsningar. IFAU visar dock att bosättning i etniska nätverk kan ha positiva effekter på kort sikt (socialt stöd) men negativa på lång sikt (språk, arbete).

## 4. Rekommendation
**OD föreslår avskaffa EBO och införa statlig bosättningsstyrning med flexibilitet.**

## 5. Referenser
- SOU 2022:19
- Andersson & Hammarstedt (2017), Ekonomisk Debatt
- Boverket (2023)
- IFAU (flera rapporter)

## 6. Preliminär OD-Position
**OD vill avskaffa EBO-systemet** och ersätta med statlig bosättningsstyrning som tar hänsyn till både integrations- och arbetsmarknadsfaktorer.
'''),
    ("MIGR-005-sprakkrav-medborgarskap.md", '''# Policyanalys: Språkkrav för medborgarskap

## Metadata
- **Fråge-ID:** MIGR-005
- **Evidensnivå:** MEDIUM

## 1. Rationale
Flera länder (Danmark, Norge, Tyskland, Nederländerna) har infört språkkrav för medborgarskap. SOU 2021:2 föreslog språk- och samhällskunskapskrav för svenskt medborgarskap.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Inget språkkrav för medborgarskap |
| A | Språkkrav på SFI D-nivå + samhällskunskap |
| B | Differentierade krav (lägre för analfabeter, äldre) |
| C | Frivilliga språkprov med medborgarskapsbonus |

## 3. Evidens
Goodman (2010) visar att språkkrav i Storbritannien ökat språkinlärning men skapat exkludering av lågutbildade. OECD (2021) noterar att språkkrav är vanliga i OECD men att evidensen för integrationseffekt är blandad — symbolpolitik snarare än effektiv integrationspolitik. SNS (2022) pekar på att språkkrav kan vara ett incitament men att tillgången till SFI måste förbättras först.

## 4. Rekommendation
**OD stödjer språkkrav med differentierade nivåer (Alternativ B).**

## 5. Referenser
- SOU 2021:2
- Goodman (2010), Journal of Ethnic and Migration Studies
- OECD (2021)

## 6. Preliminär OD-Position
**OD stödjer språkkrav för medborgarskap** i kombination med kraftigt förbättrad SFI och undantag för analfabeter och äldre.
'''),
    ("MIGR-006-utvisning-vid-brott.md", '''# Policyanalys: Utvisning vid brott

## Metadata
- **Fråge-ID:** MIGR-006
- **Evidensnivå:** MEDIUM

## 1. Rationale
Utvisning på grund av brott (utlänningslagen) är en återkommande politisk fråga. SOU 2023:25 föreslog skärpta regler. Frågan rör proportionalitet och rättssäkerhet vs. samhällsskydd.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Utvisning vid grova brott, proportionalitetsbedömning |
| A | Skärpt utvisning — obligatoriskt vid vissa brott |
| B | Differentiering efter vistelsetid (längre vistelse = färre utvisningar) |
| C | Särskilda utlänningsdomstolar |

## 3. Evidens
Brå (2022) visar att utvisning vid brott har liten preventiv effekt — få känner till reglerna innan brottet begås. ECHR (Europadomstolen) ställer krav på proportionalitet (Al-Khawaja, Maslov). Migrationsverket rapporterar att utvisningsärenden ökat 500 % sedan 2015 men att verkställigheten är låg. Den preventiva effekten är svagt belagd; opinionsmässigt är stödet starkt.

## 4. Rekommendation
**OD stödjer skärpt utvisning vid grova brott men med proportionalitetsbedömning och differentiering efter vistelsetid.**

## 5. Referenser
- SOU 2023:25
- Brå (2022)
- ECHR, Maslov v. Austria

## 6. Preliminär OD-Position
**OD stödjer utvisning vid allvarliga brott** men anser att proportionalitetsprincipen måste upprätthållas och att lång vistelsetid bör väga tungt.
'''),
    ("MIGR-007-arbetskraftsinvandring-kompetens.md", '''# Policyanalys: Arbetskraftsinvandring för kompetensförsörjning

## Metadata
- **Fråge-ID:** MIGR-007
- **Evidensnivå:** MEDIUM-HÖG

## 1. Rationale
Sverige har omfattande arbetskraftsbrist i flera sektorer (IT, vård, industri, bygg). Samtidigt finns farhågor om låglönekonkurrens och utnyttjande av arbetskraftsinvandrare.

## 2. Alternativ
| Alt | Beskrivning |
|-----|-------------|
| BAU | Nuvarande system med försörjningskrav och lön på minst 80 % av medianlön |
| A | Liberaliserad arbetskraftsinvandring för bristyrken |
| B | Skärpt arbetskraftsinvandring med högre lönekrav |
| C | Poängbaserat system (Kanada-modell) |

## 3. Evidens
OECD (2023) visar att arbetskraftsinvandring är nettogynnsam för mottagarlandet vid hög sysselsättningsgrad. SKR (2023) rapporterar 200 000+ lediga jobb i offentlig sektor som kräver arbetskraftsinvandring. Ruist (2020) visar att lågkvalificerad arbetskraftsinvandring kan pressa löner i botten av fördelningen men att effekten är liten.

## 4. Rekommendation
**OD föreslår liberaliserad arbetskraftsinvandring för bristyrken med strikta villkor för att förhindra exploatering.**

## 5. Referenser
- OECD Migration Outlook (2023)
- SKR (2023), Kompetensförsörjning
- Ruist (2020), SNS

## 6. Preliminär OD-Position
**OD vill underlätta arbetskraftsinvandring i bristyrken** genom snabbspår och sänkt byråkrati, samtidigt som löne- och anställningsvillkor bevakas strikt mot exploatering.
''')
]:
    save('migration-integration', mig_id, mig_content)

print("MIGRATION 004-007 klara")

# =============================================
# NU ÅTERSTÅR: BOSTAD, ENERGI, NÄRINGSLIV, DIGITALISERING, FÖRSVAR, PENSION, FAMILJ, INFRASTRUKTUR, DEMOKRATI
# =============================================
print("\\nÅterstående kategorier: BOSTAD (7), ENERGI (7), NÄRINGSLIV (7), DIGITALISERING (6),")
print("FÖRSVAR (4, 001-002 ev redan skapade), PENSION (6), FAMILJ (6), INFRASTRUKTUR (5), DEMOKRATI (5)")
print(f"\\nTotalt: {7+7+7+6+4+6+6+5+5} = 53 filer kvar")
print("\\nFortsätter i batch 3...")