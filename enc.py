from cryptography.fernet import Fernet

# we open on our key
with open('secret.key', 'rb') as secret: 
	key = secret.read() 
fernet = Fernet(key) 

# we open the sales file and encrypt it
with open('csv1.png', 'rb') as file: 
	org = file.read() 
encrypt = fernet.encrypt(org) 

#and now we save it as encrypted
with open('csv1.png', 'wb') as encryptFile: 
	encryptFile.write(encrypt) 

