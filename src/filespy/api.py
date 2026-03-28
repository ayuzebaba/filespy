from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from filespy.analyzer import count_lines, count_words, get_file_size, get_extension
from filespy.logger import get_logger
import os

logger = get_logger(__name__)

app = FastAPI(title="Filespy API", description="Analyze files via HTTP")

history = []


class AnalyzeRequest(BaseModel):
    filepath: str


class AnalyzeResponse(BaseModel):
    filename: str
    lines: int
    words: int
    size_kb: float
    extension: str
    analyzed_at: str


@app.get("/health")
def health():
    """Check if the server is running."""
    logger.info("Health check requested")
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    """Analyze a file and return its stats."""
    logger.info(f"Analyze requested for {request.filepath}")

    if not os.path.exists(request.filepath):
        logger.error(f"File not found: {request.filepath}")
        raise HTTPException(status_code=404, detail="File not found")

    result = AnalyzeResponse(
        filename=os.path.basename(request.filepath),
        lines=count_lines(request.filepath),
        words=count_words(request.filepath),
        size_kb=get_file_size(request.filepath),
        extension=get_extension(request.filepath),
        analyzed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    history.append(result)
    logger.info(f"Analysis complete for {request.filepath}")
    return result


@app.get("/history")
def get_history():
    """Return list of all files analyzed so far."""
    logger.info(f"History requested, {len(history)} records found")
    return {"total": len(history), "history": history}


@app.get("/ayuzehistory")
def get_history():
    """Return list of all files analyzed so far."""
    logger.info(f"History requested, {len(history)} records found")
    return {"AYODELE THE DEVELOPER IS SHOWING TOTAL =": len(history), "history": history}


@app.delete("/history")
def clear_history():
    """Clear the analysis history."""
    history.clear()
    logger.info("History cleared")
    return {"status": "history cleared"}

