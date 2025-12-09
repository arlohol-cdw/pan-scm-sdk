"""Tests for Ethernet Interface configuration service."""

# Standard library imports
from unittest.mock import MagicMock

import pytest

# Local SDK imports
from scm.config.network import EthernetInterface
from scm.exceptions import InvalidObjectError, MissingQueryParameterError
from scm.models.network import (
    EthernetInterfaceCreateModel,
    EthernetInterfaceResponseModel,
    EthernetInterfaceUpdateModel,
)
from tests.factories.network import EthernetInterfaceCreateApiFactory


@pytest.mark.usefixtures("load_env")
class TestEthernetInterfaceBase:
    """Base class for Ethernet Interface tests."""

    @pytest.fixture(autouse=True)
    def setup_method(self, mock_scm):
        """Setup method that runs before each test."""
        self.mock_scm = mock_scm
        self.mock_scm.get = MagicMock()
        self.mock_scm.post = MagicMock()
        self.mock_scm.put = MagicMock()
        self.mock_scm.delete = MagicMock()
        self.client = EthernetInterface(self.mock_scm, max_limit=5000)


class TestEthernetInterfaceInitialization(TestEthernetInterfaceBase):
    """Test Ethernet Interface service initialization."""

    def test_init_default_limit(self):
        """Test initializing with default max limit."""
        service = EthernetInterface(self.mock_scm)
        assert service.max_limit == 2500
        assert service.ENDPOINT == "/config/network/v1/ethernet-interfaces"

    def test_init_custom_limit(self):
        """Test initializing with custom max limit."""
        service = EthernetInterface(self.mock_scm, max_limit=1000)
        assert service.max_limit == 1000

    def test_init_max_limit_setter(self):
        """Test setting max_limit property."""
        service = EthernetInterface(self.mock_scm)
        service.max_limit = 3000
        assert service.max_limit == 3000

    def test_max_limit_validation_invalid_type(self):
        """Test validation of max_limit with invalid type."""
        with pytest.raises(InvalidObjectError) as exc_info:
            EthernetInterface(self.mock_scm, max_limit="invalid")
        assert "Invalid max_limit type" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400

    def test_max_limit_validation_less_than_one(self):
        """Test validation of max_limit with value less than 1."""
        with pytest.raises(InvalidObjectError) as exc_info:
            EthernetInterface(self.mock_scm, max_limit=0)
        assert "Invalid max_limit value" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400

    def test_max_limit_validation_exceeds_maximum(self):
        """Test validation of max_limit exceeding maximum allowed."""
        with pytest.raises(InvalidObjectError) as exc_info:
            EthernetInterface(self.mock_scm, max_limit=6000)
        assert "max_limit exceeds maximum allowed value" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400


class TestEthernetInterfaceCreate(TestEthernetInterfaceBase):
    """Test Ethernet Interface create operations."""

    def test_create_with_tap_mode(self):
        """Test creating an Ethernet Interface with tap mode."""
        test_interface = EthernetInterfaceCreateApiFactory.with_tap(
            name="ethernet1/1",
            folder="Texas",
        )

        mock_response = {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/1",
            "folder": "Texas",
            "tap": {},
        }

        self.mock_scm.post.return_value = mock_response
        created = self.client.create(test_interface.model_dump(by_alias=True))

        self.mock_scm.post.assert_called_once()
        assert isinstance(created, EthernetInterfaceResponseModel)
        assert created.name == "ethernet1/1"
        assert created.folder == "Texas"

    def test_create_with_layer2_mode(self):
        """Test creating an Ethernet Interface with layer2 mode."""
        test_interface = EthernetInterfaceCreateApiFactory.with_layer2(
            name="ethernet1/2",
            vlan_tag=100,
            folder="Texas",
        )

        mock_response = {
            "id": "223e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/2",
            "folder": "Texas",
            "layer2": {"vlan-tag": 100},
        }

        self.mock_scm.post.return_value = mock_response
        created = self.client.create(test_interface.model_dump(by_alias=True))

        self.mock_scm.post.assert_called_once()
        assert isinstance(created, EthernetInterfaceResponseModel)
        assert created.name == "ethernet1/2"

    def test_create_with_layer3_static(self):
        """Test creating an Ethernet Interface with layer3 static IP."""
        test_interface = EthernetInterfaceCreateApiFactory.with_layer3_static(
            name="ethernet1/3",
            ips=["10.0.0.1/24", "10.0.0.2/24"],
            folder="Texas",
        )

        mock_response = {
            "id": "323e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/3",
            "folder": "Texas",
            "layer3": {"ip": ["10.0.0.1/24", "10.0.0.2/24"]},
        }

        self.mock_scm.post.return_value = mock_response
        created = self.client.create(test_interface.model_dump(by_alias=True))

        self.mock_scm.post.assert_called_once()
        assert isinstance(created, EthernetInterfaceResponseModel)
        assert created.name == "ethernet1/3"

    def test_create_with_layer3_dhcp(self):
        """Test creating an Ethernet Interface with layer3 DHCP."""
        test_interface = EthernetInterfaceCreateApiFactory.with_layer3_dhcp(
            name="ethernet1/4",
            folder="Texas",
        )

        mock_response = {
            "id": "423e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/4",
            "folder": "Texas",
            "layer3": {
                "dhcp-client": {
                    "enable": True,
                    "create-default-route": True,
                }
            },
        }

        self.mock_scm.post.return_value = mock_response
        created = self.client.create(test_interface.model_dump(by_alias=True))

        self.mock_scm.post.assert_called_once()
        assert isinstance(created, EthernetInterfaceResponseModel)
        assert created.name == "ethernet1/4"

    def test_create_with_layer3_pppoe(self):
        """Test creating an Ethernet Interface with layer3 PPPoE."""
        test_interface = EthernetInterfaceCreateApiFactory.with_layer3_pppoe(
            name="ethernet1/5",
            username="testuser",
            password="testpass",
            folder="Texas",
        )

        mock_response = {
            "id": "523e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/5",
            "folder": "Texas",
            "layer3": {
                "pppoe": {
                    "enable": True,
                    "username": "testuser",
                    "password": "testpass",
                }
            },
        }

        self.mock_scm.post.return_value = mock_response
        created = self.client.create(test_interface.model_dump(by_alias=True))

        self.mock_scm.post.assert_called_once()
        assert isinstance(created, EthernetInterfaceResponseModel)
        assert created.name == "ethernet1/5"


class TestEthernetInterfaceGet(TestEthernetInterfaceBase):
    """Test Ethernet Interface get operations."""

    def test_get(self):
        """Test getting an Ethernet Interface by ID."""
        mock_response = {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/1",
            "folder": "Texas",
            "tap": {},
        }

        self.mock_scm.get.return_value = mock_response
        interface = self.client.get("123e4567-e89b-12d3-a456-426655440000")

        self.mock_scm.get.assert_called_once_with(
            "/config/network/v1/ethernet-interfaces/123e4567-e89b-12d3-a456-426655440000"
        )
        assert isinstance(interface, EthernetInterfaceResponseModel)
        assert interface.id == "123e4567-e89b-12d3-a456-426655440000"
        assert interface.name == "ethernet1/1"


class TestEthernetInterfaceUpdate(TestEthernetInterfaceBase):
    """Test Ethernet Interface update operations."""

    def test_update(self):
        """Test updating an Ethernet Interface."""
        update_data = EthernetInterfaceCreateApiFactory.with_tap(
            name="ethernet1/1",
            folder="Texas",
            comment="Updated comment",
        )

        update_model = EthernetInterfaceUpdateModel(
            id="123e4567-e89b-12d3-a456-426655440000",
            **update_data.model_dump(),
        )

        mock_response = {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/1",
            "folder": "Texas",
            "comment": "Updated comment",
            "tap": {},
        }

        self.mock_scm.put.return_value = mock_response
        updated = self.client.update(update_model)

        self.mock_scm.put.assert_called_once()
        assert isinstance(updated, EthernetInterfaceResponseModel)
        assert updated.comment == "Updated comment"


class TestEthernetInterfaceDelete(TestEthernetInterfaceBase):
    """Test Ethernet Interface delete operations."""

    def test_delete(self):
        """Test deleting an Ethernet Interface."""
        object_id = "123e4567-e89b-12d3-a456-426655440000"
        self.client.delete(object_id)

        self.mock_scm.delete.assert_called_once_with(
            f"/config/network/v1/ethernet-interfaces/{object_id}"
        )


class TestEthernetInterfaceList(TestEthernetInterfaceBase):
    """Test Ethernet Interface list operations."""

    def test_list_empty_folder(self):
        """Test list method with empty folder name."""
        with pytest.raises(MissingQueryParameterError) as exc_info:
            self.client.list(folder="")
        assert "folder" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400

    def test_list_no_container(self):
        """Test list method with no container specified."""
        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.list()
        assert "Invalid container parameters" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400

    def test_list_multiple_containers(self):
        """Test list method with multiple containers."""
        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.list(folder="Texas", snippet="TestSnippet")
        assert "Invalid container parameters" in str(exc_info.value)
        assert exc_info.value.http_status_code == 400

    def test_list_with_folder(self):
        """Test listing Ethernet Interfaces in a folder."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "folder": "Texas",
                    "tap": {},
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/2",
                    "folder": "Texas",
                    "layer2": {"vlan-tag": 100},
                },
            ],
            "limit": 5000,
            "offset": 0,
            "total": 2,
        }

        self.mock_scm.get.return_value = mock_response
        interfaces = self.client.list(folder="Texas")

        self.mock_scm.get.assert_called_once_with(
            "/config/network/v1/ethernet-interfaces",
            params={"folder": "Texas", "limit": 5000, "offset": 0},
        )
        assert len(interfaces) == 2
        assert all(isinstance(i, EthernetInterfaceResponseModel) for i in interfaces)

    def test_list_with_pagination(self):
        """Test listing with pagination."""
        first_response = {
            "data": [
                {
                    "id": f"{i}23e4567-e89b-12d3-a456-426655440000",
                    "name": f"ethernet1/{i}",
                    "folder": "Texas",
                    "tap": {},
                }
                for i in range(2)
            ],
            "limit": 2,
            "offset": 0,
            "total": 3,
        }

        second_response = {
            "data": [
                {
                    "id": "323e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/3",
                    "folder": "Texas",
                    "tap": {},
                }
            ],
            "limit": 2,
            "offset": 2,
            "total": 3,
        }

        self.mock_scm.get.side_effect = [first_response, second_response]
        self.client.max_limit = 2

        interfaces = self.client.list(folder="Texas")

        assert self.mock_scm.get.call_count == 2
        assert len(interfaces) == 3

    def test_list_with_exact_match(self):
        """Test listing with exact_match=True."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "folder": "Texas",
                    "tap": {},
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/2",
                    "folder": "All",
                    "tap": {},
                },
            ],
            "limit": 5000,
            "offset": 0,
            "total": 2,
        }

        self.mock_scm.get.return_value = mock_response
        interfaces = self.client.list(folder="Texas", exact_match=True)

        assert len(interfaces) == 1
        assert interfaces[0].folder == "Texas"

    def test_list_with_exclude_folders(self):
        """Test listing with exclude_folders."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "folder": "Texas",
                    "tap": {},
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/2",
                    "folder": "All",
                    "tap": {},
                },
            ],
            "limit": 5000,
            "offset": 0,
            "total": 2,
        }

        self.mock_scm.get.return_value = mock_response
        interfaces = self.client.list(device="TestDevice", exclude_folders=["All"])

        assert len(interfaces) == 1
        assert interfaces[0].folder == "Texas"

    def test_list_with_exclude_snippets(self):
        """Test listing with exclude_snippets."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "snippet": "TestSnippet",
                    "tap": {},
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/2",
                    "snippet": "ExcludeSnippet",
                    "tap": {},
                },
            ],
            "limit": 5000,
            "offset": 0,
            "total": 2,
        }

        self.mock_scm.get.return_value = mock_response
        interfaces = self.client.list(
            device="TestDevice", exclude_snippets=["ExcludeSnippet"]
        )

        assert len(interfaces) == 1
        assert interfaces[0].snippet == "TestSnippet"

    def test_list_with_exclude_devices(self):
        """Test listing with exclude_devices."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "device": "Device1",
                    "tap": {},
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/2",
                    "device": "Device2",
                    "tap": {},
                },
            ],
            "limit": 5000,
            "offset": 0,
            "total": 2,
        }

        self.mock_scm.get.return_value = mock_response
        interfaces = self.client.list(folder="Texas", exclude_devices=["Device2"])

        assert len(interfaces) == 1
        assert interfaces[0].device == "Device1"

    def test_list_invalid_response_format(self):
        """Test list with invalid response format."""
        self.mock_scm.get.return_value = "invalid"

        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.list(folder="Texas")
        assert "Response is not a dictionary" in str(exc_info.value)

    def test_list_missing_data_field(self):
        """Test list with missing 'data' field in response."""
        self.mock_scm.get.return_value = {"limit": 5000, "offset": 0}

        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.list(folder="Texas")
        assert "missing 'data' field" in str(exc_info.value)

    def test_list_data_not_list(self):
        """Test list with 'data' field that is not a list."""
        self.mock_scm.get.return_value = {"data": "not a list"}

        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.list(folder="Texas")
        assert "'data' field is not a list" in str(exc_info.value)


class TestEthernetInterfaceFetch(TestEthernetInterfaceBase):
    """Test Ethernet Interface fetch operations."""

    def test_fetch(self):
        """Test fetching an Ethernet Interface by name."""
        mock_response = {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "name": "ethernet1/1",
                    "folder": "Texas",
                    "tap": {},
                }
            ]
        }

        self.mock_scm.get.return_value = mock_response
        interface = self.client.fetch(name="ethernet1/1", folder="Texas")

        self.mock_scm.get.assert_called_once_with(
            "/config/network/v1/ethernet-interfaces",
            params={"folder": "Texas", "name": "ethernet1/1"},
        )
        assert isinstance(interface, EthernetInterfaceResponseModel)
        assert interface.name == "ethernet1/1"

    def test_fetch_empty_name(self):
        """Test fetch with empty name."""
        with pytest.raises(MissingQueryParameterError) as exc_info:
            self.client.fetch(name="", folder="Texas")
        assert "name" in str(exc_info.value)

    def test_fetch_empty_folder(self):
        """Test fetch with empty folder."""
        with pytest.raises(MissingQueryParameterError) as exc_info:
            self.client.fetch(name="ethernet1/1", folder="")
        assert "folder" in str(exc_info.value)

    def test_fetch_no_container(self):
        """Test fetch with no container."""
        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.fetch(name="ethernet1/1")
        assert "Invalid container parameters" in str(exc_info.value)

    def test_fetch_multiple_containers(self):
        """Test fetch with multiple containers."""
        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.fetch(name="ethernet1/1", folder="Texas", snippet="TestSnippet")
        assert "Invalid container parameters" in str(exc_info.value)

    def test_fetch_direct_response(self):
        """Test fetch with direct object response."""
        mock_response = {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "ethernet1/1",
            "folder": "Texas",
            "tap": {},
        }

        self.mock_scm.get.return_value = mock_response
        interface = self.client.fetch(name="ethernet1/1", folder="Texas")

        assert isinstance(interface, EthernetInterfaceResponseModel)
        assert interface.name == "ethernet1/1"

    def test_fetch_not_found(self):
        """Test fetch when object is not found."""
        self.mock_scm.get.return_value = {"data": []}

        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.fetch(name="nonexistent", folder="Texas")
        assert "not found" in str(exc_info.value)

    def test_fetch_invalid_response(self):
        """Test fetch with invalid response format."""
        self.mock_scm.get.return_value = "invalid"

        with pytest.raises(InvalidObjectError) as exc_info:
            self.client.fetch(name="ethernet1/1", folder="Texas")
        assert "Response is not a dictionary" in str(exc_info.value)


class TestEthernetInterfaceModelValidation(TestEthernetInterfaceBase):
    """Test Ethernet Interface model validation."""

    def test_mode_exclusivity_validation(self):
        """Test that only one interface mode can be specified."""
        from scm.models.network import Layer2, Layer3, Tap

        with pytest.raises(ValueError) as exc_info:
            EthernetInterfaceCreateModel(
                name="ethernet1/1",
                folder="Texas",
                tap=Tap(),
                layer2=Layer2(vlan_tag=100),
            )
        assert "Only one interface mode" in str(exc_info.value)

    def test_layer3_ip_method_exclusivity(self):
        """Test that only one Layer3 IP method can be specified."""
        from scm.models.network import DhcpClient, Layer3

        with pytest.raises(ValueError) as exc_info:
            Layer3(
                ip=["10.0.0.1/24"],
                dhcp_client=DhcpClient(enable=True),
            )
        assert "Only one IP configuration method" in str(exc_info.value)

    def test_layer3_requires_ip_method(self):
        """Test that Layer3 requires at least one IP method."""
        from scm.models.network import Layer3

        with pytest.raises(ValueError) as exc_info:
            Layer3(mtu=1500)
        assert "requires exactly one IP configuration method" in str(exc_info.value)

    def test_ddns_conditional_validation_enabled(self):
        """Test DDNS validation when enabled."""
        from scm.models.network import DdnsConfig

        with pytest.raises(ValueError) as exc_info:
            DdnsConfig(
                ddns_enabled=True,
                ddns_vendor="dyndns",
                # Missing required fields
            )
        assert "required" in str(exc_info.value).lower()

    def test_ddns_conditional_validation_disabled(self):
        """Test DDNS validation when disabled (no required fields)."""
        from scm.models.network import DdnsConfig

        # Should not raise when disabled, even without other fields
        config = DdnsConfig(ddns_enabled=False)
        assert config.ddns_enabled is False

    def test_container_exclusivity_validation(self):
        """Test that only one container can be specified."""
        from scm.models.network import Tap

        with pytest.raises(ValueError) as exc_info:
            EthernetInterfaceCreateModel(
                name="ethernet1/1",
                folder="Texas",
                snippet="TestSnippet",
                tap=Tap(),
            )
        assert "Exactly one of 'folder', 'snippet', or 'device'" in str(exc_info.value)

    def test_no_container_validation(self):
        """Test that at least one container must be specified."""
        from scm.models.network import Tap

        with pytest.raises(ValueError) as exc_info:
            EthernetInterfaceCreateModel(
                name="ethernet1/1",
                tap=Tap(),
            )
        assert "Exactly one of 'folder', 'snippet', or 'device'" in str(exc_info.value)

    def test_pppoe_requires_credentials(self):
        """Test that PPPoE requires username and password."""
        from scm.models.network import Pppoe
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Pppoe(enable=True)  # Missing username and password
