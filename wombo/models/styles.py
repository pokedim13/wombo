from pydantic import BaseModel, Field, RootModel
from typing import List


class ArtStylesModel(BaseModel):
	id: int
	name: str
	is_visible: bool
	created_at: str
	updated_at: str
	deleted_at: None = None
	photo_url: str
	is_premium: bool
	type_model: str = Field(alias="model_type")
	is_new: bool
	supports_input_images: bool
	blurDataURL: str


class StyleModel(RootModel):
	root: List[ArtStylesModel]
