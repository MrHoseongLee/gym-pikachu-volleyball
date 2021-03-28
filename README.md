# Pikachu Volleyball

Pikachu Volleyball (対戦ぴかちゅ～　ﾋﾞｰﾁﾊﾞﾚｰ編) is an old Windows game which was developed by
"(C) SACHI SOFT / SAWAYAKAN Programmers" and "(C) Satoshi Takenouchi" in 1997.

This is an OpenAI gym environment of the game created by translating
a [reversed-engineered JavaScript version](https://github.com/gorisanson/pikachu-volleyball)
by [gorisanson](https://github.com/gorisanson) to python.

## Installation
```bash
pip install gym-pikachu-volleyball
```

## Environment

### Observation
Currently the only way for an agent to observe the environment is by the position and velocity
of the ball, player1, player2 represented in a tuple of size 12.

### Action
Actions are defined by 3 numbers (xDirection, yDirection, powerHit)
- xDirection : Whether the player moves left or right or not. possible values: -1, 0, 1
- yDirection : Whether the player moves up or down or not. possible values: -1, 0, 1
- powerHit : Whether the player is power hitting. possible values 0, 1 (0 being False and 1 being True)

### Rewards
1 if player2 (right player) wins and -1 if player2 loses. Reward is 0 while the game is running.

### Done
The episode ends when the ball hits the ground.

## Interactive
By running 

```bash
python3 -m gym_pikachu_volleyball.scripts.interactive
```

You can play against the default AI. The game will end when a point is scored.

To record your game play, add `--record` to the above command and you will get a file with
all the actions you did and the seed for the game. 
