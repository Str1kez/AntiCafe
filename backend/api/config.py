from environs import Env

env = Env()
env.read_env()

TARIFF_START = env.decimal('TARIFF_START')
TARIFF_PER_MINUTE = env.decimal('TARIFF_PER_MINUTE')
