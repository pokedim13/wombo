from typing import List, Optional

from pydantic import BaseModel


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
	photo_url_list: List[str]
	result: Optional[ResultModel]
	input_spec: TaskInputSpecModel
	generated_photo_keys: List[str]
	

