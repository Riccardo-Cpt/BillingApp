import json
import os
import ollama
import numpy as np
#import Code.ModelFunctions as mf
import modules.llm_functions
import modules.train_data
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


if __name__ == '__main__':
    texts_for_embedding = extract_context(td.contesto_bollette())

    embedding_array, input_text = compute_embeddings(texts_for_embedding)

    #query="dati fornitura via goffredo mameli 67 indirizzo 21040 - morazzone (va) pod it001e24245537 tipo cliente domestico non residente tensione di fornitura bassa tensione potenza impegnata 6,00 kw potenza disponibile 6,60 kw offerta stg domestici non vulnerabili codice offerta 000155envft00dxserv_tut_graduali data scadenza contratto contratto a tempo indeterminato data inizio condizioni economiche 01/07/2024 data fine condizioni economiche 31/12/9999 data inizio fornitura 01/07/2024 consumo da inizio fornitura 12 kwh (reale) (f1: 5 - f2: 3 - f3: 4) spesa annua sostenuta 34,89 € data inizio spesa annua 17/09/2024 data fine spesa annua 17/09/2024"
    #output = getRelevantChunksTesting(query, embedding_array, texts_for_embedding, top_k=1)

    print(embedding_array, input_text)