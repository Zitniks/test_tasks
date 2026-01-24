import random
from typing import Dict, List

from sqlalchemy.orm import Session

from internal.models.device import Device, DeviceExperiment
from internal.models.experiment import Experiment, ExperimentOption


class ExperimentManager:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_device(self, device_token: str) -> Device:
        device = self.db.query(Device).filter(Device.device_token == device_token).first()
        if not device:
            device = Device(device_token=device_token)
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
        return device

    def get_experiments_for_device(self, device_token: str) -> Dict[str, str]:
        device = self.get_or_create_device(device_token)
        device_first_seen = device.first_seen_at

        experiments = {}
        existing_assignments = self.db.query(DeviceExperiment).filter(
            DeviceExperiment.device_token == device_token
        ).all()

        existing_dict = {e.experiment_key: e.experiment_value for e in existing_assignments}

        all_experiments = self.db.query(Experiment).all()
        for exp in all_experiments:
            if exp.key in existing_dict:
                experiments[exp.key] = existing_dict[exp.key]
            elif exp.created_at <= device_first_seen:
                value = self._assign_experiment(device_token, exp.key)
                if value:
                    experiments[exp.key] = value

        return experiments

    def _assign_experiment(self, device_token: str, experiment_key: str) -> str | None:
        options = self.db.query(ExperimentOption).filter(
            ExperimentOption.experiment_key == experiment_key
        ).order_by(ExperimentOption.id).all()

        if not options:
            return None

        total_weight = sum(opt.weight for opt in options)
        if total_weight == 0:
            return None

        random_value = random.randint(1, total_weight)
        cumulative = 0

        for option in options:
            cumulative += option.weight
            if random_value <= cumulative:
                assignment = DeviceExperiment(
                    device_token=device_token,
                    experiment_key=experiment_key,
                    experiment_value=option.value
                )
                self.db.add(assignment)
                self.db.commit()
                return option.value

        return options[-1].value if options else None

    def get_statistics(self) -> List[Dict]:
        experiments = self.db.query(Experiment).all()
        stats = []

        for exp in experiments:
            options = self.db.query(ExperimentOption).filter(
                ExperimentOption.experiment_key == exp.key
            ).all()

            total_devices = self.db.query(DeviceExperiment).filter(
                DeviceExperiment.experiment_key == exp.key
            ).count()

            distribution = {}
            for option in options:
                count = self.db.query(DeviceExperiment).filter(
                    DeviceExperiment.experiment_key == exp.key,
                    DeviceExperiment.experiment_value == option.value
                ).count()
                percentage = round((count / total_devices * 100) if total_devices > 0 else 0, 2)
                distribution[option.value] = {
                    'count': count,
                    'weight': option.weight,
                    'percentage': percentage
                }

            stats.append({
                'experiment_key': exp.key,
                'total_devices': total_devices,
                'distribution': distribution
            })

        return stats
