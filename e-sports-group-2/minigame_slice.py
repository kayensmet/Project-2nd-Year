import sdl2
import sdl2.ext
import random
import time
import sys, os

"""from hoofdmenu import toon_huis"""
from wapens import Wapen, Speler
import sdl2.sdlmixer as mixer

# Instellingen van het spel
window_width, window_height = 640, 480
line_speed = 10  # Snelheid van de bewegende zone
zone_width = 5  # Breedte van de zone (mes)

zonedot_width = 200
zonedot_height = 350

mes_width = 200
mes_height = 250
zone_height = 350  # Hoogte van de zone (200 pixels van 150 tot 350)
dot_count = 5  # Aantal stippen
dot_margin = 30  # Minimale afstand tussen de stippen
exit_button_rect = sdl2.SDL_Rect(10, 10, 60, 30)  # Positie en grootte van de Exit-knop
dots = []
score = 0
game_active = True
game2_active = True

# Dynamisch pad berekenen voor resources
if getattr(sys, 'frozen', False):
    # PyInstaller-gecompileerde executable
    base_path = sys._MEIPASS
else:
    # Tijdens het ontwikkelen
    base_path = os.path.dirname(os.path.abspath(__file__))

resources_path = os.path.join(base_path, "resources")
resources = sdl2.ext.Resources(resources_path)


#resources = sdl2.ext.Resources(__file__, "resources")

# Globale variabelen
zone_x = window_width // 2  # Startpositie van de zone
zone_direction = 1  # 1 voor naar rechts, -1 voor naar links
current_fish_index = 0  # Huidige visindex (0, 1, 2)
current_sliced_fish_index = 0

def setup_audio():
    if mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 3, 4096) == -1:
        print("Fout bij het openen van het audiokanaal:", mixer.Mix_GetError())
    else:
        print("Audio correct geopend.")

def generate_dots():
    global xxx
    xxx = random.randint(300, 500)



def render_game(renderer, background, mes_texture, fish_textures):
    """Teken de huidige spelstatus met vissen en stippellijnen."""
    # Wis het scherm en teken de achtergrondafbeelding
    renderer.clear()
    renderer.copy(background)  # Render de achtergrondafbeelding



    # Stel de maximale grootte voor de vis in
    max_width = 600
    max_height = 400

    # Haal de breedte en hoogte van de vis af
    fish_width = fish_textures[0].size[0]  # Breedte van de vis
    fish_height = fish_textures[0].size[1]  # Hoogte van de vis

    # Bereken de schaalfactor om de vis binnen de maximale grootte te schalen
    scale_factor = min(max_width / fish_width, max_height / fish_height)

    # Pas de nieuwe breedte en hoogte van de vis aan
    new_width = int(fish_width * scale_factor)
    new_height = int(fish_height * scale_factor)


    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 140, 255)  # Kleur van de stippen
    zone_dot = sdl2.SDL_Rect(xxx, 150, zonedot_width, zonedot_height)  # Verticaal tussen 150 en 450 pixels
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, zone_dot)


    # Plaats de vis in het midden van het scherm (pas aan indien nodig)
    fish_rect = sdl2.SDL_Rect((window_width - new_width) // 2 + 100, (window_height - new_height) // 2+100, new_width, new_height)

    # Teken de vis met de nieuwe schaal
    renderer.copy(fish_textures[0], None, fish_rect)

    # Teken de stippellijnen (5px dik)



    # Teken de lichtrode bewegende zone over de hoogte van 150-350 pixels
    zone_rect = sdl2.SDL_Rect(zone_x, 150, zone_width, zone_height)  # Verticaal tussen 150 en 350 pixels
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 0, 255)  # Lichtroze kleur
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, zone_rect)

    # Teken het mes boven de zone
    mes_rect = sdl2.SDL_Rect(zone_x, window_height-150, mes_width, 600-mes_height)  # Mes onderaan het scherm
    renderer.copy(mes_texture, None, mes_rect)

    # Teken de Exit-knop
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 0, 255)  # Rode kleur voor de knop
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)  # Vul de knop met rood

    # Teken de witte rand van de knop
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)
    sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, exit_button_rect)

    # Teken een witte "X" op de knop
    sdl2.SDL_RenderDrawLine(renderer.sdlrenderer,
                            exit_button_rect.x + 10, exit_button_rect.y + 10,
                            exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + exit_button_rect.h - 10)
    sdl2.SDL_RenderDrawLine(renderer.sdlrenderer,
                            exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + 10,
                            exit_button_rect.x + 10, exit_button_rect.y + exit_button_rect.h - 10)

    # Laat de Exit-knop zien
    sdl2.SDL_RenderPresent(renderer.sdlrenderer)



def check_cut():
    """Controleer of er correct is geklikt terwijl de bewegende lijn over de brede zone gaat."""
    global score

    # Controleer of de bewegende lijn de brede zone kruist
    if xxx <= zone_x <= xxx + zonedot_width:
        print("Correct geklikt! +1 punt")
        score += 1
        return True
    else:
        print("Te vroeg of te laat geklikt. Geen punten.")
        return False


def select_fish(renderer, window, speler):
    global current_fish_index


    inventory = speler.inventory  # Verkrijg inventory van de speler
    print(f"Inventaris van speler: {inventory}")  # Print de inventory voor debugging

    # Bestandspaden van vereiste bronnen
    background_image_file = 'select_fish_background.png'  # Voeg hier je achtergrondafbeelding toe
    required_fish_files = ['fish1Texture.png', 'fish2Texture.png', 'fish3Texture.png', 'fish4Texture.png']

    fish_textures = []

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    # Laad de achtergrondafbeelding
    try:
        background_texture = factory.from_image(resources.get_path(background_image_file))
    except FileNotFoundError:
        print(f"Achtergrondafbeelding ontbreekt. Controleer je resources.")
        return False

    # Laad de afbeeldingen van alle vissen
    for fish in required_fish_files:
        try:
            fish_textures.append(factory.from_image(resources.get_path(fish)))
        except FileNotFoundError:
            print(f"Afbeelding voor {fish} ontbreekt. Controleer je resources.")

    num_fish = len(fish_textures)
    fish_rects = []
    spacing = 155
    start_x = 170 + (window_width - (num_fish * spacing)) // 2
    y_pos = 375

    for i in range(num_fish):
        fish_rects.append(sdl2.SDL_Rect(start_x + i * spacing, y_pos, 120, 120))

    # Exit-knop instellingen (linker bovenhoek)
    exit_button_rect = sdl2.SDL_Rect(10, 10, 80, 40)

    selected = 0
    selecting = True
    nietgenoegvis = factory.from_image(resources.get_path('fout_bij_chop.png'))
    while selecting:
        # Verwerk input
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                selecting = False
                sdl2.SDL_Quit()
                exit()
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    selected = (selected - 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    selected = (selected + 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    current_fish_index = selected
                    selecting = False
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x, y = event.button.x, event.button.y
                if exit_button_rect.x <= x <= exit_button_rect.x + exit_button_rect.w and \
                        exit_button_rect.y <= y <= exit_button_rect.y + exit_button_rect.h:
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                    print("Exit-knop ingedrukt. Terug naar vorige scherm.")
                    return False  # Terug naar vorige scherm
                for i, rect in enumerate(fish_rects):
                    if rect.x <= x <= rect.x + rect.w and rect.y <= y <= rect.y + rect.h:
                        clicked_fish = required_fish_files[i]
                        if inventory.get(clicked_fish, 0) > 0:
                            current_fish_index = i
                            selecting = False
                        else:
                            print(f"{clicked_fish} is niet in de inventory!")
                            render_fail(renderer, nietgenoegvis)

        # Render de achtergrond
        renderer.clear()
        renderer.copy(background_texture, None, None)  # Render de volledige achtergrond

        # Render de vissen
        for i, rect in enumerate(fish_rects):
            renderer.copy(fish_textures[i], None, rect)
            fish_name = required_fish_files[i]
            if inventory.get(fish_name, 0) > 0:  # Controleer of de vis in de inventory zit
                sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 0, 255)  # Gele rand
                sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, rect)

        # Render de Exit-knop
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 200, 0, 0, 255)  # Rode knop
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)  # Vul de rechthoek
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)  # Witte rand
        sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, exit_button_rect)  # Rand van de knop

        # Teken een "X" op de knop (simuleert tekst)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + 10, exit_button_rect.y + 10,
                                exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + exit_button_rect.h - 10)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + 10,
                                exit_button_rect.x + 10, exit_button_rect.y + exit_button_rect.h - 10)

        renderer.present()

    print(f"Vis geselecteerd: {required_fish_files[current_fish_index]}")
    start_mini_game(renderer, window, speler, required_fish_files[current_fish_index])
    return True


def select_sliced_fish(renderer, window, speler, achtergrond, button):
    global current_sliced_fish_index

    inventory = speler.inventory  # Verkrijg inventory van de speler
    print(f"Inventaris van speler: {inventory}")  # Print de inventory voor debugging

    # Bestandspaden van vereiste bronnen
    background_image_file = 'select_fish_background.png'  # Voeg hier je achtergrondafbeelding toe
    required_fish_files = ['slicedfish1.png', 'slicedfish2.png', 'slicedfish3.png', 'slicedfish4.png']


    sliced_fish_textures = []

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    # Laad de achtergrondafbeelding
    try:
        background_texture = factory.from_image(resources.get_path(background_image_file))
    except FileNotFoundError:
        print(f"Achtergrondafbeelding ontbreekt. Controleer je resources.")
        return False

    # Laad de afbeeldingen van alle vissen
    for fish in required_fish_files:
        try:
            sliced_fish_textures.append(factory.from_image(resources.get_path(fish)))
        except FileNotFoundError:
            print(f"Afbeelding voor {fish} ontbreekt. Controleer je resources.")

    num_fish = len(sliced_fish_textures)
    fish_rects = []
    spacing = 155
    start_x = 170 + (window_width - (num_fish * spacing)) // 2
    y_pos = 375

    for i in range(num_fish):
        fish_rects.append(sdl2.SDL_Rect(start_x + i * spacing, y_pos, 120, 120))

    # Exit-knop instellingen (linker bovenhoek)
    exit_button_rect = sdl2.SDL_Rect(10, 10, 80, 40)

    selected = 0
    selecting = True

    nietgenoegtexture = factory.from_image(resources.get_path('not_enough_inv.png'))
    while selecting:
        # Verwerk input
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                selecting = False
                sdl2.SDL_Quit()
                exit()
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    selected = (selected - 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    selected = (selected + 1) % num_fish
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    current_sliced_fish_index= selected
                    selecting = False
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x, y = event.button.x, event.button.y
                if exit_button_rect.x <= x <= exit_button_rect.x + exit_button_rect.w and \
                        exit_button_rect.y <= y <= exit_button_rect.y + exit_button_rect.h:
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                    print("Exit-knop ingedrukt. Terug naar vorige scherm.")
                    return False  # Terug naar vorige scherm
                for i, rect in enumerate(fish_rects):
                    if rect.x <= x <= rect.x + rect.w and rect.y <= y <= rect.y + rect.h:
                        clicked_sliced_fish = required_fish_files[i]
                        if inventory.get(clicked_sliced_fish, 0) > 0 and speler.has_item('rollebolle.png') and speler.has_item('rijst.png'):
                            current_sliced_fish_index = i
                            selecting = False
                        else:
                            print(f"{clicked_sliced_fish} is niet in de inventory!")
                            render_fail(renderer, nietgenoegtexture)

        # Render de achtergrond
        renderer.clear()
        renderer.copy(background_texture, None, None)  # Render de volledige achtergrond

        # Render de vissen
        for i, rect in enumerate(fish_rects):
            renderer.copy(sliced_fish_textures[i], None, rect)
            fish_name = required_fish_files[i]
            if inventory.get(fish_name, 0) > 0 and speler.has_item('rollebolle.png') and speler.has_item('rijst.png'):  # Controleer of de vis in de inventory zit
                sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 0, 255)  # Gele rand
                sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, rect)

        # Render de Exit-knop
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 200, 0, 0, 255)  # Rode knop
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)  # Vul de rechthoek
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)  # Witte rand
        sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, exit_button_rect)  # Rand van de knop

        # Teken een "X" op de knop (simuleert tekst)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + 10, exit_button_rect.y + 10,
                                exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + exit_button_rect.h - 10)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + 10,
                                exit_button_rect.x + 10, exit_button_rect.y + exit_button_rect.h - 10)

        renderer.present()

    print(f"Vis geselecteerd: {required_fish_files[current_sliced_fish_index]}")
    start_mini_game2(renderer, window, speler, required_fish_files[current_sliced_fish_index])
    return True

def start_mini_game2(renderer, window, speler, clicked_sliced_fish):
    global game2_active
    game2_active = True

    #speler.remove_from_inventory(clicked_sliced_fish, 1)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    #laad afbeeldingen
    minigame2_achtergrond_surf = sdl2.ext.load_image('resources/MiniGame2_background.png')
    nori_surf = sdl2.ext.load_image('resources/Sprites/rollebolle.png')
    rice_surf = sdl2.ext.load_image('resources/Sprites/rijst.png')
    sliced_fish_surf = sdl2.ext.load_image(resources.get_path(clicked_sliced_fish))
    fail_texture = factory.from_image(resources.get_path('fail.png'))


    #maak textures van de surfaces
    minigame2_achtergrond_text = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, minigame2_achtergrond_surf)
    nori_text = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, nori_surf)
    rice_text = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, rice_surf)
    sliced_fish_text = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, sliced_fish_surf)

    if clicked_sliced_fish == 'slicedfish1.png':
        plussuhi = factory.from_image(resources.get_path('plussushi1.png'))  # Laad de vis die geselecteerd is
        speler.remove_from_inventory(clicked_sliced_fish, 1)
        speler.remove_from_inventory('rollebolle.png',1)
        speler.remove_from_inventory('rijst.png', 1)
    elif clicked_sliced_fish == 'slicedfish2.png':
        plussuhi = factory.from_image(resources.get_path('plussushi2.png'))  # Laad de vis die geselecteerd is
        speler.remove_from_inventory(clicked_sliced_fish, 1)
        speler.remove_from_inventory('rollebolle.png', 1)
        speler.remove_from_inventory('rijst.png', 1)
    elif clicked_sliced_fish == 'slicedfish3.png':
        plussuhi = factory.from_image(resources.get_path('plussushi3.png'))  # Laad de vis die geselecteerd is
        speler.remove_from_inventory(clicked_sliced_fish, 1)
        speler.remove_from_inventory('rollebolle.png', 1)
        speler.remove_from_inventory('rijst.png', 1)
    elif clicked_sliced_fish == 'slicedfish4.png':
        plussuhi = factory.from_image(resources.get_path('plussushi4.png'))  # Laad de vis die geselecteerd is
        speler.remove_from_inventory(clicked_sliced_fish, 1)
        speler.remove_from_inventory('rollebolle.png', 1)
        speler.remove_from_inventory('rijst.png', 1)

    possible_x_positions = [200, 400, 600]

    # Willekeurige, unieke x-coördinaten toewijzen aan de knoppen
    x_positions = random.sample(possible_x_positions, 3)  # Kies 3 unieke posities

    NoriButton = sdl2.SDL_Rect(x_positions[0], 390, 100, 100)  # x, y, width, height
    RiceButton = sdl2.SDL_Rect(x_positions[1], 400, 100, 100)
    SlicedFishButton = sdl2.SDL_Rect(x_positions[2], 400, 100, 100)

    correct_order = ["nori", "rice", "sliced_fish"]
    click_sequence = []

    def button_clicked(button_type):
        
        global game2_active
        click_sequence.append(button_type)

        # Als de volledige volgorde is aangeklikt, controleer deze
        if len(click_sequence) == len(correct_order):
            if click_sequence == correct_order:
                print("Gelukt!")
            else:
                print("Niet gelukt!")
            game2_active = False  # Stop de game
            return True
        return False

    # Hoofdgame-loop
    while game2_active:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                game2_active = False  # Stop de game als het venster gesloten wordt
                break

            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.button.x, event.button.y

                if exit_button_rect.x <= mouse_x <= exit_button_rect.x + exit_button_rect.w and exit_button_rect.y <= mouse_y <= exit_button_rect.y + exit_button_rect.h:
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                    print("Exit-knop ingedrukt. Terug naar vorige scherm.")
                    game2_active = False
                    break  # Terug naar vorige scherm


                # Check welke knop is aangeklikt
                if NoriButton[0] <= mouse_x <= NoriButton[0] + NoriButton[2] and NoriButton[1] <= mouse_y <= NoriButton[1] + NoriButton[3]:
                    button_clicked("nori")
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/pop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                elif RiceButton[0] <= mouse_x <= RiceButton[0] + RiceButton[2] and RiceButton[1] <= mouse_y <= RiceButton[1] + RiceButton[3]:
                    button_clicked("rice")
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/pop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                elif SlicedFishButton[0] <= mouse_x <= SlicedFishButton[0] + SlicedFishButton[2] and SlicedFishButton[1] <= mouse_y <= SlicedFishButton[1] + SlicedFishButton[3]:
                    button_clicked("sliced_fish")
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/pop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)

        # renderer.clear(sdl2.ext.Color(0, 0, 0))
        # Als de volledige volgorde is aangeklikt, controleer deze
        if len(click_sequence) == len(correct_order):
            if click_sequence == correct_order:
                makesushigeluid = mixer.Mix_LoadWAV(b'resources/audio/makesushi.mp3')
                mixer.Mix_PlayChannel(-1,makesushigeluid,0)
                print("Gelukt!")
                if clicked_sliced_fish == 'slicedfish1.png':
                    speler.add_to_inventory('sushiroll1.png', 1)
                elif clicked_sliced_fish == 'slicedfish2.png':
                    speler.add_to_inventory('sushiroll2.png', 1)
                elif clicked_sliced_fish == 'slicedfish3.png':
                    speler.add_to_inventory('Sushiroll3.png', 1)
                elif clicked_sliced_fish == 'slicedfish4.png':
                    speler.add_to_inventory('Sushiroll6.png', 1)
                render_popup(renderer, plussuhi)
                break
            else:
                print("Niet gelukt!")
                render_fail(renderer, fail_texture)
                break

        # Stop rendering als de game niet actief is
        if not minigame2_achtergrond_surf:
            raise RuntimeError("Kan de achtergrond niet laden!")
        if not nori_surf or not rice_surf or not sliced_fish_surf:
            raise RuntimeError("Kan een van de sprites niet laden!")

        # Controleer of de textures zijn aangemaakt
        if not minigame2_achtergrond_text or not nori_text or not rice_text or not sliced_fish_text:
            raise RuntimeError("Kan een van de textures niet aanmaken!")

        # Render alles in de game-loop
        # Reset de framebuffer elke frame
        renderer.clear()
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, minigame2_achtergrond_text, None, None)  # Achtergrond
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, nori_text, None, NoriButton)  # Nori knop
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, rice_text, None, RiceButton)  # Rice knop
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, sliced_fish_text, None, SlicedFishButton)  # Sliced Fish knop
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 200, 0, 0, 255)  # Rode knop
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)  # Vul de rechthoek
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)  # Witte rand
        sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, exit_button_rect)  # Rand van de knop

        # Teken een "X" op de knop (simuleert tekst)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + 10, exit_button_rect.y + 10,
                                exit_button_rect.x + exit_button_rect.w - 10,
                                exit_button_rect.y + exit_button_rect.h - 10)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer, exit_button_rect.x + exit_button_rect.w - 10,
                                exit_button_rect.y + 10,
                                exit_button_rect.x + 10, exit_button_rect.y + exit_button_rect.h - 10)
        renderer.present() # Wis het scherm

    # Cleanup na afloop van de game-loop
    renderer.clear()
    window.refresh()
    print("Mini-game 2 geëindigd.")

def start_mini_game(renderer, window, speler, clicked_fish):
    global zone_x, zone_direction, game_active, score, current_fish_index, resources
    setup_audio()
    game_active = True



    # Laad de achtergrondafbeelding en mesafbeelding
    speler.remove_from_inventory(clicked_fish, 1)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    background_path = resources.get_path("snijplank_achtergrond.jpg")  # Achtergrond afbeelding
    background = factory.from_image(background_path)

    mes_path = resources.get_path("mes.png")  # Mesafbeelding
    mes_texture = factory.from_image(mes_path)

    # Laad de visafbeelding op basis van de geselecteerde vis
    fish_texture = factory.from_image(resources.get_path(clicked_fish))  # Laad de vis die geselecteerd is

    if clicked_fish == 'fish1Texture.png':
        plusfish = factory.from_image(resources.get_path('plusslicedfish_1.png'))  # Laad de vis die geselecteerd is
    elif clicked_fish == 'fish2Texture.png':
        plusfish = factory.from_image(resources.get_path('plusslicedfish_2.png'))  # Laad de vis die geselecteerd is
    elif clicked_fish == 'fish3Texture.png':
        plusfish = factory.from_image(resources.get_path('plusslicedfish_3.png'))  # Laad de vis die geselecteerd is
    elif clicked_fish == 'fish4Texture.png':
        plusfish = factory.from_image(resources.get_path('plusslicedfish_4.png'))  # Laad de vis die geselecteerd is

    fail_texture = factory.from_image(resources.get_path('fail.png'))  # Laad de vis die geselecteerd is


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
                        chopgeluid= mixer.Mix_LoadWAV(b'resources/audio/273485-Bloody-Impact-Squirt-8.wav')
                        if not chopgeluid:
                            print('error kaka')
                        mixer.Mix_PlayChannel(-1,chopgeluid, 0)


                        print(f"Huidige score: {score}")
                        if clicked_fish == 'fish1Texture.png':
                            speler.add_to_inventory('slicedfish1.png',1)
                            print(speler.inventory)
                            render_popup(renderer, plusfish)  # Toon de pop-up
                            game_active = False
                        elif clicked_fish == 'fish2Texture.png':
                            speler.add_to_inventory('slicedfish2.png',1)
                            print(speler.inventory)
                            render_popup(renderer, plusfish)  # Toon de pop-up
                            game_active = False
                        elif clicked_fish == 'fish3Texture.png':
                            speler.add_to_inventory('slicedfish3.png',1)
                            print(speler.inventory)
                            render_popup(renderer, plusfish)  # Toon de pop-up
                            game_active = False
                        elif clicked_fish == 'fish4Texture.png':
                            speler.add_to_inventory('slicedfish4.png',1)
                            print(speler.inventory)
                            render_popup(renderer, plusfish)  # Toon de pop-up
                            game_active = False
                    else:
                        print(f"Geen punten. Huidige score: {score}")
                        render_fail(renderer, fail_texture)
                        game_active= False


        # Update de mespositie (beperk tussen 150 en 650)
        current_time = time.time()
        if current_time - last_time > 0.01:  # Update elke 10 ms
            zone_x += line_speed * zone_direction
            if zone_x >= 650 - zone_width or zone_x <= 150:  # Zorg ervoor dat het mes tussen 150 en 650 beweegt
                zone_direction *= -1  # Verander richting bij rand

            last_time = current_time

        # Render de game
        render_game(renderer, background, mes_texture, [fish_texture])  # Pas de render aan met vis

    # Toon de eindscore
    print(f"Spel beëindigd! Totale score: {score}")


def render_popup(renderer, popup_texture):
   
    # Bereken de grootte van de texture
    popup_width, popup_height = popup_texture.size

    # Plaats de afbeelding precies in het midden van het scherm
    popup_x = (window_width - popup_width) // 2
    popup_y = (window_height - popup_height) // 2

    # Render de texture op volledige schaal

    renderer.copy(popup_texture, None, sdl2.SDL_Rect(popup_x, popup_y, popup_width, popup_height))
    renderer.present()

    # Houd de pop-up zichtbaar voor een korte tijd
    time.sleep(1)  # Toon de pop-up voor 1 seconde

def render_fail(renderer, fail_texture):

    # Bereken de grootte van de texture
    popup_width, popup_height = fail_texture.size

    # Plaats de afbeelding precies in het midden van het scherm
    popup_x = (window_width - popup_width) // 2
    popup_y = (window_height - popup_height) // 2

    # Render de texture op volledige schaal

    renderer.copy(fail_texture, None, sdl2.SDL_Rect(popup_x, popup_y, popup_width, popup_height))
    renderer.present()

    # Houd de pop-up zichtbaar voor een korte tijd
    time.sleep(1)  # Toon de pop-up voor 1 seconde



# Hoofdapplicatie instellen om start_mini_game zonder een apart venster te gebruiken
if __name__ == "__main__":
    setup_audio()
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