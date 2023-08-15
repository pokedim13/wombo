from typing import Any, List, Optional

from pydantic import BaseModel


class ArtStyle(BaseModel):
    id: int
    name: str
    is_visible: bool
    created_at: str
    updated_at: str
    deleted_at: Any
    photo_url: str
    is_premium: bool
    model_type: str
    is_new: bool
    blurDataURL: str


class PageProps(BaseModel):
    artStyles: List[ArtStyle]


class StyleModel(BaseModel):
    pageProps: PageProps
    __N_SSG: bool