import asyncio

from wombo import AsyncDream, Dream


async def main() -> None:
    dream = Dream()
    async_dream = AsyncDream()
    # print(dream.style.get_styles())
    # print(await async_dream.style.get_styles())

    # print(await async_dream.auth._new_auth_key())
    dream.auth._get_auth_key()
    # print(dream.api.create_task("anime waifu"))
    print(dream.generate("anime waifu"))


asyncio.run(main())