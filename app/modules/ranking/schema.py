from pydantic import BaseModel


class RankingResponse(BaseModel):
    id: int
    name: str
    location: str
    average_rating: float
    bayesian_score: float
    total_reviews: int