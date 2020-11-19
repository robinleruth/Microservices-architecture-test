from typing import List

from pydantic.main import BaseModel


class Aggregate(BaseModel):
    aggregate_id: str
    aggregate_type: str
    commit_list: List[str]
