from pydantic import BaseModel, ConfigDict


class FoodStallCreate(BaseModel):
    name: str
    description: str
    location: str
    schedule: str
    phone: str
    owner_id: int


class FoodStallResponse(BaseModel):
    id: int
    name: str
    description: str
    location: str
    schedule: str
    phone: str
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )