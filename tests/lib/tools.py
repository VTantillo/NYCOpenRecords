import os
import uuid
import random
from itertools import product
from string import ascii_lowercase, digits
from datetime import datetime

from flask import current_app
from app.constants import (
    ACKNOWLEDGEMENT_DAYS_DUE,
    response_type,
    user_type_auth,
    user_type_request,
    submission_methods,
    request_status,
)
from app.constants.response_privacy import PRIVATE
from app.models import (
    Requests,
    Responses,
    Files,
    Users,
    Agencies,
    UserRequests,
)
from app.request.utils import (
    generate_request_id,
    generate_guid as generate_guid_anon
)
from app.lib.date_utils import (
    get_following_date,
    get_due_date
)
from app.lib.db_utils import create_object


class RequestsFactory(object):
    """
    Helper for creating test Requests data.
    """

    filepaths = []

    def __init__(self, request_id):
        date_created = datetime.utcnow()
        date_submitted = get_following_date(date_created)
        agency_ein = 2
        self.request = Requests(
            request_id or generate_request_id(agency_ein),
            title="I would like my vital essence.",
            description="Someone has taken my vital essence "
            "and I would like it back.",
            agency_ein=agency_ein,
            date_created=date_created,
            date_submitted=date_submitted,
            due_date=get_due_date(date_submitted,
                                  ACKNOWLEDGEMENT_DAYS_DUE),
            submission=submission_methods.DIRECT_INPUT,
            current_status=request_status.OPEN)
        create_object(self.request)
        self.requester = Users(
            guid=generate_user_guid(user_type_auth.PUBLIC_USER_NYC_ID),
            auth_user_type=user_type_auth.PUBLIC_USER_NYC_ID,
            agency=agency_ein,
            first_name='Jane',
            last_name='Doe',
            email='jdizzle@email.com',
            email_validated=True,
            terms_of_use_accepted=True,
            title='The Janest')
        create_object(self.requester)
        # TODO: UserRequests obj

    def add_file(self,
                 filepath=None,
                 mime_type='text/plain',
                 title=None):
        if filepath is None:
            filename = str(uuid.uuid4())
            filepath = os.path.join(current_app.config['UPLOAD_DIRECTORY'],
                                    self.request.id,
                                    filename)
        else:
            filename = os.path.basename(filepath)

        self.filepaths.append(filepath)

        # create an empty file if the specified path does not exist
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            open(filepath, 'w').close()

        file_meta = Files(
            name=filename,
            mime_type=mime_type,
            title=title or filename,
            size=os.path.getsize(filepath)
        )
        create_object(file_meta)
        response = Responses(
            request_id=self.request.id,
            type=response_type.FILE,
            date_modified=datetime.utcnow(),
            metadata_id=file_meta.id,
            privacy=PRIVATE,
        )
        # TODO: add Events FILE_ADDED
        create_object(response)
        return response

    def add_note(self):
        pass

    def __del__(self):
        """
        Clean up time!
        - remove any files created by this factory
        - ...
        """
        for path in self.filepaths:
            if os.path.exists(path):
                os.remove(path)


def create_user(auth_type):
    """
    :param auth_type: one of app.constants.user_type_auth
    """
    len_firstname = random.randrange(3, 8)
    len_lastname = random.randrange(3, 15)
    firstname = ''.join(random.choice(ascii_lowercase)
                        for _ in range(len_firstname)).title()
    lastname = ''.join(random.choice(ascii_lowercase)
                       for _ in range(len_lastname)).title()
    user = Users(
        guid=generate_user_guid(auth_type),
        auth_user_type=auth_type,
        agency=(random.choice([ein[0] for ein in
                              Agencies.query.with_entities(Agencies.ein).all()])
                if auth_type == user_type_auth.AGENCY_USER
                else None),
        first_name=firstname,
        last_name=lastname,
        email='{}{}@email.com'.format(firstname[0].lower(), lastname.lower()),
        email_validated=True,
        terms_of_use_accepted=True)
    create_object(user)
    return user


def generate_user_guid(auth_type):
    if auth_type == user_type_auth.ANONYMOUS_USER:
        return generate_guid_anon()
    else:
        non_anon_guid_length = 6  # TODO: make constant, is valid?
        return ''.join(random.choice(ascii_lowercase + digits)
                       for _ in range(non_anon_guid_length))


def create_requests_search_set(requester, other_requester):
    agency_eins = [ein[0] for ein in
                   Agencies.query.with_entities(Agencies.ein).all()]

    for title_private, agency_desc_private, is_requester in product(range(2), repeat=3):
        agency_ein = random.choice(agency_eins)
        date_created = datetime.utcnow()
        date_submitted = get_following_date(date_created)
        request = Requests(
            generate_request_id(agency_ein),
            title="Test",
            description="Test",
            agency_description="Test",
            agency_ein=agency_ein,
            date_created=date_created,
            date_submitted=date_submitted,
            due_date=get_due_date(date_submitted,
                                  ACKNOWLEDGEMENT_DAYS_DUE),
            submission=submission_methods.DIRECT_INPUT,
            current_status=request_status.OPEN,
            privacy={
                'title': bool(title_private),
                'agency_description': bool(agency_desc_private)
            }
        )
        create_object(request)
        user_request = UserRequests(
            user_guid=(requester.guid if is_requester
                       else other_requester.guid),
            auth_user_type=(requester.auth_user_type if is_requester
                            else other_requester.auth_user_type),
            request_id=request.id,
            request_user_type=user_type_request.REQUESTER,
            permissions=11
        )
        create_object(user_request)
