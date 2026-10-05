import pygame
from os.path import join

class SoundManager:
    """Manages all audio in the space game including background music and sound effects."""

    def __init__(self):
        """Initialize the audio system and load all sound assets."""
        # Initialize the mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # Load sound effects
        self.laser_sound = pygame.mixer.Sound(join("assets", "audio", "laser.wav"))
        self.explosion_sound = pygame.mixer.Sound(join("assets", "audio", "explosion.wav"))
        self.damage_sound = pygame.mixer.Sound(join("assets", "audio", "damage.ogg"))

        # Load and configure background music
        pygame.mixer.music.load(join("assets", "audio", "game_music.wav"))
        pygame.mixer.music.set_volume(0.3)  # Background music at 30% volume

        # Set sound effect volumes (optional - can adjust if needed)
        self.laser_sound.set_volume(0.5)
        self.explosion_sound.set_volume(0.7)
        self.damage_sound.set_volume(0.6)

    def play_laser(self):
        """Play the laser sound effect."""
        self.laser_sound.play()

    def play_explosion(self):
        """Play the explosion sound effect."""
        self.explosion_sound.play()

    def play_damage(self):
        """Play the damage sound effect."""
        self.damage_sound.play()

    def play_background_music(self):
        """Start or restart the background music (loops indefinitely)."""
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def stop_background_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        """Set the background music volume (0.0 to 1.0).

        Args:
            volume: Float between 0.0 (silent) and 1.0 (maximum volume)
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

    def set_sfx_volume(self, volume):
        """Set the volume for all sound effects (0.0 to 1.0).

        Args:
            volume: Float between 0.0 (silent) and 1.0 (maximum volume)
        """
        volume = max(0.0, min(1.0, volume))
        self.laser_sound.set_volume(volume)
        self.explosion_sound.set_volume(volume)
        self.damage_sound.set_volume(volume)