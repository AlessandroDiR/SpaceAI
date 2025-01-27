# SpaceAI

Elaborato soggetto ad esame per il corso "Laboratorio di Ottimizzazione, Intelligenza Artificiale e Machine Learning".

Università di Bologna  
Corso di laurea: Tecnologie dei Sistemi Informatici

## Obiettivo del progetto

Questo progetto porta un caso di NLP in cui l'obiettivo è creare un modello basato su una rete neurale sequenziale (seq2seq) a supporto di un'applicazione di prenotazione di asset aziendali. Il compito del modello è quello estrarre informazioni strutturate da comandi o frasi di input in linguaggio naturale. Ad esempio:

Input
```
"Prenota la sala riunioni domani dalle 10 a mezzogiorno"
```

Output
```json
{
  "asset": "sala riunioni",
  "start": "2025-01-23T10:00:00",
  "end": "2025-01-23T12:00:00"
}
```

## 📦 Struttura repository

- ⚙️ Config  
contiene un json di configurazione e il relativo json-shema con i parametri utili all'addestraemento

- 💾 Datasets  
raccolta dei dataset di train, test e validation generati sinteticamente

- 📚 Lib  
contiene le classi utili alla generazione di dati sintetici

- 🎁 Out  
contiene i modelli salvati

- ✨ SpaceAI.ipynb  
Notebook per l'addestramento e test del modello

## Utilizzo
> ⚠️ **Compatibilità**: accertarsi che le versioni dei pacchetti di torch e torchtext siano compatibili con la tra loro e con la versione di Python installata. Fare riferimento alla tabella sottostante. Maggiori dettagli [qui.](https://pypi.org/project/torchtext/)

| PyTorch | Torchtext | Python |
| ------- | --------- | ------- |
| 2.2.0 | 0.17.0 | >=3.8, <=3.11 |
Pyhton <= 3.11 per compatibilità con torchtext

Dopo aver clonato (o scaricato) il repository aprire il notebook ed eseguire i blocchi nell'ordine elencato