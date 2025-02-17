import asyncio
import time

from wombo import AsyncDream


async def main() -> None:
    async_dream = AsyncDream()
    start = time.perf_counter()
    await asyncio.gather(*[async_dream.generate("anime waifu") for _ in range(20)])
    print(time.perf_counter() - start)


asyncio.run(main())