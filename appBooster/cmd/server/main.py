from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.schemas.experiment import ExperimentResponse, StatisticsResponse
from internal.db.connection import get_db
from internal.db.migrations import run_migrations
from internal.experiments.manager import ExperimentManager

app = FastAPI(title='AB Testing API', version='1.0.0')

base_dir = Path(__file__).parent.parent.parent
template_dir = base_dir / 'templates'
templates = Jinja2Templates(directory=str(template_dir))


@app.on_event('startup')
def startup():
    run_migrations()
    _init_experiments()


def _init_experiments():
    db = next(get_db())
    try:
        from internal.models.experiment import Experiment, ExperimentOption

        button_color_exp = db.query(Experiment).filter(Experiment.key == 'button_color').first()
        if not button_color_exp:
            button_color_exp = Experiment(key='button_color')
            db.add(button_color_exp)
            db.commit()

            options = [
                ExperimentOption(experiment_key='button_color', value='#FF0000', weight=33),
                ExperimentOption(experiment_key='button_color', value='#00FF00', weight=33),
                ExperimentOption(experiment_key='button_color', value='#0000FF', weight=34),
            ]
            for opt in options:
                db.add(opt)
            db.commit()

        price_exp = db.query(Experiment).filter(Experiment.key == 'price').first()
        if not price_exp:
            price_exp = Experiment(key='price')
            db.add(price_exp)
            db.commit()

            options = [
                ExperimentOption(experiment_key='price', value='10', weight=75),
                ExperimentOption(experiment_key='price', value='20', weight=10),
                ExperimentOption(experiment_key='price', value='50', weight=5),
                ExperimentOption(experiment_key='price', value='5', weight=10),
            ]
            for opt in options:
                db.add(opt)
            db.commit()
    finally:
        db.close()


@app.get('/api/v1/experiments', response_model=ExperimentResponse)
def get_experiments(device_token: str = Header(..., alias='Device-Token'), db: Session = Depends(get_db)):
    if not device_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Device-Token header is required')

    manager = ExperimentManager(db)
    experiments = manager.get_experiments_for_device(device_token)

    return ExperimentResponse(**experiments)


@app.get('/api/v1/statistics', response_model=list[StatisticsResponse])
def get_statistics(db: Session = Depends(get_db)):
    manager = ExperimentManager(db)
    stats = manager.get_statistics()
    return [StatisticsResponse(**stat) for stat in stats]


@app.get('/statistics', response_class=HTMLResponse)
def statistics_page(request: Request, db: Session = Depends(get_db)):
    manager = ExperimentManager(db)
    stats = manager.get_statistics()
    return templates.TemplateResponse('statistics.html', {'request': request, 'statistics': stats})
