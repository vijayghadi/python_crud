"""Product Model."""
# from datetime import date

from oto import response
# from sqlalchemy import BigInteger
from sqlalchemy import Column
# from sqlalchemy import Date
# from sqlalchemy import desc
# from sqlalchemy import update
from sqlalchemy import Integer
from sqlalchemy import String
from env.Lib.sre_constants import error
# from my_project.config import DB_URL
# from my_project import config
from my_project.connectors import mysql
# from my_project.connectors.sentry import sentry_client
# from my_project.constants import error
# import os
# from my_project.connectors.sentry import sentry_client


class Product(mysql.BaseModel):
    """Product Model.

    Represents vw_product view in art_relations.
    """
    __tablename__ = 'release'

    release_id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False)
    release_name = Column(String)

    def to_dict(self):
        """Return a dictionary of a product's properties."""

        return {
            'product_id': self.release_id,
            'product_name': self.release_name
        }


def get_product_by_id(release_id):
    """Get product information by product id.

    Args:
        release_id (int): unique identifier for the product (release_id).
    Returns:
        response.Response: containing dict of product or error.
    """

    with mysql.db_session() as session:
        product = session.query(Product).get(release_id)

        if not product:
            return response.create_not_found_response()

        product = product.to_dict()

    return response.Response(message=product)


def get_all_product():
    """Get the product with the given upc.
    Args:
        upc (int): the UPC value to search for.
    Returns:
        response.Response: containing dict of product or error.
    """

    with mysql.db_session() as session:
        product = session.query(Product).all()

        if not product:
            return response.create_not_found_response()

        response_data = [each.to_dict() for each in product]

    return response.Response(message=response_data)


def add_product(data):
    """Add new artist localized metadata for the given release & language.
    Args:
        language_id (int): id of language.
        data (dict): dict containing artist localized data.
        e.g; [{artist_id : artist_name}]
    Returns:
        response.Response: response object containing status and payload.
    """

    '''if not data or not isinstance(data, dict):
        return response.create_error_response(
            error.ERROR_CODE_INVALID_DATA,
            'Invalid data sent for save release artist localization. data={}'.
            format(data))'''

    with mysql.db_session() as session:
        # for release_name in data.items():
        new_product = Product(release_name=data)
        session.add(new_product)

    return response.Response(message=data)


def update_product_by_id(data):
    """Add new artist localized metadata for the given track & language.
    Args:
        language_id (int): id of language.
        data (dict): dict containing artist localized data.
        e.g; {artist_id : artist_name, artist_id2 : artist_name2, ..}
        session (object): db session object, to make it transactional.
    Returns:
        response.Response: response object containing status and payload.
    """

    if not isinstance(data, dict):
        return response.create_error_response(
            error.ERROR_CODE_INVALID_DATA,
            'Invalid data sent for save track artist localization.')

    if data == {}:
        return response.Response(message=data)

    for k, v in data.items():
        with mysql.db_session() as session:
            if(k == 'release_id'):
                saved_artist = session.query(Product) \
                .filter_by(
                    release_id=v)\
                .one_or_none()
            if(k == 'release_name'):
                saved_artist.release_name = v
                session.merge(saved_artist)
            
    return response.Response(message=data)


def delete_product_by_id(data):
    """Create/Update localization data in DB lookup with data provided.
    Args:
        product_id (int): primary key product_id.
        language_id (int): secondary key language_id.
        data (dict): additional translations for fields.
    Returns:
        Response: A Response obj with message = List of model object
        representation
    """

    with mysql.db_session() as session:
        product = session.query(Product).get(data)
        product = product.to_dict()
        saved_artist = session.query(Product) \
        .filter_by(
            release_id=data)\
        .one_or_none()

        session.delete(saved_artist)

    return response.Response(
        message='{} successfully deleted.'.format(product))
