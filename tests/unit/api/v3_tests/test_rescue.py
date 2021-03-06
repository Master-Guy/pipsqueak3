import json
from importlib import resources
from typing import Dict
from uuid import UUID

import pytest

from src.packages.fuelrats_api.v3.models.v1.rescue import Rescue as ApiRescue
from src.packages.rescue import Rescue as InternalRescue
from .. import v3_tests
import cattr
pytestmark = [pytest.mark.unit, pytest.mark.api_v3]

RAW_ENUMERATE_RESCUE_RESPONSE: Dict = json.loads(
    resources.read_text(v3_tests, "raw_rescue_enumerate_response.json"))


def test_deserialize():
    original = RAW_ENUMERATE_RESCUE_RESPONSE.copy()
    rescue = cattr.structure(RAW_ENUMERATE_RESCUE_RESPONSE['data'][0], ApiRescue)

    assert RAW_ENUMERATE_RESCUE_RESPONSE == original, "illegal mutation of input data"
    assert rescue.id == UUID("a8acc8d6-af38-4256-9911-7455e33012f2")
    assert rescue.attributes.client == "Test Client"
    assert rescue.attributes.clientLanguage is None
    assert rescue.attributes.codeRed is True
    assert rescue.attributes.commandIdentifier is None
    assert rescue.attributes.notes == 'hello world2222222!'


def test_from_internal(rescue_sop_fx):
    # assert we can build a API rescue from mecha's internal data model
    rescue = ApiRescue.from_internal(rescue_sop_fx)

    assert rescue.id == rescue_sop_fx.api_id
    assert rescue.attributes.client == rescue_sop_fx.client
    assert rescue.attributes.createdAt.tzinfo is not None


def test_to_internal(rescue_sop_fx):
    """ verify converting a rescue to and from an API datamodel produces an equivalent object """
    rescue = ApiRescue.from_internal(rescue_sop_fx)
    rescue = rescue.into_internal()
    assert rescue_sop_fx == rescue, "unequivalent rescues created!"


def test_to_internal_w_quotes():
    """ convert a rescue to the API datamodel with quotes. """
    rescue = InternalRescue(client="someone")
    rescue.system = "somewhere"
    rescue.add_quote("some message")
    rescue.add_quote("some other message")
    api_rescue = ApiRescue.from_internal(rescue)
    assert api_rescue.attributes.quotes


def test_diff(rescue_sop_fx):
    rescue_sop_fx.modified.clear()
    # Modify some attributes to populated the `modified` tracking attribute
    rescue_sop_fx.client = "some_other_client"
    assert len(rescue_sop_fx.modified) == 1, "unexpected modification!"

    # serialize object to an API datamodel object
    rescue = ApiRescue.from_internal(rescue_sop_fx)
    # compute json blob from changed fields on the internal object
    # (we can't bring the modified into the internal model without messing up serialization).
    obj = rescue.to_delta(changes=rescue_sop_fx.modified)
    # check that the attributes are as we expected.
    modified_keys = list(obj['attributes'].keys())
    assert modified_keys == ['client']
