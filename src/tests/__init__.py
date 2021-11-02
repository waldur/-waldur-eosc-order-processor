import datetime
from oms_jira.services.mp import MPProject, ProjectOwner, ProjectAttributes, MPProjectItem, ProjectItemAttributes, Event

# 1. test_get_or_create_project_first
MOCK_LIST_PROJECTS_1 = [{'url': 'project_url',
                         'uuid': 'project_uuid',
                         'name': 'TEST4',
                         'customer': 'customer_url',
                         'customer_uuid': 'customer_uuid',
                         'customer_name': 'Test4all',
                         'created': '2021-08-16T11:44:22.851786Z',
                         'backend_id': '1452',
                         }]

EOSC_PROJECT_DATA_1 = MPProject(id=1452, owner=ProjectOwner(
    uid='owner@aai.eosc-portal.eu',
    email='owner@ut.ee', name='OWNER'), project_items=[1, 2, 3],
                                attributes=ProjectAttributes(name='TEST4',
                                                             customer_typology='single_user',
                                                             organization='ETAIS',
                                                             department='backend',
                                                             department_webpage='https://etais.ee/',
                                                             scientific_domains=[
                                                                 'Economics & Business'],
                                                             country='Estonia',
                                                             collaboration_countries=[],
                                                             user_group_name=''))

WALDUR_ORGANIZATION_DATA_1 = [{
    'url': 'customer_url',
    'uuid': 'customer_uuid',
    'created': '2017-03-21T07:24:34.090847Z',
    'division': 'customer_division',
    'division_name': 'Tests',
    'division_uuid': 'customer_division_uuid',
    'division_type_name': 'Department',
    'division_type_uuid': 'customer_division_type_uuid',
    'display_name': 'Test4all',
    'projects': [
        {'url': 'project_url',
         'uuid': 'project_uuid',
         'name': 'TEST4'}],
    'owners': [
        {'url': 'owner_url',
         'uuid': 'owner_uuid',
         'username': 'owner@ut.ee',
         'full_name': 'OWNER',
         'native_name': ''}
    ],
    'accounting_start_date': '2018-02-11T22:52:29.951974Z',
    'name': 'Test4all'}]

MOCK_CREATE_PROJECT_1 = {
    'url': 'project_url',
    'uuid': 'project_uuid',
    'name': 'TEST4',
    'customer': 'customer_url',
    'customer_uuid': 'customer_uuid',
    'customer_name': 'Test4all',
    'created': '2021-08-16T11:44:22.851786Z',
    'backend_id': '1452'}

# 3. test_create_order

MOCK_CREATE_MARKETPLACE_ORDER_3 = {
    "url": "order_url",
    "uuid": "order_uuid",
    "created": "2021-10-13T13:58:51.471159Z",
    "created_by": "created_by_user",
    "created_by_username": "user@ut.ee",
    "created_by_full_name": "TestUser",
    "approved_by": "approved_by_user",
    "approved_at": "2021-10-13T13:58:51.548927Z",
    "approved_by_username": "user@ut.ee",
    "approved_by_full_name": "TestUser",
    "project": "project_url",
    "project_uuid": "project_uuid",
    "project_name": "TEST",
    "project_description": "",
    "customer_name": "customer_name",
    "customer_uuid": "customer_uuid",
    "state": "done",
    "items": [
        {
            "offering": "offering_url",
            "offering_name": "offering_name",
            "offering_uuid": "offering_uuid",
            "offering_description": "",
            "offering_thumbnail": "offering_thumbnail_url",
            "offering_type": "SlurmInvoices.SlurmPackage",
            "offering_terms_of_service": "",
            "offering_shared": True,
            "offering_billable": True,
            "provider_name": "ETAIS",
            "provider_uuid": "provider_uuid",
            "category_title": "title",
            "category_uuid": "category_uuid",
            "plan": "plan_url",
            "plan_unit": "day",
            "plan_name": "plan_name",
            "plan_uuid": "plan_uuid",
            "plan_description": "",
            "attributes": {
                "name": "test_test"
            },
            "limits": {},
            "uuid": "item_uuid",
            "created": "2021-10-13T13:58:51.498607Z",
            "modified": "2021-10-13T13:59:09.704655Z",
            "type": "Create",
            "resource_uuid": "resource_uuid",
            "resource_type": "SLURM.Allocation",
            "resource_name": "test_test",
            "cost": "0.0000000000",
            "state": "done",
            "output": "",
            "marketplace_resource_uuid": "marketplace_resource_uuid",
            "error_message": ""
        }
    ],
    "total_cost": "0.0000000000",
    "file": "file_url",
    "type": "Create",
    "error_message": "error_uuid: "
}

MOCK_OFFERING_DATA_3 = [
    {'url': 'offering_url',
     'uuid': 'offering_uuid',
     'created': '2019-05-03T12:03:13.531473Z',
     'name': 'service',
     'description': 'sample',
     'customer': 'customer_url',
     'customer_uuid': 'customer_uuid',
     'customer_name': 'ETAIS',
     'category': 'category_url',
     'category_uuid': 'category_uuid',
     'category_title': 'Private clouds',
     'attributes': {'vpc_Support_email': 'support@hpc.ut.ee',
                    'vpc_Security_certification': ['vpc_Security_certification_iskem']
                    },
     'options': {'order': [],
                 'options': {}
                 },
     'components': [
         {'billing_type': 'limit',
          'type': 'cores',
          'name': 'Cores',
          'measured_unit': 'cores',
          'limit_period': None,
          'limit_amount': None,
          'article_code': '',
          'max_value': 10,
          'min_value': 1,
          'is_boolean': False,
          'default_limit': None,
          'factor': 1,
          'is_builtin': True},
     ],
     'plugin_options': {'storage_mode': 'fixed'},
     'native_name': '',
     'thumbnail': 'thumbnail_url',
     'order_item_count': 804.0,
     'plans': [
         {'url': 'plan_url',
          'uuid': 'plan_uuid',
          'name': 'plan_name',
          'prices': {'cores': 0.1,
                     'ram': 0.1,
                     'storage': 0.1},
          'quotas': {'cores': 0,
                     'ram': 0,
                     'storage': 0},
          'unit_price': '0.0000000',
          'unit': 'day',
          'init_price': 0,
          'switch_price': 0,
          'backend_id': '',
          'plan_type': 'limit',
          'minimal_price': 0.0}
     ],
     'scope': 'scoper_url',
     'scope_uuid': 'scope_uuid',
     'quotas': [
         {'url': 'quota_url',
          'uuid': 'quota_uuid',
          'name': 'quota_name',
          'limit': -1.0,
          'usage': 0.0}
     ],
     'backend_id': ''}
]

WALDUR_PROJECT_DATA_3 = {'url': 'project_url',
                         'uuid': 'project_uuid',
                         'name': 'project_name',
                         'customer': 'customer_name',
                         'customer_uuid': 'customer_uuid',
                         'customer_name': 'customer_name',
                         'created': '2021-08-16T11:38:29.677204Z',
                         'backend_id': '1449',
                         }

EOSC_PROJECT_ITEM_DATA_3 = MPProjectItem(id=3,
                                         project_id=1449,
                                         status=MPProjectItem.Status(value='registered',
                                                                     type='registered'),
                                         attributes=ProjectItemAttributes(category='Applications',
                                                                          service='service',
                                                                          offer='plan_name',
                                                                          offer_properties=[
                                                                              {'id': 'name',
                                                                               'type': 'input',
                                                                               'unit': '',
                                                                               'label': 'Name',
                                                                               'value': 'my offer',
                                                                               'value_type': 'string',
                                                                               'description': 'sample'}
                                                                          ],
                                                                          platforms=[],
                                                                          request_voucher=False,
                                                                          order_type='order_required'),
                                         user_secrets={})

# 4. test_process_orders_first

EVENTS_4 = [Event(timestamp=datetime.datetime(2021, 8, 10, 13, 17, 45, tzinfo=datetime.timezone.utc),
                  type='create',
                  resource='project',
                  project_id=1453,
                  project_item_id=None,
                  message_id=None,
                  changes=None),
            Event(timestamp=datetime.datetime(2021, 8, 19, 12, 33, 32, tzinfo=datetime.timezone.utc),
                  type='create',
                  resource='project_item',
                  project_id=1454,
                  project_item_id=1,
                  message_id=None,
                  changes=None),
            Event(timestamp=datetime.datetime(2021, 8, 19, 12, 33, 32, tzinfo=datetime.timezone.utc),
                  type='update',
                  resource='project_item',
                  project_id=1454,
                  project_item_id=1,
                  message_id=None,
                  changes=[
                      Event.Change(field='status.type',
                                   before='created',
                                   after='registered'),
                      Event.Change(field='status.value',
                                   before='created',
                                   after='registered')
                  ]
                  )
            ]

MOCK_WALDUR_ORGANIZATION_4 = [{
    'url': 'customer_url',
    'uuid': 'customer_uuid',
    'created': '2017-03-21T07:24:34.090847Z',
    'division': 'customer_division',
    'division_name': 'Tests',
    'division_uuid': 'customer_division_uuid',
    'division_type_name': 'Department',
    'division_type_uuid': 'customer_division_type_uuid',
    'display_name': 'Test4all',
    'projects': [
        {'url': 'project_url',
         'uuid': 'project_uuid',
         'name': 'TEST4'}],
    'owners': [
        {'url': 'owner_url',
         'uuid': 'owner_uuid',
         'username': 'owner@ut.ee',
         'full_name': 'OWNER',
         'native_name': ''}
    ],
    'backend_id': '',
    'default_tax_percent': '0.00',
    'accounting_start_date': '2018-02-11T22:52:29.951974Z',
    'name': 'Test4all',
    'native_name': ''
}]

MOCK_WALDUR_OFFERING_4 = [{
    'url': 'offering_url',
    'uuid': 'offering_uuid',
    'created': '2019-05-03T12:05:07.578937Z',
    'name': 'Rocket (UT HPC)',
    'customer': 'customer_url',
    'customer_uuid': 'customer_uuid',
    'customer_name': 'ETAIS',
    'category': 'category_url',
    'category_uuid': 'category_uuid',
    'category_title': 'HPC',
    'rating': None,
    'attributes': {},
    'options': {},
    'components': [
        {'billing_type': 'usage',
         'type': 'cpu',
         'name': 'CPU',
         'measured_unit': 'hours',
         'limit_period': None,
         'limit_amount': None,
         'max_value': None,
         'min_value': None,}
    ],
    'state': 'Active',
    'native_name': '',
    'thumbnail': 'thumbnail_url',
    'order_item_count': 0.0,
    'plans': [
        {'url': 'plan_url',
         'uuid': 'plan_uuid',
         'name': 'Rocket',
         'prices': {'cpu': 0.1,
                    'gpu': 0.1,
                    'ram': 0.1},
         'quotas': {'cpu': 0,
                    'gpu': 0,
                    'ram': 0},
         'unit_price': '0.0000000',
         'unit': 'day',
         'init_price': 0,
         'switch_price': 0,
         'backend_id': ''}
    ],
    'scope': 'scope_url',
    'scope_uuid': 'scope_uuid',
    'backend_id': ''
}]

MOCK_LIST_PROJECTS_4 = [{'url': 'project_url',
                         'uuid': 'project_uuid',
                         'name': 'TEST4',
                         'customer': 'customer_url',
                         'customer_uuid': 'customer_uuid',
                         'customer_name': 'Test4all',
                         'created': '2021-08-16T11:44:22.851786Z',
                         'backend_id': '1452',}]

MOCK_CREATE_PROJECT_4 = {
    'url': 'project_url',
    'uuid': 'project_uuid',
    'name': 'TEST4',
    'customer': 'customer_url',
    'customer_uuid': 'customer_uuid',
    'customer_name': 'Test4all',
    'created': '2021-08-16T11:44:22.851786Z',
    'backend_id': '1452'}

# 6. test_get_events

MOCK_GET_EVENTS_6 = [
    Event(timestamp=datetime.datetime(2021, 9, 28, 10, 57, 27, tzinfo=datetime.timezone.utc),
          type='create',
          resource='project_item',
          project_id=1452,
          project_item_id=3,
          message_id=None,
          changes=None),
    Event(timestamp=datetime.datetime(2021, 9, 28, 10, 57, 28, tzinfo=datetime.timezone.utc),
          type='update',
          resource='project_item',
          project_id=1452,
          project_item_id=3,
          message_id=None,
          changes=[
              Event.Change(field='status.type',
                           before='created',
                           after='registered'),
              Event.Change(field='status.value',
                           before='created',
                           after='registered')
          ]
          )
]

# 7. test_new_events

MOCK_GET_EVENTS_7 = [
    Event(timestamp=datetime.datetime(2021, 9, 28, 10, 57, 27, tzinfo=datetime.timezone.utc),
          type='create',
          resource='project_item',
          project_id=1452,
          project_item_id=3,
          message_id=None,
          changes=None),
    Event(timestamp=datetime.datetime(2021, 9, 28, 10, 57, 28, tzinfo=datetime.timezone.utc),
          type='update',
          resource='project_item',
          project_id=1452,
          project_item_id=3,
          message_id=None,
          changes=[Event.Change(field='status.type',
                                before='created',
                                after='registered'),
                   Event.Change(field='status.value',
                                before='created',
                                after='registered')
                   ]
          )

]

EXPECTED_EVENTS_7 = [Event(timestamp=datetime.datetime(2021, 9, 28, 10, 57, 27, tzinfo=datetime.timezone.utc),
                           type='create',
                           resource='project_item',
                           project_id=1452,
                           project_item_id=3,
                           message_id=None,
                           changes=None)
                     ]
