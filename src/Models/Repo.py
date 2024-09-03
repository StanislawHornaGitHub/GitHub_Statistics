from pydantic import BaseModel

class Repo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    visibility: str
    created_at: str
    updated_at: str
    pushed_at: str