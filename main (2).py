import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# 🔐 API DETAILS
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
SESSION_STRING = os.getenv("STRING_SESSION")  # Railway variables me STRING_SESSION add karein

# 🔒 CHANNEL IDS
SOURCE_1 = -1003744550266
TARGET_1 = -1003041329400

SOURCE_2 = -1003748343664
TARGET_2 = -1003784582566

# 🆕 COMMON TARGET
TARGET_3 = -1003154697036   # 👈 NEW TARGET ID

# 🏷 NAMES
BASENAME = "GOOD HOTMAIL"
FIXED_NAME = "VAULT CLOUD MIX"

# 🆕 TARGET 3 NAMES
SOURCE1_TARGET3_NAME = "TRIDENT CLOUD HOTMAIL"
SOURCE2_TARGET3_NAME = "TRIDENT CLOUD MIX"

# 📁 COUNTER FILE
COUNTER_FILE = "counter.txt"

# 🔐 LOCK
file_lock = asyncio.Lock()

# 🔢 Load counter
def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    return 0

# 💾 Save counter
def save_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))

async def main():
    # StringSession ka use karke client initialize kiya gaya hai
    client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)

    await client.start()

    counter = load_counter()

    print(f"🚀 Bot started with StringSession, counter = {counter}")

    # =========================
    # SOURCE 1
    # =========================
    @client.on(events.NewMessage(chats=SOURCE_1))
    async def handler1(event):

        nonlocal counter

        if not event.file:
            return

        async with file_lock:

            try:

                file_path = await event.download_media()

                _, ext = os.path.splitext(file_path)

                # TARGET 1
                counter += 1
                save_counter(counter)

                final_name = f"{BASENAME} {counter}{ext}"

                final_path = os.path.join(
                    os.path.dirname(file_path),
                    final_name
                )

                os.rename(file_path, final_path)

                await client.send_file(TARGET_1, final_path)

                # TARGET 3
                target3_name = f"{SOURCE1_TARGET3_NAME}{ext}"

                target3_path = os.path.join(
                    os.path.dirname(final_path),
                    target3_name
                )

                os.rename(final_path, target3_path)

                await client.send_file(TARGET_3, target3_path)

                os.remove(target3_path)

                print(f"✅ Source1: {final_name}")

            except Exception as e:
                print("❌ Source1 Error:", e)

    # =========================
    # SOURCE 2
    # =========================
    @client.on(events.NewMessage(chats=SOURCE_2))
    async def handler2(event):

        async with file_lock:

            try:

                file_path = await event.download_media()

                _, ext = os.path.splitext(file_path)

                # TARGET 2
                final_name = f"{FIXED_NAME}{ext}"

                final_path = os.path.join(
                    os.path.dirname(file_path),
                    final_name
                )

                os.rename(file_path, final_path)

                await client.send_file(TARGET_2, final_path)

                # TARGET 3
                target3_name = f"{SOURCE2_TARGET3_NAME}{ext}"

                target3_path = os.path.join(
                    os.path.dirname(final_path),
                    target3_name
                )

                os.rename(final_path, target3_path)

                await client.send_file(TARGET_3, target3_path)

                os.remove(target3_path)

                print(f"✅ Source2: {final_name}")

            except Exception as e:
                print("❌ Source2 Error:", e)

    await client.run_until_disconnected()

asyncio.run(main())
