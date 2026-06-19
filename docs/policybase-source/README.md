# Oberoende Digital — Policybas

## Vad detta är
En strukturerad, evidensbaserad kunskapsbas med 100 policyanalyser för svenska politiska frågor. Varje analys följer Green Book-strukturen (UK Treasury) med rationale, alternativ, evidensgenomgång, sammanvägd bedömning, referenser och preliminär OD-position.

## Struktur
```
OD-policybas/
├── index.json          # Maskinläsbart index över alla dokument
├── README.md           # Denna fil
├── kategorier/         # 15 politikområden
│   ├── skatt/          # 8 analyser
│   ├── arbetsmarknad/  # 8 analyser
│   ├── utbildning/     # 8 analyser
│   ├── vard-omsorg/    # 7 analyser
│   ├── brott-ratt/     # 7 analyser
│   ├── migration-integration/  # 7 analyser
│   ├── bostad-bygg/    # 7 analyser
│   ├── energi-klimat/  # 7 analyser
│   ├── naringsliv/     # 7 analyser
│   ├── digitalisering/ # 6 analyser
│   ├── forsvar/        # 6 analyser
│   ├── pension/        # 6 analyser
│   ├── familj/         # 6 analyser
│   ├── infrastruktur/  # 5 analyser
│   └── demokrati/      # 5 analyser
└── mallar/             # Mallar och generation scripts
```

## Dokumentformat
Varje analysdokument innehåller:
1. **Metadata** — ID, kategori, evidensnivå, politisk laddning, opinionsgap
2. **Rationale & Målbild** — Varför agera, vad vill man uppnå
3. **Alternativ** — BAU + minst 2 alternativ
4. **Evidensgenomgång** — Citerade studier, kvantifierade effekter
5. **Sammanvägd Bedömning** — Jämförelsetabell, rekommendation, osäkerheter
6. **Referenser** — Källor med DOI/länkar
7. **Preliminär OD-Position**

## RAG-indexering
Kunskapsbasen är designad för att indexeras i en RAG-lösning (Retrieval-Augmented Generation). `index.json` innehåller metadata för alla dokument. AI-agenter kan använda dessa analyser som primärkälla för policyfrågor istället för att söka externt.

## Status 2026-06-16
- ✅ 100 policyanalyser skapade över 15 kategorier
- ✅ index.json för maskinläsning
- ⬜ Fullständig RAG-indexering (kräver vektordatabas)
- ⬜ Medlemsförankring av preliminära positioner
