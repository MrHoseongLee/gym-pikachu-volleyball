import gym
import pyglet
from time import time, sleep
from pyglet.window import key as keycodes

env = gym.make('gym_pikachu_volleyball:pikachu-volleyball-v0', isPlayer1Computer=True, isPlayer2Computer=False)
env.reset()
env.render()
key_handler = pyglet.window.key.KeyStateHandler()
env.viewer.window.push_handlers(key_handler)

enter_down = False

sleep(1)

def getInput():
    global enter_down

    action = [ 0 ] * 3

    keys_pressed = set()

    for key_code, pressed in key_handler.items():

        if pressed:
            keys_pressed.add(key_code)

    keys = set()

    for keycode in keys_pressed:
        for name in dir(keycodes):
            if getattr(keycodes, name) == keycode:
                keys.add(name)

    if 'LEFT' in keys:
        action[0] = -1
    elif 'RIGHT' in keys:
        action[0] = 1

    if 'UP' in keys:
        action[1] = -1
    elif 'DOWN' in keys:
        action[1] = 1

    if 'ENTER' in keys:
        if not enter_down:
            action[2] = 1

        enter_down = True
    else:
        enter_down = False

    return (action[0] + 1) * 6 + (action[1] + 1) + action[2] * 3

for _ in range(10000):
    curTime = time()
    env.render()

    observation, reward, done, _ = env.step((0, getInput()))

    if done:
        break

    sleepTime = 1 / 30 - (time() - curTime)
    if sleepTime > 0:
        sleep(sleepTime)

