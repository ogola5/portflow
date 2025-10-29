from fastapi import APIRouter
from app.api import kra, kpa, cfs, truckers

router = APIRouter()
router.include_router(kra.router)
router.include_router(kpa.router)
router.include_router(cfs.router)
router.include_router(truckers.router)
