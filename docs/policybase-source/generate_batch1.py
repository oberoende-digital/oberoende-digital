#!/usr/bin/env python3
"""Generera policyanalysdokument för OD-policybasen — batch 1: SKATT 002-008"""

import os

OUT = '/Users/quberon1/OD-policybas/kategorier'

def save(cat, filename, content):
    path = os.path.join(OUT, cat, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    return len(content)

# =============================================
# SKATT-002: Arvsskatt
# =============================================
save('skatt', 'SKATT-002-arvsskatt.md', '''# Policyanalys: Arvsskatt i Sverige

## Metadata
- **Fråge-ID:** SKATT-002
- **Kategori:** Skattepolitik
- **Underkategori:** Kapitalbeskattning, förmögenhetsöverföring
- **Evidensnivå:** MEDIUM-HÖG
- **Politisk laddning:** HÖG
- **Opinionsgap:** JA — opinionen är splittrad, historiskt trauma (avskaffades 2004)
- **Närliggande frågor:** SKATT-001 (förmögenhetsskatt), SKATT-003 (ISK), SKATT-004 (fastighetsskatt)

---

## 1. Rationale & Målbild

### Varför agera?
Sverige avskaffade arvsskatten 2004 efter decennier av kritik mot att den drabbade familjeföretag vid generationsskiften. Samtidigt ökar förmögenhetskoncentrationen och arv spelar en växande roll för livsinkomster. Enligt SCB ägde den rikaste procenten ~35 % av nettoförmögenheten 2023. Arv är en central mekanism för att reproducera förmögenhetsklyftor över generationer (Piketty, 2014).

### Vad vill man uppnå?
1. **Fördelningspolitiskt:** Bryta reproduktionen av förmögenhetsklyftor över generationer
2. **Fiskalt:** Skatteintäkter från stora arv, med höga fribelopp
3. **Rättviseuppfattning:** Beskatta överföring, inte arbete eller sparande

### Problem med status quo
Sverige är ett av få OECD-länder utan arvsskatt. Stora förmögenheter överförs skattefritt. Familjeföretag har inget incitament att planera generationsskiften i förtid.

---

## 2. Alternativ

| Alternativ | Beskrivning |
|------------|-------------|
| **BAU** | Ingen arvsskatt |
| **A. Modern arvsskatt med högt fribelopp** | 25 % skatt på arv över 5 Mkr, undantag för familjeföretag med aktiva generationsskiften |
| **B. Arvsskatt med successionsprincip** | Skatt på mottagaren, progressiv efter mottagen summa, 0-40 % |
| **C. Gåvoskatt som komplement** | Återinförd gåvoskatt för att förhindra kringgående |

---

## 3. Evidensgenomgång

### Teoretiskt ramverk
Piketty & Saez (2013) visar i "A Theory of Optimal Inheritance Taxation" att:
- Optimal arvsskatt beror på elasticiteten i arv (hur mycket minskar sparandet?)
- Om de rika sparar främst för arv (snarare än egen konsumtion) är hög arvsskatt optimal
- Om elasticiteten är låg kan optimal skattesats vara 50-60 % för stora arv

### Svensk historisk erfarenhet
Elinder, Erixson & Waldenström (2018) dokumenterar i "Inheritance and wealth taxation in Sweden":
- Arvsskatten avskaffades främst pga familjeföretag, inte ideologiskt motstånd
- Skatteintäkterna var modesta (~0,1 % av BNP)
- Undantag för familjeföretag var administrativt komplexa men tekniskt möjliga
- De flesta svenskar betalade aldrig arvsskatt (höga fribelopp)

### Internationell evidens
OECD (2021), "Inheritance Taxation in OECD Countries":
- 24 av 37 OECD-länder har någon form av arv-/gåvoskatt
- OECD bedömer arvsskatt som en av de minst snedvridande kapitalskatterna
- Intäkterna är generellt låga (0,1-0,5 % av BNP) men progressiviteten är hög
- Länder med avskaffad arvsskatt (Sverige, Norge, Österrike) har svårt att återinföra

### Familjeföretagsproblemet
Detta är den verkliga svårigheten:
- Ägare till onoterade bolag har ofta hög förmögenhet men låg likviditet
- Generationsskiften tvingar fram försäljning till utländska ägare om skatten är hög
- Undantag och uppskov är tekniskt möjliga men öppnar för skatteplanering (Bjuggren & Sund, 2020)

---

## 4. Sammanvägd Bedömning

| Kriterium | BAU | A (Modern m. fribelopp) | B (Succession) | C (Gåvoskatt) |
|-----------|-----|-------------------------|----------------|---------------|
| Intäktspotential | 0 | MEDIUM | MEDIUM-HÖG | LÅG |
| Progressivitet | LÅG | HÖG | HÖG | MEDIUM |
| Entreprenörseffekter | NEUTRAL | MILT NEGATIV (undantag möjliga) | NEGATIV | MILT NEGATIV |
| Kapitalflyktsrisk | LÅG | MEDIUM | HÖG | LÅG |
| Administrativ komplexitet | LÅG | MEDIUM-HÖG | HÖG | MEDIUM |
| Politisk genomförbarhet | HÖG | LÅG | LÅG | LÅG |

### Rekommendation
**OD bör utreda Alternativ A (modern arvsskatt med högt fribelopp + företagsundantag)** som en långsiktig position. På kort sikt är den politiska kostnaden för hög — arvsskattefrågan är symboliskt laddad efter 2004 års avskaffande. OD bör:

1. Inte driva återinförande som förstalinjepolitik
2. Lyfta fram OECD:s analys av arvsskatt som en av de minst skadliga kapitalskatterna
3. Föreslå en statlig utredning med tydligt mandat att utforma företagsundantag

### Osäkerheter
- Beteendeeffekter i dagens globaliserade ekonomi (kan förmögenheter flyttas ut?)
- Familjeföretagsundantag: svåra att täta men avgörande för acceptans
- Intäktspotential vid olika fribeloppsnivåer

---

## 5. Referenser

| Källa | Länk/DOI |
|-------|----------|
| Piketty & Saez (2013), "A Theory of Optimal Inheritance Taxation", Econometrica | https://doi.org/10.3982/ECTA10702 |
| Elinder, Erixson & Waldenström (2018), IFN Working Paper | https://www.ifn.se |
| OECD (2021), "Inheritance Taxation in OECD Countries" | https://doi.org/10.1787/e2879a7d-en |
| Piketty (2014), "Capital in the Twenty-First Century" | Harvard University Press |
| Bjuggren & Sund (2020), "Generationsskiften i familjeföretag" | Ratio |

---

## 6. Preliminär OD-Position

**OD anser att frågan om en modern arvsskatt med högt fribelopp och starka företagsundantag bör utredas förutsättningslöst.** Partiet erkänner att arvsskatt har teoretiskt och empiriskt starkare stöd än förmögenhetsskatt som fördelningspolitiskt verktyg. OD avvisar dock ett okritiskt återinförande utan robusta skyddsmekanismer för familjeföretag.

*Preliminär position — medlemsbeslut krävs.*
''')

print("SKATT-002 skapad")

# =============================================
# SKATT-003: ISK-skatt
# =============================================
save('skatt', 'SKATT-003-isk-skatt.md', '''# Policyanalys: ISK-skatten — Är den för låg?

## Metadata
- **Fråge-ID:** SKATT-003
- **Kategori:** Skattepolitik
- **Underkategori:** Kapitalbeskattning, sparande
- **Evidensnivå:** HÖG (omfattande svensk data, utvärderingar)
- **Politisk laddning:** MEDIUM
- **Opinionsgap:** JA — de flesta förstår inte ISK-skatten, opinionsläge oklart
- **Närliggande frågor:** SKATT-001, SKATT-005, SKATT-006

---

## 1. Rationale & Målbild

### Varför agera?
ISK (investeringssparkonto) infördes 2012 och har blivit den dominerande sparformen för svenska hushåll med över 3 000 mdr kr i förvaltat kapital. Skatten tas ut som en schablon (30 % av statslåneräntan + 1 procentenhet, minimum 1,25 %). Kritiken handlar om att effektiv beskattning är mycket låg vid normal avkastning — långt under den nominella kapitalinkomstskatten på 30 %.

### Vad vill man uppnå?
1. Ökad rättvisa mellan sparformer och mellan sparare med olika avkastning
2. Ökade skatteintäkter från kapital
3. Behålla ISK:s enkelhet och administrativa fördelar

### Problem med status quo
- Vid 7% avkastning är effektiv skatt ~0,38% — lägre än kapitalinkomstskattens 30%
- Höginkomsttagare med hög avkastning gynnas mest
- Skatteintäkterna är låga relativt den totala kapitalstocken

---

## 2. Alternativ

| Alternativ | Beskrivning |
|------------|-------------|
| **BAU** | Nuvarande schablonbeskattning (statslåneränta + 1pp, golv 1,25 %) |
| **A. Höjd schablonsats** | Öka från 30 % till 35-40 % av schablonunderlaget |
| **B. Progressiv ISK-skatt** | Högre skattesats för större innehav |
| **C. Tak på ISK-innehav** | Maxbelopp för skattegynnad avkastning, resten beskattas normalt |
| **D. Faktisk avkastningsbeskattning** | Återgå till beskattning av faktisk kapitalvinst (som före 2012) |

---

## 3. Evidensgenomgång

### ISK:s effekter på sparandet
Finansdepartementets utvärderingar visar:
- ISK har ökat hushållens aktiesparande signifikant
- Förenklingen har sänkt tröskeln för småsparare
- Avkastningsskatten (före ISK) var administrativt tung och skapade inlåsningseffekter

### Effektiv beskattning
Riksgäldens och FI:s analyser:
- Vid statslåneränta 2,5 % + 1 pp = 3,5 %, ger 30 % skatt: 1,05 % effektiv skatt
- Jämfört med 30 % kapitalinkomstskatt: vid 7 % avkastning är kapitalinkomstskatten 2,1 % — dubbelt så hög
- Ju högre avkastning, desto större gap mellan ISK och vanlig beskattning

### Fördelningseffekter
SCB:s statistik över ISK-innehav:
- Medianvärdet på ISK-konton är ~200 000 kr
- Genomsnittet är ~600 000 kr — indikerar skev fördelning
- De 10 % största kontona står för ~70 % av kapitalet

### Schablonmetodens legitimitet
SNS Konjunkturråd (2023) argumenterar att:
- Schablonbeskattningen är legitim för att den eliminerar inlåsningseffekter
- Men nivån bör kalibreras så att effektiv skatt närmar sig kapitalinkomstbeskattning
- En golvnivå på 1,25 % är för låg i en normalräntemiljö

---

## 4. Sammanvägd Bedömning

| Kriterium | BAU | A (Höjd schablon) | B (Progressiv) | C (Tak) | D (Faktisk avk.) |
|-----------|-----|-------------------|----------------|---------|------------------|
| Intäktspotential | LÅG | MEDIUM | MEDIUM-HÖG | MEDIUM | MEDIUM-HÖG |
| Rättvisa mellan sparare | LÅG | MEDIUM | HÖG | MEDIUM | HÖG |
| Enkelhet | HÖG | HÖG | MEDIUM | MEDIUM | LÅG |
| Inlåsningseffekter | LÅGA | LÅGA | LÅGA | MEDIUM | HÖGA |
| Småsparareffekt | POSITIV | NEUTRAL | POSITIV | POSITIV | NEGATIV |
| Politisk genomförbarhet | HÖG | MEDIUM | LÅG-MEDIUM | MEDIUM | LÅG |

### Rekommendation

**Alternativ A (höjd schablonsats) som första steg, med utredning av B (progressiv modell) på sikt.**

Motivering:
1. Höjd schablonsats från 30 % till ~35 % av schablonunderlaget är tekniskt enkelt
2. Progressiv modell är rättvisare men kräver ny infrastruktur hos banker
3. Tak på ISK-innehav är en kompromiss som skyddar småsparare
4. Återgång till faktisk avkastningsbeskattning är en återgång till gamla problem

### Osäkerheter
- Hur mycket minskar sparandet vid höjd skatt? Elasticiteten är okänd
- Kapitalflykt till utländska konton vid progressiv modell
- EU-rättsliga aspekter av progressiv beskattning

---

## 5. Referenser

| Källa | Länk |
|-------|------|
| Finansdepartementet, promemorior ISK | https://regeringen.se |
| Riksgälden, statslåneränta | https://riksgalden.se |
| Finansinspektionen, stabilitetsrapporter | https://fi.se |
| SCB, hushållens tillgångar | https://scb.se |
| SNS Konjunkturråd (2023) | https://sns.se |

---

## 6. Preliminär OD-Position

**OD anser att ISK-skatten bör reformeras för att minska gapet mot kapitalinkomstbeskattning**, samtidigt som ISK:s grundläggande fördelar (enkelhet, frånvaro av inlåsningseffekter) bevaras. Partiet föreslår en höjning av skattesatsen på schablonunderlaget från 30 % till 35 % som första steg, samt en utredning av progressiv ISK-beskattning för mycket stora innehav (>5 Mkr).

*Preliminär position — medlemsbeslut krävs.*
''')

print("SKATT-003 skapad")

# =============================================
# Fortsätt med SKATT-004 till SKATT-008 i nästa batch
# =============================================
print("Batch 1 klar: SKATT-002, SKATT-003")