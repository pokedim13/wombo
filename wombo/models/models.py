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
	blurDataURL: str # noqa: N815


class StylesModel(RootModel):
	root: list[StyleModel]
	

##########

class TaskInputSpecModel(BaseModel):
	aspect_ratio_height: int
	aspect_ratio_width: int
	origin_device: str
	aspect_ratio: str
	app_version: str
	gen_type: str
	prompt: str
	style: int
	

class ResultModel(BaseModel):
	final: str


class TaskModel(BaseModel):
	id: str
	user_id: str
	is_nsfw: bool
	premium: bool
	created_at: str
	updated_at: str
	photo_url_list: list[str]
	result: ResultModel | None = None
	input_spec: TaskInputSpecModel
	generated_photo_keys: list[str]