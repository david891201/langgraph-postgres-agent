import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

from src.agents.graph import run_graph
from src.utils.utils import load_config, setup_logger
from src.utils.args_parser import parse_args


# Parse arguments
args = parse_args()

# Setup logging
app_home = os.environ.get('APP_HOME', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
log_dir = os.path.join(app_home, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logger = setup_logger(log_file)

# Load configuration
config = load_config(args.config, args.env)

logger.info(f"正在執行{os.path.basename(__file__)}")
logger.info(f"Using config from: {args.config}")
logger.info(f"Environment: {args.env}")
logger.info(f"Run date: {args.date}")

# pydantic verification
class InputQuery(BaseModel):
    user_query: str
    session_id: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定來源，例如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法，包括 OPTIONS
    allow_headers=["*"]
)

@app.post("/stock-qa")
async def stock_qa_handler (request: Request):
    try:
        body = await request.json()
        body = InputQuery(**body)  
        response = run_graph(config, user_input=body.user_query, session_id=body.session_id)
    except Exception as e:
        return JSONResponse(content={"error": f"{e}"}, status_code=400)       
    return response

logger.info("Job completed successfully")
    
if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=3000, reload=True)