"""Logic for Hello.

Hello World is one of the most complex operations in the world. It requires all
the robots and nanotechnology from Terminator to define whether or not our
future will survive an apocalypse.

In other words: always make sure that whenever you add a description it's
something meaningful that you will enjoy reading days, months, or years later.
One more thing: you will automatically be associated with those, and some of us
really enjoy “git blame”.
"""

from oto import response
from my_project.models import product as product_model


def say_hello():
    return response.Response('Hello Buddy!')


def fetch_all_product():
    product_response = product_model.get_all_product()
    if product_response:
        return product_response


def fetch_product_by_id(product_id):
    """Logic handlers.

    Args:
        name (str): the name to display alongside the Hello.

    Returns:
        Response: the hello message.
    """

    product_response = product_model.get_product_by_id(product_id)
    if product_response:
        return product_response


def add_product(data):
    product_response = product_model.add_product(data)
    if product_response:
        return product_response


def update_product(data):
    product_response = product_model.update_product_by_id(data)
    if product_response:
        return product_response


def delete_product(data):
    product_response = product_model.delete_product_by_id(data)
    if product_response:
        return product_response