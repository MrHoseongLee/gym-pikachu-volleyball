import os
import pyglet
import pyglet.gl as gl

def get_window(width, height, display: pyglet.canvas.Display, **kwargs):
    screen = display.get_screens()
    config = screen[0].get_best_config()
    context = config.create_context(None)
    
    return pyglet.window.Window(width=width, height=height, display=display, caption='Pikachu Volleyball', config=config, context=context, **kwargs)

def getFrameNumberForPlyaerAnimatedSprite(state, frameNumber):
    if state < 4:
        return 5 * state + frameNumber
    elif state == 4:
        return 17 + frameNumber
    elif state > 4:
        return 18 + 5 * (state - 5) + frameNumber

class Viewer(object):
    def __init__(self, width, height, scale=3):

        self.width = width * scale
        self.height = height * scale

        self.window = get_window(self.width, self.height, pyglet.canvas.get_display())
        gl.glScalef(scale, scale, scale)

        self.ball_images = []
        self.pika_images = []

        PATH = os.path.abspath(os.path.dirname(__file__))

        files = os.listdir(f'{PATH}/../envs/sprites')
        files.sort()

        self.background = pyglet.graphics.Batch()
        self.net = pyglet.graphics.Batch()
        self.balls = pyglet.graphics.Batch()
        self.players = pyglet.graphics.Batch()

        for file in files:
            if file[:4] == 'ball' and len(file) == 10:
                self.ball_images.append(self.load_image(f'{PATH}/../envs/sprites/{file}'))

            if file[:4] == 'pika':
                self.pika_images.append(self.load_image(f'{PATH}/../envs/sprites/{file}'))

        net_pillar_image = self.load_image(f'{PATH}/../envs/sprites/net_pillar.png')
        net_pillar_top_image = self.load_image(f'{PATH}/../envs/sprites/net_pillar_top.png')

        ball_hyper_image = self.load_image(f'{PATH}/../envs/sprites/ball_hyper.png')
        ball_trail_image = self.load_image(f'{PATH}/../envs/sprites/ball_trail.png')

        sky_image = self.load_image(f'{PATH}/../envs/sprites/sky_blue.png')

        ground_red_image = self.load_image(f'{PATH}/../envs/sprites/ground_red.png')

        ground_yellow_image = self.load_image(f'{PATH}/../envs/sprites/ground_yellow.png')

        ground_line_image = self.load_image(f'{PATH}/../envs/sprites/ground_line.png')
        ground_line_leftmost_image = self.load_image(f'{PATH}/../envs/sprites/ground_line_leftmost.png')
        ground_line_rightmost_image = self.load_image(f'{PATH}/../envs/sprites/ground_line_rightmost.png')

        mountain_image = self.load_image(f'{PATH}/../envs/sprites/mountain.png')

        self.ball_hyper = pyglet.sprite.Sprite(ball_hyper_image, batch=self.balls)
        self.ball_trail = pyglet.sprite.Sprite(ball_trail_image, batch=self.balls)

        self.net_pillars = [pyglet.sprite.Sprite(net_pillar_image, batch=self.net) for _ in range(12)]
        self.net_pillar_top = pyglet.sprite.Sprite(net_pillar_top_image, batch=self.net)

        self.skys = [pyglet.sprite.Sprite(sky_image, batch=self.background) for _ in range(324)]
        self.grounds_yellow = [pyglet.sprite.Sprite(ground_yellow_image, batch=self.background) for _ in range(54)]
        self.grounds_red = [pyglet.sprite.Sprite(ground_red_image, batch=self.background) for _ in range(27)]
        self.grounds_line = [pyglet.sprite.Sprite(ground_line_image, batch=self.background) for _ in range(25)]
        self.grounds_line.append(pyglet.sprite.Sprite(ground_line_leftmost_image, batch=self.background))
        self.grounds_line.append(pyglet.sprite.Sprite(ground_line_rightmost_image, batch=self.background))

        self.mountain = pyglet.sprite.Sprite(mountain_image, batch=self.background)

        self.ball = pyglet.sprite.Sprite(self.ball_images[0], batch=self.balls)

        self.player1 = pyglet.sprite.Sprite(self.pika_images[0], batch=self.players)
        self.player2 = pyglet.sprite.Sprite(self.pika_images[0], batch=self.players)
        self.player2.scale_x = -1

        self.net_pillar_top.update(216, 128)

        for i, net_pillar in enumerate(self.net_pillars):
            net_pillar.update(216, 32 + 8 * i)

        for i in range(27):
            for j in range(12):
                self.skys[i * 12 + j].update(16 * i + 8, 304 - 16 * j)

        for i in range(27):
            for j in range(2):
                self.grounds_yellow[i * 2 + j].update(16 * i + 8, 16 * j)

        for i in range(27):
            self.grounds_red[i].update(16 * i + 8, 48)

        for i in range(1, 26):
            self.grounds_line[i - 1].update(16 * i + 8, 32)

        self.grounds_line[25].update(8, 32)
        self.grounds_line[26].update(424, 32)

        self.mountain.update(216, 88)

        self.window.set_vsync(False)

        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def load_image(self, path):
        image = pyglet.image.load(path)
        texture = image.get_texture()
        texture.anchor_x = image.width // 2
        texture.anchor_y = image.height // 2
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture.id)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        return image

    def update(self, player1, player2, ball):
        self.ball.image = self.ball_images[ball.rotation]
        self.player1.image = self.pika_images[getFrameNumberForPlyaerAnimatedSprite(player1.state, player1.frameNumber)]
        self.player2.image = self.pika_images[getFrameNumberForPlyaerAnimatedSprite(player2.state, player2.frameNumber)]

        if player1.state == 3 or player1.state == 4:
            self.player1.scale_x = -1 if player1.divingDirection == -1 else 1
        else:
            self.player1.scale_x = 1

        if player2.state == 3 or player2.state == 4:
            self.player2.scale_x = 1 if player2.divingDirection == 1 else -1
        else:
            self.player2.scale_x = -1

        self.player1.update(player1.x, 304 - player1.y)
        self.player2.update(player2.x, 304 - player2.y)

        self.ball.update(ball.x, 304 - ball.y)

        if ball.isPowerHit:
            self.ball_hyper.update(ball.previousX, 304 - ball.previousY)
            self.ball_trail.update(ball.previousPreviousX, 304 - ball.previousPreviousY)

            self.ball_hyper.opacity = 255
            self.ball_trail.opacity = 255
        else:
            self.ball_hyper.opacity = 0
            self.ball_trail.opacity = 0

    def render(self):
        gl.glClearColor(1, 1, 1, 1)

        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST) 
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        self.background.draw()
        self.net.draw()
        self.balls.draw()
        self.players.draw()

        self.window.flip()

