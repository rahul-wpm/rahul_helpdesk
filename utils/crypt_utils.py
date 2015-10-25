__author__ = 'Rahul.R'
import base64
from Crypto.Cipher import AES

class MyCryptUtils(object):
    """"
    """
    def __init__(self):
        """
        :return:
        """
        self.padding_symbol = "X"
        # self.secret_key = 'my random secret'
        self.secret_key = 'Temiles is cool!'
        self.cipher = AES.new(self.secret_key, AES.MODE_ECB)

    def encrypt_data(self, password):
        """
        :param password:
        :return:
        """
        aes_size = 32
        aes_encode_construct = lambda password: password + (aes_size - len(
            password) % aes_size) * self.padding_symbol

        aes_encode = lambda c, password: base64.b64encode(c.encrypt(
            aes_encode_construct(password)))
        encrypted_value = aes_encode(self.cipher, password)

        return encrypted_value

    def decrypt_data(self, password):
        """
        @summary:
        @param password:
        @return:
        """
        # import pdb;pdb.set_trace()
        aes_decode_func = lambda cipher, password: cipher.decrypt(
            base64.b64decode(password)).rstrip(self.padding_symbol)
        decrypted_value = aes_decode_func(self.cipher, password)
        return decrypted_value
if __name__ == '__main__':
    """
    """
    crypt_obj=MyCryptUtils()
    encrypted_value = crypt_obj.encrypt_data('Password')
    decrypted_value = crypt_obj.decrypt_data(encrypted_value)
    print(decrypted_value , encrypted_value)

