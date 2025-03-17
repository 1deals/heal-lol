import dotenv
from tools.heal import Heal
import datetime

dotenv.load_dotenv()

if __name__ == "__main__":
    bot = Heal()
    bot.run("Your token here")
