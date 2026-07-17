import sdl2
import sdl2.ext

from minigame_slice import render_popup
from wapens import Wapen
import sdl2
import sdl2.ext

import tkinter as tk
from wapens import Wapen, Speler
import sdl2.sdlmixer as mixer

wapens = [
    Wapen("level1_stok", 0, 5, "resources/Sprites/level1_stok.png"),
    Wapen("level2_stok", 50, 10, "resources/Sprites/level2_stok.png"),
    Wapen("level3_stok", 100, 15, "resources/Sprites/level3_stok.png"),
]


"""from hoofdmenu import toon_hoofdmenu"""

moet_afsluiten = False
global in_inventory
in_inventory = False  # Voeg dit toe om de status van de inventaris te volgen
from wapens import Wapen, Speler
import sdl2.sdlmixer as mixer
# Globale variabelen
volume = 50  # Initiële volumewaarde
in_menu = True  # Of de applicatie in het hoofdmenu is
in_settings = False  # Of de applicatie in het instellingenmenu is
in_home = False  # Of de applicatie in de 'home' mode is
in_gohome = False

moet_afsluiten = False  # Of de applicatie moet sluiten

HOOGTE = 600  # Totale hoogte van het venster of canvas
BREEDTE = 800



RESOURCES = sdl2.ext.Resources(__file__, "resources/Sprites")
resources = sdl2.ext.Resources(__file__, "resources")

# def quit_inv():
#     global in_inventory
#     in_inventory = False
#
# def open_inv():
#     global in_inventory
#     in_inventory = True

GRID_COLS = 4  # Aantal kolommen
GRID_ROWS = 4  # Aantal rijen
GRID_START_X = 5  # X-positie van het eerste vakje
GRID_START_Y = 112  # Y-positie van het eerste vakje
CELL_WIDTH = 110 # Breedte van elk vakje
CELL_HEIGHT = 115# Hoogte van elk vakje

resources = sdl2.ext.Resources(__file__, "resources")
RESOURCES = sdl2.ext.Resources(__file__, "resources/Sprites")

def setup_audio():
    if mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 3, 4096) == -1:
        print("Fout bij het openen van het audiokanaal:", mixer.Mix_GetError())
    else:
        print("Audio correct geopend.")

def get_cell_position(index):
    col = index % GRID_COLS
    row = index // GRID_COLS
    x = GRID_START_X + col * CELL_WIDTH
    y = GRID_START_Y + row * CELL_HEIGHT
    return x, y

def render_inventory_text(font, renderer, window, speler, xp_texture):
    # Als de XP niet is veranderd, render dan niet opnieuw
    text_x = 200
    text_y = 20
    padding = 10
    box_x = text_x - padding
    box_y = text_y - padding
    box_width = xp_texture.size[0] + 2 * padding
    box_height = xp_texture.size[1] + 2 * padding

    # Teken de blauwe box
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 192, 192, 192, 255)
    box_rect = sdl2.SDL_Rect(box_x, box_y, box_width, box_height)
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, box_rect)

    # Render de XP-tekst bovenop de box
    renderer.copy(xp_texture, dstrect=(text_x, text_y, xp_texture.size[0], xp_texture.size[1]))






def render_inventory(renderer, window, speler):
    global in_inventory, moet_afsluiten
    in_inventory = True

    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE)
    sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    achtergrond = factory.from_image(resources.get_path("inventory_screen1.png"))

    # Achtergrondafbeelding details
    bg_width = 800  # Breedte van de achtergrondafbeelding
    bg_height = 600  # Hoogte van de achtergrondafbeelding

    # Venstergrootte ophalen
    screen_width, screen_height = 800,600

    # Bereken de offsets om de achtergrondafbeelding te centreren
    x_offset = (screen_width - bg_width) // 2
    y_offset = (screen_height - bg_height) // 2

    while in_inventory:

        key_states = sdl2.SDL_GetKeyboardState(None)
        if key_states[sdl2.SDL_SCANCODE_SPACE]:
            in_inventory = False
        # Verwerk input events
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                in_inventory = False
                moet_afsluiten = True
                sdl2.ext.quit()
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:
                    moet_afsluiten = True
                    return
                if key == sdl2.SDLK_e:
                    moet_afsluiten = True
                    in_inventory = not in_inventory
                    return
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if event.button.button == sdl2.SDL_BUTTON_LEFT:  # Linkermuisklik
                    mouse_x, mouse_y = event.button.x, event.button.y

                    # Bereken de grenzen van de box
                    box_center_x, box_center_y = 590, 435
                    box_width, box_height = 190, 190
                    box_x_min = box_center_x - box_width // 2
                    box_x_max = box_center_x + box_width // 2
                    box_y_min = box_center_y - box_height // 2
                    box_y_max = box_center_y + box_height // 2
                    print('ik doe dit')

                    # Controleer of de muisklik binnen de box valt
                    if box_x_min <= mouse_x <= box_x_max and box_y_min <= mouse_y <= box_y_max:
                        print(speler.xp)
                        selectgeluidje=mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
                        mixer.Mix_PlayChannel(-1, selectgeluidje, 0)
                        if speler.huidig_wapen_index + 1 != 3:
                            if speler.xp >= wapens[speler.huidig_wapen_index + 1].kosten:
                                speler.huidig_wapen_index = (speler.huidig_wapen_index + 1) % 3  # Wissel het wapen
                                print(f"Huidig wapen gewijzigd naar index: {speler.huidig_wapen_index}")
                            else:
                                popupTexture = factory.from_image(resources.get_path('tekstje_voor_wapen.png'))
                                render_popup(renderer, popupTexture)
                                print('niet genoeg xp')

        # Maak het scherm zwart
        renderer.clear(sdl2.ext.Color(0, 0, 0))  # Vul het volledige scherm met zwart
        # Render de achtergrond gecentreerd
        renderer.copy(achtergrond, dstrect=(x_offset, y_offset, bg_width, bg_height))

        item_index = 0
        for item_name, quantity in speler.inventory.items():
            # Bereken vakje locatie
            x, y = get_cell_position(item_index)

            # Laad en render item sprite
            sprite_path = f"resources/Sprites/{item_name}.png"
            item_texture = factory.from_image(RESOURCES.get_path(f"{item_name}"))
            renderer.copy(item_texture, dstrect=(x, y, CELL_WIDTH, CELL_HEIGHT))

            # Render hoeveelheid (optioneel)
            font = sdl2.ext.FontTTF(font="CourierPrime.ttf", size=30, color=sdl2.ext.Color(255, 255, 255))
            quantity_text = font.render_text(f"{quantity}")
            text_width, text_height = 30,30
            text_x = x + CELL_WIDTH - text_width - 5  # Rechts uitlijnen
            text_y = y + CELL_HEIGHT - text_height - 5  # Onder uitlijnen
            quantity_texture = sdl2.ext.renderer.Texture(renderer, quantity_text)
            renderer.copy(quantity_texture, dstrect=(text_x, text_y, text_width, text_height))

            item_index += 1

        if speler.huidig_wapen_index == 0:
            weapon_texture = factory.from_image(RESOURCES.get_path("level1_stok.png"))
            renderer.copy(weapon_texture, dstrect=(510, 215, 200, 200))
        elif speler.huidig_wapen_index == 1:
            weapon_texture = factory.from_image(RESOURCES.get_path("level2_stok.png"))
            renderer.copy(weapon_texture, dstrect=(510, 215, 200, 200))
        elif speler.huidig_wapen_index == 2:
            weapon_texture = factory.from_image(RESOURCES.get_path("level3_stok.png"))
            renderer.copy(weapon_texture, dstrect=(510, 215, 200, 200))

        # Toon de wijzigingen op het scherm
        renderer.present()