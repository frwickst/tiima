import environs

env = environs.Env()
env.read_env()

TIIMA_USERNAME = env.str("TIIMA_USERNAME", "")
TIIMA_PASSWORD = env.str("TIIMA_PASSWORD", "")
TIIMA_COMPANY_ID = env.str("TIIMA_COMPANY_ID", "")
TIIMA_API_KEY = env.str("TIIMA_API_KEY", "")
