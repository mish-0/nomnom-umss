from pydantic import BaseModel, ConfigDict, Field



class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)  
    comment: str | None = None            
    food_stall_id: int


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str | None
    user_id: int
    food_stall_id: int

    model_config = ConfigDict(from_attributes=True)