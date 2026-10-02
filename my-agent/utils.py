def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def get_user_name(user):
    return user["name"].upper()


if __name__ == "__main__":
    print(calculate_average([6, 7]))
    print(get_user_name({"name": "peter"}))


""" 
python -c "from utils import calculate_average; print(calculate_average([6, 7]))"
python -c "from utils import get_user_name; print(get_user_name({'name': 'peter'}))"

----------------------

python

>>> from utils import calculate_average, get_user_name
>>> calculate_average([6, 7])
6.5
>>> get_user_name({"name": "peter"})
'PETER'
>>> exit()

~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    print(calculate_average([6, 7]))
    print(get_user_name({"name": "peter"}))

"""