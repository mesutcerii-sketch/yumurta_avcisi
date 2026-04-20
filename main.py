import os
import sys
import random
import pygame
from kivy.config import Config

# Beyaz ekran hatasını engelleyen ayar
os.environ['KIVY_AUDIO'] = 'none'

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.text import Label as CoreLabel

pygame.mixer.init()

# KLASÖR YOLU AYARI
KLASOR_YOLU = r"C:\Users\Mesut\Desktop\Yumurta Avcısı"
if os.path.exists(KLASOR_YOLU):
    os.chdir(KLASOR_YOLU)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class ChickenGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.level = 1
        self.broken_eggs = 0
        self.menu_state = "main"
        self.show_about_popup = False
        self.objects = []

        # BOYUTLAR
        self.basket_size = (90, 70)
        self.basket_pos = [355, 0]
        self.egg_size = (20, 26)
        self.gold_egg_size = (30, 40)
        self.bomb_size = (35, 35)
        self.logo_size = (180, 180)

        # SEVİYE RENKLERİ - Level 1 Açık Lacivert olarak ayarlandı
        self.level_colors = {
            1: (0.1, 0.3, 0.6, 1),  # Açık Lacivert
            2: (0.0, 0.5, 0.5, 1),  # Petrol Mavisi
            3: (0.4, 0.2, 0.7, 1),  # Mor
            4: (0.1, 0.6, 0.3, 1),  # Yeşil
            5: (0.7, 0.4, 0.1, 1),  # Turuncu
            6: (0.6, 0.1, 0.2, 1),  # Kırmızı/Bordo
        }

        self.load_assets()
        Clock.schedule_once(lambda dt: self.play_sound('intro', -1), 0.5)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def load_assets(self):
        self.sounds = {}
        sesler = {'intro': 'intro.wav', 'game_bg': 'ses1.wav', 'puan': 'ses2.wav',
                  'altin': 'ses2.wav', 'bomba': 'bomb.wav'}
        for k, v in sesler.items():
            yol = resource_path(v)
            if os.path.exists(yol): self.sounds[k] = pygame.mixer.Sound(yol)

        self.tex = {}
        resimler = {'s1': 'sepet.png', 's2': 'sepet2.png', 'b': 'bomb.png',
                    'g': 'altin.png', 'logo': 'kanal.png'}
        for k, v in resimler.items():
            yol = resource_path(v)
            if os.path.exists(yol): self.tex[k] = CoreImage(yol).texture

        self.bg_textures = {}
        for i in range(1, 11):
            yol = resource_path(f'arka{i}.jpg')
            if os.path.exists(yol): self.bg_textures[i] = CoreImage(yol).texture

    def play_sound(self, key, loops=0):
        if key in self.sounds: self.sounds[key].play(loops)

    def safe_draw_text(self, text, font_size, pos, color=(1, 1, 1, 1), bold=False):
        label = CoreLabel(text=text, font_size=font_size, bold=bold)
        label.refresh()
        if label.texture:
            Color(*color)
            Rectangle(texture=label.texture, pos=pos, size=label.texture.size)

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            # --- DİNAMİK ARKA PLAN ---
            current_bg = self.bg_textures.get(self.level)
            if current_bg:
                Color(1, 1, 1, 1)
                Rectangle(texture=current_bg, pos=(0, 0), size=(800, 600))
            else:
                # Resim yoksa level renklerini kullan (Level 1: Açık Lacivert)
                r, g, b, a = self.level_colors.get(self.level, (0.05, 0.05, 0.1, 1))
                Color(r, g, b, a)
                Rectangle(pos=(0, 0), size=(800, 600))

            if self.menu_state == "main":
                self.draw_main_menu()
                if self.show_about_popup:
                    self.draw_modern_about_popup()
            elif self.menu_state == "game":
                self.draw_game_screen()

            # Versiyon
            Color(1, 1, 1, 0.2)
            RoundedRectangle(pos=(715, 5), size=(80, 22), radius=[5])
            self.safe_draw_text("ver.1.0", 11, (728, 9), color=(1, 1, 1, 0.7))

    def draw_main_menu(self):
        if self.tex.get('logo'):
            Color(1, 1, 1, 1)
            Rectangle(texture=self.tex['logo'], pos=(400 - self.logo_size[0] / 2, 380), size=self.logo_size)
        self.safe_draw_text("YUMURTA AVCISI", 40, (260, 330), bold=True)
        Color(0.1, 0.8, 0.4, 1)
        RoundedRectangle(pos=(300, 220), size=(200, 60), radius=[15])
        self.safe_draw_text("OYUNA BAŞLA", 20, (335, 238), bold=True)
        Color(0.2, 0.5, 0.9, 1)
        RoundedRectangle(pos=(300, 140), size=(200, 60), radius=[15])
        self.safe_draw_text("HAKKINDA", 20, (355, 158), bold=True)

    def draw_modern_about_popup(self):
        Color(0, 0, 0, 0.75)
        Rectangle(pos=(0, 0), size=(800, 600))
        Color(0.1, 0.15, 0.3, 0.95)
        RoundedRectangle(pos=(150, 150), size=(500, 350), radius=[30])
        self.safe_draw_text("HAKKINDA", 30, (330, 430), bold=True, color=(0.2, 0.8, 1, 1))
        info = "Hazırlayan: Mesut ÇERİ\n\nBurhanettin Yıldız And. Tek. Lisesi Yazılım Mezunu\n\nYoutube : @mesutunhayalatolyesi"
        self.safe_draw_text(info, 18, (215, 280))
        Color(0.9, 0.3, 0.3, 1)
        RoundedRectangle(pos=(325, 180), size=(150, 45), radius=[12])
        self.safe_draw_text("KAPAT", 16, (375, 192), bold=True)

    def draw_game_screen(self):
        # Skor Paneli
        Color(1, 1, 1, 0.15)
        RoundedRectangle(pos=(50, 540), size=(700, 50), radius=[20])
        skor_txt = f"SKOR: {self.score}  |  SEVİYE: {self.level}  |  HATA: {self.broken_eggs}/5"
        self.safe_draw_text(skor_txt, 20, (210, 552), bold=True)

        # Sepet
        sepet_key = 's2' if self.score >= 10 else 's1'
        if self.tex.get(sepet_key):
            Color(1, 1, 1, 1)
            Rectangle(texture=self.tex[sepet_key], pos=self.basket_pos, size=self.basket_size)

        for obj in self.objects[:]:
            hiz = 4 + (self.level * 1.3)
            obj['y'] -= hiz

            if self.basket_pos[0] < obj['x'] < self.basket_pos[0] + self.basket_size[0] and \
                    obj['y'] < self.basket_pos[1] + self.basket_size[1] - 10:
                if obj['type'] == 'bomb':
                    self.game_over()
                    return
                elif obj['type'] == 'gold':
                    self.score += 5
                    self.play_sound('altin')
                else:
                    self.score += 2
                    self.play_sound('puan')

                if self.score >= self.level * 20:
                    self.level += 1

                self.objects.remove(obj)
                continue

            Color(1, 1, 1, 1)
            if obj['type'] == 'gold' and self.tex.get('g'):
                Rectangle(texture=self.tex['g'], pos=(obj['x'], obj['y']), size=self.gold_egg_size)
            elif obj['type'] == 'bomb' and self.tex.get('b'):
                Rectangle(texture=self.tex['b'], pos=(obj['x'], obj['y']), size=self.bomb_size)
            else:
                Ellipse(pos=(obj['x'], obj['y']), size=self.egg_size)

            if obj['y'] < 0:
                if obj['type'] != 'bomb': self.broken_eggs += 1
                self.objects.remove(obj)
                if self.broken_eggs >= 5: self.game_over()

    def on_touch_move(self, touch):
        if self.menu_state == "game":
            self.basket_pos[0] = max(0, min(touch.x - self.basket_size[0] / 2, 800 - self.basket_size[0]))

    def on_touch_down(self, touch):
        if self.menu_state == "main":
            if self.show_about_popup:
                if 325 <= touch.x <= 475 and 180 <= touch.y <= 225: self.show_about_popup = False
            else:
                if 300 <= touch.x <= 500:
                    if 220 <= touch.y <= 280:
                        self.start_game()
                    elif 140 <= touch.y <= 200:
                        self.show_about_popup = True
        return True

    def start_game(self):
        self.score, self.level, self.broken_eggs, self.objects = 0, 1, 0, []
        self.menu_state = "game"
        for s in self.sounds.values(): s.stop()
        self.play_sound('game_bg', -1)
        Clock.schedule_once(self.spawn, 0.5)

    def spawn(self, dt):
        if self.menu_state == "game":
            r = random.random()
            tipo = 'egg'
            if r < 0.15:
                tipo = 'bomb'
            elif r < 0.25 and self.level >= 2:
                tipo = 'gold'

            self.objects.append({'x': random.randint(50, 750), 'y': 600, 'type': tipo})

            bekleme = max(0.35, 1.1 - (self.level * 0.12))
            Clock.schedule_once(self.spawn, bekleme)
        else:
            return False

    def game_over(self):
        self.menu_state = "main"
        for s in self.sounds.values(): s.stop()
        self.play_sound('bomba')
        Clock.schedule_once(lambda dt: self.play_sound('intro', -1), 2)


class YumurtaApp(App):
    def build(self):
        self.title = "Yumurta Avcısı - Mesut ÇERİ"
        return ChickenGame()


if __name__ == "__main__":
    YumurtaApp().run()

