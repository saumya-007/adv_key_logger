# Instructions
This is a key logger developed using python which can log keystrokes, extracting system information, recording audio (every 2 mins), taking screenshots (every 2 mins), encrypt the logfiles and send the encrypted files and screenshot via email. Additionally developed a python program to decrypt the encrypted files gathered via mail.

# NOTE: This can be detected by windows defender and other anti virus softwares.
# Following changes must be done prior to trying it out.

In keylogger.py :
- Line 30: File path must be changed
- Line 34: Email address from which you want the logs and screenshots to be sent.
- Line 35: Password of that email account.
- Line 36: Email of the user to whom the logs and screenshots are sent (can be the same as line 34).
- Line 57: Change the value of KEY. You must first run the program Cryptography/encryption_key.py which will create a new text file with a key which can be used for encryption.

In DecryptFile.py
- Line 3: Change the value of KEY. with the key generated.

# Instructions

Run the keylogger.py file after making the above changes.
Go to your email and see that you have received the mails of screenshots and log files (in encrypted format).
Encrypted files will also be sored in the folder in which the program runs.
Take the encrypted files and keepm them in the same folder in which DecryptFile.py and run DecryptFile.py to decyphe the encrypted files.



 
