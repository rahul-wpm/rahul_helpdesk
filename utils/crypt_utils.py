__author__ = 'Rahul.R'

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