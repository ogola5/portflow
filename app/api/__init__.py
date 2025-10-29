from fastapi import APIRouter
from app.api import kpa, kra, cfs, truckers

router = APIRouter()
router.include_router(kpa.router, prefix="/kpa")
router.include_router(kra.router, prefix="/kra")
router.include_router(cfs.router, prefix="/cfs")
router.include_router(truckers.router, prefix="/truckers")
