from __future__ import annotations

from pydantic import BaseModel


class InputSpec(BaseModel):
    """Спецификация входных данных для задачи генерации."""
    gen_type: str
    origin_device: str
    app_version: str
    style: int
    aspect_ratio_width: int
    aspect_ratio_height: int
    aspect_ratio: str
    prompt: str


class ResultItem(BaseModel):
    """Результат выполнения задачи."""
    final: str


class TaskModel(BaseModel):
    """Модель задачи генерации изображения."""
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
    result: ResultItem | None = None