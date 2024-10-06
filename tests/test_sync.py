from wombo import Dream, models

dream = Dream()

def test_generate():
    assert isinstance(dream.generate("anime waifu"), models.TaskModel)

def test_styles():
    assert isinstance(dream.style._get_styles(), models.StyleModel)
    assert dream.style["Dreamland v3"] == 115