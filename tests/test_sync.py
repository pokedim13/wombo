from wombo import Dream, StylesModel, TaskModel

dream = Dream()

def test_generate() -> None:
    assert isinstance(dream.generate("anime waifu"), TaskModel)

def test_styles() -> None:
    assert isinstance(dream.style.get_styles(), StylesModel)