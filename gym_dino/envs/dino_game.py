import random
from gym_dino.envs.dino_cfg import *
from gym_dino.envs.dyno_gameobjects import Dino, Ground, Scoreboard, Cactus, Cloud, load_image, load_sprite_sheet, Ptera


class DinoGame:
    def __init__(self):
        self.high_score = 0
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
        self.highsc = Scoreboard(width * 0.78)
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

    def reset(self):
        pass

    def play(self):
        while not self.game_quit:
            while not self.game_over:
                if pygame.display.get_surface() is None:
                    print("Couldn't load display surface")
                    self.game_quit = True
                    self.game_over = True
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_quit = True
                            self.game_over = True

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                if self.playerDino.rect.bottom == int(0.98 * height):
                                    self.playerDino.isJumping = True
                                    if pygame.mixer.get_init() is not None:
                                        jump_sound.play()
                                    self.playerDino.movement[1] = -1 * self.playerDino.jumpSpeed

                            if event.key == pygame.K_DOWN:
                                if not (self.playerDino.isJumping and self.playerDino.isDead):
                                    self.playerDino.isDucking = True

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_DOWN:
                                self.playerDino.isDucking = False
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
                self.highsc.update(self.high_score)

                if pygame.display.get_surface() is not None:
                    self.screen.fill(background_col)
                    self.ground.draw(self.screen)
                    self.clouds.draw(self.screen)
                    self.scoreboard.draw(self.screen)
                    if self.high_score != 0:
                        self.highsc.draw(self.screen)
                        self.screen.blit(self.HI_image, self.HI_rect)
                    self.cacti.draw(self.screen)
                    if pteras_on:
                        self.pteras.draw(self.screen)
                    self.playerDino.draw(self.screen)

                    pygame.display.update()
                self.clock.tick(fps)

                if self.playerDino.isDead:
                    self.game_over = True
                    if self.playerDino.score > self.high_score:
                        self.high_score = self.playerDino.score

                if self.counter % 700 == 699:
                    self.ground.speed -= 0  # initial era 1
                    self.game_speed += 0  # era initial +1
                    # pygame.image.save(screen,"screenshot.png")
                    # imagine = pygame.image.tostring(screen,"RGB")
                    # imagine = pygame.surfarray.array3d(self.screen)  # dim (600,150,3)
                    # plt.imshow(np.flip(np.rot90(imagine,k=1,axes=(1,0)),axis=1)) # imaginea corecta
                    # plt.show()

                counter = (self.counter + 1)

            if self.game_quit:
                break

            while self.game_over:
                if pygame.display.get_surface() is None:
                    print("Couldn't load display surface")
                    self.game_quit = True
                    self.game_over = False
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_quit = True
                            self.game_over = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.game_quit = True
                                self.game_over = False

                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                self.game_over = False
                                self.play()
                self.highsc.update(self.high_score)
                if pygame.display.get_surface() is not None:
                    self.disp_gameOver_msg(self.retbutton_image, self.gameover_image)
                    if self.high_score != 0:
                        self.highsc.draw(self.screen)
                        self.screen.blit(self.HI_image, self.HI_rect)
                    pygame.display.update()
                self.clock.tick(fps)

        pygame.quit()
        quit()

    def get_current_state(self):
        pass

    def disp_gameOver_msg(self, retbutton_image, gameover_image):
        retbutton_rect = retbutton_image.get_rect()
        retbutton_rect.centerx = width / 2
        retbutton_rect.top = height * 0.52

        gameover_rect = gameover_image.get_rect()
        gameover_rect.centerx = width / 2
        gameover_rect.centery = height * 0.35

        self.screen.blit(retbutton_image, retbutton_rect)
        self.screen.blit(gameover_image, gameover_rect)


if __name__ == "__main__":
    game = DinoGame()
    game.play()
