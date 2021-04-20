import gym
from gym import spaces
import numpy as np
import random as pr
from typing import Tuple

from time import time, sleep

GROUND_WIDTH: int = 432
GROUND_HALF_WIDTH: int = GROUND_WIDTH // 2
PLAYER_LENGTH: int = 64
PLAYER_HALF_LENGTH: int = PLAYER_LENGTH // 2
PLAYER_TOUCHING_GROUND_Y_COORD: int = 244
BALL_RADIUS: int = 20
BALL_TOUCHING_GROUND_Y_COORD: int = 252
NET_PILLAR_HALF_WIDTH: int = 25
NET_PILLAR_TOP_TOP_Y_COORD: int = 176
NET_PILLAR_TOP_BOTTOM_Y_COORD: int = 192
INFINITE_LOOP_LIMIT: int = 1000

action_converter_p1 = ((+1, -1,  0),
                       (+1,  0,  0),
                       (+1, +1,  0),
                       (+1, -1, +1),
                       (+1,  0, +1),
                       (+1, +1, +1),
                       ( 0, -1,  0),
                       ( 0,  0,  0),
                       ( 0, +1,  0),
                       ( 0, -1, +1),
                       ( 0,  0, +1),
                       ( 0, +1, +1),
                       (-1, -1,  0),
                       (-1,  0,  0),
                       (-1, +1,  0),
                       (-1, -1, +1),
                       (-1,  0, +1),
                       (-1, +1, +1))

action_converter_p2 = ((-1, -1,  0),
                       (-1,  0,  0),
                       (-1, +1,  0),
                       (-1, -1, +1),
                       (-1,  0, +1),
                       (-1, +1, +1),
                       ( 0, -1,  0),
                       ( 0,  0,  0),
                       ( 0, +1,  0),
                       ( 0, -1, +1),
                       ( 0,  0, +1),
                       ( 0, +1, +1),
                       (+1, -1,  0),
                       (+1,  0,  0),
                       (+1, +1,  0),
                       (+1, -1, +1),
                       (+1,  0, +1),
                       (+1, +1, +1))

class PikachuVolleyballEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, isPlayer1Computer: bool, isPlayer2Computer: bool):
        self.action_space = spaces.MultiDiscrete([18, 18])

        self.player1 = Player(False, isPlayer1Computer)
        self.player2 = Player(True, isPlayer2Computer)
        self.ball = Ball(False)

        self.viewer = None

    def step(self, action=Tuple[int, int]):
        action = (UserInput(*action_converter_p1[action[0]]), UserInput(*action_converter_p2[action[1]]))
        isBallTouchingGround = physicsEngine(self.player1, self.player2, self.ball, action)

        observation_p1 = ((self.ball.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.ball.y / 304,
                          (self.ball.xVelocity) / 20, self.ball.yVelocity / 36, 
                          (self.player1.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player1.y / 304,
                          (self.player1.xVelocity) / 6, self.player1.yVelocity / 16,
                          (self.player2.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player2.y / 304,
                          (self.player2.xVelocity) / 6, self.player2.yVelocity / 16)

        observation_p2 = (-(self.ball.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.ball.y / 304,
                          -(self.ball.xVelocity) / 20, self.ball.yVelocity / 36, 
                          -(self.player2.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player2.y / 304,
                          -(self.player2.xVelocity) / 6, self.player2.yVelocity / 16,
                          -(self.player1.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player1.y / 304,
                          -(self.player1.xVelocity) / 6, self.player1.yVelocity / 16)
        
        observation = (observation_p1, observation_p2)
        
        if isBallTouchingGround:
            if self.ball.punchEffectX < GROUND_HALF_WIDTH:
                return observation, 1, True, {}
            else: 
                return observation, -1, True, {}

        return observation, 0, False, {}
    
    def render(self):
        if self.viewer is None:
            from gym_pikachu_volleyball.envs.viewer import Viewer
            self.viewer = Viewer(GROUND_WIDTH, 304, scale=4)
            self.startTime = time()

        self.viewer.update(self.player1, self.player2, self.ball)

        self.viewer.render()

        diffTime = time() - self.startTime

        if diffTime < 1 / 30:
            sleep(1 / 30 - diffTime)

        self.startTime = time()

    def reset(self, isPlayer2Serve: bool = None):
        self.player1.initializeForNewRound()
        self.player2.initializeForNewRound()

        if isPlayer2Serve is None:
            self.ball.initializeForNewRound(pr.randrange(0, 2) == 0)
        else:
            self.ball.initializeForNewRound(isPlayer2Serve)

        observation_p1 = ((self.ball.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.ball.y / 304,
                          (self.ball.xVelocity) / 20, self.ball.yVelocity / 36, 
                          (self.player1.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player1.y / 304,
                          (self.player1.xVelocity) / 6, self.player1.yVelocity / 16,
                          (self.player2.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player2.y / 304,
                          (self.player2.xVelocity) / 6, self.player2.yVelocity / 16)

        observation_p2 = (-(self.ball.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.ball.y / 304,
                          -(self.ball.xVelocity) / 20, self.ball.yVelocity / 36, 
                          -(self.player2.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player2.y / 304,
                          -(self.player2.xVelocity) / 6, self.player2.yVelocity / 16,
                          -(self.player1.x - GROUND_HALF_WIDTH) / GROUND_HALF_WIDTH, self.player1.y / 304,
                          -(self.player1.xVelocity) / 6, self.player1.yVelocity / 16)
        
        observation = (observation_p1, observation_p2)

        return observation
        
    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def seed(self, seed):
        pr.seed(seed)
        np.random.seed(seed)

class CopyBall:
    __slots__ = ['x', 'y', 'xVelocity', 'yVelocity']
    def __init__(self, x, y, xVelocity, yVelocity):
        self.x = x
        self.y = y
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

class UserInput:
    __slots__ = ['xDirection', 'yDirection', 'powerHit']
    def __init__(self, xDirection, yDirection, powerHit):
        self.xDirection = xDirection
        self.yDirection = yDirection
        self.powerHit = powerHit

    def __repr__(self):
        return f'{self.xDirection} {self.yDirection} {self.powerHit}'

class Ball:
    def __init__(self, isPlayer2Serve: bool):
        self.initializeForNewRound(isPlayer2Serve)
        self.expectedLandingPointX: int = 0
        self.rotation: int = 0
        self.fineRotation: int = 0
        self.punchEffectX: int = 0
        self.punchEffectY: int = 0

        self.previousX: int = 0
        self.previousPreviousX: int = 0
        self.previousY: int = 0
        self.previousPreviousY: int = 0

    def initializeForNewRound(self, isPlayer2Serve: bool):
        self.x: int = 56 if not isPlayer2Serve else GROUND_WIDTH - 56
        self.y: int = 0 
        self.xVelocity: int = 0
        self.yVelocity: int = 1
        self.punchEffectRadius: int = 0
        self.isPowerHit = False

class Player:
    def __init__(self, isPlayer2: bool, isComputer: bool):
        self.isPlayer2: bool = isPlayer2
        self.isComputer: bool = isComputer
        self.divingDirection: int = 0
        self.lyingDownDurationLeft: int = -1
        self.isWinner: bool = False
        self.gameEnded: bool = False
        self.computerWhereToStandBy: int = 0

    def initializeForNewRound(self):
        self.x: int = 36 if not self.isPlayer2 else GROUND_WIDTH - 36
        self.y: int = PLAYER_TOUCHING_GROUND_Y_COORD
        self.xVelocity: int = 0
        self.yVelocity: int = 0
        self.isCollisionWithBallHappened: bool = False

        self.previousX = self.x

        self.state: int = 0
        self.frameNumber: int = 0
        self.normalStatusArmSwingDirection: int = 1
        self.delayBeforeNextFrame: int = 0

        self.computerBoldness: int = pr.randrange(0, 5)

def physicsEngine(player1: Player, player2: Player, ball: Ball, userInputArray: Tuple[UserInput, UserInput]) -> bool:
    isBallTouchGround: bool = processCollisionBetweenBallAndWorldAndSetBallPosition(ball)

    calculate_expected_landing_point_x_for(ball)
    processPlayerMovementAndSetPlayerPosition(player1, userInputArray[0], player2, ball)

    calculate_expected_landing_point_x_for(ball)
    processPlayerMovementAndSetPlayerPosition(player2, userInputArray[1], player1, ball)

    for userInput, player in zip(userInputArray, (player1, player2)):
        is_happend: bool = isCollisionBetweenBallAndPlayerHappened(ball, player.x, player.y)
        if is_happend:
            if not player.isCollisionWithBallHappened:
                processCollisionBetweenBallAndPlayer(ball, player.x, userInput, player.state)
                player.isCollisionWithBallHappened = True
        else:
            player.isCollisionWithBallHappened = False

    return isBallTouchGround

def isCollisionBetweenBallAndPlayerHappened(ball: Ball, playerX: int, playerY: int) -> bool:
    return abs(ball.x - playerX) < PLAYER_HALF_LENGTH and\
           abs(ball.y - playerY) < PLAYER_HALF_LENGTH

def processCollisionBetweenBallAndWorldAndSetBallPosition(ball: Ball) -> bool:
    ball.previousPreviousX = ball.previousX
    ball.previousPreviousY = ball.previousY
    ball.previousX = ball.x
    ball.previousY = ball.y

    ball.fineRotation = (ball.fineRotation + ball.xVelocity // 2) % 50
    ball.rotation = ball.fineRotation // 10

    futureBallX: int = ball.x + ball.xVelocity
    futureBallY: int = ball.y + ball.yVelocity

    if futureBallX < BALL_RADIUS or futureBallX > GROUND_WIDTH:
        ball.xVelocity = -ball.xVelocity

    if futureBallY < 0:
        ball.yVelocity = 1

    if abs(ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and ball.y > NET_PILLAR_TOP_TOP_Y_COORD:
        if ball.y <= NET_PILLAR_TOP_BOTTOM_Y_COORD:
            if ball.yVelocity > 0:
                ball.yVelocity = -ball.yVelocity
        else:
            if ball.x < GROUND_HALF_WIDTH:
                ball.xVelocity = -abs(ball.xVelocity)
            else:
                ball.xVelocity = abs(ball.xVelocity)

    futureBallY: int = ball.y + ball.yVelocity

    if futureBallY > BALL_TOUCHING_GROUND_Y_COORD:
        ball.yVelocity = -ball.yVelocity
        ball.punchEffectX = ball.x
        ball.y = BALL_TOUCHING_GROUND_Y_COORD
        ball.punchEffectRadius = BALL_RADIUS
        ball.punchEffectY = BALL_TOUCHING_GROUND_Y_COORD + BALL_RADIUS
        return True
    
    ball.y = futureBallY
    ball.x = ball.x + ball.xVelocity
    ball.yVelocity += 1

    return False

def processPlayerMovementAndSetPlayerPosition(player: Player, userInput: UserInput, theOtherPlayer: Player, ball: Ball):
    player.previousX = player.x

    if player.isComputer:
        letComputerDecideUserInput(player, ball, theOtherPlayer, userInput)

    if player.state == 4:
        player.lyingDownDurationLeft -= 1
        if player.lyingDownDurationLeft < -1:
            player.state = 0
        return

    playerVelocityX: int = 0
    if player.state < 5:
        if player.state < 3:
            playerVelocityX = userInput.xDirection * 6
        else:
            playerVelocityX = player.divingDirection * 8
    
    futurePlayerX: int = player.x + playerVelocityX
    player.x = futurePlayerX

    if not player.isPlayer2:
        if futurePlayerX < PLAYER_HALF_LENGTH:
            player.x = PLAYER_HALF_LENGTH
        elif futurePlayerX > GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH:
            player.x = GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH
    else:
        if futurePlayerX < GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH:
            player.x = GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH
        elif futurePlayerX > GROUND_WIDTH - PLAYER_HALF_LENGTH:
            player.x = GROUND_WIDTH - PLAYER_HALF_LENGTH

    if player.state < 3 and userInput.yDirection == -1 and player.y == PLAYER_TOUCHING_GROUND_Y_COORD:
        player.yVelocity = -16
        player.state = 1
        player.frameNumber = 0

    futurePlayerY: int = player.y + player.yVelocity
    player.y = futurePlayerY

    if futurePlayerY < PLAYER_TOUCHING_GROUND_Y_COORD:
        player.yVelocity += 1
    elif futurePlayerY > PLAYER_TOUCHING_GROUND_Y_COORD:
        player.yVelocity = 0
        player.y = PLAYER_TOUCHING_GROUND_Y_COORD
        player.frameNumber = 0

        if player.state == 3:
            player.state = 4
            player.frameNumber = 0
            player.lyingDownDurationLeft = 3
        else:
            player.state = 0

    if userInput.powerHit == 1:
        if player.state == 1:
            player.delayBeforeNextFrame = 5
            player.frameNumber = 0
            player.state = 2
        elif player.state == 0 and userInput.xDirection != 0:
            player.state = 3
            player.frameNumber = 0
            player.divingDirection = userInput.xDirection
            player.yVelocity = -5

    if player.state == 1:
        player.frameNumber = (player.frameNumber + 1) % 3
    elif player.state == 2:
        if player.delayBeforeNextFrame < 1:
            player.frameNumber += 1
            if player.frameNumber > 4:
                player.frameNumber = 0
                player.state = 1
        else:
            player.delayBeforeNextFrame -= 1
    elif player.state == 0:
        player.delayBeforeNextFrame += 1
        if player.delayBeforeNextFrame > 3:
            player.delayBeforeNextFrame = 0
            futureFrameNumber: int = player.frameNumber + player.normalStatusArmSwingDirection
            if futureFrameNumber < 0 or futureFrameNumber > 4:
                player.normalStatusArmSwingDirection = -player.normalStatusArmSwingDirection
            player.frameNumber = player.frameNumber + player.normalStatusArmSwingDirection
    
    if player.gameEnded:
        if player.state == 0:
            if player.isWinner:
                player.state = 5
            else:
                player.state = 6
            player.delayBeforeNextFrame = 0
            player.frameNumber = 0
        processGameEndFrameFor(player)

    player.xVelocity = player.x - player.previousX

def processGameEndFrameFor(player: Player):
    if player.gameEnded and player.frameNumber < 4:
        player.delayBeforeNextFrame += 1
        if player.delayBeforeNextFrame > 4:
            player.delayBeforeNextFrame = 0
            player.frameNumber += 1

def processCollisionBetweenBallAndPlayer(ball: Ball, playerX: int, userInput, playerState: int):
    if ball.x < playerX:
        ball.xVelocity = -(abs(ball.x - playerX) // 3)
    elif ball.x > playerX:
        ball.xVelocity = abs(ball.x - playerX) // 3

    if ball.xVelocity == 0:
        ball.xVelocity = pr.randrange(0, 3) - 1

    ballAbsYVelocity: int = abs(ball.yVelocity)
    ball.yVelocity = -ballAbsYVelocity

    if ballAbsYVelocity < 15:
        ball.yVelocity = -15

    if playerState == 2:
        if ball.x < GROUND_HALF_WIDTH:
            ball.xVelocity = (abs(userInput.xDirection) + 1) * 10
        else:
            ball.xVelocity = -(abs(userInput.xDirection) + 1) * 10

        ball.punchEffectX = ball.x
        ball.punchEffectY = ball.y
        ball.yVelocity = abs(ball.yVelocity) * userInput.yDirection * 2
        ball.punchEffectRadius = BALL_RADIUS

        ball.isPowerHit = True

    else:
        ball.isPowerHit = False

    calculate_expected_landing_point_x_for(ball)

def calculate_expected_landing_point_x_for(ball: Ball):
    copyBall: CopyBall = CopyBall(ball.x, ball.y, ball.xVelocity, ball.yVelocity)
    loopCounter: int = 0
    while True:
        loopCounter += 1

        futureCopyBallX: int = copyBall.xVelocity + copyBall.x
        if futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH:
            copyBall.xVelocity = -copyBall.xVelocity
        if copyBall.y + copyBall.yVelocity < 0:
            copyBall.yVelocity = 1

        if abs(copyBall.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and copyBall.y > NET_PILLAR_TOP_TOP_Y_COORD:
            if copyBall.y < NET_PILLAR_TOP_BOTTOM_Y_COORD:
                if copyBall.yVelocity > 0:
                    copyBall.yVelocity = -copyBall.yVelocity
            else:
                if copyBall.x < GROUND_HALF_WIDTH:
                    copyBall.xVelocity = -abs(copyBall.xVelocity)
                else:
                    copyBall.xVelocity = abs(copyBall.xVelocity)
        
        copyBall.y = copyBall.y + copyBall.yVelocity

        if copyBall.y > BALL_TOUCHING_GROUND_Y_COORD or loopCounter >= INFINITE_LOOP_LIMIT:
            break

        copyBall.x = copyBall.x + copyBall.xVelocity
        copyBall.yVelocity += 1

    ball.expectedLandingPointX = copyBall.x

def letComputerDecideUserInput(player: Player, ball: Ball, theOtherPlayer: Player, userInput: UserInput):
    userInput.xDirection = 0
    userInput.yDirection = 0
    userInput.powerHit = 0

    virtualExpectedLandingPointX: int = ball.expectedLandingPointX

    if abs(ball.x - player.x) > 100 and abs(ball.xVelocity) < player.computerBoldness + 5:
        leftBoundary: int = int(player.isPlayer2) * GROUND_HALF_WIDTH
        if (ball.expectedLandingPointX <= leftBoundary or\
           ball.expectedLandingPointX >= int(player.isPlayer2) * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
           player.computerWhereToStandBy == 0:
               virtualExpectedLandingPointX = leftBoundary + GROUND_HALF_WIDTH // 2

    if abs(virtualExpectedLandingPointX - player.x) > player.computerBoldness + 8:
        userInput.xDirection = 1 if player.x < virtualExpectedLandingPointX else -1

    elif pr.randrange(0, 20) == 0:
        player.computerWhereToStandBy = pr.randrange(0, 2)

    if player.state == 0:
        if abs(ball.xVelocity) < player.computerBoldness + 3 and\
           abs(ball.x - player.x) < PLAYER_HALF_LENGTH and\
           ball.y > -36 and ball.y < 10 * player.computerBoldness + 84 and ball.yVelocity > 0:
               userInput.yDirection = -1
        
        leftBoundary: int = int(player.isPlayer2) * GROUND_HALF_WIDTH
        rightBoundary: int = (int(player.isPlayer2) + 1) * GROUND_HALF_WIDTH

        if ball.expectedLandingPointX > leftBoundary and ball.expectedLandingPointX < rightBoundary and\
           abs(ball.x - player.x) > player.computerBoldness * 5 + PLAYER_LENGTH and\
           ball.x > leftBoundary and ball.x < rightBoundary and ball.y > 174:
               userInput.powerHit = 1
               userInput.xDirection = 1 if player.x < ball.x else -1

    elif player.state == 1 or player.state == 2:
        if abs(ball.x - player.x) > 8:
            userInput.xDirection = 1 if player.x < ball.x else -1

        if abs(ball.x - player.x) < 48 and abs(ball.y - player.y) < 48:
            willInputPowerHit: bool = decideWheterInputPowerHit(player, ball, theOtherPlayer, userInput)
            
            if willInputPowerHit:
                userInput.powerHit = 1
                if abs(theOtherPlayer.x - player.x) < 80 and userInput.yDirection != -1:
                    userInput.yDirection = -1
        
def decideWheterInputPowerHit(player: Player, ball: Ball, theOtherPlayer: Player, userInput: UserInput) -> bool:
    if pr.randrange(0, 2) == 0:
        for xDirection in range(1, -1, -1):
            for yDirection in range(-1, 2):
                expectedLandingPointX = expectedLandingPointXWhenPowerHit(xDirection, yDirection, ball)
                if (expectedLandingPointX <= int(player.isPlayer2) * GROUND_HALF_WIDTH or\
                    expectedLandingPointX >= int(player.isPlayer2) * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expectedLandingPointX - theOtherPlayer.x) > PLAYER_LENGTH:
                        userInput.xDirection = xDirection
                        userInput.yDirection = yDirection
                        return True
    else:
        for xDirection in range(1, -1, -1):
            for yDirection in range(1, -2, -1):
                expectedLandingPointX = expectedLandingPointXWhenPowerHit(xDirection, yDirection, ball)
                if (expectedLandingPointX <= int(player.isPlayer2) * GROUND_HALF_WIDTH or\
                    expectedLandingPointX >= int(player.isPlayer2) * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expectedLandingPointX - theOtherPlayer.x) > PLAYER_LENGTH:
                        userInput.xDirection = xDirection
                        userInput.yDirection = yDirection
                        return True
    return False

def expectedLandingPointXWhenPowerHit(userInputXDirection: int, userInputYDirection: int, ball: Ball) -> int:
    copyBall: CopyBall = CopyBall(ball.x, ball.y, ball.xVelocity, ball.yVelocity)
    if copyBall.x < GROUND_HALF_WIDTH:
        copyBall.xVelocity = (abs(userInputXDirection) + 1) * 10
    else:
        copyBall.xVelocity = -(abs(userInputXDirection) + 1) * 10

    copyBall.yVelocity = abs(copyBall.yVelocity) * userInputYDirection * 2
    loopCounter: int = 0
    while True:
        loopCounter += 1

        futureCopyBallX = copyBall.x + copyBall.xVelocity
        if futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH:
            copyBall.xVelocity = -copyBall.xVelocity

        if copyBall.y + copyBall.yVelocity < 0:
            copyBall.yVelocity = 1

        if abs(copyBall.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and copyBall.y > NET_PILLAR_TOP_TOP_Y_COORD:
            if copyBall.y <= NET_PILLAR_TOP_BOTTOM_Y_COORD:
                if copyBall.yVelocity > 0:
                    copyBall.yVelocity = -copyBall.yVelocity
            else:
                if copyBall.x < GROUND_HALF_WIDTH:
                    copyBall.xVelocity = -abs(copyBall.xVelocity)
                else:
                    copyBall.xVelocity = abs(copyBall.xVelocity)

        copyBall.y = copyBall.y + copyBall.yVelocity

        if copyBall.y > BALL_TOUCHING_GROUND_Y_COORD or loopCounter >= INFINITE_LOOP_LIMIT:
            return copyBall.x

        copyBall.x = copyBall.x + copyBall.xVelocity
        copyBall.yVelocity += 1

