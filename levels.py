# levels.py

# Aquí definimos todos los mapas del juego.
# Cada capa se describe por su 'type' (cómo se dibuja) y sus propiedades.
LEVEL_DATA = {
    "forest_zone": {
        "name": "Forest Zone",
        "thumbnail": "assets/backgrounds/forest-zone/forest_thumb.png",
        "layers": [
            # Capa 0: Cielo
            {"type": "solid_color", "color": (135, 206, 235)},
            # Capa 1: Nubes
            {
                "type": "circles",
                "color": (255, 255, 255, 180), # Nubes blancas semi-transparentes
                "speed": 0.1,
                "elements": [ # [x_relativo, y, radio]
                    [150, 100, 40], [200, 120, 50], [230, 100, 30],
                    [600, 150, 60], [660, 160, 70], [710, 150, 50],
                    [1000, 110, 45], [1050, 130, 55], [1080, 110, 35],
                ]
            },
            # Capa 2: Montañas lejanas (polígonos)
            {
                "type": "polygons",
                "color": (100, 120, 100), # Verde grisáceo
                "speed": 0.2,
                "elements": [ # Lista de puntos para cada polígono
                    [[0, 500], [200, 250], [400, 500]],
                    [[300, 500], [550, 200], [800, 500]],
                    [[700, 500], [900, 300], [1100, 500]],
                    [[1000, 500], [1250, 220], [1500, 500]],
                ]
            },
            # Capa 3: Troncos de árboles
            {
                "type": "rects", "color": (139, 69, 19), "speed": 0.6,
                "elements": [
                    [50, 350, 20, 150], [250, 380, 25, 120], [550, 320, 30, 180],
                    [900, 400, 20, 100], [1150, 360, 28, 140],
                ],
            },
            # Capa 4: Copas de los árboles
            {
                "type": "circles", "color": (34, 139, 34), "speed": 0.6,
                "elements": [ # [x_relativo, y, radio]
                    [60, 320, 40], [262, 340, 50], [565, 280, 60],
                    [910, 370, 45], [1164, 320, 55],
                ]
            },
            # Capa 5: Suelo
            {"type": "solid_rect", "color": (34, 139, 34), "speed": 1.0, "rect": [0, 500, 1280, 220]},
        ],
    },
    "desert_zone": {
        "name": "Desert Zone",
        "thumbnail": "assets/backgrounds/desert-zone/desert_thumb.png",
        "layers": [
            {"type": "solid_color", "color": (240, 230, 140)}, # Amarillo caqui
            # Sol
            {"type": "circles", "color": (255, 215, 0), "speed": 0.05, "elements": [[1000, 100, 80]]},
            # Pirámides lejanas
            {
                "type": "polygons", "color": (210, 180, 140), "speed": 0.15,
                "elements": [
                    [[200, 500], [400, 200], [600, 500]],
                    [[800, 500], [950, 250], [1100, 500]],
                ]
            },
            # Dunas
            {
                "type": "rects", "color": (210, 180, 140), "speed": 0.3,
                "elements": [[50, 350, 400, 150], [500, 300, 350, 200], [900, 380, 300, 120]],
            },
            # Cactus
            {
                "type": "rects", "color": (0, 100, 0), "speed": 0.8,
                "elements": [
                    [150, 420, 15, 80], [145, 440, 25, 10], # Cactus 1
                    [700, 450, 20, 50], [690, 460, 40, 10], # Cactus 2
                    [1100, 400, 18, 100], [1092, 420, 34, 12], # Cactus 3
                ]
            },
            # Suelo de arena
            {"type": "solid_rect", "color": (194, 178, 128), "speed": 1.0, "rect": [0, 500, 1280, 220]},
        ],
    },
    "cityspace_zone": {
        "name": "City Escape",
        "thumbnail": "assets/backgrounds/city-escape/city_thumb.png",
        "layers": [
            {"type": "solid_color", "color": (40, 40, 60)}, # Cielo nocturno
            # Estrellas
            {
                "type": "rects", "color": (255, 255, 224), "speed": 0.05,
                "elements": [
                    [100, 50, 2, 2], [250, 80, 1, 1], [400, 40, 2, 2], [550, 120, 1, 1],
                    [700, 60, 3, 3], [850, 150, 1, 1], [1000, 70, 2, 2], [1150, 130, 1, 1],
                ]
            },
            # Luna
            {"type": "circles", "color": (240, 240, 240), "speed": 0.1, "elements": [[200, 150, 60]]},
            # Edificios
            {
                "type": "rects", "color": (80, 80, 90), "speed": 0.2,
                "elements": [
                    [50, 150, 100, 350], [200, 200, 80, 300], [350, 100, 120, 400],
                    [600, 250, 90, 250], [800, 180, 150, 320], [1100, 220, 100, 280],
                ],
            },
            # Ventanas
            {
                "type": "rects", "color": (255, 255, 0, 150), "speed": 0.2,
                "elements": [
                    [60, 160, 20, 20], [90, 160, 20, 20], [60, 200, 20, 20], [90, 200, 20, 20],
                    [360, 120, 25, 40], [405, 120, 25, 40], [360, 180, 25, 40], [405, 180, 25, 40],
                    [810, 200, 30, 30], [860, 200, 30, 30], [810, 250, 30, 30], [860, 250, 30, 30],
                ]
            },
            # Carretera
            {"type": "solid_rect", "color": (50, 50, 50), "speed": 1.0, "rect": [0, 500, 1280, 220]},
        ],
    },
}
