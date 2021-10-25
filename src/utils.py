import os

async def save_image_from_message_get_name(message):
    for attachment in message.attachments:
        image_types = ["png", "jpeg", "gif", "jpg"]
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            print('Got attachments')
            _, ext = os.path.splitext(attachment.filename)
            final_fname = 'temp/temp'+ext
            await attachment.save(final_fname)
            return final_fname