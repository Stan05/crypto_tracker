import uvicorn

def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """
    Starts the Uvicorn server to serve the API.
    """
    uvicorn.run(
        "crypto_tracker.api:app",  # Path to your FastAPI app
        host=host,
        port=port,
        reload=reload
    )