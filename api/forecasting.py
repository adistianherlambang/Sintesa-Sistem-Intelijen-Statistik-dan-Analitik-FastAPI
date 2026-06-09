from fastapi import APIRouter
from controllers.forecasting_controller import ForecastRequest, handle_forecasting_request

router = APIRouter()

@router.post("/forecast")
async def get_forecast(body: ForecastRequest):
    """
    Endpoint to trigger ANN training and forecast values for a given city
    """
    return await handle_forecasting_request(body)
