from wireup.integration import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .apis import api_router
from .di import container

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register APIs
app.include_router(api_router)
fastapi.setup(container, app)
