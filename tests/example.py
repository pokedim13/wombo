from wombo import AsyncDream, Dream
import asyncio


dream = Dream()
styles = dream.style._get_styles()
print(dream.style["Dreamland v3"])
