import pytest

from wombo import AsyncDream, StylesModel, TaskModel

dream = AsyncDream()

@pytest.mark.asyncio
async def test_generate()-> None:
    assert isinstance(await dream.generate("anime waifu"), TaskModel)

@pytest.mark.asyncio
async def test_styles() -> None:
    assert isinstance(await dream.style.get_styles(), StylesModel)