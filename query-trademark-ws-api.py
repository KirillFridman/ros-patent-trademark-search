import asyncio
import json
import websockets
from pydantic import BaseModel, Field
from typing import List, Optional

# Define Pydantic models for request and response
class SearchQueryParameters(BaseModel):
    algorithm_id: int = 1
    search_kind_id: str = "fuzzy"
    join_words: bool = True
    use_edge_ngram: bool = False
    use_reversed_edge_ngram: bool = False
    split: bool = False
    algorithm_val: int = 2
    data_sources: List[str] = ["trademarks", "known_trademarks", "international_trademarks"]
    similar_letter: bool = False
    morphological: bool = False
    stopwords: bool = True
    translate: bool = False
    transliteration: bool = False
    languages: List[str] = []

class SearchQueryData(BaseModel):
    search_query: str
    parameters: SearchQueryParameters

class SearchQuery(BaseModel):
    data: SearchQueryData
    type: str = "search_letter"

class SearchData(BaseModel):
    query: SearchQuery
    filter: dict = {}
    info: str = "MTQuMTM3LjEzOS4xNjt1bmRlZmluZWQtdW5kZWZpbmVkLXVuZGVmaW5lZC11bmRlZmluZWQtdW5kZWZpbmVk"
    oisType: str = "trademarks"

class SearchRequest(BaseModel):
    method: str = "POST"
    service_name: str = "esi-search"
    service_path: str = "/api/v1/search"
    params: dict = {"page": 1, "size": 10}
    data: SearchData

class FileEntry(BaseModel):
    id: str
    file_link: Optional[str]
    file_name: Optional[str]
    #base64: Optional[str]
    sortOrder: Optional[int]

class SearchResultItem(BaseModel):
    object_uid: str
    ois_uid: str
    row_number: int
    oisType: int
    trademarkKind: int
    appellationType: int
    appl_number: Optional[str]
    appl_date: Optional[str]
    reg_number: Optional[str]
    reg_date: Optional[str]
    reg_publ_date: Optional[str]
    corr_address: Optional[str]
    priority_date: List[str]
    expiry_date: Optional[str]
    effective_date: Optional[str]
    holders: Optional[str]
    authors: Optional[str]
    status_code: Optional[str]
    tmk_kind: str
    #goods: str
    goods_classes: str
    mark_description_text: Optional[str]
    appl_description_text: Optional[str]
    appl_territory_name: Optional[str]
    open_registry_url: str
    appl_registry_url: str
    disclaimers: Optional[str]
    mark_image_colour: Optional[str]
    goodClasses: List[str]
    files: List[FileEntry]
    variant_files: Optional[str]

class SearchResponse(BaseModel):
    totalResult: int
    currentPage: int
    totalPages: int
    resultsPerPage: int
    data: List[SearchResultItem]

async def search_websocket():
    uri = "wss://searchplatform.rospatent.gov.ru/socket.io/?EIO=4&transport=websocket"
    async with websockets.connect(uri, ping_interval=None, max_size=150_000_000) as ws:
        # Send initial connection message
        msg = await ws.recv()
        print("Connected to WebSocket:", msg)

        await ws.send("40/search,")
        msg = await ws.recv()
        print("Search init:", msg)
        
        async def heartbeat():
            while True:
                msg = await ws.recv()
                if msg == "2":
                    await ws.send("3")
                    print("Heartbeat sent")
                elif msg.startswith("42/search,"):
                    _, json_data = msg.split("42/search,", 1)
                    try:
                        response = json.loads(json_data)
                        if (response[0] == "send_results"):
                            #print("Received search response:", response[1])
                            search_response = SearchResponse(**(response[1]))
                            print("Received search response records:", len(search_response.data))
                            print("-------------- Received search response --------------\n", search_response.model_dump_json(indent=2))
                        else:
                            print("Received unknown response:", response[0])
                    except Exception as e:
                        print("Failed to parse response:", e)
                else:
                    print("Received unknown message:", msg)
                await asyncio.sleep(1)

        # Start heartbeat loop
        asyncio.create_task(heartbeat())
        
        # Prepare search request
        search_request = SearchRequest(
            data=SearchData(
                query=SearchQuery(
                    data=SearchQueryData(
                        search_query="милые курочки",
                        parameters=SearchQueryParameters()
                    )
                )
            )
        )
        search_message = f"42/search,{json.dumps(['send_task', search_request.model_dump()])}"
        await ws.send(search_message)
        print("-------------- Search query sent --------------\n", search_request.model_dump_json(indent=2))
        
        # Keep connection open to receive responses
        await asyncio.Future()

# Run the WebSocket client
asyncio.run(search_websocket())
