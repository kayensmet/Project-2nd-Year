import sdl2
import sdl2.ext
from minigame_slice import select_fish, select_sliced_fish
import tkinter as tk


from wapens import Wapen, Speler
import sdl2.sdlmixer as mixer

import time

# Je moet de RESOURCES variabele ook verplaatsen of apart definiëren in dit bestand
RESOURCES = sdl2.ext.Resources(__file__, "resources/Sprites")
resources = sdl2.ext.Resources(__file__, "resources")

# Globale variabelen
volume = 50  # Initiële volumewaarde
in_menu = True  # Of de applicatie in het hoofdmenu is
in_settings = False  # Of de applicatie in het instellingenmenu is
in_home = False  # Of de applicatie in de 'home' mode is
in_gohome = False

moet_afsluiten = False  # Of de applicatie moet sluiten
root = tk.Tk()
root.title("Fade Effect")
HOOGTE = 600           # Totale hoogte van het venster of canvas
BREEDTE = 800
font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=(255, 255, 255))



def setup_audio():
    if mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 3, 4096) == -1:
        print("Fout bij het openen van het audiokanaal:", mixer.Mix_GetError())
    else:
        print("Audio correct geopend.")




def onclickStart(button, event, geluid):
    print("Startknop ingedrukt")
    global in_menu
    in_menu = False  # Verlaat het hoofdmenu
    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
    mixer.Mix_PlayChannel(-1, selectgeluid, 0)

    # Stop het geluid
    mixer.Mix_HaltChannel(1)


def onclickHome(button, event, renderer, window, achtergrond, spriterenderer, speler, geluid):
    print("Ga naar huis knop ingedrukt")

    mixer.Mix_HaltChannel(1)
    global in_home, in_gohome
    in_home = True
    in_gohome = False
    toon_huis(window, renderer, achtergrond, button, speler)



def onclickSettings(button, event, window, renderer,speler):
    print("help geopend")
    global in_menu, in_settings
    in_menu = False
    in_settings = True
    toon_help_menu(renderer, window)
    toon_hoofdmenu(renderer, window, speler)


def adjust_volume(change, speler):
    global volume
    # Pas het volume aan met de wijziging, begrens het tussen 0 en 100
    volume = max(0, min(100, volume + change))
    print(f"Volume: {volume}%")


def onclickMiniGame(button, event, renderer, window, speler):
    print("Mini-game knop ingedrukt")
    selectgeluid= mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
    select_fish(renderer, window, speler)

def onclickMiniGame2(button, event, renderer, window, speler, achtergrond):
    print("Mini-game2 knop ingedrukt")
    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
    select_sliced_fish(renderer, window, speler, achtergrond, button)





def gohome(button, event, renderer, window, achtergrond, spriterenderer, speler):
    global in_menu, in_gohome
    in_menu = False
    in_gohome = True
    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknopgood.mp3')
    mixer.Mix_PlayChannel(-1, selectgeluid, 0)

    # Initialize factories and UI components
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    spriterenderer = factory.create_sprite_render_system(window)

    # Load the background image (keeps static)
    background_image = factory.from_image(resources.get_path("gohomebackground.jpg"))

    # Load the moving image
    boot_image = factory.from_image(resources.get_path("boot_heenn.png"))

    # Get the width of the window
    window_width = window.size[0]

    # Set initial position of the boot image off-screen (left)
    x_pos = 100  # Start at pixel 300
    y_pos = 430  # Constant y-position

    # Render background and the boot image moving from left to right
    running = True
    while running:
        # Event handling to break out of the loop
        for e in sdl2.ext.get_events():
            if e.type == sdl2.SDL_QUIT:
                window.close()
                running = False

        # Clear the screen
        renderer.clear()

        # Render the static background image
        spriterenderer.render(background_image)

        # Update the x position of the boot image to make it move right
        if x_pos < 500:  # The boot image should stop at 500px
            x_pos += 3  # Speed of the movement (increase or decrease to change speed)
        else:
            running = False  # Stop moving when image reaches the right edge (500px)

        # Set new position for the boot image
        boot_image.position = (x_pos, y_pos)

        # Render the boot image
        spriterenderer.render(boot_image)

        # Refresh the window with the new image positions
        window.refresh()

        # Delay to control the animation speed
        sdl2.SDL_Delay(10)

    # Call the next function (onclickHome)
    onclickHome(button, event, renderer, window, achtergrond, spriterenderer, speler, menugeluid)


def nohome(button, event, renderer, window, speler):
    selectgeluid=mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
    mixer.Mix_PlayChannel(-1,selectgeluid,0)
    global in_menu, in_gohome, in_home
    in_menu = False
    in_gohome = True
    in_home= False

    # Initialize factories and UI components
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    spriterenderer = factory.create_sprite_render_system(window)

    # Load the background image (keeps static)
    house_image = factory.from_image(resources.get_path("gohomebackground.jpg"))

    # Load the moving image (boot_heen.png)
    boot_image = factory.from_image(resources.get_path("boot_heen.png"))

    # Get the width of the window
    window_width = window.size[0]

    # Set initial position of the boot image off-screen to the right
    x_pos = 500  # Start at pixel 300
    y_pos = 430  # Constant y-position

    # Render the background and the boot image moving from right to left
    running = True
    while running:
        # Event handling to break out of the loop
        for e in sdl2.ext.get_events():
            if e.type == sdl2.SDL_QUIT:
                running = False

        # Clear the screen
        renderer.clear()

        # Render the static background image
        spriterenderer.render(house_image)

        # Update the x position of the boot image to move it left
        if x_pos > 100:  # The boot image should stop at 300px
            x_pos -= 3  # Speed of the movement (increase or decrease to change speed)
        else:
            running = False  # Stop moving when image reaches the left edge (300px)

        # Set new position for the boot image
        boot_image.position = (x_pos, y_pos)

        # Render the boot image
        spriterenderer.render(boot_image)

        # Refresh the window with the new image positions
        window.refresh()

        # Delay to control the animation speed
        sdl2.SDL_Delay(10)

    # Call the next function (toon_hoofdmenu)
    renderer.clear()
    window.refresh()
    toon_hoofdmenu(renderer, window, speler)

def toon_huis(window, renderer, achtergrond, button, speler):
    global in_home

    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE)
    sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)
    print(speler.inventory)

    # Initialiseer de sprite- en UI-factories
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    uifactory = sdl2.ext.UIFactory(factory)
    uiprocessor = sdl2.ext.UIProcessor()

    # Renderer voor de sprites
    spriterenderer = factory.create_sprite_render_system(window)

    # Laad de achtergrondafbeelding
    house_image = factory.from_image(resources.get_path("binnenkant_winkel.jpg"))

    # Creëer knoppen als UI-elementen
    MiniGameButton = uifactory.from_image(sdl2.ext.BUTTON, resources.get_path("MiniGameButton.jpg"))
    MiniGame2Button = uifactory.from_image(sdl2.ext.BUTTON, resources.get_path("MiniGame2Button.png"))
    HomeButton = uifactory.from_image(sdl2.ext.BUTTON, resources.get_path("menuknop.png"))



    # Positie van de knoppen
    MiniGameButton.position = (460, 325)
    HomeButton.position = (5, 5)
    MiniGame2Button.position = (280, 110)


    # Voeg click-events toe aan de knoppen
    MiniGameButton.click += lambda button, event: onclickMiniGame(button, event, renderer, window, speler)
    HomeButton.click += lambda button, event: nohome(button, event, renderer, window, speler)
    MiniGame2Button.click += lambda button, event: onclickMiniGame2(button, event, renderer, window, speler, achtergrond)


    # Initialiseer achtergrond en knoppen eenmaal, buiten de loop
    renderer.clear()
    spriterenderer.render(house_image)
    spriterenderer.render(MiniGameButton)
    spriterenderer.render(HomeButton)
    spriterenderer.render(MiniGame2Button)
    window.refresh()

    while in_home:
        key_states = sdl2.SDL_GetKeyboardState(None)
        if key_states[sdl2.SDL_SCANCODE_SPACE]:
            in_home = False
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                global moet_afsluiten
                moet_afsluiten = True
                window.close()
                return
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:
                    nohome(button, event, renderer, window, speler)
                    return

            # Verwerk de UI-events voor de knoppen
            uiprocessor.dispatch([MiniGameButton, HomeButton, MiniGame2Button], event)

        # Voorkom herladen door niet te her-renderen zonder verandering
        window.refresh()  # Alleen nodig bij event-activiteit



def toon_hoofdmenu(renderer, window, speler):
    global in_menu, in_gohome, menugeluid, in_help_menu
    in_menu = True
    in_gohome = False
    in_help_menu = False
    print(speler.inventory)
    sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE)
    sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    uifactory = sdl2.ext.UIFactory(factory)

    setup_audio()
    menugeluid = mixer.Mix_LoadWAV(b'resources/audio/menu_song.mp3')
    mixer.Mix_PlayChannel(1, menugeluid, -1)

    uiprocessor = sdl2.ext.UIProcessor()
    spriterenderer = factory.create_sprite_render_system(window)
    achtergrond = factory.from_image(resources.get_path("menu_achtergrond2.jpg"))

    StartButton = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("StartButton2.jpg"))
    Helpbutton = uifactory.from_image(sdl2.ext.BUTTON, resources.get_path("helpbutton.png"))
    HomeButton = uifactory.from_image(sdl2.ext.BUTTON, resources.get_path("HomeButton2.jpg"))

    StartButton.position = 280, 170
    Helpbutton.position = 10, 1
    HomeButton.position = 280, 300

    StartButton.click += lambda button, event: onclickStart(button, event, menugeluid)
    Helpbutton.click += lambda button, event: onclickSettings(button, event, window, renderer,speler)
    HomeButton.click += lambda button, event: gohome(button, event, renderer, window, achtergrond, spriterenderer, speler)

    while in_menu:
        key_states = sdl2.SDL_GetKeyboardState(None)
        if key_states[sdl2.SDL_SCANCODE_SPACE]:
            in_menu = False
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                global moet_afsluiten
                window.close()
                in_menu = False
                moet_afsluiten = True
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:
                    if in_help_menu:
                        global moet_afluiten
                        moet_afsluiten= False
                    else:
                        mixer.Mix_Volume(1,0)
                        moet_afsluiten = True
                        print('dit gebeur')

                    return


            uiprocessor.dispatch([StartButton, Helpbutton, HomeButton], event)

        renderer.clear()
        spriterenderer.render((achtergrond, StartButton, Helpbutton, HomeButton))
        window.refresh()

def load_image(image_path, renderer):
    surface = sdl2.ext.load_image(image_path)  # Gebruik SDL_image om te laden
    texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
    return texture

def toon_help_menu(renderer, window):
    # Laad de Help-afbeelding
    global in_help_menu, in_menu
    renderer.clear()
    window.refresh()

    exit_button_rect = sdl2.SDL_Rect(10, 10, 80, 40)


    help_image_path = "help.png"  # Pad naar je afbeelding
    help_texture = load_image(help_image_path, renderer)
    in_menu=False

    in_help_menu = True
    while in_help_menu:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                global moet_afsluiten
                moet_afsluiten = True
                window.close()
                return
            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:  # Escape om het help-menu te verlaten
                    in_help_menu = False
                    return
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x, y = event.button.x, event.button.y
                if exit_button_rect.x <= x <= exit_button_rect.x + exit_button_rect.w and \
                        exit_button_rect.y <= y <= exit_button_rect.y + exit_button_rect.h:
                    selectgeluid = mixer.Mix_LoadWAV(b'resources/audio/selectknop.mp3')
                    mixer.Mix_PlayChannel(-1, selectgeluid, 0)
                    print("Exit-knop ingedrukt. Terug naar vorige scherm.")
                    return False  # Terug naar vorige scherm


        # Render de help-afbeelding als overlay
        renderer.clear()  # Maak het scherm leeg (als nodig)
        dstrect = sdl2.SDL_Rect(0, 0, 800, 600)  # Volledig scherm
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, help_texture, None, dstrect)  # Render afbeelding
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 250, 0, 0, 255)  # Rode kleur voor de knop
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, exit_button_rect)  # Vul de knop met rood

        # Teken de witte rand van de knop
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 255, 255, 255)
        sdl2.SDL_RenderDrawRect(renderer.sdlrenderer, exit_button_rect)

        # Teken een witte "X" op de knop
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer,
                                exit_button_rect.x + 10, exit_button_rect.y + 10,
                                exit_button_rect.x + exit_button_rect.w - 10,
                                exit_button_rect.y + exit_button_rect.h - 10)
        sdl2.SDL_RenderDrawLine(renderer.sdlrenderer,
                                exit_button_rect.x + exit_button_rect.w - 10, exit_button_rect.y + 10,
                                exit_button_rect.x + 10, exit_button_rect.y + exit_button_rect.h - 10)
        renderer.present()  # Breng de wijzigingen in beeld

