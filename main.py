import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
from tqdm import tqdm

def sendemail(senderemail, senderpassword, recipientemail, subject, messagetext, attachments=None):
    try:
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(senderemail, senderpassword)

        message = MIMEMultipart()
        message['From'] = senderemail
        message['To'] = recipientemail
        message['Subject'] = subject

        body = messagetext
        message.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as file:
                    img = MIMEImage(file.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                    message.attach(img)

        server.send_message(message)
        now = datetime.datetime.now()
        print(f"[{now.strftime('%H:%M:%S')}] Письмо от {senderemail} успешно отправлено на {recipientemail}.")

        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке письма: {str(e)}")

def get_screenshots(folder_path):
    screenshots = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.jpeg') or file_name.endswith('.png') or file_name.endswith('.jpg'):
            screenshots.append(os.path.join(folder_path, file_name))
    return screenshots


logo = """
_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_
    owner by RIMURU & Paranormal Liberation
        все кроме нас.
        а чë сразу мы?

"""


if __name__ == "__main__":
    folder_path = "screen"
    recipients = ["abuse@telegram.org", "Spam@telegram.org"]
    senders = []
    
    with open("mail.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            email, password = line.strip().split(":")
            senders.append((email, password))

    print(logo)
    subject = str(input("[AC] название письма > "))
    messagetext = str(input("[AC] текст письма > "))

    screenshots = get_screenshots(folder_path)
    for senderemail, senderpassword in senders:
        for recipientemail in recipients:
            sendemail(senderemail, senderpassword, recipientemail, subject, messagetext, attachments=screenshots)
            for _ in tqdm(range(100)):
                pass
