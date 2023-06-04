from __future__ import annotations

from typing import List, Any

from pydantic import BaseModel


class InputSpec(BaseModel):
    gen_type: str
    style: int
    prompt: str
    aspect_ratio_width: int
    aspect_ratio_height: int
    aspect_ratio: str


class CreateTask(BaseModel):
    id: str
    user_id: str
    state: str
    input_spec: InputSpec
    premium: bool
    created_at: str
    updated_at: str
    is_nsfw: bool
    photo_url_list: List
    generated_photo_keys: List
    result: Any
