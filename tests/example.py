from wombo import AsyncDream, Dream
import asyncio

async def main():
    dream = AsyncDream("eyJhbGciOiJSUzI1NiIsImtpZCI6IjhkNzU2OWQyODJkNWM1Mzk5MmNiYWZjZWI2NjBlYmQ0Y2E1OTMxM2EiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wYWludC1wcm9kIiwiYXVkIjoicGFpbnQtcHJvZCIsImF1dGhfdGltZSI6MTcyNzE4NzIyNSwidXNlcl9pZCI6IlRBeXZseU5FMmRSVlh3YmFDY1IyZGxZcmFhMDIiLCJzdWIiOiJUQXl2bHlORTJkUlZYd2JhQ2NSMmRsWXJhYTAyIiwiaWF0IjoxNzI4MTg3MTQwLCJleHAiOjE3MjgxOTA3NDAsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.pFLDKAIU7XaXdfPTEJQJFrKK-FE799Pooiw-KRUk2y6lHgu_GibSatUwp_TNVg1T3sXSLbKCgtlVVEZUfTtxD26ckuapQ7UX7zOtLOUg_Ou_QvWtgceoJOoLDX1voYhnz5gEX65nCLGvR5t39gqiqIHsAhHjYMLMk77JvB7dqy4x4t6KCFkJCs8mCN45pnVqQCmdixZvY0Ers20gTIk_mCqaD7x1H9Pba4OL5Ro3qZEjpz8O_4Bwm1IY4YBqJepk5idxJ_emVEjfufDOVL8HOHNJBqsoLWz02unumUSVHgJoHr5MZyLWeKVelaLpB6LdT-sCoJ4xtmARJb07j2is-A", debug=True)
    print(await dream.style._get_styles())
    print(len(dream.style.free.dict()))

asyncio.run(main())
