import pygame

from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario

windowSize = 640, 480
menu = None
level = None
dashboard = None
marioGlobal = None
mario = None


def main():
    global marioGlobal
    global mario
    global menu
    global level
    global dashboard

    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    sound = Sound()

    if marioGlobal is None:
        dashboard = Dashboard("./img/font.png", 8, screen)
        level = Level(screen, sound, dashboard)
        menu = Menu(screen, dashboard, level, sound)
        mario = Mario(0, 0, level, screen, dashboard, sound)

    if mario.isNextLevel:
        menu.loadNextLevel()

        if menu.isGameWon():
            mario.gameWon()
            return 'restart'

        level = menu.level
        level.dashboard = menu.dashboard
        mario = Mario(0, 0, level, screen, dashboard, sound)
        if marioGlobal.powerUpState:
            mario.powerup(1)
        marioGlobal = mario

    if mario.backToMenu:
        menu.start = False
        marioGlobal = None
        return 'restart'

    while not menu.start:
        menu.update()

    if marioGlobal is None:
        mario = Mario(0, 0, level, screen, dashboard, sound)
        marioGlobal = mario

    clock = pygame.time.Clock()

    while not mario.backToMenu and not mario.isNextLevel:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
