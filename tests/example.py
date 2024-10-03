from wombo import AsyncDream, Dream
import asyncio

async def main():
    dream = AsyncDream()
    print(await dream.generate("anime waifu"))


dream = Dream()
print(dream.generate("anime waifu"))
asyncio.run(main())