# MOODY DATA QUERIES

La repo contiene 3 cartelle: 
- **data_raw**: ogni cartella dentro **data_raw** dovrebbe corrispondere a una cartella di Moody (eg: *ownership history*). Questa rimane la fonte originale dei dati (da non modificare)
- **queries**: ogni notebook in **queries** dovrebbe dare come output un file (stata, excel...) con dati processati
- **data_processed**: contiene i dati processati dalle queries. I dati vanno poi trasferiti su dropbox


## QUERIES
Al momento, le query estraggono dati delle imprese multinazionali europee. Nello specifico:
- **firmographics_processing**: crea dati 'intermedi' (da usare nelle altre query principali come intermediary tables), estraendo dai da *firmographics* per paese
- **guo_europee**: GUOs europei con subsidiaries mondiali
- **sub_europee**: SUBs europee con guos mondiali
- **sub_europee_ish**: Principali shareholders delle subsidiaries europee 
- **sub_balkans**: SUBs dei paesi balkans on guos mondiali

**DATI
**** Dati originali
Al momento, abbiamo 3 principali folders 
- **ownership_history**: contiene tutti i dati storici delle imprese mondiali per anno (identificativo: bvd number)
- **firmographics**: dati non storici su info varie (localizzaione, tipo impresa) e 'semi_storici' (per esempio: il n_employees viene registrto ogni anno in cui c'e' un cambiamento)
- **key_financials**: dati non storici su informazioni finanziarie

**** Dati intermedi
Ho creato una cartella con dati intermedi di *firmographics* in modo che i dati semi-storici siano pronti come dati storici (longitudinali) da usare nella query principale
eg: impresa X - n_employees - anno
    11111 -     100         - 2007
    11111 -     101         - 2007


### ESEMPIO QUERY
Questa query estrae i dati dei GUOs europei. 

- path: andra' inserito nella funzione che lancia la query come il path che contiene i dati storici (eg: data_raw/ownership_history/links_2007/...)
- TEMP_TABLE_FIRMOGRAPHICS: sono i dati intermedi di cui sopra. (Un altro modo sarebbe di crearli direttamente nella query, ma e' piu' difficile da ottimizzare)
- COUNTRY_KEY_FINANCIALS: estrae sul momento i dati di key_financials

La query fa, in sequenza:
1. Estrae tutti i dati storici da ownership_history e li divide per paese
2. Mergia i dati storici con i dati intermedi di firmographics
3. Mergia i dati storici con i key_financials

'''
        SELECT
            main.subsidiary_bvd_id,
            main.guo_25,
            firmographics_sub.nuts2 AS subsidiary_nuts2,
            firmographics_sub.nace_rev_2_core_code_4_digits_ AS subsidiary_nace4,
            firmographics_guo.nuts2 AS guo_nuts2,
            firmographics_guo.nace_rev_2_core_code_4_digits_ AS guo_nace4,
            firmographics_guo.type_of_entity AS guo_type_of_entity,
            firmographics_guo.status AS guo_status,
            {year} AS year,
            key_financials.number_of_employees AS guo_number_of_employees,
            key_financials.closing_date AS guo_closing_date
        FROM 
            '{path}' AS main
        LEFT JOIN 
            '{TEMP_TABLE_FIRMOGRAPHICS}' AS firmographics_sub
        ON 
            main.subsidiary_bvd_id = firmographics_sub.bvd_id_number
        LEFT JOIN
            '{TEMP_TABLE_FIRMOGRAPHICS}' AS firmographics_guo
        ON
            main.guo_25 = firmographics_guo.bvd_id_number
        LEFT JOIN 
            (SELECT * 
             FROM '{COUNTRY_KEY_FINANCIALS}'
             WHERE 
                year = {year}
            ) AS key_financials
        ON
            main.subsidiary_bvd_id = key_financials.bvd_id_number   -- CHANGE HERE FOR SUBS
        AND
            key_financials.year = {year}
        WHERE 
            main."type_of_relation" = 'GUO 25'
        AND 
            main."subsidiary_bvd_id" LIKE '{country}%'
    '''

GUO: Global Ultimate owner
SUBS: imprese sussidiarie