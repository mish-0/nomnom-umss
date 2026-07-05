from pydantic import BaseModel, ConfigDict


class MenuItemCreate(BaseModel):
    name: str
    price: float
    available: bool
    food_stall_id: int


class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    available: bool
    food_stall_id: int

    model_config = ConfigDict(
        from_attributes=True
    )