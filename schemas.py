from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier for the user")
    message: str = Field(..., description="User prompt or academic query")
    use_rag: bool = Field(default=False, description="Flag to enable vector database search")

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: Optional[List[str]] = Field(default=None, description="Retrieved RAG source files")

class DocumentUploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    status: str