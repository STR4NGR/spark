import random
import string
import os
from dotenv import load_dotenv

from vkbottle.bot import Bot, Message
from vkbottle import GroupTypes, GroupEventType

load_dotenv()

bot = Bot(token=os.getenv("VK_TOKEN"))
GROUP_ID = int(os.getenv("GROUP_ID"))

CODE_LENGTH = 6
used_codes = set()

def generate_code():
    while True:
        code = "A" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=CODE_LENGTH-1))
        if code not in used_codes:
            used_codes.add(code)
            return code

@bot.on.raw_event(GroupEventType.MESSAGE_NEW, dataclass=GroupTypes.MessageNew)
async def handle_message(event: GroupTypes.MessageNew):
    message = event.object.message
    user_id = message.from_id
    text = message.text.strip().lower()

    if text != "хочу скидку":
        return

    try:
        member_status = await bot.api.groups.is_member(group_id=GROUP_ID, user_id=user_id)
    except Exception as e:
        await bot.api.messages.send(peer_id=user_id, message="Ошибка сервера, попробуй позже", random_id=0)
        return

    if member_status:
        code = generate_code()
        await bot.api.messages.send(
            peer_id=user_id,
            message=f"Ваш личный промокод на скидку:\n\n{code}\n\nДействует только один раз!",
            random_id=0
        )
    else:
        await bot.api.messages.send(
            peer_id=user_id,
            message="Чтобы получить промокод, сначала подпишись на группу и включи все уведомления!\n\nПосле этого напиши снова «хочу скидку»",
            random_id=0
        )

if __name__ == "__main__":
    bot.run_forever()