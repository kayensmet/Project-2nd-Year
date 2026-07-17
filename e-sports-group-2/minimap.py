import sdl2.ext

kleuren = [
    sdl2.ext.Color(0, 0, 0),  # 0 = Zwart
    sdl2.ext.Color(255, 0, 0),  # 1 = Rood
    sdl2.ext.Color(0, 255, 0),  # 2 = Groen
    sdl2.ext.Color(0, 0, 255),  # 3 = Blauw
    sdl2.ext.Color(64, 64, 64),  # 4 = Donker grijs
    sdl2.ext.Color(128, 128, 128),  # 5 = Grijs
    sdl2.ext.Color(192, 192, 192),  # 6 = Licht grijs
    sdl2.ext.Color(255, 255, 255),  # 7 = Wit
]


def teken_minimap(renderer,speelwereld,p_speler_x,p_speler_y,sprites):
    minimap_schaal = 8  # De schaalverhouding tussen de wereld en de minimap
    minimap_grootte = 150  # Grootte van de minimap in pixels
    muur_kleur = kleuren[7]  # Witte muren op de minimap
    speler_kleur = kleuren[2]
    sprite_kleur = kleuren[1]# Rode speler op de minimap

    # Teken de muren van de minimap
    for y in range(len(speelwereld)):
        for x in range(len(speelwereld[0])):
            if speelwereld[y][x] > 0:  # Als er een muur is
                renderer.color = muur_kleur
                renderer.fill((x * minimap_schaal, y * minimap_schaal, minimap_schaal, minimap_schaal))

    # Teken de speler op de minimap
    renderer.color = speler_kleur
    speler_grootte = 5  # Dikte van de speler-markering op de minimap
    renderer.fill((
        int(p_speler_x * minimap_schaal - speler_grootte // 2),
        int(p_speler_y * minimap_schaal - speler_grootte // 2),
        speler_grootte, speler_grootte
    ))

    for sprite in sprites:
        renderer.color = sprite_kleur
        speler_grootte = 5  # Dikte van de speler-markering op de minimap
        renderer.fill((
            int(sprite.x * minimap_schaal - speler_grootte // 2),
            int(sprite.y * minimap_schaal - speler_grootte // 2),
            speler_grootte, speler_grootte
        ))


