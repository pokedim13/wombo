from pydantic import BaseModel, Field, RootModel


class StyleModel(BaseModel):
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
	blur_data_url: str = Field(..., alias="blurDataURL")


class ArtStyleModel(RootModel):
	root: list[StyleModel]