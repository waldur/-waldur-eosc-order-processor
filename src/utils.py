import logging
import os
import re
from datetime import datetime

import pycountry
from oms_jira import MPClient
from oms_jira.services.mp import (
    MessageAuthor,
    MPMessage,
    ProjectItemStatusEnum,
    ScopeEnum,
)
from waldur_client import ProjectRole, WaldurClient

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def get_env_or_fail(env_variable_name):
    # check that required environment variables is set and exit otherwise
    value = os.environ.get(env_variable_name)
    if not value:
        logger.error(f'Mandatory variable {env_variable_name} is missing or empty.')
        sys.exit(1)
    else:
        return value


EOSC_URL = get_env_or_fail("EOSC_URL")  # polling url
TOKEN = get_env_or_fail("TOKEN")
OMS_ID = get_env_or_fail("OMS_ID")
WALDUR_API_URL = get_env_or_fail("WALDUR_URL")
WALDUR_TARGET_ORGANIZATION_NAME = get_env_or_fail(
    "WALDUR_TARGET_ORGANIZATION_NAME",
)
WALDUR_TOKEN = get_env_or_fail("WALDUR_TOKEN")

waldur_client = WaldurClient(WALDUR_API_URL, WALDUR_TOKEN)
mp = MPClient(endpoint_url=EOSC_URL, oms_id=OMS_ID, auth_token=TOKEN)


def refresh_timestamp(time_now):  # file must be present, create in app.py or dockerfile
    try:
        with open("last_timestamp.txt", "r") as stamp:
            last_timestamp = stamp.readline()

    except FileNotFoundError:
        with open("last_timestamp.txt", "w+") as stamp:
            last_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
            logging.debug(f"File {stamp} was created.")

    else:
        logging.info(f"Timestamp: {last_timestamp} from {stamp.name}")

    now = str(time_now)

    with open("last_timestamp.txt", "w+") as stamp:
        stamp.write(now)

    return last_timestamp


def get_events(timestamp):
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    events = mp.list_events(timestamp_datetime, limit=None)
    logging.info(f"Received the following events from EOSC MP from {timestamp_datetime}: {events}.")
    return events


def invite_user_to_project(email, project):
    waldur_client.create_project_invitation(
        email=email, project=project, project_role=ProjectRole.ADMINISTRATOR
    )


def post_message(project_item_data, content):
    msg_author = MessageAuthor(
        email="test@example.com", name="Test Admin", role="provider"
    )

    msg = MPMessage(
        project_id=project_item_data.project_id,
        project_item_id=project_item_data.id,
        author=msg_author,
        content=content,
        scope=ScopeEnum.public,
    )

    # return mp.create_message(message=msg)
    try:
        post_message_data = mp.post(mp.endpoint.message_list, data=msg.dict())
    except ValueError:
        logging.error(
            f"Message for new order {project_item_data.id} for project "
            f"{project_item_data.project_id} was NOT posted"
        )
    else:
        logging.info(
            f"Message for new order {project_item_data.id} for project "
            f"{project_item_data.project_id} was posted"
        )
        return post_message_data


def patch_project_item(project_item_data):
    try:
        patch_project_item_data = mp.patch(
            mp.endpoint.project_item.format(
                project_id=project_item_data.project_id,
                project_item_id=project_item_data.id,
            ),
            verify=False,
            data={
                "status": {
                    "value": "string",
                    "type": "ready"
                },
            },
        )
    except ValueError:
        logging.exception(
            f"Project item {project_item_data.id} from project "
            f"{project_item_data.project_id} was NOT patched. "
        )
    else:
        logging.info(
            f"Project item {project_item_data.id} from project "
            f"{project_item_data.project_id} has been set to ready. "
        )
        return patch_project_item_data


def update_project_item(project_item_data, event_data):
    for change in event_data.changes:
        # for testing purposes because of invalid test input in eosc mp
        try:
            update_project_item_data = mp.update_project_item(
                project_id=project_item_data.project_id,
                project_item_id=project_item_data.id,
                status=ProjectItemStatusEnum(change.after),
            )
        except ValueError:
            logging.error(
                f"Project item {project_item_data.id} from project "
                f"{project_item_data.project_id} was NOT updated. "
                f"{change.field}: {change.before} -> {change.after}"
            )
        else:
            logging.info(
                f"Project item {project_item_data.id} from project "
                f"{project_item_data.project_id} was updated. "
                f"{change.field}: {change.before} -> {change.after}"
            )
            return update_project_item_data


def _get_item_value_by_name(item_list, property_name):
    for item in item_list:
        if property_name == item["id"]:
            return item["value"]
        if property_name.lower() == item["label"].lower():
            return item["value"]


def get_plan(eosc_project_item_data, waldur_offering_data):
    plan = None
    for waldur_plan in waldur_offering_data["plans"]:
        if eosc_project_item_data.attributes.offer == waldur_plan["name"]:
            plan = waldur_plan
    return plan


def create_order(
    waldur_offering_data, waldur_project_data_for_order, eosc_project_item_data, invitation_email
):
    plan = get_plan(eosc_project_item_data, waldur_offering_data)

    attributes = {}
    limits = {}

    # 1. Extract mandatory name from the attributes
    attributes["name"] = _get_item_value_by_name(
        eosc_project_item_data.attributes.offer_properties, "name"
    )
    try:
        if attributes["name"] == "name":
            attributes["name"] = re.sub(
                "[^A-Za-z0-9-]+",  # alphanumeric values and hyphen
                "",
                eosc_project_item_data.attributes.offer_properties["value"],
            )
    except attributes["name"] is None:
        logging.error(f"Name of the order can not be {None}!")
    else:
        logging.info(f'Name of the order is correct: {attributes["name"]}')

    # TODO: Decide what goes where based on id
    for offer_property in eosc_project_item_data.attributes.offer_properties:
        if offer_property["value_type"] == "integer":
            if offer_property["id"] == "name":
                continue
            try:
                property_type, property_id = offer_property["id"].split()
                # TODO: drop once publishing works, id cannot be edited in MP
                if property_id == 'gpu_k_hours':
                    property_id = 'gpu_hours'
            except ValueError:
                logging.error(
                    f'{offer_property["id"]}: not enough values to unpack (expected 2, got 1)'
                )
            else:
                if property_type == "limit":
                    if property_id == "ram" or property_id == "storage":
                        limits[property_id] = int(offer_property["value"] * 1024)
                    else:
                        limits[property_id] = int(offer_property["value"])

                if property_type == "attributes":
                    attributes[property_id] = offer_property["value"]

    try:
        order_data = waldur_client.create_marketplace_order(
            project=waldur_project_data_for_order["uuid"],
            offering=waldur_offering_data["uuid"],
            plan=plan["uuid"],
            attributes=attributes,
            limits=limits,
        )
        pass
    except ValueError:
        logging.error(f'There is no {plan["name"]} in ETAIS.')
        raise
    else:
        logging.info(
            f'Order for {waldur_offering_data["name"]} with plan {plan["name"]} plan was created.'
        )

        content = (
            f"Invitation has been sent to your email: {invitation_email}"
        )

        post_message(project_item_data=eosc_project_item_data, content=content)
        patch_project_item(project_item_data=eosc_project_item_data)

        return order_data


def get_or_create_project(eosc_project_data, waldur_organization_data):
    projects_with_backend_id = waldur_client.list_projects(
        {
            "backend_id": str(eosc_project_data.id),
            "customer_uuid": waldur_organization_data[0]["uuid"],
        }
    )
    if len(projects_with_backend_id) != 0:
        logging.info(
            f"Project with backend_id {eosc_project_data.id} is already in Waldur, "
            f'name: {projects_with_backend_id[0]["name"]}.'
        )
        return projects_with_backend_id[0]
    try:
        create_project_data = waldur_client.create_project(
            customer_uuid=waldur_organization_data[0]["uuid"],
            name=eosc_project_data.attributes.name,
            backend_id=str(eosc_project_data.id),
        )
    except ValueError:
        logging.error(f"Cannot create project with id {eosc_project_data.id}")
    else:
        logging.info(
            f"Project with backend_id {eosc_project_data.id} was created in Waldur. "
            f"Name of the project: {eosc_project_data.attributes.name}. "
            f'Customer name: {waldur_organization_data[0]["name"]}.'
        )
        # TODO: exctract to a separate call
        invite_user_to_project(
            email=eosc_project_data.owner.email, project=create_project_data["uuid"]
        )
        return create_project_data


def get_or_create_customer_for_project(project_data):
    customers_filter_list = waldur_client.list_customers(
        {"name_exact": project_data.attributes.organization}
    )
    if len(customers_filter_list) != 0:
        logging.info(
            f"Customer named {project_data.attributes.organization} is already in WALDUR."
        )
        return customers_filter_list[0]  # data of existing customer with this name
    try:
        customer_data = waldur_client.create_customer(
            name=project_data.attributes.organization,
            # data of a new customer
            email=project_data.owner.email,
            backend_id=project_data.attributes.organization,
            country=pycountry.countries.get(
                name=project_data.attributes.country
            ).alpha_2,
            domain=project_data.attributes.department_webpage,
            homepage=project_data.attributes.department_webpage,
            native_name=project_data.attributes.organization,
        )
    except ValueError:
        logging.error(f"Cannot customer named {project_data.attributes.organization}.")
    else:
        logging.info(
            f"Customer named {project_data.attributes.organization} was created in Waldur."
        )
        return customer_data


def get_target_waldur_organization():
    return waldur_client.list_customers(
        {"display_name": WALDUR_TARGET_ORGANIZATION_NAME}
    )


def get_new_events(events, time_now):
    new_events = []
    for event in events:
        event_timestamp = event.timestamp.replace(tzinfo=None)
        if event_timestamp < time_now:
            new_events.append(event)
        else:
            break

    return new_events


def process_orders():
    # test with older timestamps in last_timestamp.txt
    time_now = datetime.utcnow()
    events = get_events(refresh_timestamp(time_now=time_now))
    new_events = get_new_events(events, time_now)
    for event in new_events:
        try:
            if event.resource == "project_item" and event.type == "create":
                eosc_project_data = mp.get_project(event.project_id)

                eosc_project_item_data = mp.get_project_item(
                    event.project_id, event.project_item_id
                )
                waldur_organization_data = get_target_waldur_organization()

                waldur_offering_data = waldur_client.list_marketplace_offerings(
                    {"name_exact": eosc_project_item_data.attributes.service}
                )
                if len(waldur_offering_data) == 0:
                    raise Exception(f'Could not lookup offering in Waldur with requested name {eosc_project_item_data.attributes.service}.')

                waldur_project_data = get_or_create_project(
                    eosc_project_data=eosc_project_data,
                    waldur_organization_data=waldur_organization_data,
                )
                create_order(
                    waldur_offering_data=waldur_offering_data[0],
                    waldur_project_data_for_order=waldur_project_data,
                    eosc_project_item_data=eosc_project_item_data,
                    invitation_email=eosc_project_data.owner.email
                )

            if event.type == "delete" or event.type == "update":
                logging.info(f"Found event with unsupported type: {event.type}.")
        except Exception as e:
            logger.exception(
                "The event can not be processed due to the following exception"
            )
