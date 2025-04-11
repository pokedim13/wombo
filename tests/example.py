from wombo import Dream

dream = Dream()
dream.Auth.new_auth_key()

with open("assets/example.png", "wb") as file:
    res = dream.generate("Anime waifu, see rain in window")
    file.write(dream._client.get(res.result.final).content)