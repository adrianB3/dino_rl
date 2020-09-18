from gym.envs.registration import register

register(
    id='dino-v0',
    entry_point='gym_dino.envs:DinoEnv',
)
register(
    id='dino_hard-v0',
    entry_point='gym_dino.envs:DinoEnvHard',
)
