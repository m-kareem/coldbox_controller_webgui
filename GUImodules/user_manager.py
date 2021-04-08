from cryptography.fernet import Fernet
import pickle
import os.path

#crypt_key = Fernet.generate_key()
crypt_key = b'KgMq7oocb2iRF4NftAmfI-nV6KMNun0L5bF4iwxe1Ew='
cipher_suite = Fernet(crypt_key)
encoded_pass_file = 'user_DB.bin'
#user_dict={}


class User(object):
    USER_LEVEL_NOT_AUTHENTICATED = 0
    USER_LEVEL_USER = 1
    USER_LEVEL_ADMIN = 2

    def __init__(self, username, pwd, user_level=0):
        self.username = username
        self.pwd = pwd
        self.user_level = user_level




def load_user_dic(encoded_pass_file='user_DB.bin'):
    user_dict={}
    if os.path.isfile(encoded_pass_file):
        try:
            with open(encoded_pass_file, 'rb') as f_handler:
                user_dict = pickle.load(f_handler)
                #print('user_dict is loaded')
                return user_dict
        except:
            print('no user_dict found in database')
            return False
    else:
        print('Database file not found')
        return False




def add_new_user(user, password, user_level, encoded_pass_file='user_DB.bin'):
    user_dict={}
    if load_user_dic():
        user_dict=load_user_dic()
        if user.lower() in user_dict.keys():
            print('user \'' + user + '\' already exists!')
            return None

    with open(encoded_pass_file, 'wb') as f_handler:
        ciphered_text = cipher_suite.encrypt(password.encode())   #required to be bytes
        #user_dict[user.lower()] = (ciphered_text,user_level)
        user_dict[user.lower()] = User(user.lower(), ciphered_text, user_level)
        pickle.dump(user_dict, f_handler, protocol=pickle.HIGHEST_PROTOCOL)
        print('user \'' + user + '\' is added to the database')
        return True


def get_user_pwd(user):
    user_dict={}
    if load_user_dic():
        user_dict=load_user_dic()
        try:
            uncipher_text = (cipher_suite.decrypt(user_dict[user.lower()].pwd))
            plain_text_encryptedpassword = bytes(uncipher_text).decode("utf-8") #convert to string
            #print(user_dict[user.lower()].username, plain_text_encryptedpassword, user_dict[user.lower()].user_level)
            return plain_text_encryptedpassword
        except:
            print('User \'' + user + '\' not found!')
            return None


def set_user_credential(user, newPaw, new_user_level):
    user_dict={}
    if load_user_dic():
        user_dict=load_user_dic()
        if user.lower() in user_dict:
            newciphered_text = cipher_suite.encrypt(newPaw.encode())   #required to be bytes
            user_dict[user.lower()] = User(user.lower(), newciphered_text, new_user_level)
            with open(encoded_pass_file, 'wb') as f_handler:
                pickle.dump(user_dict, f_handler, protocol=pickle.HIGHEST_PROTOCOL)
                print('user \'' + user + '\' credential was modified')
                return True
        else:
            print('User \'' + user + '\' not found!')
            return False


def delete_user(user):
    user_dict={}
    if load_user_dic():
        user_dict=load_user_dic()
        if user.lower() in user_dict:
            del user_dict[user.lower()]
            with open(encoded_pass_file, 'wb') as f_handler:
                pickle.dump(user_dict, f_handler, protocol=pickle.HIGHEST_PROTOCOL)
                print('user \'' + user + '\' was deleted from user_dict')
                return True
        else:
            print('User \'' + user + '\' not found!')
            return False
#------------------------------------------------



if __name__ == '__main__':
    print('--User_manager--')


    #load_user_dic()
    ##
    add_new_user('admin','admin',User.USER_LEVEL_ADMIN)
    #add_new_user('ITk','YorkDAQ',User.USER_LEVEL_USER)
    #add_new_user('guest','myGuestPass',User.USER_LEVEL_NOT_AUTHENTICATED)
    ##
    #get_user_pwd('admin')
    #get_user_pwd('itk')
    #get_user_pwd('guest')
    #get_user_pwd('tim')
    ##
    #delete_user('itk')
    #delete_user('admin')
    ##
    #set_user_credential('admin','my_Pass',2)
    #get_user_pwd('admin')
    ##
