import pytest

from wombo import AsyncDream, models

dream = AsyncDream()

@pytest.mark.asyncio
async def test_generate()-> None:
    await dream.Auth.new_auth_key()
    assert isinstance(await dream.generate("anime waifu"), models.TaskModel)

@pytest.mark.asyncio
async def test_styles() -> None:
    assert isinstance(await dream.Style.get_styles(), models.ArtStyleModel)