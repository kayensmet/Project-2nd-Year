import sdl2.ext
from PIL import Image
import os

class Sprite:
    def __init__(self, x, y, scale, image_path, renderer, rotation=0, max_health=100):
        """
        Initialiseert een sprite met positie, schaal en afbeelding.

        Args:
        x (float): X-positie van de sprite.
        y (float): Y-positie van de sprite.
        scale (float): Schaalfactor van de sprite.
        image_path (str): Bestandspad naar de sprite-afbeelding.
        renderer: Het SDL2 renderer object.
        """
        self.x = x
        self.y = y
        self.scale = scale
        self.image_path = image_path
        self.image = sdl2.ext.load_image(image_path)  # Laad de afbeelding met SDL2
        self.texture = sdl2.ext.Texture(renderer, self.image)  # Maak de texture aan
        self.pil_image = Image.open(image_path)  # Gebruik Pillow om de afbeelding te openen voor breedte/hoogte
        self.rotation = rotation
        # Gezondheidsattributen
        self.max_health = max_health
        self.current_health = max_health  # Start met maximale HP

    def take_damage(self, damage):
        """
        Vermindert de huidige gezondheid met de gegeven schade.
        """
        self.current_health = max(0, self.current_health - damage)  # Zorg dat health niet onder 0 gaat

    def is_dead(self):
        """
        Controleert of de sprite dood is.
        """
        return self.current_health == 0

    def get_health_percentage(self):
        """
        Geeft het percentage van de overgebleven gezondheid terug.
        """
        return self.current_health / self.max_health



    def get_position(self):
        return self.x, self.y

    def get_positionX(self):
        return self.x

    def get_positionY(self):
        return self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_scale(self, scale):
        self.scale = scale

    def get_texture(self):
        """Geeft de SDL2 texture terug."""
        return self.texture

    def get_width(self):
        """Geeft de breedte van de sprite afbeelding terug."""
        return self.pil_image.width

    def get_height(self):
        """Geeft de hoogte van de sprite afbeelding terug."""
        return self.pil_image.height

    def get_spritepathname(self):
        return os.path.basename(self.image_path)

    def take_damage(self, damage):
        """
        Vermindert de huidige gezondheid met de gegeven schade.

        Args:
        damage (int): Het aantal schadepunten.
        """
        self.current_health = max(0, self.current_health - damage)  # Zorg dat health niet onder 0 gaat

    def is_dead(self):
        """
        Controleert of de sprite dood is.

        Returns:
        bool: True als de sprite geen health meer heeft, anders False.
        """
        return self.current_health == 0

    def get_current_health(self):
        return self.current_health
