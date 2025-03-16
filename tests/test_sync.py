from wombo import Dream, models

dream = Dream()

def test_generate() -> None:
    dream.Auth.new_auth_key()
    assert isinstance(dream.generate("anime waifu"), models.TaskModel)

def test_styles() -> None:
    assert isinstance(dream.Style.get_styles(), models.ArtStyleModel)