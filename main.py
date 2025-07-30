import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.vector import Vector
from kivy.uix.label import Label

# Configurações iniciais
CELL = 20
Window.size = (640, 480)

class Player(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.sprite = Rectangle(source='assets/player.png', pos=self.pos, size=(CELL, CELL))
        self.bind(pos=self._update_sprite)

    def _update_sprite(self, instance, value):
        self.sprite.pos = value

    def move(self):
        new_pos = Vector(*self.velocity) + Vector(self.x, self.y)
        self.x = max(0, min(new_pos.x, self.parent.width - CELL))
        self.y = max(0, min(new_pos.y, self.parent.height - CELL))

class Snake(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.sprite = Rectangle(source='assets/snake.png', pos=self.pos, size=(CELL, CELL))
        self.bind(pos=self._update_sprite)

    def _update_sprite(self, instance, value):
        self.sprite.pos = value

    def chase(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        if abs(dx) > abs(dy):
            self.x += CELL if dx > 0 else -CELL
        else:
            self.y += CELL if dy > 0 else -CELL

class GameField(Widget):
    player = ObjectProperty(None)
    snake = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spawn_door()
        self.score = 0
        self.lives = 3
        # HUD
        self.score_lbl = Label(text="Score: 0", pos=(10, self.height - 30))
        self.lives_lbl = Label(text="Lives: 3", pos=(10, self.height - 60))
        self.add_widget(self.score_lbl)
        self.add_widget(self.lives_lbl)
        self.touch_start = None

    def spawn_door(self):
        self.door_x = random.randint(0, int(self.width/CELL)-1) * CELL
        self.door_y = random.randint(0, int(self.height/CELL)-1) * CELL

    def update(self, dt):
        self.player.move()
        self.snake.chase(self.player)

        # Colisão cobra ↔ player
        if self.player.collide_widget(self.snake):
            self.lives -= 1
            self.reset_positions()
            if self.lives == 0:
                self.score = 0
                self.lives = 3

        # Colisão player ↔ porta
        if abs(self.player.x - self.door_x) < CELL/2 and abs(self.player.y - self.door_y) < CELL/2:
            self.score += 1
            self.spawn_door()

        # Atualiza HUD
        self.score_lbl.text = f"Score: {self.score}"
        self.lives_lbl.text = f"Lives: {self.lives}"

        # Desenho da porta
        self.canvas.after.clear()
        with self.canvas.after:
            Rectangle(source='assets/door.png', pos=(self.door_x, self.door_y), size=(CELL, CELL))

    def on_touch_down(self, touch):
        self.touch_start = (touch.x, touch.y)
        return True

    def on_touch_up(self, touch):
        if not self.touch_start:
            return
        dx = touch.x - self.touch_start[0]
        dy = touch.y - self.touch_start[1]
        if abs(dx) > abs(dy):
            direction = (CELL, 0) if dx > 0 else (-CELL, 0)
        else:
            direction = (0, CELL) if dy > 0 else (0, -CELL)
        self.player.velocity = direction
        self.touch_start = None
        return True

    def reset_positions(self):
        self.player.center = self.center
        self.snake.pos = (0, 0)
        self.spawn_door()

class SnakeChaseApp(App):
    def build(self):
        game = GameField()
        game.player = Player(pos=(game.width/2, game.height/2), size=(CELL, CELL))
        game.snake = Snake(pos=(0, 0), size=(CELL, CELL))
        game.add_widget(game.player)
        game.add_widget(game.snake)
        Clock.schedule_interval(game.update, 0.5)
        return game

if __name__ == '__main__':
    SnakeChaseApp().run()

