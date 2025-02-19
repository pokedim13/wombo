from __future__ import annotations

from pydantic import BaseModel


class InputSpec(BaseModel):
    gen_type: str
    origin_device: str
    app_version: str
    style: int
    aspect_ratio_width: int
    aspect_ratio_height: int
    aspect_ratio: str
    prompt: str


class ResultItem(BaseModel):
    final: str


class TaskModel(BaseModel):
    id: str
    user_id: str
    state: str
    input_spec: InputSpec
    premium: bool
    created_at: str
    updated_at: str
    is_nsfw: bool
    photo_url_list: list[str]
    generated_photo_keys: list[str]
    result: ResultItem | None