from fastapi import APIRouter, Depends
from src.modules.dashboard.dashboard_dto import DashboardCountsResponse
from src.modules.dashboard.dashboard_service import DashboardService

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@dashboard_router.get("/counts", response_model=DashboardCountsResponse)
async def get_dashboard_counts():
    dashboard_service = DashboardService()
    return dashboard_service.get_dashboard_counts() 