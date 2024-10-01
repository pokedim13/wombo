from pydantic import BaseModel
from typing import Union, Optional, List


class ArtStylesModel(BaseModel):
	id: int
	name: str
	is_visible: bool
	created_at: str
	updated_at: str
	deleted_at: None = None
	photo_url: str
	is_premium: bool
	model_type: str
	is_new: bool
	supports_input_images: bool
	blurDataURL: str


class StyleModel(BaseModel):
	art_styles: List[ArtStylesModel]
