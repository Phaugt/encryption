from cryptography.fernet import Fernet

# we open on our key
with open('secret.key', 'rb') as secret: 
	key = secret.read() 
fernet = Fernet(key) 
  
# we open the sales file and decrypt it
with open('csv1.png', 'rb') as encryptFile: 
    encrypted = encryptFile.read() 
decrypt = fernet.decrypt(encrypted) 
  
#and now we save it as decrypted
with open('csv1.png', 'wb') as decryptFile: 
    decryptFile.write(decrypt) 