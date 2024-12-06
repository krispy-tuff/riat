import logging
from fastapi import FastAPI
from routes import router

logging.basicConfig(level=logging.INFO, filename='report_service.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Report Service")

app.include_router(router)