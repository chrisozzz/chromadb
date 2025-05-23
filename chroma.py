import chromadb
import requests

#7OOYZDM6H53OW8L8

def add_ticker_to_chroma(ticker: str) -> None:
    transcript_dict: dict = {}
    year = 2025
    quarter = 1

    while len(transcript_dict) == 0 and transcript_dict is not None:

        query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={year}Q{quarter}&apikey=7OOYZDM6H53OW8L8'
        response = requests.get(query_url)

        if response.status_code != 200:
            print(f"Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

        else:
            data: dict = response.json()
            try:
                transcript_dict: dict = data["transcript"]

                if len(transcript_dict) == 0:
                    quarter -= 1
                    if quarter == 0:
                        quarter = 4
                        year -= 1

                    if year == 2024 and quarter < 3:
                        print(f"No transcript found for {ticker} in any recent quarter.")
                        return None
            
            except Exception as e:
                print(f"No transcript found for {ticker}. Probably API rate limit exceeded.")
                return None
            
    potential_id = f"{ticker}_0"
    
    if potential_id in collection.get(ids=[potential_id])["ids"]:
        print(f"{ticker} earnings call already exists in ChromaDB.")
    
    else:
        documents = []
        metadatas = []
        ids = []

        for i, entry in enumerate(transcript_dict):
            speaker: str = entry["speaker"]
            speaker_title: str = entry["title"]
            content: str = entry["content"]
            sentiment: str = entry["sentiment"]

            documents.append(content)
            metadatas.append({"speaker": speaker, "title": speaker_title, "sentiment": sentiment})
            ids.append(f"{ticker}_{i}")

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} entries to ChromaDB for {ticker} in quarter {year}Q{quarter}.")

    return None
            

    

if __name__ == "__main__":
    client = chromadb.PersistentClient()
    collection = client.get_or_create_collection("database")


    tickers = ["KO", "NDAQ", "PLTR", "GME", "TSM", "SMCI", 
               "RKLB", "RDDT", "BLK", "ORCL", "INTC", "CSCO",
               "AAPL", "MSFT", "HTZ", "NSANY", "TM", "RACE", 
               "GM", "HMC", "MTSUY", "^RUT", "^DJI", "^GSPC"]

    for ticker in tickers:
        add_ticker_to_chroma(ticker)


    # query = "is tesla ramping up production?"
    # results = collection.query(
    #     query_texts=[query],
    #     n_results=3
    # )
    # print("\nExample query results for 'financial performance of tesla' in all transcripts:")
    # print(results["documents"])