from typing import List

from pydantic import BaseModel


class InputSpec(BaseModel):
    gen_type: str
    style: int
    prompt: str
    aspect_ratio_width: int
    aspect_ratio_height: int
    aspect_ratio: str


class Result(BaseModel):
    final: str


class CheckTask(BaseModel):
    id: str
    user_id: str
    state: str
    input_spec: InputSpec
    premium: bool
    created_at: str
    updated_at: str
    is_nsfw: bool
    photo_url_list: List[str]
    generated_photo_keys: List[str]
    result: Result = None
