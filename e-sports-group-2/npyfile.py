import random
from operator import truediv

import numpy as np
import sdl2
import sdl2.ext
import math
import time  # Voor de timer
import sdl2.sdlmixer as mixer
import serial
from numpy.ma.core import correlate
from sdl2 import SDL_Event, SDL_PollEvent, SDL_KEYDOWN

from ControllerFunctions import sound_vib_on_pickup, controller_init, show_timer_controller
#import SerialTest
from Sprites import Sprite
from hoofdmenu import toon_hoofdmenu, in_settings, in_home, nohome
from inventory import in_inventory, render_inventory
""",toon_hoofdmenu, in_settings, in_home, nohome"""
from wapens import Wapen, Speler
from MazeGenerator import generate_maze, spawn_sprites_in_maze
from numba import njit
from minimap import teken_minimap
"""from line_profiler_pycharm import profile"""


#from line_profiler_pycharm import profilez
# Globale variabelen
p_speler_x, p_speler_y = 3 + 1 / math.sqrt(2), 4 - 1 / math.sqrt(2)
r_speler_x, r_speler_y = 1 / math.sqrt(2), -1 / math.sqrt(2)
r_cameravlak_x, r_cameravlak_y = -1 / math.sqrt(2), -1 / math.sqrt(2)

# Wereldmap met numpy
world_map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])

wereld_map4 = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7],
])

wereld_map3 = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])

winkel_map = np.array([
    [0, 1, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 3, 3, 0],
    [1, 0, 0, 1, 7, 7, 2, 0, 0, 2, 7, 7, 3, 0, 0, 3],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 0, 4, 7, 7, 5, 0, 0, 5, 7, 7, 6, 0, 0, 6],
    [0, 4, 4, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 6, 6, 0],
])

maze_map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

])

m_button_pressed = False
v_button_pressed = False
x_button_pressed = False
map_start_time = None
switch_interval = 20 #seconden wachten in maze
#in_inventory = False


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

#randomconstants
muisklik=False
GOLF_FREQUENTIE = 1.0  # Je kunt deze waarde aanpassen
GOLF_AMPLITUDE = 10.0    # Hoe hoog de golf is
HOOGTE = 600           # Totale hoogte van het venster of canvas
BREEDTE= 800
sprite_zichtbaar=True
zoom = 1

animation_active = False  # Om animatie te starten bij klik
animation_start_time = 0  # Tijd bijhouden voor animatie
animation_duration = 1  # Lengte van animatie in seconden

moet_afsluiten = False
is_bewegen = False
loopgeluid_kanaal = None  # Variabele om het geluidskanaal bij te houden
loopgeluid = None  # Om het geladen geluid bij te houden
geld = 0
imagechooser = "resources/Sprites/level1_stok.png"
killgeluid= None


def laad_afbeelding_rechtsboven(renderer, pad_naar_afbeelding):
    afbeelding_text = sdl2.ext.load_image(pad_naar_afbeelding)
    return sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, afbeelding_text)


def teken_afbeelding_rechtsboven(renderer, afbeelding_texture, scherm_breedte, scherm_hoogte):
    afbeelding_breedte = 363  # Breedte van de skybox-afbeelding in pixels
    afbeelding_hoogte = 117   # Hoogte van de skybox-afbeelding in pixels


    bron_rect = sdl2.SDL_Rect(0, 0, afbeelding_breedte, afbeelding_hoogte)
    doel_rect = sdl2.SDL_Rect(scherm_breedte-358, -8, afbeelding_breedte, afbeelding_hoogte)  # Skybox bovenin het scherm# Render de eerste sectie van de skybox
    sdl2.SDL_RenderCopy(renderer.sdlrenderer, afbeelding_texture, bron_rect, doel_rect)



def bereken_r_straal_vector(scherm_breedte):
    """
    Bereken de richtingen van stralen voor alle kolommen tegelijk met numpy.
    """

    global zoom
    camera_x = np.linspace(-1, 1, scherm_breedte) #linspace verdeelt in gelijke stukken interval -1,1
    r_straal_x = zoom*r_speler_x + r_cameravlak_x * camera_x
    r_straal_y = zoom*r_speler_y + r_cameravlak_y * camera_x
    return r_straal_x, r_straal_y

def switch_to_map(map_choice):
    global p_speler_x, p_speler_y, wereld_map3, speelwereld

    #speelwereld = random.choice([world_map, wereld_map4, wereld_map3]) #speelwereld gelijk aan een random van de 3 maps
    speelwereld = map_choice
    p_speler_x = min(max(p_speler_x, 1), len(wereld_map3[0]) - 2) #zorgt ervoor dat de speler niet buiten de wereld spawned
    p_speler_y = min(max(p_speler_y, 1), len(wereld_map3) - 2)

    if map_choice is winkel_map:
        p_speler_x = 2
        p_speler_y = 3
        



resources = sdl2.ext.Resources(__file__, "resources")
def render_afbeelding_rechtsboven(renderer, window):
    # Maak een sprite factory
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Laad de afbeelding
    afbeelding = factory.from_image(resources.get_path("tekstje_maze_official.png"))
    afbeelding.position = 800 - afbeelding.size[0] - 10, 10  # 10px van rechterrand en bovenrand

    # Render afbeelding
    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render((afbeelding,))


def load_maze_map():
    global map_start_time,speelwereld,p_speler_y, p_speler_x,maze_map,maze_sprites
    maze_map,kleinerspelerx,kleinerspelery = generate_maze(15, 15,p_speler_x,p_speler_y)
    maze_sprites = spawn_sprites_in_maze(maze_map, 4, renderer)
    # print(meejs_map)
    speelwereld,p_speler_x, p_speler_y = maze_map,len(maze_map)//2,len(maze_map)//2 #generate_maze(15, 15,p_speler_x,p_speler_y)
    map_start_time = time.time()  # Reset the timer to the current time
    #print("map loaded, timer started.")

def handle_sprite_hit(p_speler_x, p_speler_y, r_speler_x, r_speler_y, sprites, speler ):
    """
    Functie die wordt aangeroepen wanneer de speler een sprite raakt.
    Het verwerkt de hit, speelt geluiden af, en voegt items toe aan de inventaris.
    """

    huidig_wapen = speler.huidig_wapen()
    schade = huidig_wapen.schade
    # Loop door alle sprites om te controleren of de sprite geraakt is
    for sprite in sprites:
        if hit_detectie(p_speler_x, p_speler_y, r_speler_x, r_speler_y, sprite):
            sprite.current_health -= schade
            if sprite.current_health <= 0:
                sprites.remove(sprite)
                speler.add_to_inventory(sprite.get_spritepathname(), 1)
                spawn_sprite(renderer, sprites)
                killgeluid= mixer.Mix_LoadWAV(b'resources/audio/realkillsound.wav')
                mixer.Mix_PlayChannel(-1, killgeluid, 0)


            hitgeluid = mixer.Mix_LoadWAV(b'resources/audio/killsound.wav')
            mixer.Mix_PlayChannel(-1, hitgeluid, 0)  # -1 geeft aan: probeer het volgende beschikbare kanaal

            break  # Stop na de eerste hit

def spawn_sprite(renderer, sprites):
    # Lijst van vis-afbeeldingen
    vis_afbeeldingen1 = [
        "resources/Sprites/fish1Texture.png",
        "resources/Sprites/fish2Texture.png",
    ]
    vis_afbeeldingen2 = [
        "resources/Sprites/fish3Texture.png",
        "resources/Sprites/fish4Texture.png"
    ]

    map_height = len(speelwereld[1])
    map_width = len(speelwereld[0])
    # Willekeurig een vis kiezen uit de lijst
    random_value= random.randint(0, 1)
    if random_value == 0:
        image_path = random.choice(vis_afbeeldingen1)
        midden_map_x = map_height / 2 - random.randint(0, 5)
        midden_map_y = map_width / 2 - random.randint(0, 5)
        x = midden_map_x
        y = midden_map_y
        scale = 0.4
        max_health = 100

    else:
        image_path = random.choice(vis_afbeeldingen2)
        midden_map_x = map_height / 2 - random.randint(0, 5)
        midden_map_y = map_width / 2 - random.randint(0, 5)
        x = midden_map_x
        y = midden_map_y
        scale = 0.4
        max_health = 200



    # Maak een nieuwe sprite en voeg deze toe aan de lijst van sprites
    nieuwe_sprite = Sprite(x, y, scale, image_path, renderer, max_health)
    sprites.append(nieuwe_sprite)

rotatie_hoek = 0
rotatie = 0

def verwerk_input(delta):
    global moet_afsluiten, p_speler_x, p_speler_y, r_speler_x, r_speler_y, r_cameravlak_x, r_cameravlak_y
    global oud_muis_x, oud_muis_y, rotatie_hoek, rotatie
    global animation_active, animation_start_time
    global is_bewegen, imagechooser
    global renderer, window
    global is_bewegen
    global speelwereld,m_button_pressed, v_button_pressed,zoom,x_button_pressed
    global snelheid, sprites
    global snelheid,in_inventory
    global correct, oncorrect, eerste, speler, visited_shops

    oud_muis_y = 0
    oud_muis_x = 0

    snelheid = 4 * delta
    nieuwe_x, nieuwe_y = p_speler_x, p_speler_y  # nieuwe potentiÃ«le positie
    is_bewegen = False

    # event = SDL_Event()
    # while SDL_PollEvent(event):  # Zorgt ervoor dat alle events verwerkt worden
    #     if event.type == SDL_KEYDOWN:
    #         print("Toets ingedrukt:", event.key.keysym.sym)
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            moet_afsluiten = True
            window.close()
            break
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            button = event.button.button
            if speelwereld is not maze_map:
                if button == sdl2.SDL_BUTTON_LEFT:
                    handle_sprite_hit(p_speler_x, p_speler_y, r_speler_x, r_speler_y, sprites, speler)
                    if speelwereld is wereld_map4:
                        animation_active  = True
                        animation_start_time = time.time()
                        mixer.Mix_PlayChannel(-1,swinggeluid, 0)

        elif event.type == sdl2.SDL_MOUSEMOTION:
            # Variabele om de rotatiehoek van de speler bij te houden
            rotatie_hoek = 0

            # Bereken de verandering in rotatie op basis van de muisbeweging
            beweging = -event.motion.xrel
            rotatiesnelheid = 0.003  # Rotatiesnelheid van de speler
            rotatie = beweging * rotatiesnelheid  # Hoeveelheid rotatie gebaseerd op muisbeweging

            # Update de totale rotatiehoek van de speler
            rotatie_hoek = rotatie

            # Bereken de cosinus en sinus van de cumulatieve rotatiehoek
            cos_rotatie = math.cos(rotatie_hoek)
            sin_rotatie = math.sin(rotatie_hoek)
            # Het cameravlak en de speler draaien met de rotatie matrix
            # Gebruik de geÃ¼pdatete rotatiehoek om de speler te draaien
            nieuwe_speler_x = r_speler_x * cos_rotatie - r_speler_y * sin_rotatie
            nieuwe_speler_y = r_speler_x * sin_rotatie + r_speler_y * cos_rotatie

            nieuwe_camera_x = r_cameravlak_x * cos_rotatie - r_cameravlak_y * sin_rotatie
            nieuwe_camera_y = r_cameravlak_x * sin_rotatie + r_cameravlak_y * cos_rotatie

            # Werk de spelerpositie bij
            r_speler_x, r_speler_y = nieuwe_speler_x, nieuwe_speler_y
            r_cameravlak_x, r_cameravlak_y = nieuwe_camera_x, nieuwe_camera_y


        elif event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym #Bepaal welke knop is ingedrukt
            if key == sdl2.SDLK_ESCAPE:
                if in_home:
                    # Toon het hoofdmenu wanneer op Escape wordt gedrukt
                    renderer.clear()
                    nohome(button, event, renderer, window)
                else:
                    # Toon het hoofdmenu wanneer op Escape wordt gedrukt
                    renderer.clear()
                    toon_hoofdmenu(renderer, window, speler)

            elif key == sdl2.SDLK_p:
                if speler.has_item("sushiroll1.png") or speler.has_item("sushiroll2.png") or speler.has_item("Sushiroll3.png") or speler.has_item("Sushiroll6.png"):
                    switch_to_map(winkel_map)
                    correct = False
                    eerste = True
                    oncorrect = False
                    visited_shops = []
            #This is purely for the demo and will not be in the final game
            elif key == sdl2.SDLK_i:
                speler.increase_xp(5)

            elif key == sdl2.SDLK_e:
                render_inventory(renderer, window, speler)

            elif key == sdl2.SDLK_z:
                nieuwe_x += r_speler_x * snelheid
                nieuwe_y += r_speler_y * snelheid
                is_bewegen = True

            elif key == sdl2.SDLK_q:
                handle_sprite_hit(p_speler_x, p_speler_y, r_speler_x, r_speler_y, sprites, speler)
                if speelwereld is wereld_map4:
                    animation_active = True
                    animation_start_time = time.time()
                    mixer.Mix_PlayChannel(-1, swinggeluid, 0)



    key_states = sdl2.SDL_GetKeyboardState(None)  # Bepaal welke knoppen zijn ingedrukt



    #lees_seriele_poort(nieuwe_x, r_speler_x, nieuwe_y, r_speler_y, snelheid, is_bewegen)

    # Map switchen
    #
    # lees_seriele_poort(nieuwe_x, r_speler_x, nieuwe_y, r_speler_y, snelheid, is_bewegen)

    if key_states[sdl2.SDL_SCANCODE_SEMICOLON] and not m_button_pressed:
        #switch_to_map()
        load_maze_map()
        m_button_pressed = True

    elif not key_states[sdl2.SDL_SCANCODE_SEMICOLON]:
        m_button_pressed = False

    # Beweeg naar voren
    if key_states[sdl2.SDL_SCANCODE_W]:
        nieuwe_x += r_speler_x * snelheid
        nieuwe_y += r_speler_y * snelheid
        is_bewegen=True

    # Beweeg naar achteren
    if key_states[sdl2.SDL_SCANCODE_S]:
        nieuwe_x -= r_speler_x * snelheid
        nieuwe_y -= r_speler_y * snelheid
        is_bewegen=True

    nieuwe_x = min(max(nieuwe_x, 0), len(speelwereld[0]) - 1) # Controleer of de nieuwe positie buiten het scherm blijft
    nieuwe_y = min(max(nieuwe_y, 0), len(speelwereld) - 1) # Controleer of de nieuwe positie buiten het scherm blijft


    # Controleer of de nieuwe positie geen muur bevat (een muur is alles anders dan 0)
    if speelwereld[int(nieuwe_y)][int(nieuwe_x)] == 0:  # Alleen verplaatsen als er geen muur is
       p_speler_x, p_speler_y = nieuwe_x, nieuwe_y

    if key_states[sdl2.SDL_SCANCODE_A]:
        nieuwe_x = p_speler_x - r_speler_y * snelheid  # Beweeg loodrecht op de kijkrichting
        nieuwe_y = p_speler_y + r_speler_x * snelheid  # Beweeg loodrecht op de kijkrichting
        is_bewegen=True
        if speelwereld[int(nieuwe_y)][int(nieuwe_x)] == 0:  # Controleer op muur
            p_speler_x, p_speler_y = nieuwe_x, nieuwe_y

    # Beweeg naar rechts (D)
    if key_states[sdl2.SDL_SCANCODE_D]:
        nieuwe_x = p_speler_x + r_speler_y * snelheid  # Beweeg loodrecht op de kijkrichting
        nieuwe_y = p_speler_y - r_speler_x * snelheid  # Beweeg loodrecht op de kijkrichting
        is_bewegen=True
        if speelwereld[int(nieuwe_y)][int(nieuwe_x)] == 0:  # Controleer op muur
            p_speler_x, p_speler_y = nieuwe_x, nieuwe_y

    if is_bewegen:
        start_loopgeluid()
    else:
        stop_loopgeluid()



def render_kolom_met_texture(renderer, scherm_breedte, scherm_hoogte, d_muur, muur_hit_x, k_muur, textures, z_buffer):
    for kolom in range(scherm_breedte):
        afstandtotmuur = d_muur[kolom]
        muur_type = k_muur[kolom] - 1  # Adjust for 0-indexed texture array

        # Skip rendering if wall type is invalid
        #if muur_type < 0 or muur_type >= len(textures):
            #continue

        # Calculate wall height based on distance
        muur_hoogte = int(scherm_hoogte / afstandtotmuur)
        begin_y = max(0, scherm_hoogte // 2 - muur_hoogte // 2)
        eind_y = min(scherm_hoogte, scherm_hoogte // 2 + muur_hoogte // 2)

        # Calculate texture X-coordinate based on hit position
        tex_x = int(muur_hit_x[kolom] * textures[muur_type].size[0])

        # Adjust texture coordinates for cases where the wall is taller than the screen
        tex_begin_y = 0
        tex_eind_y = textures[muur_type].size[1]
        if muur_hoogte > scherm_hoogte:
            tex_begin_y = (muur_hoogte - scherm_hoogte) // 2
            tex_eind_y = tex_begin_y + scherm_hoogte
        else:
            tex_begin_y = 0
            tex_eind_y = textures[muur_type].size[1]

        # Calculate the scaling factor for texture mapping
        scaling_factor = textures[muur_type].size[1] / muur_hoogte

        # Adjust the texture section based on scaling
        tex_begin_y = int(tex_begin_y * scaling_factor)
        tex_eind_y = int(tex_eind_y * scaling_factor)

        # Render the texture for this column
        renderer.copy(textures[muur_type],
                      srcrect=(tex_x, tex_begin_y, 1, tex_eind_y - tex_begin_y),
                      dstrect=(kolom, begin_y, 1, eind_y - begin_y))
        z_buffer[kolom] = afstandtotmuur


def render_kolom_met_texture2(renderer, scherm_breedte, scherm_hoogte, d_muur, muur_hit_x, k_muur, textures, textures2, z_buffer, golf_index):
    for kolom in range(scherm_breedte):
        afstandtotmuur = d_muur[kolom]
        muur_type = k_muur[kolom] - 1

        if muur_type==0:


            # Gebruik de golf_index om de juiste texture te kiezen
            # Zorg ervoor dat de golf_index binnen het bereik van de textures ligt
            texture = textures[golf_index]  # Kies de juiste texture uit de lijst met behulp van golf_index


            # Calculate wall height based on distance
            muur_hoogte = int(scherm_hoogte / afstandtotmuur)
            begin_y = max(0, scherm_hoogte // 2 - muur_hoogte // 2)
            eind_y = min(scherm_hoogte, scherm_hoogte // 2 + muur_hoogte // 2)

            # Calculate texture X-coordinate based on hit position
            tex_x = int(muur_hit_x[kolom] * texture.size[0])

            # Adjust texture coordinates for cases where the wall is taller than the screen
            tex_begin_y = 0
            tex_eind_y = texture.size[1]
            if muur_hoogte > scherm_hoogte:
                tex_begin_y = (muur_hoogte - scherm_hoogte) // 2
                tex_eind_y = tex_begin_y + scherm_hoogte
            else:
                tex_begin_y = 0
                tex_eind_y = texture.size[1]

            # Calculate the scaling factor for texture mapping
            scaling_factor = texture.size[1] / muur_hoogte

            # Adjust the texture section based on scaling
            tex_begin_y = int(tex_begin_y * scaling_factor)
            tex_eind_y = int(tex_eind_y * scaling_factor)

            # Render the texture for this column

            renderer.copy(texture,
                        srcrect=(tex_x, tex_begin_y, 1, tex_eind_y - tex_begin_y),
                        dstrect=(kolom, begin_y, 1, eind_y - begin_y))
            z_buffer[kolom] = afstandtotmuur

        else:

            # Calculate wall height based on distance
            muur_hoogte = int(scherm_hoogte / afstandtotmuur)
            begin_y = max(0, scherm_hoogte // 2 - muur_hoogte // 2)
            eind_y = min(scherm_hoogte, scherm_hoogte // 2 + muur_hoogte // 2)

            # Calculate texture X-coordinate based on hit position
            tex_x = int(muur_hit_x[kolom] * textures2[muur_type].size[0])

            # Adjust texture coordinates for cases where the wall is taller than the screen
            tex_begin_y = 0
            tex_eind_y = textures2[muur_type].size[1]
            if muur_hoogte > scherm_hoogte:
                tex_begin_y = (muur_hoogte - scherm_hoogte) // 2
                tex_eind_y = tex_begin_y + scherm_hoogte
            else:
                tex_begin_y = 0
                tex_eind_y = textures2[muur_type].size[1]

            # Calculate the scaling factor for texture mapping
            scaling_factor = textures2[muur_type].size[1] / muur_hoogte

            # Adjust the texture section based on scaling
            tex_begin_y = int(tex_begin_y * scaling_factor)
            tex_eind_y = int(tex_eind_y * scaling_factor)

            # Render the texture for this column
            renderer.copy(textures2[muur_type],
                          srcrect=(tex_x, tex_begin_y, 1, tex_eind_y - tex_begin_y),
                          dstrect=(kolom, begin_y, 1, eind_y - begin_y))
            z_buffer[kolom] = afstandtotmuur


def start_loopgeluid():
    global loopgeluid_kanaal
    if loopgeluid_kanaal is None:  # Controleer of er al een geluid wordt afgespeeld
        loopgeluid_kanaal = mixer.Mix_PlayChannel(-1, loopgeluid, -1)  # Herhaal het geluid eindeloos


def stop_loopgeluid():
    global loopgeluid_kanaal
    if loopgeluid_kanaal is not None:
        mixer.Mix_HaltChannel(loopgeluid_kanaal)
        loopgeluid_kanaal = None


def setup_audio():
    # Initialiseer SDL_mixer voor geluid
    mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 3, 4096)
    global loopgeluid, swinggeluid, killgeluid

    loopgeluid = mixer.Mix_LoadWAV(b'resources/audio/walking-in-water-199418-[AudioTrimmer.com].mp3')  # Laad het loopgeluid (vervang met het juiste pad)

    swinggeluid = mixer.Mix_LoadWAV(b'resources/audio/swing_sound.mp3')

    if not killgeluid:
        print("Fout bij het laden van het killgeluid:", mixer.Mix_GetError())



def raycast_vector(r_straal_x, r_straal_y):
    global speelwereld
    epsilon = 1e-10  # Small value to avoid division by zero

    # Replace any zero values in r_straal_x or r_straal_y with epsilon
    r_straal_x = np.where(r_straal_x == 0, epsilon, r_straal_x)
    r_straal_y = np.where(r_straal_y == 0, epsilon, r_straal_y)

    map_x = np.full(r_straal_x.shape, int(p_speler_x), dtype=int) #Dit stelt de startpositie van elke straal in op de positie van de speler in de speelwereld.
    map_y = np.full(r_straal_y.shape, int(p_speler_y), dtype=int)

    delta_dist_x = np.abs(1 / r_straal_x) #om van de ene rasterlijn naar de andere te gaan (DDA principe)
    delta_dist_y = np.abs(1 / r_straal_y)

    stap_x = np.where(r_straal_x < 0, -1, 1) #stap_x en stap_y bepalen of de straal positief of negatief beweegt
    # langs de x- en y-as. Als de component negatief is, gaat de straal naar links of naar beneden (-1), anders gaat deze naar rechts of omhoog (+1).

    stap_y = np.where(r_straal_y < 0, -1, 1)

    zij_afstand_x = np.where(r_straal_x < 0, (p_speler_x - map_x) * delta_dist_x, (map_x + 1.0 - p_speler_x) * delta_dist_x) #zij afstanden zijn de afstanden tot de rasterlijnen
    zij_afstand_y = np.where(r_straal_y < 0, (p_speler_y - map_y) * delta_dist_y, (map_y + 1.0 - p_speler_y) * delta_dist_y)

    geraakt = np.zeros(r_straal_x.shape, dtype=bool)
    kant = np.zeros(r_straal_x.shape, dtype=int)
    k_muur = np.zeros(r_straal_x.shape, dtype=int)
    muur_hit_x = np.zeros(r_straal_x.shape)

    while not np.all(geraakt): #while lus uit totdat alle stralen een muur geraakt
        mask_x = (zij_afstand_x < zij_afstand_y) & ~geraakt #controleert welke eerst is, verticale lijnen of horizontale rasterlijnen?
        mask_y = (zij_afstand_y <= zij_afstand_x) & ~geraakt #geeft beide een bool terug

        zij_afstand_x[mask_x] += delta_dist_x[mask_x] #updates de afstanden en stapgroottes voor de stralen die nog niet hebben geraakt
        zij_afstand_y[mask_y] += delta_dist_y[mask_y]
        map_x[mask_x] += stap_x[mask_x]
        map_y[mask_y] += stap_y[mask_y]
#Voor stralen die een verticale rasterlijn raken (mask_x is True), wordt zij_afstand_x verhoogd met delta_dist_x. Vervolgens wordt map_x aangepast door Ã©Ã©n tegel in de richting van de straal te verplaatsen (stap_x).
#Voor stralen die een horizontale rasterlijn raken (mask_y is True), wordt zij_afstand_y verhoogd met delta_dist_y (de afstand tot de volgende horizontale rasterlijn).
        binnen_grenzen = (map_x >= 0) & (map_x < speelwereld.shape[1]) & (map_y >= 0) & (map_y < speelwereld.shape[0]) #controleert of de stralen nog binnen de speelwereld liggen
        geraakt = (~binnen_grenzen) | (binnen_grenzen & (speelwereld[map_y, map_x] > 0)) | geraakt

        k_muur[geraakt & binnen_grenzen] = speelwereld[map_y[geraakt & binnen_grenzen], map_x[geraakt & binnen_grenzen]]
        kant[mask_x] = 0 #muur raken aan kant van verticale
        kant[mask_y] = 1 #muur raken aan horizontale

    afstand = np.where(kant == 0, (map_x - p_speler_x + (1 - stap_x) / 2) / r_straal_x,
                                 (map_y - p_speler_y + (1 - stap_y) / 2) / r_straal_y)

    # Calculate `muur_hit_x`
    muur_hit_x = np.where(kant == 0, p_speler_y + afstand * r_straal_y, p_speler_x + afstand * r_straal_x)
    muur_hit_x -= np.floor(muur_hit_x)  # Keep only the fractional part

    return afstand, kant, muur_hit_x, k_muur
#De afstand wordt anders berekend afhankelijk van welke kant van de tegel de straal als eerste raakt â€” een verticale kant (x-richting)
# of een horizontale kant (y-richting). Dit onderscheid wordt aangegeven door de variabele kant

# Functie om de afstand te berekenen tussen de speler en de sprite
def bereken_afstand(x1, y1, x2, y2):
    #print("afstandjes")
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def kijkrichting(speler_x, speler_y, kijk_x, kijk_y, sprite_x, sprite_y, max_bereik=10):
    # Normaliseer de kijkrichting
    kijk_length = (kijk_x**2 + kijk_y**2) ** 0.5
    kijk_x /= kijk_length
    kijk_y /= kijk_length

    # Bepaal de vector van de speler naar de sprite
    sprite_vector_x = sprite_x - speler_x
    sprite_vector_y = sprite_y - speler_y

    # Bereken de afstand
    afstand = (sprite_vector_x**2 + sprite_vector_y**2) ** 0.5
    if afstand > max_bereik:
        return False  # Sprite is te ver weg

    # Bereken de hoeken
    speler_hoek = math.atan2(kijk_y, kijk_x)
    sprite_hoek = math.atan2(sprite_vector_y, sprite_vector_x)

    # Bereken het verschil tussen de hoeken, genormaliseerd naar [-pi, pi]
    verschil = abs((speler_hoek - sprite_hoek + math.pi) % (2 * math.pi) - math.pi)

    # Controleer of het verschil binnen de gewenste hoek ligt (bijvoorbeeld 45 graden)
    return verschil < math.radians(45)


# Functie die controleert of de sprite wordt geraakt
def hit_detectie(speler_x, speler_y, kijk_x, kijk_y, sprite):
    """
    Controleert of een sprite wordt geraakt door de speler.

    Parameters:
    - speler_x, speler_y: De huidige positie van de speler.
    - kijk_x, kijk_y: De kijkrichting van de speler (unit vector).
    - sprite: Een instantie van de Sprite-klasse.
    - muisklik: Boolean die aangeeft of de muisknop is ingedrukt.

    Returns:
    - True als de sprite wordt geraakt, anders False.
    """
    # Haal de positie van de sprite op
    sprite_x, sprite_y = sprite.get_position()

    # Bereken afstand tussen speler en sprite
    afstand = bereken_afstand(speler_x, speler_y, sprite_x, sprite_y)

    # Controleer of sprite binnen bereik is
    binnen_bereik = afstand <= 1.5

    # Controleer kijkrichting
    in_kijkrichting = kijkrichting(speler_x, speler_y, kijk_x, kijk_y, sprite_x, sprite_y,10)

    # Controleer of er geklikt wordt
    if binnen_bereik and in_kijkrichting:
        #print("dit is er al")
        return True  # Sprite is geraakt
    return False  # Sprite niet geraakt



def render_sprite_met_health_bar(renderer, sprite, z_buffer):
    # Verplaats de sprite naar de camera-coÃ¶rdinaten
    sprite_position = np.array([sprite['x'] - p_speler_x, sprite['y'] - p_speler_y])


    # Bereken de inverse van de determinant en de adjunct matrix
    inverse_determinant_M = 1.0 / (r_cameravlak_x * r_speler_y - r_cameravlak_y * r_speler_x)
    adjunct_M = np.array([[r_speler_y, -r_speler_x], [-r_cameravlak_y, r_cameravlak_x]])

    # Transformeer de sprite-positie naar de camera-ruimte
    sprite_camera = inverse_determinant_M * np.dot(adjunct_M, sprite_position)
    sprite_camera_x = sprite_camera[0]
    sprite_camera_y = sprite_camera[1]

    # Als de sprite buiten het gezichtsveld is, render dan niet
    if sprite_camera_y <= 0:
        return

    # Bereken de positie en grootte van de sprite op het scherm

    sprite_screen_x = int((BREEDTE // 2) * (1 + sprite_camera_x / sprite_camera_y))
    sprite_height = abs(int(HOOGTE / sprite_camera_y)) * sprite['scale']
    sprite_width = abs(int(HOOGTE / sprite_camera_y)) * sprite['scale']

    # Bereken de verticale grenzen van de sprite op het scherm (nu met gecorrigeerde hoogte)
    start_y = int((HOOGTE - sprite_height) / 2)
    end_y =  min(HOOGTE, HOOGTE // 2 + sprite_height // 2)

    # Bereken de horizontale grenzen van de sprite op het scherm
    start_x = int(sprite_screen_x - sprite_width // 2)
    end_x = int(start_x + sprite_width)

    # Healthbar width en height aanpassen op basis van sprite_camera_y
    healthbar_base_width = 60  # Basisbreedte van de healthbar
    healthbar_base_height = 30  # Basishoogte van de healthbar

    # Vergroot de healthbar als de sprite dichtbij is en verklein als hij ver weg is
    healthbar_width = int(healthbar_base_width * (1 / sprite_camera_y))  # Verhouding van camera_y
    healthbar_height = int(healthbar_base_height * (1 / sprite_camera_y))  # Verhouding van camera_y

    healthbar_start_x = int(sprite_screen_x - healthbar_width // 2)
    healthbar_start_y = int(start_y - healthbar_height)

    # Bereken de groene en rode breedte van de healthbar
    green_width = int(healthbar_width * (sprite['current_health'] / sprite['max_health']))


    # Zorg ervoor dat de afbeelding een geldige SDL2 Texture is
    if not isinstance(sprite['image'], sdl2.ext.Texture):
        if isinstance(sprite['image'], sdl2.surface.SDL_Surface):
            sprite['image'] = sdl2.ext.renderer.Texture(renderer, sprite['image'])
        else:
            raise TypeError("Expected sprite['image'] to be an SDL2 Texture or SDL2 Surface, got {}".format(type(sprite['image'])))

    # Verkrijg de breedte en hoogte van de textuur
    texture_width, texture_height = sprite['image'].size
    # Loop door de kolommen van de sprite om te renderen
    for column in range(start_x, end_x):
        if 0 <= column < BREEDTE and np.hypot(sprite_position[0], sprite_position[1]) <= z_buffer[column] and (end_y - start_y):
            # Bereken de juiste texture-coÃ¶rdinaten
            tex_x = int((column - start_x) / (end_x - start_x) * texture_width)
            renderer.copy(sprite['image'], srcrect=(tex_x, 0, 1, texture_height),
                          dstrect=(column, start_y, 1, end_y - start_y))

            renderer.fill((healthbar_start_x, healthbar_start_y, healthbar_width, healthbar_height),
                          kleuren[1])  # Rood
            renderer.fill((healthbar_start_x, healthbar_start_y, green_width, healthbar_height),
                          kleuren[2])

def render_sprite(renderer, sprite, z_buffer):
    # Verplaats de sprite naar de camera-coÃ¶rdinaten
    sprite_position = np.array([sprite['x'] - p_speler_x, sprite['y'] - p_speler_y])


    # Bereken de inverse van de determinant en de adjunct matrix
    inverse_determinant_M = 1.0 / (r_cameravlak_x * r_speler_y - r_cameravlak_y * r_speler_x)
    adjunct_M = np.array([[r_speler_y, -r_speler_x], [-r_cameravlak_y, r_cameravlak_x]])

    # Transformeer de sprite-positie naar de camera-ruimte
    sprite_camera = inverse_determinant_M * np.dot(adjunct_M, sprite_position)
    sprite_camera_x = sprite_camera[0]
    sprite_camera_y = sprite_camera[1]

    # Als de sprite buiten het gezichtsveld is, render dan niet
    if sprite_camera_y <= 0:
        return

    # Bereken de positie en grootte van de sprite op het scherm

    sprite_screen_x = int((BREEDTE // 2) * (1 + sprite_camera_x / sprite_camera_y))
    sprite_height = abs(int(HOOGTE / sprite_camera_y)) * sprite['scale']
    sprite_width = abs(int(HOOGTE / sprite_camera_y)) * sprite['scale']

    # Bereken de verticale grenzen van de sprite op het scherm (nu met gecorrigeerde hoogte)
    start_y = int((HOOGTE - sprite_height) / 2)
    end_y = start_y + sprite_height


    # Bereken de horizontale grenzen van de sprite op het scherm
    start_x = int(sprite_screen_x - sprite_width // 2)
    end_x = int(start_x + sprite_width)

    # Zorg ervoor dat de afbeelding een geldige SDL2 Texture is
    if not isinstance(sprite['image'], sdl2.ext.Texture):
        if isinstance(sprite['image'], sdl2.surface.SDL_Surface):
            sprite['image'] = sdl2.ext.renderer.Texture(renderer, sprite['image'])
        else:
            raise TypeError("Expected sprite['image'] to be an SDL2 Texture or SDL2 Surface, got {}".format(type(sprite['image'])))

    # Verkrijg de breedte en hoogte van de textuur
    texture_width, texture_height = sprite['image'].size
    # Loop door de kolommen van de sprite om te renderen
    for column in range(start_x, end_x):
        if 0 <= column < BREEDTE and sprite_camera_y<=z_buffer[column]and (end_y - start_y):


            # Bereken de juiste texture-coÃ¶rdinaten
            tex_x = int((column - start_x) / (end_x - start_x) * texture_width)
            renderer.copy(sprite['image'], srcrect=(tex_x, 0, 1, texture_height),
                          dstrect=(column, start_y, 1, end_y - start_y))

def render_stok(renderer, stok_texture):
    global animation_active, animation_start_time
    stok_breedte = 350
    stok_hoogte = 350

    # Definieer een vaste positie in het rechterondergedeelte van het scherm voor de stok
    scherm_stok_x = int(BREEDTE * 0.6)
    scherm_stok_y = int(HOOGTE * 0.5)

    # Controleer of animatie actief is
    if animation_active:
        #print('actief')
        elapsed_time = time.time() - animation_start_time
        if elapsed_time < animation_duration:
            # Vergroot of verklein de stok voor het animatie-effect
            schaalfactor = 1 + 0.5 * math.sin((elapsed_time / animation_duration) * math.pi)
            stok_breedte = int(stok_breedte * schaalfactor)
            stok_hoogte = int(stok_hoogte * schaalfactor)
        else:
            # Stop de animatie na de duur
            animation_active = False

    # Render de stok op deze positie met de aangepaste breedte en hoogte
    renderer.copy(stok_texture, dstrect=(scherm_stok_x, scherm_stok_y, stok_breedte, stok_hoogte))



def show_fps(font, renderer, window):
    fps_list = []
    fps = 0
    loop_time = 1

    while True:
        fps_list.append(1 / (time.time() - loop_time))
        loop_time = time.time()
        if len(fps_list) == 20:
            fps = sum(fps_list) / len(fps_list)
            fps_list = []
        text = sdl2.ext.renderer.Texture(renderer, font.render_text(f'{fps:.2f} fps'))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        yield fps


def load_textures(renderer):
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    spriteresource = sdl2.ext.Resources(__file__, "resources")
    muur_textures = [
        factory.from_image(spriteresource.get_path("WinkelFront1.png")), #0
        factory.from_image(spriteresource.get_path("WinkelFront2.png")),   #1
        factory.from_image(spriteresource.get_path("WinkelFront3.png")),#2
        factory.from_image(spriteresource.get_path("WinkelFront4.png")),#3
        factory.from_image(spriteresource.get_path("WinkelFront5.png")),#4
        factory.from_image(spriteresource.get_path("WinkelFront6.png")),#5
        factory.from_image(spriteresource.get_path("muur1.png")),#6
        factory.from_image(spriteresource.get_path("muurmetbord.png")),  # 6
        factory.from_image(spriteresource.get_path("random_winkel.png")),#7 ,
    ]
    return muur_textures

def load_textures2(renderer):
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    spriteresource = sdl2.ext.Resources(__file__, "resources")
    muur_textures_wave = [
        factory.from_image(spriteresource.get_path("wave1.jpg")),#0
        factory.from_image(spriteresource.get_path("wave2.jpg")),#1
        factory.from_image(spriteresource.get_path("wave3.jpg")),#2
        factory.from_image(spriteresource.get_path("wave4.jpg")),#3
        factory.from_image(spriteresource.get_path("wave5.jpg")),#4
        factory.from_image(spriteresource.get_path("wave6.jpg")),#5
        factory.from_image(spriteresource.get_path("wave7.jpg")),#6
        factory.from_image(spriteresource.get_path("wave8.jpg")),#7
        factory.from_image(spriteresource.get_path("wave9.jpg")),#8
        factory.from_image(spriteresource.get_path("wave10.jpg")),#9
        factory.from_image(spriteresource.get_path("wave11.jpg")),#10
        factory.from_image(spriteresource.get_path("wave12.jpg")),#11
    ]
    return muur_textures_wave


def render_xp(font, renderer, window, speler,xp_texture):
      # Als de XP niet is veranderd, render dan niet opnieuw
      text_x = 20
      text_y = 550
      padding = 10
      box_x = text_x - padding
      box_y = text_y - padding
      box_width = xp_texture.size[0] + 2 * padding
      box_height = xp_texture.size[1] + 2 * padding

      # Teken de blauwe box
      sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 255, 255)
      box_rect = sdl2.SDL_Rect(box_x, box_y, box_width, box_height)
      sdl2.SDL_RenderFillRect(renderer.sdlrenderer, box_rect)

      # Render de XP-tekst bovenop de box
      renderer.copy(xp_texture, dstrect=(text_x, text_y, xp_texture.size[0], xp_texture.size[1]))


def render_text(font, renderer, window, speler, xp_texture,scalingfactor):
    # Als de XP niet is veranderd, render dan niet opnieuw
    text_x = 230
    text_y = 550
    padding = 10

    # Schaalfactor instellen (nu op 0.8 voor 80% van de originele grootte)
    scale_factor = scalingfactor  # Pas dit aan naar 0.8
    new_width = int(xp_texture.size[0] * scale_factor)
    new_height = int(xp_texture.size[1] * scale_factor)

    # Box afmetingen aanpassen aan de geschaalde tekst
    box_x = text_x - padding
    box_y = text_y - padding
    box_width = new_width + 2 * padding  # Box breedte op basis van de geschaalde tekst
    box_height = new_height + 2 * padding  # Box hoogte op basis van de geschaalde tekst

    # Teken de blauwe box
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 255, 255)  # Donkerblauw
    box_rect = sdl2.SDL_Rect(box_x, box_y, box_width, box_height)
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, box_rect)

    # Render de geschaalde XP-tekst bovenop de box
    renderer.copy(
        xp_texture,
        dstrect=(text_x, text_y, new_width, new_height)  # Geschaalde afmetingen
    )

def render_text_met_tijd(font, renderer, window, speler, xp_texture, start_time, duration=3000):
    # Als de XP niet is veranderd, render dan niet opnieuw
    text_x = 400
    text_y = 300
    padding = 10

    # Controleer of de tijd is verstreken
    current_time = time.time()
    if current_time - start_time > duration:
        return  # Stop met renderen als de tijd is verstreken

    # Schaalfactor instellen (nu op 0.8 voor 80% van de originele grootte)
    scale_factor = 0.8  # Pas dit aan naar 0.8
    new_width = int(xp_texture.size[0] * scale_factor)
    new_height = int(xp_texture.size[1] * scale_factor)

    # Box afmetingen aanpassen aan de geschaalde tekst
    box_x = text_x - padding
    box_y = text_y - padding
    box_width = new_width + 2 * padding  # Box breedte op basis van de geschaalde tekst
    box_height = new_height + 2 * padding  # Box hoogte op basis van de geschaalde tekst

    # Teken de blauwe box
    sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 139, 255)  # Donkerblauw
    box_rect = sdl2.SDL_Rect(box_x, box_y, box_width, box_height)
    sdl2.SDL_RenderFillRect(renderer.sdlrenderer, box_rect)

    # Render de geschaalde XP-tekst bovenop de box
    renderer.copy(
        xp_texture,
        dstrect=(text_x, text_y, new_width, new_height)  # Geschaalde afmetingen
    )

def move_sprite_away_from_player(sprite, game_world, delta, move_speed=0.1, steps_per_direction=30, buffer_size=1):
    """
    Beweegt een sprite willekeurig binnen de grenzen van game_world.

    Parameters:
        sprite: Object met attributen `x` en `y` voor positie.
        game_world: 2D-array waarin 0 vrije ruimte is en 1 obstakels zijn.
        delta: Tijd (in seconden) verstreken sinds de laatste frame.
        move_speed: Hoe snel de sprite beweegt (basissnelheid per seconde).
        steps_per_direction: Hoeveel stappen de sprite in dezelfde richting beweegt.
        buffer_size: Hoeveel ruimte rondom de sprite gecontroleerd wordt op obstakels.
    """
    if not hasattr(sprite, 'move_counter'):
        sprite.move_counter = 0
        sprite.current_direction = np.array([0, 0])  # Geen beweging aan het begin

    # Tel de stappen in de huidige richting
    sprite.move_counter += 1

    # Kies een nieuwe willekeurige richting als het aantal stappen bereikt is
    if sprite.move_counter >= steps_per_direction or np.array_equal(sprite.current_direction, [0, 0]):
        possible_directions = [
            np.array([1, 0]),  # Rechts
            np.array([-1, 0]),  # Links
            np.array([0, 1]),  # Omlaag
            np.array([0, -1]),  # Omhoog
            np.array([1, 1]),  # Rechts-omlaag
            np.array([1, -1]),  # Rechts-omhoog
            np.array([-1, 1]),  # Links-omlaag
            np.array([-1, -1])  # Links-omhoog
        ]
        sprite.current_direction = possible_directions[np.random.randint(len(possible_directions))]
        sprite.move_counter = 0  # Reset de teller

    # Snelheid schalen met delta-tijd
    scaled_speed = move_speed * delta

    # Bereken de nieuwe positie
    new_x = sprite.x + sprite.current_direction[0] * scaled_speed
    new_y = sprite.y + sprite.current_direction[1] * scaled_speed

    # Controleer of de nieuwe positie binnen de grenzen ligt
    grid_x = int(new_x)
    grid_y = int(new_y)
    if 0 <= grid_x < game_world.shape[1] and 0 <= grid_y < game_world.shape[0]:
        # Controleer of de nieuwe positie geen obstakel is
        clear_space = True
        for i in range(-buffer_size, buffer_size + 1):
            for j in range(-buffer_size, buffer_size + 1):
                check_x = grid_x + i
                check_y = grid_y + j
                if 0 <= check_x < game_world.shape[1] and 0 <= check_y < game_world.shape[0]:
                    if game_world[check_y][check_x] == 1:  # Muur gevonden
                        clear_space = False
                        break
            if not clear_space:
                break

        if clear_space:
            # Update de positie van de sprite
            sprite.x = new_x
            sprite.y = new_y
        else:
            # Kies een nieuwe richting als een obstakel wordt geraakt
            sprite.move_counter = steps_per_direction
    else:
        # Kies een nieuwe richting als buiten de grenzen
        sprite.move_counter = steps_per_direction



def render_sea_pattern(renderer, screen_width, screen_height):
    # Stel het aantal lagen en de kleurintensiteit in
    num_layers = 20  # Hoe meer lagen, hoe vloeiender het verloop
    start_color = (173, 216, 230)  # Lichtblauw (RGB voor lichtblauw)
    end_color = (0, 0, 139)  # Donkerblauw (RGB voor donkerblauw)

    # Bereken de hoogte van elke laag
    layer_height = (screen_height // 2) // num_layers

    # Bereken het verschil tussen de start- en eindkleur
    color_step = (
        (end_color[0] - start_color[0]) / num_layers,
        (end_color[1] - start_color[1]) / num_layers,
        (end_color[2] - start_color[2]) / num_layers,
    )

    for i in range(num_layers):
        # Bereken de huidige kleur
        current_color = (
            int(start_color[0] + color_step[0] * i),
            int(start_color[1] + color_step[1] * i),
            int(start_color[2] + color_step[2] * i),
        )

        # Stel de renderer-kleur in op de huidige laagkleur
        renderer.color = sdl2.ext.Color(*current_color)

        # Teken de laag
        renderer.fill((0, screen_height // 2 + i * layer_height, screen_width, layer_height))


directional_sprites_heks = [
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_0_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_700_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_600_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_500_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_400_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_300_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_200_0.png",
    "resources/Directionelesprites/HeksMaze/mage_sprite_01_cut_100_0.png",
]





directional_sprites_reefs = [
    "resources/Directionelesprites/Guystaand/IdleFront.png",
    "resources/Directionelesprites/Guystaand/IdleLeftFront.png",
    "resources/Directionelesprites/Guystaand/IdleLeft.png",
    "resources/Directionelesprites/Guystaand/IdleLeftBack.png",
    "resources/Directionelesprites/Guystaand/IdleBack.png",
    "resources/Directionelesprites/Guystaand/IdleRightBack.png",
    "resources/Directionelesprites/Guystaand/IdleRight.png",
    "resources/Directionelesprites/Guystaand/IdleRightFront.png",
]


def determine_sprite_direction(speler_x, speler_y, sprite_x, sprite_y):
    """
    Bepaal de richting van de sprite die zichtbaar moet zijn op basis van de positie van de speler.

    Parameters:
        speler_x, speler_y: De positie van de speler.
        sprite_x, sprite_y: De positie van de sprite.

    Returns:
        hoek_index: Een integer van 0 tot 7 die overeenkomt met de 8 sectoren.
    """
    # Bereken de vector van de sprite naar de speler
    dx = speler_x - sprite_x
    dy = speler_y - sprite_y

    # Bereken de hoek van de sprite naar de speler in graden
    angle_to_player = math.degrees(math.atan2(dy, dx)) % 360

    # Verdeel de cirkel in 8 sectoren van 45 graden
    hoek_index = int((angle_to_player + 22.5) // 45) % 8
    return hoek_index




def render_directional_sprite(renderer, speler_x, speler_y, sprite, z_buffer,spritearray):
    """
    Render een sprite op basis van de relatieve positie van de speler.

    Parameters:
        renderer: SDL2 renderer.
        speler_x, speler_y: Positie van de speler.
        sprite: Sprite-object.
        z_buffer: Dieptebuffer voor z-sorting.
    """
    hoek_index = determine_sprite_direction(speler_x, speler_y, sprite.x, sprite.y)
    sprite_image = sdl2.ext.load_image(spritearray[hoek_index])
    sprite.texture = sdl2.ext.Texture(renderer, sprite_image)

    # Render de sprite zoals gebruikelijk
    render_sprite(renderer, {'x': sprite.x, 'y': sprite.y, 'scale': sprite.scale, 'image': sprite.texture}, z_buffer)

# Laad de skybox
def laad_skybox(renderer, pad_naar_afbeelding):
    skybox_texture = sdl2.ext.load_image(pad_naar_afbeelding)
    return sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, skybox_texture)


def teken_skybox(renderer, skybox_texture, scherm_breedte, scherm_hoogte, r_speler_x, r_speler_y):
    global rotatie
    skybox_breedte = 1920  # Breedte van de skybox-afbeelding in pixels
    skybox_hoogte = 480   # Hoogte van de skybox-afbeelding in pixels

    # Bereken de kijkhoek van de speler
    kijkhoek = math.degrees(math.atan2(r_speler_y, r_speler_x)) % 360

    # Bereken de offset in de skybox op basis van de kijkhoek
    offset_x = int(-(kijkhoek / 360) * skybox_breedte + rotatie * 0.03) % skybox_breedte

    # Bepaal het brongebied
    bron_rect = sdl2.SDL_Rect(offset_x, 0, skybox_breedte - offset_x, skybox_hoogte)
    doel_rect = sdl2.SDL_Rect(0, 0, skybox_breedte - offset_x, scherm_hoogte // 2)  # Skybox bovenin het scherm

    # Render de eerste sectie van de skybox
    sdl2.SDL_RenderCopy(renderer.sdlrenderer, skybox_texture, bron_rect, doel_rect)

    # Als de offset buiten de afbeelding valt, render het begin van de afbeelding
    if offset_x + scherm_breedte > skybox_breedte:
        bron_rect = sdl2.SDL_Rect(0, 0, offset_x + scherm_breedte - skybox_breedte, skybox_hoogte)
        doel_rect = sdl2.SDL_Rect(skybox_breedte - offset_x, 0, offset_x + scherm_breedte - skybox_breedte, scherm_hoogte // 2)
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, skybox_texture, bron_rect, doel_rect)




def toon_ladingscherm(renderer, window, resources):
    # Initialiseer SDL2_mixer
    if sdl2.sdlmixer.Mix_OpenAudio(44100, sdl2.sdlmixer.MIX_DEFAULT_FORMAT, 2, 2048) < 0:
        print("Error initializing SDL_mixer:", sdl2.sdlmixer.Mix_GetError())
        return

    # Laad het geluid
    sound_path = resources.get_path("introsound.mp3")
    introsound = sdl2.sdlmixer.Mix_LoadWAV(sound_path.encode('utf-8'))
    if not introsound:
        print("Error loading sound:", sdl2.sdlmixer.Mix_GetError())
        return

    # Speel het geluid af
    sdl2.sdlmixer.Mix_PlayChannel(-1, introsound, 0)

    # SpriteFactory en renderer instellen
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    spriterenderer = factory.create_sprite_render_system(window)

    # Achtergrond- en bewegende afbeelding laden
    background_image = factory.from_image(resources.get_path("Starting_a_new_life_in_Japan.png"))
    boot_image = factory.from_image(resources.get_path("vliegtuig.png"))

    # Beginposities instellen
    x_pos = 100  # Startpositie
    y_pos = 330

    # Start de timer
    start_time = time.time()  # Starttijd van de animatie

    # Loop zolang de tijd minder is dan 2,5 seconden
    while time.time() - start_time < 2.5:
        for e in sdl2.ext.get_events():
            if e.type == sdl2.SDL_QUIT:
                return  # Verlaat direct bij een quit-event

        # Scherm wissen en opnieuw tekenen
        renderer.clear()
        spriterenderer.render(background_image)

        # Update positie en render bewegende afbeelding
        if x_pos < 500:
            x_pos += 3  # Beweging naar rechts
        boot_image.position = (x_pos, y_pos)
        spriterenderer.render(boot_image)

        # Scherm verversen
        window.refresh()

        # Animatiesnelheid
        sdl2.SDL_Delay(10)

    # Opruimen
    sdl2.sdlmixer.Mix_FreeChunk(introsound)
    sdl2.sdlmixer.Mix_CloseAudio()

# def show_xp_controller(xp):
#     # ser = serial.Serial("COM7", 9600)
#     eenheden = xp % 10
#     tientallen = xp // 10
#
#     commandEenheden = "s1" + str(eenheden) + "x"
#     commandTientallen = "s1" + str(tientallen) + "x"
#     return commandEenheden, commandTientallen



def main():
    global renderer, window, speler, speelwereld,sprites, map_start_time, in_inventory, visitShopsText,maze_sprites
    global correct, oncorrect, eerste, visited_shops,p_speler_x, p_speler_y, soldsushinognietgebeurd

    scherm_breedte = 800
    scherm_hoogte = 600
    sdl2.ext.init()
    window = sdl2.ext.Window("Fish to Dish", size=(scherm_breedte, scherm_hoogte))
    icon = sdl2.ext.load_image("resources/Sprites/fish1Texture.png")
    sdl2.SDL_SetWindowIcon(window.window, icon)
    controller_init()

    '''
    
    Met onderstaand stukjes kan je de game layout veranderen enzo
    
    '''


    #hiermee kunnen we de windowsize aanpassen
    #sdl2.SDL_SetWindowFullscreen(window.window, 0x00000001)
    # sdl2.SDL_SetWindowFullscreen(window.window, 0x00000000)
    #hiermee resize je de window
    #sdl2.SDL_SetWindowResizable(window.window, 0x00000020)
    # sdl2.SDL_SetWindowBordered(window.window, True)
    window.show()
    sdl2.SDL_SetRelativeMouseMode(True)
    renderer = sdl2.ext.Renderer(window)

    toon_ladingscherm(renderer, window, resources)





    speler= Speler()

    # In de render-loop
    skybox_texture = laad_skybox(renderer, "resources/skyboxtest.png")
    skybox_texture_flashlight = laad_skybox(renderer, "resources/skybox_flashlight.png")
    afbeelding_texture = laad_afbeelding_rechtsboven(renderer, "resources/sprites/tekstje_maze_official.png")
    afbeelding_texture_geen_sushi = laad_afbeelding_rechtsboven(renderer, "resources/sprites/heks_tekst_geen_sushi.png")
    afbeelding_texture_sushi = laad_afbeelding_rechtsboven(renderer, "resources/sprites/heks_als_wel_sushi.png")
    # Render muren en objecten daarna

    huidig_wapen = speler.huidig_wapen()
    stok_image = sdl2.ext.load_image(huidig_wapen.afbeelding)
    stok_texture = sdl2.ext.Texture(renderer, stok_image)

    toon_hoofdmenu(renderer, window,speler)
    sdl2.SDL_SetRelativeMouseMode(True)
    sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)

    fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])
    fps_generator = show_fps(fps_font, renderer, window)




    sprite_world_x = 3  # X-coÃ¶rdinaat in de wereld
    sprite_world_y = 3  # Y-coÃ¶rdinaat in de wereld



    # Bepaal de sprite-positie
    sprite_x, sprite_y = 10, 5 # Positie van de sprite in de wereld
    map_choice= wereld_map4
    loopt = True
    speelwereld = map_choice
    textures = load_textures(renderer)
    textures2= load_textures2(renderer)
    setup_audio()

    # Sla de sprites op in een lijst
    sprites = [
        Sprite(x=10, y=5, scale=0.3, image_path='resources/Sprites/fish4Texture.png', renderer=renderer, max_health=200),
        Sprite(x=5, y=10, scale=0.3, image_path='resources/Sprites/fish1Texture.png', renderer=renderer, max_health=100),
        Sprite(x=8, y=3, scale=0.3, image_path='resources/Sprites/fish2Texture.png', renderer=renderer, max_health=150),
        Sprite(x=8, y=3, scale=0.3, image_path='resources/Sprites/fish3Texture.png', renderer=renderer,max_health=200)
    ]


    reefs = [
        Sprite(x=5, y=4, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
        Sprite(x=3, y=6, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
        Sprite(x=6, y=8, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
        Sprite(x=8, y=2, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
        Sprite(x=10, y=12, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
        Sprite(x=7, y=13, scale=1, image_path='resources/Sprites/reef1.png', renderer=renderer),
    ]

    directional_sprites = [
        Sprite(x=6, y=6, scale=1, image_path="resources/Directionelesprites/Guystaand/IdleFront.png",
               renderer=renderer),
        Sprite(x=4, y=7, scale=1, image_path="resources/Directionelesprites/Guystaand/IdleFront.png",
               renderer=renderer, rotation=90),
        Sprite(x=8, y=6, scale=1, image_path="resources/Directionelesprites/Guystaand/IdleFront.png",
               renderer=renderer, rotation=45)

    ]

    z_buffer = np.full(scherm_breedte, float('inf'))
    xp_texture = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(f"XP: {speler.xp}"))

    randomShopArray = np.random.permutation(np.arange(1, 7))
    visited_shops = []
    correct_order_printed =  False
    correct_order = False


    shop_locations = {
        (1, 1): 1,
        (2, 1): 1,
        (1, 4): 4,
        (2, 4): 4,
        (7, 1): 2,
        (8, 1): 2,
        (7, 4): 5,
        (8, 4): 5,
        (13, 1): 3,
        (14, 1): 3,
        (13, 4): 6,
        (14, 4): 6,
        # Add more locations as needed
    }



    golf_index=0
    counter=0
    interval=0.5
    correct = False
    oncorrect = False
    eerste = True
    # Initialiseer variabelen voor de timer
    switch_time = None  # Houdt bij wanneer we moeten overschakelen
    switch_to_map_scheduled = False  # Controleer of er een switch is gepland
    soldsushinognietgebeurd= False
    flashlight_surf = sdl2.ext.load_image('resources/Flashlighttextureoverlaynieuw.png')
    flashlight_text = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, flashlight_surf)
    #ser = serial.Serial("COM7", 9600)

    # commandoEenheden, commandoTientallen = show_xp_controller(speler.xp)
    # ser.write(commandoEenheden.encode())
    # ser.write(commandoTientallen.encode())


    while loopt:
        # sdl2.SDL_SetWindowResizable(window.window, 0x00000020)
        key_states = sdl2.SDL_GetKeyboardState(None)
        if key_states[sdl2.SDL_SCANCODE_SPACE]:
            loopt = False


        start_time =time.time()
        events = sdl2.ext.get_events()

        sprites.sort(
            key=lambda sprite: (sprite.x - p_speler_x) ** 2 + (sprite.y - p_speler_y) ** 2,
            reverse=True  # Voor verre objecten eerst
        )

        reefs.sort(
            key=lambda sprite: (sprite.x - p_speler_x) ** 2 + (sprite.y - p_speler_y) ** 2,
            reverse=True  # Voor verre objecten eerst
        )

        objects = [
                      {'type': 'sprite', 'data': sprite} for sprite in sprites
                  ] + [
                      {'type': 'reef', 'data': reef} for reef in reefs
                  ]

        for event in events:
            if event.type == sdl2.SDL_QUIT:
                loopt = False
                break


        # Wis het scherm
        renderer.clear(sdl2.ext.Color(0, 0, 0))
        # Render de raycasting-scÃ¨ne
        r_straal_x, r_straal_y = bereken_r_straal_vector(scherm_breedte)
        afstand, kant, muur_hit_x, k_muur = raycast_vector(r_straal_x, r_straal_y)

        teken_skybox(renderer, skybox_texture, scherm_breedte, scherm_hoogte, r_speler_x, r_speler_y)
        delta= time.time()-start_time

        if speelwereld is wereld_map4:
            render_sea_pattern(renderer,BREEDTE,HOOGTE)
        # Render walls with textures
        if speelwereld is wereld_map4:
            render_kolom_met_texture2(renderer, scherm_breedte, scherm_hoogte, afstand, muur_hit_x, k_muur, textures2, textures, z_buffer,golf_index)
        else:
            render_kolom_met_texture(renderer, scherm_breedte, scherm_hoogte, afstand, muur_hit_x, k_muur, textures, z_buffer)
        if speelwereld is wereld_map4:
            for obj in objects:
                if obj['type'] == 'sprite':
                    render_sprite_met_health_bar(renderer, {
                        'x': obj['data'].x,
                        'y': obj['data'].y,
                        'scale': obj['data'].scale,
                        'image': obj['data'].image,
                        'rotation': obj['data'].rotation,
                        'current_health': obj['data'].current_health,
                        'max_health': obj['data'].max_health
                    }, z_buffer)
                    move_sprite_away_from_player(obj['data'], speelwereld, delta, 50, 300, 1)
                elif obj['type'] == 'reef':
                    render_sprite(renderer, {
                        'x': obj['data'].x,
                        'y': obj['data'].y,
                        'scale': obj['data'].scale,
                        'image': obj['data'].image,
                        'rotation': obj['data'].rotation,
                        'current_health': obj['data'].current_health,
                        'max_health': obj['data'].max_health
                    }, z_buffer)


        if speelwereld is maze_map:
            heks = Sprite(x=7, y=7, scale=1, image_path="resources/Directionelesprites/Guystaand/IdleFront.png", renderer = renderer)
            render_directional_sprite(renderer, p_speler_x, p_speler_y, heks, z_buffer,directional_sprites_heks)
            sdl2.SDL_RenderCopy(renderer.sdlrenderer, flashlight_text, None, None)  # render flashlight
            skybox_texture = laad_skybox(renderer, "resources/skybox_flashlight.png")
            teken_afbeelding_rechtsboven(renderer,afbeelding_texture, scherm_breedte, scherm_hoogte)
            maze_sprites.sort(
                key=lambda sprite: (sprite.x - p_speler_x) ** 2 + (sprite.y - p_speler_y) ** 2,
                reverse=True  # Voor verre objecten eerst
            )
            for sprite in maze_sprites:

                render_sprite(renderer, {'x': sprite.x, 'y': sprite.y, 'scale': sprite.scale, 'image': sprite.image},
                          z_buffer)
                sprite_x, sprite_y = sprite.get_position()

                # Bereken afstand tussen speler en sprite
                afstand = bereken_afstand(p_speler_x, p_speler_y, sprite_x, sprite_y)
                # print(maze_map[int(p_speler_y)], maze_map[int(p_speler_x)])
                """
                
                TODO: hit detectie werkende krijgen op de sprites
                
                """


                if afstand <= 0.5:
                    #print ("botsing")
                    maze_sprites.remove(sprite)
                    sound_vib_on_pickup()

                    pickupsound = mixer.Mix_LoadWAV(b'resources/audio/pickupsound.mp3')
                    mixer.Mix_PlayChannel(-1, pickupsound, 0)

                    speler.add_to_inventory(sprite.get_spritepathname(),1)


            # for sprite in directional_sprites:
            #     render_directional_sprite(renderer, p_speler_x, p_speler_y, sprite, z_buffer,directional_sprites_reefs)

        if speelwereld is wereld_map4:
            heks = Sprite(x=11, y=22, scale=1, image_path="resources/Directionelesprites/Guystaand/IdleLeft.png",
                          renderer = renderer)
            render_directional_sprite(renderer, p_speler_x, p_speler_y, heks, z_buffer, directional_sprites_heks)

            if 9 < p_speler_x < 13 and 20 < p_speler_y < 24:
                if speler.has_item("sushiroll1.png") or speler.has_item("sushiroll2.png") or speler.has_item("Sushiroll3.png") or speler.has_item("Sushiroll6.png"):
                    teken_afbeelding_rechtsboven(renderer, afbeelding_texture_sushi, scherm_breedte, scherm_hoogte)
                else:
                    teken_afbeelding_rechtsboven(renderer, afbeelding_texture_geen_sushi, scherm_breedte, scherm_hoogte)


        delta = time.time() - start_time
        verwerk_input(delta)



        sdl2.SDL_SetRelativeMouseMode(True)
        nieuwe_huidige_wapen = speler.huidig_wapen()  # Haal het huidige wapen opnieuw op

        if nieuwe_huidige_wapen.afbeelding != huidig_wapen.afbeelding:
            stok_image = sdl2.ext.load_image(nieuwe_huidige_wapen.afbeelding)
            stok_texture = sdl2.ext.Texture(renderer, stok_image)  # Laad nieuwe texture
            huidig_wapen = nieuwe_huidige_wapen

        if speelwereld is wereld_map4:
            render_stok(renderer, stok_texture)

        #print(int(p_speler_x), int(p_speler_y))

        if speelwereld is winkel_map:
            if eerste==True:
                visitShopsText = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(
                    f"Visit the shops in this order to sell sushi: {randomShopArray}"))
                render_text(fps_font, renderer, window, speler, visitShopsText,0.8)


            # Check if the player is in a shop and visit the shop
            if (int(p_speler_x), int(p_speler_y)) in shop_locations:
                shop_id = shop_locations[(int(p_speler_x), int(p_speler_y))]

                # If the shop has not been visited, add it
                if shop_id not in visited_shops:
                    visited_shops.append(shop_id)
                    print(f"Shop {shop_id} visited and added to the array!")

                # Check if the player visited shops in the correct order
                if len(visited_shops) == len(randomShopArray):
                    if np.array_equal(visited_shops, randomShopArray):
                        #print("All shops visited in the correct order!")
                        correct_order = True
                        correctgeluid= mixer.Mix_LoadWAV(b'resources/audio/answer-correct.mp3')
                        mixer.Mix_PlayChannel(-1, correctgeluid, 0)
                        correct = True
                        eerste= False
                        oncorrect = False

                        if soldsushinognietgebeurd == False:
                            speler.sell_sushi()
                            #print('gebeurd')
                        visited_shops= []
                        randomShopArray = np.random.permutation(np.arange(1, 7))
                        soldsushinognietgebeurd ==True

                    else:
                        #print("Sorry, you lost all your loot")
                        oncorrect = True
                        correct = False
                        eerste = False
                        foutgeluid = mixer.Mix_LoadWAV(b'resources/audio/fout.mp3')
                        mixer.Mix_PlayChannel(-1, foutgeluid, 0)
                        speler.delete_inventory()
                        speler.decrease_xp(speler.xp//2)

                        correct_order = False
                        visited_shops= []
                        randomShopArray = np.random.permutation(np.arange(1, 7))

                # Correct antwoord: plan een switch over 5 seconden
                if correct and not oncorrect and switch_time is None:
                    current_message = "All shops visited in the correct order!"
                    visitShopsText = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(current_message))
                    render_text(fps_font, renderer, window, speler, visitShopsText,0.8)
                    switch_time = time.time() + 3  # 3 seconden vanaf nu

                # Fout antwoord: plan een switch over 5 seconden
                if not correct and oncorrect and switch_time is None:
                    current_message = "Wrong order, you lost all your sushi and half your XP!"
                    visitShopsText = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(current_message))
                    render_text(fps_font, renderer, window, speler, visitShopsText,0.8)
                    switch_time = time.time() + 3  # 3 seconden vanaf nu

                # Herhaal het renderen van de boodschap totdat de map wordt gewisseld
            if switch_time is not None:
                visitShopsText = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(current_message))
                render_text(fps_font, renderer, window, speler, visitShopsText,0.8)

            # Controleer of de tijd is verstreken en wissel de map
            if switch_time is not None and time.time() >= switch_time:
                switch_to_map(wereld_map4)
                switch_time = None  # Reset de timer voor toekomstige acties
                current_message = None  # Reset de boodschap







        #render_xp(fps_font, renderer, window, speler)
        if map_start_time is not None:
            elapsed_time = int(time.time() - map_start_time) # Calculate elapsed time
            #print(elapsed_time)

            tijd_texture = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(f"Time: {switch_interval - elapsed_time}"))

            if elapsed_time >= switch_interval/2:
                # skybox_texture = laad_skybox(renderer, "resources/skyboxtest.png")
                teken_minimap(renderer,speelwereld,p_speler_x,p_speler_y,maze_sprites)
            if elapsed_time >= switch_interval:
                # Switch back to the default map
                skybox_texture = laad_skybox(renderer, "resources/skyboxtest.png")
                switch_to_map(wereld_map4)
                map_start_time = None  # Reset the timer so it doesn't repeat
            if tijd_texture:
                render_text(fps_font, renderer, window, speler, tijd_texture, 1.2)


        if speler.xp_veranderd:
            xp_texture = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(f"XP: {speler.xp}"))
            speler.xp_veranderd = False

            # Render xp_texture elke frame, zodat de box blijft staan
        if xp_texture:
            render_xp(fps_font, renderer, window, speler, xp_texture)
            # commandEenheden, commandTientallen = show_xp_controller(speler.xp)
            # ser.write(commandEenheden.encode("utf-8"))
            # ser.write(commandTientallen.encode("utf-8"))


        next(fps_generator)
        # Toon het getekende scherm

        renderer.present()
        if speelwereld is wereld_map4:
            counter += delta
            if counter >= interval:
                golf_index += 1  # Verander de afbeelding
                if golf_index >= len(textures2):  # Reset de index als het einde is bereikt
                    golf_index = 0
                counter = 0  # Reset de counter
    mixer.Mix_CloseAudio()
    mixer.Mix_CloseAudio()
    sdl2.ext.quit()

if __name__ == "__main__":
    main()