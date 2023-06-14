from wombo.base_models import BaseDream
from wombo.api import Dream, AsyncDream

styles_list = {
    3: 'no_style', 
    9: 'psychic', 
    14: 'etching',
    16: 'wuhtercuhler', 
    17: 'provenance', 
    18: 'rose_gold', 
    22: 'ghibli', 
    28: 'melancholic', 
    31: 'toasty', 
    32: 'realistic', 
    34: 'arcane', 
    35: 'throwback', 
    36: 'daydream', 
    37: 'surreal', 
    38: 'ink', 
    39: 'pandora', 
    40: 'malevolent', 
    41: 'street_art', 
    42: 'unrealistic', 
    45: 'comic', 
    46: 'anime', 
    47: 'line_art', 
    48: 'gouache', 
    49: 'polygon', 
    50: 'paint', 
    52: 'hdr', 
    53: 'analogue', 
    54: 'retro_futurism', 
    55: 'isometric', 
    57: 'bad_trip', 
    58: 'cartoonist', 
    60: 'vector', 
    61: 'fantastical', 
    63: 'Spectral', 
    65: 'diorama', 
    67: 'abstract', 
    68: 'flora', 
    71: 'soft_touch', 
    72: 'winter', 
    73: 'festive', 
    74: 'splatter', 
    76: 'figure', 
    77: 'expressionism', 
    78: 'realistic_v2', 
    80: 'anime_v2', 
    81: 'flora_v2', 
    84: 'buliojourney_v2', 
    88: 'blues_v2', 
    91: 'watercolor_v2', 
    92: 'spectral_v2', 
    94: 'gloomy', 
    95: 'the_cut', 
    96: 'the_bulio_cut', 
    97: 'dreamwave_v2', 
    98: 'illustrated_v2', 
    99: 'abstract_fluid_v2'
}

class Style:
    def __init__(self, dream: BaseDream = None) -> None:
        self.dream = dream
    def __getattr__(self, param: str):
        if param.isupper():
            return list(styles_list.keys())[list(styles_list.values()).index(param.lower())]
        else:
            if self.dream is not None:
                if isinstance(self.dream, Dream):
                    def sync_func(text: str):
                        return self.dream.generate(text=text, style=list(styles_list.keys())[list(styles_list.values()).index(param.lower())])
                    return sync_func
                elif isinstance(self.dream, AsyncDream):
                    async def async_func(text: str):
                        return self.dream.generate(text=text, style=list(styles_list.keys())[list(styles_list.values()).index(param.lower())])
                    return async_func
                else:
                    return None
