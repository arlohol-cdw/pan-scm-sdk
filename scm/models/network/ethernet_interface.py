"""Ethernet Interface models for Strata Cloud Manager SDK.

Contains Pydantic models for representing Ethernet Interface objects and related data.
"""

# scm/models/network/ethernet_interface.py

from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LinkSpeed(str, Enum):
    """Link speed options for Ethernet interfaces."""

    AUTO = "auto"
    TEN = "10"
    HUNDRED = "100"
    THOUSAND = "1000"
    TEN_THOUSAND = "10000"
    FORTY_THOUSAND = "40000"
    HUNDRED_THOUSAND = "100000"


class LinkDuplex(str, Enum):
    """Link duplex options for Ethernet interfaces."""

    AUTO = "auto"
    HALF = "half"
    FULL = "full"


class LinkState(str, Enum):
    """Link state options for Ethernet interfaces."""

    AUTO = "auto"
    UP = "up"
    DOWN = "down"


class PppoeAuthentication(str, Enum):
    """PPPoE authentication protocol options."""

    CHAP = "CHAP"
    PAP = "PAP"
    AUTO = "auto"


class PoE(BaseModel):
    """Power over Ethernet configuration.

    Attributes:
        poe_enabled (Optional[bool]): Enable PoE on interface.
        poe_rsvd_pwr (Optional[int]): PoE reserved power (0-90 watts).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    poe_enabled: Optional[bool] = Field(
        None,
        alias="poe-enabled",
        description="Enable PoE on interface",
    )
    poe_rsvd_pwr: Optional[int] = Field(
        None,
        alias="poe-rsvd-pwr",
        ge=0,
        le=90,
        description="PoE reserved power in watts",
    )


class SendHostname(BaseModel):
    """DHCP send hostname configuration.

    Attributes:
        enable (Optional[bool]): Enable sending hostname to DHCP server.
        hostname (Optional[str]): Hostname to send (default: system hostname).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    enable: Optional[bool] = Field(
        None,
        description="Enable sending hostname to DHCP server",
    )
    hostname: Optional[str] = Field(
        None,
        min_length=1,
        max_length=64,
        pattern=r"^[a-zA-Z0-9\._-]+$",
        description="Hostname to send to DHCP server",
    )


class DhcpClient(BaseModel):
    """DHCP client configuration for Layer 3 interfaces.

    Attributes:
        enable (Optional[bool]): Enable DHCP client.
        create_default_route (Optional[bool]): Auto-create default route from DHCP.
        send_hostname (Optional[SendHostname]): Send hostname configuration.
        default_route_metric (Optional[int]): Metric for default route (1-65535).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    enable: Optional[bool] = Field(
        None,
        description="Enable DHCP client",
    )
    create_default_route: Optional[bool] = Field(
        None,
        alias="create-default-route",
        description="Automatically create default route from DHCP gateway",
    )
    send_hostname: Optional[SendHostname] = Field(
        None,
        alias="send-hostname",
        description="Send hostname configuration",
    )
    default_route_metric: Optional[int] = Field(
        None,
        alias="default-route-metric",
        ge=1,
        le=65535,
        description="Metric for default route created",
    )


class StaticAddress(BaseModel):
    """Static IP address configuration for PPPoE.

    Attributes:
        ip (str): Static IP address.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    ip: str = Field(
        ...,
        max_length=63,
        description="Static IP address",
    )


class Pppoe(BaseModel):
    """PPPoE configuration for Layer 3 interfaces.

    Attributes:
        enable (Optional[bool]): Enable PPPoE.
        username (str): PPPoE username.
        password (str): PPPoE password.
        authentication (Optional[PppoeAuthentication]): Authentication protocol.
        static_address (Optional[StaticAddress]): Static address configuration.
        default_route_metric (Optional[int]): Metric for default route (1-65535).
        access_concentrator (Optional[str]): Access concentrator name.
        service (Optional[str]): Service name.
        passive (Optional[bool]): Enable passive mode.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    enable: Optional[bool] = Field(
        None,
        description="Enable PPPoE",
    )
    username: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="PPPoE username",
    )
    password: str = Field(
        ...,
        max_length=255,
        description="PPPoE password",
        json_schema_extra={"format": "password"},
    )
    authentication: Optional[PppoeAuthentication] = Field(
        None,
        description="Authentication protocol",
    )
    static_address: Optional[StaticAddress] = Field(
        None,
        alias="static-address",
        description="Static IP address configuration",
    )
    default_route_metric: Optional[int] = Field(
        None,
        alias="default-route-metric",
        ge=1,
        le=65535,
        description="Metric for default route created",
    )
    access_concentrator: Optional[str] = Field(
        None,
        alias="access-concentrator",
        min_length=1,
        max_length=255,
        description="Access concentrator name",
    )
    service: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Service name",
    )
    passive: Optional[bool] = Field(
        None,
        description="Enable passive mode",
    )


class ArpEntry(BaseModel):
    """ARP table entry.

    Attributes:
        name (Optional[str]): IP address for ARP entry.
        hw_address (Optional[str]): MAC address for ARP entry.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    name: Optional[str] = Field(
        None,
        description="IP address for ARP entry",
    )
    hw_address: Optional[str] = Field(
        None,
        alias="hw-address",
        description="MAC address for ARP entry",
    )


class DdnsConfig(BaseModel):
    """Dynamic DNS configuration.

    Attributes:
        ddns_enabled (Optional[bool]): Enable DDNS.
        ddns_vendor (Optional[str]): DDNS vendor name.
        ddns_update_interval (Optional[int]): Update interval in days (1-30).
        ddns_cert_profile (Optional[str]): Certificate profile for DDNS.
        ddns_hostname (Optional[str]): Hostname to register with DDNS.
        ddns_ip (Optional[str]): IP address to register (static only).
        ddns_vendor_config (Optional[str]): DDNS vendor configuration.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    ddns_enabled: Optional[bool] = Field(
        None,
        alias="ddns-enabled",
        description="Enable Dynamic DNS",
    )
    ddns_vendor: Optional[str] = Field(
        None,
        alias="ddns-vendor",
        max_length=127,
        description="DDNS vendor name",
    )
    ddns_update_interval: Optional[int] = Field(
        None,
        alias="ddns-update-interval",
        ge=1,
        le=30,
        description="Update interval in days",
    )
    ddns_cert_profile: Optional[str] = Field(
        None,
        alias="ddns-cert-profile",
        description="Certificate profile for DDNS",
    )
    ddns_hostname: Optional[str] = Field(
        None,
        alias="ddns-hostname",
        pattern=r"^[a-zA-Z0-9_\.\-]+$",
        max_length=255,
        description="Hostname to register with DDNS",
    )
    ddns_ip: Optional[str] = Field(
        None,
        alias="ddns-ip",
        description="IP address to register (static only)",
    )
    ddns_vendor_config: Optional[str] = Field(
        None,
        alias="ddns-vendor-config",
        max_length=255,
        description="DDNS vendor configuration",
    )

    @model_validator(mode="after")
    def validate_ddns_required_fields(self) -> "DdnsConfig":
        """Validate that required DDNS fields are present when DDNS is enabled.

        When ddns_enabled is True, the following fields must be provided:
        - ddns_vendor
        - ddns_cert_profile
        - ddns_hostname
        - ddns_vendor_config

        Returns:
            DdnsConfig: Validated model instance.

        Raises:
            ValueError: If DDNS is enabled but required fields are missing.
        """
        if self.ddns_enabled is True:
            required_fields = {
                "ddns_vendor": self.ddns_vendor,
                "ddns_cert_profile": self.ddns_cert_profile,
                "ddns_hostname": self.ddns_hostname,
                "ddns_vendor_config": self.ddns_vendor_config,
            }
            missing = [field for field, value in required_fields.items() if not value]
            if missing:
                raise ValueError(
                    f"When DDNS is enabled, the following fields are required: "
                    f"{', '.join(missing)}"
                )
        return self


class Tap(BaseModel):
    """Tap mode configuration (empty object).

    Attributes:
        None - Tap mode requires no additional configuration.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )


class Layer2(BaseModel):
    """Layer 2 interface configuration.

    Attributes:
        vlan_tag (Optional[int]): VLAN tag assignment (1-9999).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    vlan_tag: Optional[int] = Field(
        None,
        alias="vlan-tag",
        ge=1,
        le=9999,
        description="VLAN tag assignment",
    )


class Layer3(BaseModel):
    """Layer 3 interface configuration.

    Exactly one IP configuration method must be specified: ip (static), dhcp_client, or pppoe.
    Common Layer 3 fields can be specified regardless of IP method.

    Attributes:
        ip (Optional[List[str]]): Static IP addresses.
        dhcp_client (Optional[DhcpClient]): DHCP client configuration.
        pppoe (Optional[Pppoe]): PPPoE configuration.
        interface_management_profile (Optional[str]): Interface management profile name.
        mtu (Optional[int]): Maximum transmission unit (576-9216).
        arp (Optional[List[ArpEntry]]): ARP table entries.
        ddns_config (Optional[DdnsConfig]): Dynamic DNS configuration.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    # IP configuration methods (mutually exclusive)
    ip: Optional[List[str]] = Field(
        None,
        description="Static IP addresses",
    )
    dhcp_client: Optional[DhcpClient] = Field(
        None,
        alias="dhcp-client",
        description="DHCP client configuration",
    )
    pppoe: Optional[Pppoe] = Field(
        None,
        description="PPPoE configuration",
    )

    # Common Layer 3 fields
    interface_management_profile: Optional[str] = Field(
        None,
        alias="interface-management-profile",
        max_length=31,
        description="Interface management profile name",
    )
    mtu: Optional[int] = Field(
        None,
        ge=576,
        le=9216,
        description="Maximum transmission unit",
    )
    arp: Optional[List[ArpEntry]] = Field(
        None,
        description="ARP table entries",
    )
    ddns_config: Optional[DdnsConfig] = Field(
        None,
        alias="ddns-config",
        description="Dynamic DNS configuration",
    )

    @model_validator(mode="after")
    def validate_ip_method(self) -> "Layer3":
        """Validate that exactly one IP configuration method is specified.

        Ensures mutual exclusivity of ip (static), dhcp_client, and pppoe.

        Returns:
            Layer3: Validated model instance.

        Raises:
            ValueError: If zero or multiple IP methods are specified.
        """
        ip_methods = {
            "ip (static)": self.ip,
            "dhcp_client": self.dhcp_client,
            "pppoe": self.pppoe,
        }
        specified = [method for method, value in ip_methods.items() if value is not None]

        if len(specified) == 0:
            raise ValueError(
                "Layer 3 interface requires exactly one IP configuration method: "
                "ip (static), dhcp_client, or pppoe"
            )
        if len(specified) > 1:
            raise ValueError(
                f"Only one IP configuration method can be specified. "
                f"Found: {', '.join(specified)}"
            )
        return self


class EthernetInterfaceBaseModel(BaseModel):
    """Base model for Ethernet Interface objects.

    Contains fields common to all CRUD operations for Ethernet interfaces.

    Attributes:
        name (str): Interface name.
        default_value (Optional[str]): Default interface assignment.
        comment (Optional[str]): Interface description (0-1023 characters).
        link_speed (Optional[LinkSpeed]): Link speed setting.
        link_duplex (Optional[LinkDuplex]): Link duplex setting.
        link_state (Optional[LinkState]): Link state setting.
        poe (Optional[PoE]): Power over Ethernet configuration.
        tap (Optional[Tap]): Tap mode configuration.
        layer2 (Optional[Layer2]): Layer 2 configuration.
        layer3 (Optional[Layer3]): Layer 3 configuration.
        folder (Optional[str]): Folder location (max 64 chars).
        snippet (Optional[str]): Snippet location (max 64 chars).
        device (Optional[str]): Device location (max 64 chars).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    # Required fields
    name: str = Field(
        ...,
        description="Interface name",
    )

    # Optional basic fields
    default_value: Optional[str] = Field(
        None,
        alias="default-value",
        description="Default interface assignment",
    )
    comment: Optional[str] = Field(
        None,
        min_length=0,
        max_length=1023,
        description="Interface description",
    )
    link_speed: Optional[LinkSpeed] = Field(
        None,
        alias="link-speed",
        description="Link speed setting",
    )
    link_duplex: Optional[LinkDuplex] = Field(
        None,
        alias="link-duplex",
        description="Link duplex setting",
    )
    link_state: Optional[LinkState] = Field(
        None,
        alias="link-state",
        description="Link state setting",
    )
    poe: Optional[PoE] = Field(
        None,
        description="Power over Ethernet configuration",
    )

    # Interface mode (mutually exclusive)
    tap: Optional[Tap] = Field(
        None,
        description="Tap mode configuration",
    )
    layer2: Optional[Layer2] = Field(
        None,
        description="Layer 2 configuration",
    )
    layer3: Optional[Layer3] = Field(
        None,
        description="Layer 3 configuration",
    )

    # Container fields (mutually exclusive)
    folder: Optional[str] = Field(
        None,
        pattern=r"^[a-zA-Z\d\-_. ]+$",
        max_length=64,
        description="Folder location",
    )
    snippet: Optional[str] = Field(
        None,
        pattern=r"^[a-zA-Z\d\-_. ]+$",
        max_length=64,
        description="Snippet location",
    )
    device: Optional[str] = Field(
        None,
        pattern=r"^[a-zA-Z\d\-_. ]+$",
        max_length=64,
        description="Device location",
    )

    @model_validator(mode="after")
    def validate_interface_mode(self) -> "EthernetInterfaceBaseModel":
        """Validate that exactly one interface mode is specified.

        Ensures mutual exclusivity of tap, layer2, and layer3.

        Returns:
            EthernetInterfaceBaseModel: Validated model instance.

        Raises:
            ValueError: If zero or multiple interface modes are specified.
        """
        modes = {
            "tap": self.tap,
            "layer2": self.layer2,
            "layer3": self.layer3,
        }
        specified = [mode for mode, value in modes.items() if value is not None]

        if len(specified) == 0:
            raise ValueError(
                "Exactly one interface mode must be specified: tap, layer2, or layer3"
            )
        if len(specified) > 1:
            raise ValueError(
                f"Only one interface mode can be specified. Found: {', '.join(specified)}"
            )
        return self


class EthernetInterfaceCreateModel(EthernetInterfaceBaseModel):
    """Model for creating a new Ethernet Interface.

    Inherits all fields from EthernetInterfaceBaseModel and adds container validation.
    """

    @model_validator(mode="after")
    def validate_container_type(self) -> "EthernetInterfaceCreateModel":
        """Validate that exactly one container type is specified.

        Ensures mutual exclusivity of folder, snippet, and device.

        Returns:
            EthernetInterfaceCreateModel: Validated model instance.

        Raises:
            ValueError: If zero or multiple containers are specified.
        """
        container_fields = ["folder", "snippet", "device"]
        provided = [
            field for field in container_fields if getattr(self, field) is not None
        ]

        if len(provided) != 1:
            raise ValueError(
                "Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )
        return self


class EthernetInterfaceUpdateModel(EthernetInterfaceBaseModel):
    """Model for updating an existing Ethernet Interface.

    Includes the id field required for updates.

    Attributes:
        id (UUID): UUID of the Ethernet Interface.
    """

    id: UUID = Field(
        ...,
        description="UUID of the Ethernet Interface",
        examples=["123e4567-e89b-12d3-a456-426655440000"],
    )


class EthernetInterfaceResponseModel(EthernetInterfaceBaseModel):
    """Model for Ethernet Interface API responses.

    Includes the id field returned by the API.

    Attributes:
        id (UUID): UUID of the Ethernet Interface.
    """

    id: UUID = Field(
        ...,
        description="UUID of the Ethernet Interface",
        examples=["123e4567-e89b-12d3-a456-426655440000"],
    )

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="allow",  # Allow extra fields from API responses
    )
