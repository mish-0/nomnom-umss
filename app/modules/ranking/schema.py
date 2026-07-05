from pydantic import BaseModel


class RankingResponse(BaseModel):
    id: int
    name: str
    average_rating: float
    total_reviews: int