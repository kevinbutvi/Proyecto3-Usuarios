# FUNCIONES EXTRAS DE LA APP USERS


import random
import string

def code_generator(size = 6, chars = string.ascii_uppercase + string.digits):
    """ Generador de codigo validador al alzar de 6 digitos """
    return(''.join(random.choice(chars) for _ in range(size)))