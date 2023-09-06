import pyrebase
from setting.conf import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()


async def get_db_user(telegram_id):
    data = db.child(telegram_id).get().val()
    return data if data else None


async def get_db_users():
    data = db.get().val()
    return data if data else None


async def update_db_user(telegram_id, new_data):
    existing_data = await get_db_user(telegram_id)

    if existing_data:
        db.child(telegram_id).update({**existing_data, **new_data})
    else:
        db.child(telegram_id).set({**new_data})


async def remove_db_user(telegram_id):
    db.child(telegram_id).remove()
