import dotenv
from tools.heal  import Heal
import datetime

dotenv.load_dotenv()

def get_bot_metrics(bot: Heal):
    start_time = datetime.datetime.utcnow()
    latency = bot.latency * 1000  
    user_count = len(bot.users)
    server_count = len(bot.guilds)
    uptime = datetime.datetime.utcnow() - start_time
    return latency, user_count, server_count, uptime

if __name__ == "__main__":
    bot = Heal()
    bot.run('MTIzMjc3ODUwODQyNjgwOTM2NQ.GOa0ii.YTQG3x22Mc66Q-6tnOqz2A17Y8Ucx_Ykbqn1y0')
