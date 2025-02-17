# Rospatent Web-socket API

## Link
wss://searchplatform.rospatent.gov.ru/socket.io/?EIO=4&transport=websocket

## Messages

- Initiate request/reply

```json
40/search,
```

```json
40/search,{"sid":"P7IxDfhudz7K1roqHNOo"}
```

- Heartbeat

if message "2" received, reply with "3"

- Search request/reply

```json
42/search,
[
  "send_task",
  {
    "method": "POST",
    "service_name": "esi-search",
    "service_path": "/api/v1/search",
    "params": {
      "page": 1,
      "size": 10
    },
    "data": {
      "query": {
        "data": {
          "search_query": "test",
          "parameters": {
            "algorithm_id": 1,
            "search_kind_id": "fuzzy",
            "join_words": true,
            "use_edge_ngram": false,
            "use_reversed_edge_ngram": false,
            "split": false,
            "algorithm_val": 2,
            "data_sources": [
              "trademarks",
              "known_trademarks",
              "international_trademarks"
            ],
            "similar_letter": false,
            "morphological": false,
            "stopwords": true,
            "translate": false,
            "transliteration": false,
            "languages": []
          }
        },
        "type": "search_letter"
      },
      "filter": {},
      "info": "MTQuMTM3LjEzOS4xNjt1bmRlZmluZWQtdW5kZWZpbmVkLXVuZGVmaW5lZC11bmRlZmluZWQtdW5kZWZpbmVk",
      "oisType": "trademarks"
    }
  }
]
````

```json
42/search,
[
  "send_results",
  {
    "totalResult": 3436,
    "currentPage": 1,
    "totalPages": 3436,
    "resultsPerPage": 1,
    "data": [
      {
        "object_uid": "fc8d4ce6-a8f4-11ee-90dd-0242ac110002",
        "ois_uid": "fc8f99a6-a8f4-11ee-90dd-0242ac110002",
        "row_number": 1,
        "oisType": 1,
        "trademarkKind": 2,
        "appellationType": 0,
        "appl_number": "2023832699",
        "appl_date": "2023-12-29T00:00:00",
        "reg_number": null,
        "reg_date": null,
        "reg_publ_date": null,
        "corr_address": "119121, Москва, 1-й Тружеников переулок,12 строение 3, Правовой департамент ООО Центр защиты товарных знаков, Карпов Александр Владимирович",
        "priority_date": [],
        "expiry_date": null,
        "effective_date": null,
        "holders": "Крылов Илья Валерьевич",
        "authors": null,
        "status_code": "8",
        "tmk_kind": "Заявка",
        "goods": "03 - абразивы; амбра....",
        "goods_classes": "03; 29; 30; 35; 41; 43; 44",
        "mark_description_text": "TEST",
        "appl_description_text": null,
        "appl_territory_name": null,
        "open_registry_url": "",
        "appl_registry_url": "https://www.fips.ru/registers-doc-view/fips_servlet?DB=RUTMAP&DocNumber=2023832699&TypeFile=html",
        "disclaimers": null,
        "mark_image_colour": null,
        "goodClasses": [
          "03",
          "29",
          "30",
          "35",
          "41",
          "43",
          "44"
        ],
        "files": [
          {
            "id": "fd164b54-a8f4-11ee-90dd-0242ac110002",
            "file_link": "/mnt/nfs/data/datamart/2023/12/29/fc8d4ce6a8f411ee90dd0242ac110002/fce8f21ca8f411ee90dd0242ac110002/TRADEMARK_IMAGE/fd164cc6a8f411ee90dd0242ac110002_1_01961500.JPG",
            "file_name": "fd164cc6a8f411ee90dd0242ac110002_1_01961500.JPG",
            "base64": "",
            "sortOrder": 0
          }
        ],
        "variant_files": null
      }
    ]
  }
]

```


