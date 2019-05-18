from livewires import games, color

import random

games.init(screen_width=840, screen_height=480, fps=50)


class Hero(games.Sprite):

    image = games.load_image('img/ship.png')

    MISSILE_DELAY = 40

    def __init__(self,  x = 30, y=240):
        super(Hero, self).__init__(image=Hero.image,
                                   x=x,y=y
                                   )
        self.missile_wait = 0


    def update(self):
        if games.keyboard.is_pressed(games.K_DOWN):
            self.y += 4
        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 4


        if self.missile_wait > 0:
            self.missile_wait -= 1

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait==0:
            new_missile = Missile(self.x, self.y)
            games.screen.add(new_missile)
            self.missile_wait = Hero.MISSILE_DELAY




class Rocket(games.Sprite):

    image = games.load_image('img/flash.png')
    speed = -3

    def __init__(self, y,x=820):
        super(Rocket, self).__init__(image=Rocket.image,
                                     x=x,
                                     y=y,
                                     dx=Rocket.speed)


    def smert(self):
        self.destroy()

    def update(self):
        for _ in self.overlapping_sprites:
            if not games.keyboard.is_pressed(games.K_SPACE):
                for sprite in self.overlapping_sprites:
                    sprite.destroy()
                    self.destroy()
    def update(self):
        if self.left < 0:
            self.end_game()


    def end_game(self):

        end_msg = games.Message(value='Вы проиграли!',
                                size=90,
                                color=color.red,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime=5 * games.screen.fps,
                                after_death=games.screen.quit
                                )
        games.screen.add(end_msg)



class Evil(games.Sprite):

    image = games.load_image('img/monster.png')

    def __init__(self, speed=2, odds_change=200):
        super(Evil, self).__init__(image=Evil.image,
                                   x=810,
                                   y=games.screen.height / 2,
                                   dy=speed)
        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        if self.bottom > 480 or self.top < 0:
            self.dy = -self.dy
        elif random.randrange(self.odds_change) == 0:
            self.dy = -self.dy
        self.check_drop()

    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_rocket = Rocket(y=self.y, x = 750)
            games.screen.add(new_rocket)

            self.time_til_drop = random.randint(30, 100)


class Missile(games.Sprite):
    image = games.load_image('img/fireworks.png')

    VELOCITY_FACTOR = 30
    LIFETIME = 20

    def __init__(self,hero_x,hero_y):
        x = hero_x
        y = hero_y
        dx = Missile.VELOCITY_FACTOR


        super(Missile, self).__init__(image=Missile.image,
                                     x=x+100,
                                     y=y,
                                     dx=dx,

                                          )
        self.lifetime = Missile.LIFETIME

        self.score = games.Text(value=0,
                                size=30,
                                right=games.screen.width - 10,
                                color=color.yellow,
                                top=5
                                )
        games.screen.add(self.score)

    def boom(self):
        for rocket in self.overlapping_sprites:
            rocket.handle_caught()
            self.score.value += 1

    def handle_caught(self):
        self.destroy()

    def smert(self):
        pass

    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:

                sprite.smert()
            self.destroy()
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        #self.boom()
class Game:
    def __init__(self):

        self.the_hero = Hero()
        games.screen.add(self.the_hero)

    def start(self):
        wall_image = games.load_image('img/space.jpg', transparent=False)
        games.screen.background = wall_image
        games.music.load('music/theme.wav')
        games.music.play()





def main():
    start = Game()
    start.start()

    the_hero = Hero()
    games.screen.add(the_hero)

    the_evil = Evil()
    games.screen.add(the_evil)

    games.screen.mainloop()

if __name__ == '__main__':
    main()
