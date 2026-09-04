from pgzero.rect import Rect
from pgzero.actor import Actor

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.music_on = True

        self.play_btn = Rect((width // 2 - 100, 350), (200, 50))
        self.music_btn = Rect((width // 2 - 100, 450), (200, 50))
        
        self.mushroom = Actor("mushroom_red")
        self.mushroom.x = width // 2 - 100
        self.mushroom.y = height - 50

    def handle_click(self, pos, music):
        if self.play_btn.collidepoint(pos):
            return "start_game"

        if self.music_btn.collidepoint(pos):
            self.music_on = not self.music_on
            if self.music_on:
                music.play("bg_music")
            else:
                music.stop()

        return None

    def draw(self, screen):
        screen.fill((87, 194, 119))
        screen.draw.text("Doodle Game", center=(self.width // 2, 200), fontsize=64, color="black")

        # Кнопка грати
        screen.draw.filled_rect(self.play_btn, (173, 114, 237))
        screen.draw.text("Play", center=self.play_btn.center, fontsize=32, color="white")

        # Кнопка музики
        screen.draw.filled_rect(self.music_btn, (173, 114, 237))
        music_text = "On" if self.music_on else "Off"
        screen.draw.text(music_text, center=self.music_btn.center, fontsize=24, color="white")

        # Інтерактивні елементи
        self.mushroom.draw()