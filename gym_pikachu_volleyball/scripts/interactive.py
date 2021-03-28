import gym
import pyglet
import argparse
import random as pr
from pyglet.window import key as keycodes

env = gym.make('gym_pikachu_volleyball:pikachu-volleyball-v0', isPlayer1Computer=True, isPlayer2Computer=False)
seed = pr.randint(0, int(1e8))
env.seed(seed)
env.reset()
env.render()
key_handler = pyglet.window.key.KeyStateHandler()
env.viewer.window.push_handlers(key_handler)

enter_down = False

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

def store_actions(actions):
    with open('actions.txt', 'a') as f:
        f.write(f'{seed},')
        for action in actions:
            f.write(f'{chr(65 + action)}')
        f.write('\n')

parser = argparse.ArgumentParser()
parser.add_argument('--record', action='store_true')
args = parser.parse_args()

actions = []

while True:
    env.render()

    action = getInput()
    observation, reward, done, _ = env.step((0, action))
    actions.append(action)

    if done:
        if args.record and reward == 1: store_actions(actions)
        seed = pr.randint(0, int(1e8))
        env.seed(seed)
        env.reset()
        actions = []

