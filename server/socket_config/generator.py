import string
import random

class Generator:
    @staticmethod
    def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        generated_string = ''.join(random.choice(characters) for _ in range(length))
        # Ensure the generated string is a valid group name
        valid_group_name = "".join(char for char in generated_string if char.isalnum() or char in ['-', '_', '.'])
        return valid_group_name

    @staticmethod
    def generate_valid_group_name(prefix='group', length=10):
        random_string = Generator.generate_random_string(length - len(prefix))
        return f"{prefix}_{random_string}"
