import json

def contesto_bollette():
    # Fix the JSON strings to be valid JSON objects
    train_data = [
        '{"INFORMAZIONI GENERALI": {\n'
        '    "PERIODO BOLLETTA": "Intervallo di competenza della bolletta, è formato da due date. Esempio: 01/07/2024 - 31/08/2024",\n'
        '    "COSTI TOTALI": "Totale in bolletta da pagare, identificabile di solito per la presenza della parola: \'Totale\'. In caso ci siano più totali, considera solo quello che non comprende prezzi come abbonamento TV o altri costi. Example: Totale bolletta 12,12. Output: float"\n'
        '}}',

        '{"DATI FORNITURA ELETTRICO": {\n'
        '    "INDIRIZZO": "Indirizzo contatore del cliente (solitamente inizia con via/p.zza) e numero civico",\n'
        '    "POD": "Codice univoco del contatore. Inizia con it seguito da stringa alfanumerica, lunghezza 13 o 14 caratteri",\n'
        '    "POTENZA IMPEGNATA": "Potenza impegnata espressa in kw",\n'
        '    "POTENZA DISPONIBILE": "Potenza disponibile espressa in kw. Maggiore o uguale a potenza impegnata",\n'
        '    "TIPOLOGIA OFFERTA": "Generalmente clienti domestici vulnerabili o non vulnerabili. Altre offerte riconoscibili per stringa placet",\n'
        '    "INIZIO OFFERTA": "Data di inizio condizioni economiche in formato dd-mm-yyyy",\n'
        '    "FINE OFFERTA": "Data di fine condizioni economiche in formato dd-mm-yyyy"\n'
        '}}',

        '{"CONSUMI FATTURATI ED EFFETTIVI": {\n'
        '    "CONSUMI FATTURATI": "Totale consumi pagati in fattura. Estrai solo il valore intero. Es: 18",\n'
        '    "CONSUMI EFFETTIVI": "Totale consumi reali. Estrai solo il valore intero. Es: 18"\n'
        '}}',

        '{"CONSUMI": {\n'
        '    "PERIODO": "Mese o abbreviazione del mese di competenza + anno. Esempi: Gen-2021, Feb-2021, Mar-2021, Apr-2021, Mag-2021, Giu-2021, Lug-2021, Set-2021, Ott-2021, Nov-2021, Dic-2021",\n'
        '    "TIPO": "Effettivo/Stimato",\n'
        '    "Fascia F1": "Es: 202",\n'
        '    "Fascia F2": "Es: 202",\n'
        '    "Fascia F3": "Es: 202"\n'
        '}}',

        '{"LETTURE": {\n'
        '    "PERIODO": "Mese o abbreviazione del mese di competenza + anno. Esempi: Gen-2021, Feb-2021, Mar-2021, Apr-2021, Mag-2021, Giu-2021, Lug-2021, Set-2021, Ott-2021, Nov-2021, Dic-2021",\n'
        '    "TIPO": "Effettivo/Stimato",\n'
        '    "Fascia F1": "Es: 202",\n'
        '    "Fascia F2": "Es: 202",\n'
        '    "Fascia F3": "Es: 202"\n'
        '}}',

        '{"NOME FORNITORE": "Nome dell\'ente fornitore di energia"}'
    ]

    return train_data
