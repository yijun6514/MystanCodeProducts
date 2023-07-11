"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
NUM_LIVES = 3

COLORS = ["red", "orange", "yellow", "green", "blue"]


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout',
                 num_lives=NUM_LIVES):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT, x=(window_width-paddle_width)/2,
                            y=window_height-paddle_offset-paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = "black"
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(2*ball_radius, 2*ball_radius, x=window_width/2-ball_radius,
                          y=window_height/2-ball_radius)
        self.ball.filled = True
        self.ball.fill_color = "black"
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # label for the score/ win the game / game over
        self.label_1 = GLabel('Game Over')
        self.label_1.font = 'Courier-80-bold'
        self.label_1.color = 'red'
        self.label_2 = GLabel('You Win!!')
        self.label_2.font = '-80'
        self.score = 0
        self.score_label = GLabel('☆☆☆'+str(self.score)+'☆☆☆')
        self.score_label.font = '-30-bold'
        self.score_label.color = 'gray'
        self.window.add(self.score_label, x=window_width-self.score_label.width*9/7, y=self.window.height)
        self.lives = num_lives
        self.label_live = GLabel('❤'*self.lives)
        self.label_live.font = '-30-bold'
        self.label_live.color = 'red'
        self.window.add(self.label_live, x=0, y=self.label_live.height)

        # Initialize our mouse listeners
        onmouseclicked(self.start_game)
        onmousemoved(self.move_paddle)

        # Draw bricks
        self.brick_num = 0
        color_index = 0
        for i in range(brick_rows):
            if i % 2 == 0 and i != 0:
                color_index += 1
            for j in range(brick_cols):
                brick = GRect(brick_width, brick_height, x=j*(brick_width+brick_spacing),
                              y=brick_offset+i*(brick_height+brick_spacing))
                color = COLORS[color_index % len(COLORS)]
                brick.filled = True
                brick.fill_color = color
                self.window.add(brick)
                self.brick_num += 1

    # 控制paddle左右移動
    def move_paddle(self, mouse):
        if self.paddle.width/2 < mouse.x < self.window.width-self.paddle.width/2:
            self.paddle.x = mouse.x-self.paddle.width/2
        elif self.paddle.width > mouse.x:
            self.paddle.x = 0
        else:
            self.paddle.x = self.window.width-self.paddle.width

    # 控制遊戲開始
    def start_game(self, _):
        if self.not_move():
            self.set_ball_velocity()

    def not_move(self):
        if self.__dx == self.__dy == 0:
            return True

    # 重新開始後，給予求速度
    def set_ball_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:  # 設定一個0-1的隨機float, 0.5表示有一半的機會
            self.__dx = -self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    # 球碰撞後偵測是磚塊還是邊界/paddle
    def detect(self):                       # 設定ball四個角碰到的物件分別是 maybe_object 1234
        maybe_obj1 = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_obj2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        maybe_obj3 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        maybe_obj4 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        if maybe_obj1 is not None:
            if maybe_obj1 is not self.paddle and maybe_obj1 is not self.score_label\
                    and maybe_obj1 is not self.label_live:  # 若碰到磚塊，消除磚塊並改變速度
                # self.__dx *= -1
                self.__dy *= -1
                self.window.remove(maybe_obj1)
                self.score += 10
                self.score_label.text = '☆☆☆'+str(self.score)+'☆☆☆'
                self.brick_num -= 1
                if self.brick_num == 0:
                    self.win_the_game()
            elif maybe_obj1 is self.paddle:
                if self.__dy > 0:       # 若碰到paddle，且dy>0才會版彈，避免在板子上震盪
                    self.__dy *= -1
        elif maybe_obj2 is not None:
            if maybe_obj2 is not self.paddle and maybe_obj2 is not self.score_label\
                    and maybe_obj2 is not self.label_live:        # 若碰到brick 則反彈並消除
                self.__dy *= -1
                self.window.remove(maybe_obj2)
                self.score += 10
                self.score_label.text = '☆☆☆'+str(self.score)+'☆☆☆'
                self.brick_num -= 1
                if self.brick_num == 0:
                    self.win_the_game()
            elif maybe_obj2 is self.paddle:
                if self.__dy > 0:
                    self.__dy *= -1
        elif maybe_obj3 is not None:                 # 若碰到brick 則反彈並消除
            if maybe_obj3 is not self.paddle and maybe_obj3 is not self.score_label\
                    and maybe_obj3 is not self.label_live:
                self.__dy *= -1
                self.window.remove(maybe_obj3)
                self.score += 10
                self.score_label.text = '☆☆☆'+str(self.score)+'☆☆☆'
                self.brick_num -= 1
                if self.brick_num == 0:
                    self.win_the_game()
            elif maybe_obj3 is self.paddle:
                if self.__dy > 0:
                    self.__dy *= -1
        elif maybe_obj4 is not None:                 # 若碰到brick 則反彈並消除
            if maybe_obj4 is not self.paddle and maybe_obj4 is not self.score_label\
                    and maybe_obj4 is not self.label_live:
                self.__dy *= -1
                self.window.remove(maybe_obj4)
                self.score += 10
                self.score_label.text = '☆☆☆'+str(self.score)+'☆☆☆'
                self.brick_num -= 1
                if self.brick_num == 0:
                    self.win_the_game()
            elif maybe_obj4 is self.paddle:
                if self.__dy > 0:
                    self.__dy *= -1

        # 碰到邊界反彈
        elif self.ball.x <= 0:
            if self.__dx < 0:
                self.__dx *= -1
        elif self.ball.x + self.ball.width >= self.window.width:
            if self.__dx > 0:
                self.__dx *= -1
        elif self.ball.y <= 0:
            if self.__dy < 0:
                self.__dy *= -1

        # 碰到底部重新遊戲 並減少一條命
        elif self.ball.y + self.ball.height >= self.window.height:
            self.lives -= 1
            self.label_live.text = '❤' * self.lives
            # 若沒有命，則清空畫面並顯示game over
            if self.lives == 0:
                self.window.clear()
                self.window.add(self.label_1, x=self.window.width/2-self.label_1.width/2,
                                y=self.window.height/2-self.label_1.height/2)
            else:
                self.reset_game()

    # 重設球的速度、位置
    def reset_game(self):
        self.__dx = 0
        self.__dy = 0
        self.ball.x = self.window.width/2-self.ball.width
        self.ball.y = self.window.height/2-self.ball.height

    def get_lives(self):
        return self.lives

    # 消除所有方塊並顯示獲勝
    def win_the_game(self):
        self.window.clear()
        self.window.add(self.label_2, x=self.window.width/2 - self.label_2.width/2,
                        y=self.window.height/2 - self.label_2.height/2)


