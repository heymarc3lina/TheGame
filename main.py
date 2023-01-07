import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480
marioGlobal = None
mario = None
menuGlobal = None
menu = None
levelGlobal = None
level = None
dashboardGlobal = None
dashboard = None
def main():
    global marioGlobal
    global mario
    global menu
    global menuGlobal
    global levelGlobal
    global level
    global dashboardGlobal
    global dashboard

    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    sound = Sound()

    if marioGlobal is None:
        dashboard = Dashboard("./img/font.png", 8, screen)
        dashboardGlobal = dashboard
        level = Level(screen, sound, dashboard)
        levelGlobal = level
        mario = Mario(0, 0, level, screen, dashboard, sound)
        marioGlobal = mario
        menu = Menu(screen, dashboard, level, sound)
        menuGlobal = menu

    if mario.isNextLevel:
        menu.loadNextLevel()
        level = menu.level
        level.dashboard = menu.dashboard

    if mario.backToMenu and menu.isGameWon():
        menu.start = False
        marioGlobal = None
        return 'restart'

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()

    while not mario.backToMenu:
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
