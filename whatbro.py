import bcrypt

def hash_password(plain_text_pass):
    pass_bytes = plain_text_pass.encode('utf-8')
    #for a in pass_bytes:
    #    print(str(a) +" -- "+ chr(a))
    salt= bcrypt.gensalt()
    hashed_pass= bcrypt.hashpw(pass_bytes, salt)
    return hashed_pass

pw= "a"
pw_hash= hash_password(pw)
print(f'Password: {pw} Hash: {str(pw_hash)}')

pw= "apple"
pw_hash= hash_password(pw)
print(f'Password: {pw} Hash: {str(pw_hash)}')