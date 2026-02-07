import cv2 as cv
import subprocess
import time
from discord_webhook import DiscordWebhook

WEBHOOK = ""

prev_path = "prev.jpg"
curr_path = "curr.jpg"

def send_discord_message():
    webhook = DiscordWebhook(url=WEBHOOK, content = "Motion Detected")
    with open(curr_path, 'rb') as f:
        webhook.add_file(file=f.read(), filename='example.jpg')
    response = webhook.execute()

def compare_two_images():
    prev = cv.imread(prev_path, cv.IMREAD_GRAYSCALE)
    curr = cv.imread(curr_path, cv.IMREAD_GRAYSCALE)
    
    difference = cv.absdiff(prev, curr)    
    value = difference.mean() / 255

    if value > 0.05:
        send_discord_message()

def take_picture(path):
    subprocess.run(f"termux-camera-photo {path}", shell=True)

def rename_photo():
    subprocess.run(f"mv {curr_path} {prev_path}", shell=True)

def main():
    take_picture(prev_path)
    time.sleep(1)

    while True: 
        take_picture(curr_path)
        compare_two_images()
        rename_photo()
        time.sleep(1)

if __name__ == "__main__":
    main()
