import random
from gym_dino.envs.dino_cfg import *
from gym_dino.envs.dyno_gameobjects import Dino, Ground, Scoreboard, Cactus, Cloud, load_image, load_sprite_sheet, Ptera


class DinoGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.counter = 0

        self.game_quit = False
        self.game_over = False
        self.game_speed = game_speed

        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("T-Rex Rush")

        self.playerDino = Dino(44, 47)
        self.ground = Ground(-1 * game_speed)
        self.scoreboard = Scoreboard()
        self.cacti = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()
        if pteras_on:
            self.pteras = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Cloud.containers = self.clouds

        self.retbutton_image, self.retbutton_rect = load_image('replay_button.png', 35, 31, -1)
        self.gameover_image, self.gameover_rect = load_image('game_over.png', 190, 11, -1)

        temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.HI_image = pygame.Surface((22, int(11 * 6 / 5)))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(background_col)
        self.HI_image.blit(temp_images[10], temp_rect)
        temp_rect.left += temp_rect.width
        self.HI_image.blit(temp_images[11], temp_rect)
        self.HI_rect.top = height * 0.1
        self.HI_rect.left = width * 0.73

    def step(self, action):
        """
        Renders a step in the environment
        :param action:
        0 -> no action
        1 -> jump
        2 -> duck
        :return:
        """
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            self.game_quit = True
            self.game_over = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_quit = True
                    self.game_over = True

            if action == 1:
                if self.playerDino.rect.bottom == int(0.98 * height):
                    self.playerDino.isJumping = True
                    if pygame.mixer.get_init() is not None:
                        jump_sound.play()
                    self.playerDino.movement[1] = -1 * self.playerDino.jumpSpeed

            if action == 2:
                if not (self.playerDino.isJumping and self.playerDino.isDead):
                    self.playerDino.isDucking = True

            if action == 0:
                self.playerDino.isDucking = False

        if self.playerDino.isDead:
            self.game_over = True

        if self.counter % 700 == 699:
            self.ground.speed -= 0  # initial era 1
            self.game_speed += 0  # era initial +1

        self.counter = self.counter + 1

        if self.game_quit:
            pygame.quit()
            quit()

    def draw(self):

        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            self.game_quit = True
            self.game_over = True

        for c in self.cacti:
            c.movement[0] = -1 * self.game_speed
            if pygame.sprite.collide_mask(self.playerDino, c):
                self.playerDino.isDead = True
                if pygame.mixer.get_init() is not None:
                    die_sound.play()
        if pteras_on:
            for p in self.pteras:
                p.movement[0] = -1 * self.game_speed
                if pygame.sprite.collide_mask(self.playerDino, p):
                    self.playerDino.isDead = True
                    if pygame.mixer.get_init() is not None:
                        die_sound.play()

        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(self.game_speed, 40, 40))
            else:
                for obstacle in self.last_obstacle:
                    if obstacle.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(self.game_speed, 40, 40))
        if pteras_on:
            if len(self.pteras) == 0 and random.randrange(0, 200) == 10 and self.counter > 500:
                for obstacle in self.last_obstacle:
                    if obstacle.rect.right < width * 0.8:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Ptera(self.game_speed, 46, 40))

        if len(self.clouds) < 5 and random.randrange(0, 300) == 10:
            Cloud(width, random.randrange(height / 5, height / 2))

        self.playerDino.update()
        self.cacti.update()
        if pteras_on:
            self.pteras.update()
        self.clouds.update()
        self.ground.update()
        self.scoreboard.update(self.playerDino.score)

        if pygame.display.get_surface() is not None:
            self.screen.fill(background_col)
            self.ground.draw(self.screen)
            self.clouds.draw(self.screen)
            self.scoreboard.draw(self.screen)
            self.cacti.draw(self.screen)
            if pteras_on:
                self.pteras.draw(self.screen)
            self.playerDino.draw(self.screen)

            pygame.display.update()

        self.clock.tick(fps)


    def get_current_state(self):
        observation = pygame.image.tostring(self.screen, 'RGB')
        reward = self.playerDino.score
        done = self.game_over

        return observation, reward, done
