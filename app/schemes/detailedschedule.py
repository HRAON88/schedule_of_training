from app.database.models.schedules import ScheduleModel


class ScheduleModelDetail(ScheduleModel):
    sport: str
    participants: int
