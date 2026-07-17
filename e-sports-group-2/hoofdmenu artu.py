import sdl2
import sdl2.ext
import random
import time
from wapens import Wapen, Speler

# Instellingen van het spel
window_width, window_height = 640, 480
line_speed = 3  # Snelheid van de bewegende zone
zone_width = 5  # Breedte van de zone (mes)

zonedot_width = 10
zonedot_height = 300

mes_width = 200
mes_height = 250
zone_height = 350  # Hoogte van de zone (200 pixels van 150 tot 350)
dot_count = 5  # Aantal stippen
dot_margin = 30  # Minimale afstand tussen de stippen
exit_button_rect = sdl2.SDL_Rect(10, 10, 60, 30)  # Positie en grootte van de Exit-knop
dots = []
score = 0
game_active = True
resources = sdl2.ext.Resources(__file__, "resources")

# Globale variabelen
zone_x = window_width // 2  # Startpositie van de zone
zone_direction = 1  # 1 voor naar rechts, -1 voor naar links
current_fish_index = 0  # Huidige visindex (0, 1, 2)

def generate_dots():
    global dots
    dots = []
    while len(dots) < dot_count:
        # Genereer een X-coördinaat tussen 200 en 500
        x = random.randint(200, 600)
        if all(abs(x - dot[0]) > dot_margin for dot in dots):  # Zorg voor voldoende afstand
            dots.append((x, window_height // 2))  # Y-coördinaat kan blijven zoals het is, bijvoorbeeld in het midden van het scherm


def render_game(renderer, background, mes_texture, fish_textures):
    """Teken de huidige spelstatus met vissen en stippellijnen."""
    # Wis het scherm en teken de achtergrondafbeelding
    renderer.clear()
    renderer.copy(background)  # Render de achtergrondafbeelding

    # Teken de stippellijnen (5px dik)
    for dot in dots:
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 140, 255)  # Kleur van de stippen
        # Teken de rechthoek bij de X-coördinaat van de stip, en laat de hoogte tussen 150 en 450 liggen
        zone_dot = sdl2.SDL_Rect(dot[0], 150, zonedot_width, zonedot_height)  # Verticaal tussen 150 en 450 pixels
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, zone_dot)

    # Teken de vis die momenteel geselecteerd is
    fish_rect = sdl2.SDL_Rect(-150 , -150, 1100, 1000)  # Positie voor de vis
    renderer.copy(fish_textures[current_fish_index], None, fish_rect)

    # Teken de lichtrode bewegende zone over de hoogte van 150-350 pixels
    zone_rect = sdl2.SDL_Rect(zone_x, 150, zone_width, zone_height)  # Verticaal tussen 150 en 350 pixels
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 0, 255)  # Lichtroze kleur
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, zone_rect)

    # Teken het mes boven de zone
    mes_rect = sdl2.SDL_Rect(zone_x, window_height-150, mes_width, 600-mes_height)  # Mes onderaan het scherm
    renderer.copy(mes_texture, None, mes_rect)

    # Teken de Exit-knop
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 0, 255)  # Rode kleur voor de knop
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)  # Witte kleur voor tekst
    sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, 15, 15, 55, 15)  # Simulatie van "Exit"-tekst

    sdl2.SDL_RenderPresent(renderer.sdlrenderer)


def check_cut():
    """Controleer of de zone van het mes een stip raakt."""
    global score
    for dot in dots:
        if zone_x <= dot[0] <= zone_x + zone_width:  # Controleer of de stip binnen de meszone valt
            print("Snijpunt! +1 punt")
            score += 1
            return True
    print("Geen snijpunt! Geen punten")
    return False


def select_fish(renderer, window, speler):
    global current_fish_index


    inventory = speler.inventory  # Verkrijg inventory van de speler
    print(f"Inventaris van speler: {inventory}")  # Print de inventory voor debugging

    required_fish_files = ['fish1Texture.png', 'fish2Texture.png', 'fish3Texture.png',
                           'fish4Texture.png']  # Alle vissen die beschikbaar moeten zijn
    fish_textures = []  # Lijst om de textures van vissen te bewaren

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    # Laad de afbeeldingen van alle vissen
    for fish in required_fish_files:
        try:
            fish_textures.append(factory.from_image(resources.get_path(fish)))
        except FileNotFoundError:
            print(f"Afbeelding voor {fish} ontbreekt. Controleer je resources.")

    num_fish = len(fish_textures)  # Aantal vissen dat we hebben geladen
    fish_rects = []
    spacing = 150
    start_x = (window_width - (num_fish * spacing)) // 2
    y_pos = window_height // 2 - 100

    # Plaats de rechthoeken voor de vis-afbeeldingen
    for i in range(num_fish):
        fish_rects.append(sdl2.SDL_Rect(start_x + i * spacing, y_pos, 120, 120))

    selected = 0
    selecting = True

    while selecting:
        # Verwerk input
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                selecting = False
                sdl2.SDL_Quit()
                exit()
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:  # Navigeer naar links
                    selected = (selected - 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:  # Navigeer naar rechts
                    selected = (selected + 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:  # Bevestig selectie
                    current_fish_index = selected
                    selecting = False
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x, y = event.button.x, event.button.y
                for i, rect in enumerate(fish_rects):
                    if rect.x <= x <= rect.x + rect.w and rect.y <= y <= rect.y + rect.h:
                        # Na klikken, controleer of de vis in de inventory zit
                        clicked_fish = required_fish_files[i]
                        found = False  # Indicator of we de vis hebben gevonden in de inventory

                        # Doorloop de inventory van de speler om te kijken of de vis er is
                        for item_name, quantity in inventory.items():
                            print(
                                f"Controleer {clicked_fish} tegen {item_name} met hoeveelheid {quantity}")  # Debugging output
                            if clicked_fish == item_name and quantity > 0:
                                found = True
                                break

                        if found:  # Vis gevonden in de inventory
                            current_fish_index = i  # Vis is geselecteerd, stel index in
                            selecting = False
                        else:
                            print(
                                f"{clicked_fish} is niet in de inventory!")  # Geef aan dat vis niet in de inventory zit

        # Render de vissen
        renderer.clear()
        for i, rect in enumerate(fish_rects):
            renderer.copy(fish_textures[i], None, rect)
            if i == selected:  # Highlight geselecteerde vis
                sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 0, 255)  # Gele rand
                sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, rect)
        renderer.present()

    print(f"Vis geselecteerd: {required_fish_files[current_fish_index]}")
    start_mini_game(renderer, window, clicked_fish)
    return True  # Keuze succesvol gemaakt


def start_mini_game(renderer, window, clicked_fish):
    global zone_x, zone_direction, game_active, score, current_fish_index, resources

    # Laad de achtergrondafbeelding en mesafbeelding
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    background_path = resources.get_path("snijplank_achtergrond.jpg")  # Achtergrond afbeelding
    background = factory.from_image(background_path)

    mes_path = resources.get_path("mes.png")  # Mesafbeelding
    mes_texture = factory.from_image(mes_path)

    # Laad de visafbeeldingen
    fish_paths = clicked_fish  # Vervang dit met je visafbeeldingen
    fish_texture = factory.from_image(resources.get_path(clicked_fish))

    generate_dots()
    last_time = time.time()

    while game_active:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                game_active = False
                break
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x, y = event.button.x, event.button.y
                if exit_button_rect.x <= x <= exit_button_rect.x + exit_button_rect.w and \
                        exit_button_rect.y <= y <= exit_button_rect.y + exit_button_rect.h:
                    # Exit-knop is ingedrukt
                    print("Terug naar home.")
                    game_active = False
                    return  # Verlaat de mini-game
                elif event.button.button == sdl2.SDL_BUTTON_LEFT:
                    if check_cut():
                        print(f"Huidige score: {score}")
                    else:
                        print(f"Geen punten. Huidige score: {score}")
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_SPACE:  # Druk op spatiebalk om van vis te wisselen
                    current_fish_index = (current_fish_index + 1) % len(fish_texture)  # Wissel vis

        # Update de mespositie (beperk tussen 150 en 650)
        current_time = time.time()
        if current_time - last_time > 0.01:  # Update elke 10 ms
            zone_x += line_speed * zone_direction
            if zone_x >= 650 - zone_width or zone_x <= 150:  # Zorg ervoor dat het mes tussen 150 en 650 beweegt
                zone_direction *= -1  # Verander richting bij rand

            last_time = current_time

        render_game(renderer, background, mes_texture, fish_texture)

    # Toon de eindscore
    print(f"Spel beëindigd! Totale score: {score}")


# Hoofdapplicatie instellen om start_mini_game zonder een apart venster te gebruiken
if __name__ == "__main__":
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    window = sdl2.SDL_CreateWindow(b"Vis Kiezen", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                                   window_width, window_height, sdl2.SDL_WINDOW_SHOWN)
    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    # Verwijzing naar de resource-map
    resources = sdl2.ext.Resources(__file__, "resources")

    # Start vis-selectiescherm
    select_fish(renderer, window)

    # Start het mini-spel met de gekozen vis
    start_mini_game(renderer, window)

    # Opruimen
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()