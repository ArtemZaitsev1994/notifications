from user_info.models import UserInfo


async def send_sms(phone_number: str, text: str):
    print(f'Sent sms with text: "{text}". to {phone_number}')


async def send_email(email: str, text: str):
    print(f'Sent email with text: "{text}". to {email}')


async def send_push(*args, **kwargs):
    ...


async def send_all_ways_notification(user: UserInfo, notification: str):
    if user.available_sms_notification and user.cellphone and user.country_code:
        phone_number = user.country_code + user.phone
        await send_sms(phone_number, notification)

    if user.available_email_notification and user.email:
        await send_email(user.email, notification)

    await send_push()
