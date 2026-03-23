#compare speed of md5 with that of bcrypt

#md5

import hashlib 
hashlib.md5(b'myS3cr3tP@ssw0rd!').hexdigest() 

for i in range(1000000): 
    x = hashlib.md5(b'myS3cr3tP@ssw0rd!').hexdigest()
    print (x)
    
    
#bcrypt
from passlib.hash import bcrypt 
bcrypt.hash('myS3cr3tP@ssw0rd!') 

for i in range(100): 
    x = bcrypt.hash('myS3cr3tP@ssw0rd!') 
    print(x)