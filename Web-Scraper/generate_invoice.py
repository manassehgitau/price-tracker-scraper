import random
import string

def generate_invoice_number(length=6):
    characters = string.ascii_uppercase + string.digits
    invoice_id = ''.join(random.choice(characters) for _ in range(length))

    return invoice_id 