from pydantic import BaseModel, Json


class ChangeMainPage(BaseModel):
    vacancy_name: str
    first_paragraph: str
    second_paragraph_name: str
    second_paragraph: str


class ChangeStatsPage(BaseModel):
    data: dict
