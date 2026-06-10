from fastapi import APIRouter, BackgroundTasks
from controllers.forecasting_controller import ForecastRequest, handle_forecasting_request, handle_batch_forecasting_task

router = APIRouter()

@router.post("/forecast")
async def get_forecast(body: ForecastRequest):
    """
    Endpoint to trigger ANN training and forecast values for a given city
    """
    return await handle_forecasting_request(body)

@router.post("/forecast/batch")
async def trigger_batch_forecast(background_tasks: BackgroundTasks):
    """
    Endpoint to trigger background batch forecasting for all 150+ cities
    """
    background_tasks.add_task(handle_batch_forecasting_task)
    return {
        "status": "processing",
        "message": "Batch forecasting task has been started in the background."
    }

