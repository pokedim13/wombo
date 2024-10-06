from wombo import AsyncDream, models

import pytest

dream = AsyncDream()

@pytest.mark.asyncio
async def test_generate():
    assert isinstance(await dream.generate("anime waifu"), models.TaskModel)

@pytest.mark.asyncio
async def test_styles():
    assert isinstance(await dream.style._get_styles(), models.StyleModel)
    assert dream.style["Dreamland v3"] == 115