from gym.envs.registration import register

register(
    id='pikachu-volleyball-v0',
    entry_point='gym_pikachu_volleyball.envs:PikachuVolleyballEnv',
)

