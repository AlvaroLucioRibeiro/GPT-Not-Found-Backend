import random
import string


# Helper function to generate a random email
def generate_random_email():
    """
    Generates a random email for testing purposes.

    Returns:
        str: A randomly generated email address.
    """
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@gmail.com"


def calculate_digit(numbers):
    weight = len(numbers) + 1
    total = sum(int(num) * weight for num, weight in zip(numbers, range(weight, 1, -1)))
    remainder = total % 11
    return "0" if remainder < 2 else str(11 - remainder)


def generate_cpf():
    numbers = [str(random.randint(0, 9)) for _ in range(9)]
    numbers.append(calculate_digit(numbers))
    numbers.append(calculate_digit(numbers))

    return f"{''.join(numbers[:3])}.{''.join(numbers[3:6])}.{''.join(numbers[6:9])}-{''.join(numbers[9:])}"


def generate_cnpj():
    def calculate_digit(numbers, weights):
        total = sum(int(num) * weight for num, weight in zip(numbers, weights))
        remainder = total % 11
        return "0" if remainder < 2 else str(11 - remainder)

    numbers = [str(random.randint(0, 9)) for _ in range(12)]
    weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights_second = [6] + weights_first

    numbers.append(calculate_digit(numbers, weights_first))
    numbers.append(calculate_digit(numbers, weights_second))

    return f"{''.join(numbers[:2])}.{''.join(numbers[2:5])}.{''.join(numbers[5:8])}/{''.join(numbers[8:12])}-{''.join(numbers[12:])}"


def generate_password(length=12, use_symbols=True):
    """
    Generates a random password.

    Parameters:
        length (int): The length of the password to generate.
        use_symbols (bool): If True, includes symbols in the password.

    Returns:
        str: The generated password.
    """
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation

    password = "".join(random.choice(characters) for _ in range(length))
    return password
