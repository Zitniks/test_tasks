"""FastAPI application: AB Testing API."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.schemas.experiment import ExperimentResponse, StatisticsResponse
from internal.db.connection import get_db
from internal.db.migrations import run_migrations
from internal.experiments.manager import ExperimentManager

base_dir = Path(__file__).parent.parent.parent
template_dir = base_dir / 'templates'
templates = Jinja2Templates(directory=str(template_dir))


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(title='AB Testing API', version='1.0.0', lifespan=lifespan)


@app.get(
    '/api/v1/experiments',
    response_model=ExperimentResponse,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'description': 'Device-Token header is missing'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Internal server error'},
    },
)
async def get_experiments(
    device_token: str = Header(..., alias='Device-Token'),
    db: Session = Depends(get_db),
):
    manager = ExperimentManager(db)
    experiments = manager.get_experiments_for_device(device_token)
    return ExperimentResponse(**experiments)


@app.get(
    '/api/v1/statistics',
    response_model=list[StatisticsResponse],
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Internal server error'}},
)
async def get_statistics(db: Session = Depends(get_db)):
    manager = ExperimentManager(db)
    stats = manager.get_statistics()
    return [StatisticsResponse(**stat) for stat in stats]


@app.get(
    '/statistics',
    response_class=HTMLResponse,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Internal server error'}},
)
async def statistics_page(request: Request, db: Session = Depends(get_db)):
    manager = ExperimentManager(db)
    stats = manager.get_statistics()
    return templates.TemplateResponse('statistics.html', {'request': request, 'statistics': stats})
