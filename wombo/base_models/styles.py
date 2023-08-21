from __future__ import annotations
from typing import TYPE_CHECKING, Union
import httpx

from wombo.models.style import StyleModel

if TYPE_CHECKING:
    from wombo.api import AsyncDream, Dream


class Style:
    BASESTYLE = 84

    def __init__(self) -> None:
        self._styles = self._get_awaible_styles()

    def __getattr__(self, param: str):
        return self._styles.get(param.lower())

    def _get_awaible_styles(self) -> dict:
        res = self._get_styles()
        styles_dict = {}
        for style in res.pageProps.artStyles:
            if not style.is_premium:
                name = style.name.lower().replace(" ", "_")
                styles_dict[name] = style.id
        return styles_dict
    
    def _get_styles(self) -> StyleModel:
        res = httpx.get("https://dream.ai/_next/data/ddBu0LvpgvZcniN77Wr0h/create.json")
        return StyleModel.model_validate(res.json())

    def get_awaible_styles(self) -> dict:
        return self._styles