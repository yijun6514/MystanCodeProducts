"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 0			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    while True:
        if graphics.get_dx() != 0 and graphics.get_dy() != 0:  # 當click啟動後才去接BreakoutGraphics，x, y 速度
            live = graphics.get_lives()
            vx = graphics.get_dx()
            vy = graphics.get_dy()
            if live == NUM_LIVES or graphics.brick_num == 0:
                break
            else:
                graphics.ball.move(vx, vy)
                graphics.detect()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
