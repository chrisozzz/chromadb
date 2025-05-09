import chromadb
import requests


#7OOYZDM6H53OW8L8

def get_earnings_call_transcript(ticker: str, quarter: str) -> dict|None:


#format
# 
# {
#     "symbol": ,
#     "quarter": ,
#     "transcript": [
#         {
#             "speaker": "",
#             "title": "",
#             "content": "",
#             "sentiment": ""
#         }, 
# 

    query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={quarter}&apikey=7OOYZDM6H53OW8L8'

    response = requests.get(query_url)

    if response.status_code != 200:
        print(f"Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

    else:
        data: dict = response.json()
        
    
    try:
        transcript_dict: dict = data["transcript"]

    except Exception as e:
        #print(f"No transcript found. Probably API rate limit exceeded.")
        return None

    if len(transcript_dict) == 0:
        return None

    return transcript_dict


def add_transcript_to_chroma(ticker, quarter, transcript: dict) -> None:
    


    documents = []
    metadatas = []
    ids = []

    if transcript is None:
        print(f"No transcript found for {ticker} in quarter {quarter}.")
        return

    for i, entry in enumerate(transcript):
         speaker: str = entry["speaker"]
         speaker_title: str = entry["title"]
         content: str = entry["content"]
         sentiment: str = entry["sentiment"]

         documents.append(content)
         metadatas.append({"speaker": speaker, "title": speaker_title, "sentiment": sentiment})
         ids.append(f"{ticker}_{quarter}_{i}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Added {len(documents)} entries to ChromaDB for {ticker} in quarter {quarter}.")
    return None

if __name__ == "__main__":
    client = chromadb.PersistentClient()
    collection = client.get_or_create_collection("database")

    #Top 20 tickers added;
    #TODO: make it so it doesn't add double entries
    #TODO: get the quarter dynamically so we can use that on new tickers

    tickers = ["MSFT", "NVDA", "AMZN", "GOOG", "2222.SR",
               "META", "BRK-B", "AVGO", "TSLA", "TSM",
               "WMT", "JPM", "LLY", "V", "TCEHY", 
               "MA", "NFLX", "XOM", "COST"]
    quarters = ["2025Q3", "2025Q4", "2025Q1", "2025Q1", "2024Q4",
                "2025Q1", "2024Q4", "2025Q2", "2025Q1", "2025Q1",
                "2025Q4", "2025Q1", "2025Q1", "2025Q2", "2024Q4",
                "2025Q1", "2025Q1", "2025Q1", "2025Q2"]
    
    for ticker, quarter in zip(tickers, quarters):
        print(f"Processing {ticker} for quarter {quarter}...")
        transcript = get_earnings_call_transcript(ticker, quarter)
        add_transcript_to_chroma(ticker, quarter, transcript)

    need_to_add = ["2222.SR", "BRK-B", "AVGO", "TCEHY"]



    # query = "financial performance"
    # results = collection.query(
    #     query_texts=[query],
    #     n_results=1
    # )
    # print("\nExample query results for 'financial performance' in AAPL transcripts:")
    # print(results)