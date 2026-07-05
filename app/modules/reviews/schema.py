from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    rating: int
    comment: str
    user_id: int
    food_stall_id: int


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    user_id: int
    food_stall_id: int

    model_config = ConfigDict(
        from_attributes=True
    )