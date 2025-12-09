"""Factory for creating Ethernet Interface test objects."""

import factory

from scm.models.network.ethernet_interface import (
    ArpEntry,
    DdnsConfig,
    DhcpClient,
    EthernetInterfaceCreateModel,
    Layer2,
    Layer3,
    LinkDuplex,
    LinkSpeed,
    LinkState,
    PoE,
    Pppoe,
    SendHostname,
    StaticAddress,
    Tap,
)


class EthernetInterfaceCreateApiFactory(factory.Factory):
    """Factory for creating EthernetInterfaceCreateModel instances for testing."""

    class Meta:
        """Factory configuration."""

        model = EthernetInterfaceCreateModel

    # Required fields
    name = factory.Sequence(lambda n: f"ethernet1/{n}")

    # Default container
    folder = "Texas"

    # Optional fields with defaults
    comment = factory.Faker("sentence")
    link_speed = LinkSpeed.AUTO
    link_duplex = LinkDuplex.AUTO
    link_state = LinkState.AUTO

    @classmethod
    def with_tap(cls, **kwargs):
        """Create an Ethernet Interface with tap mode.

        Args:
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface configured in tap mode
        """
        return cls(
            tap=Tap(),
            layer2=None,
            layer3=None,
            **kwargs,
        )

    @classmethod
    def with_layer2(cls, vlan_tag: int = 100, **kwargs):
        """Create an Ethernet Interface with layer2 mode.

        Args:
            vlan_tag: VLAN tag assignment (1-9999)
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface configured in layer2 mode
        """
        return cls(
            tap=None,
            layer2=Layer2(vlan_tag=vlan_tag),
            layer3=None,
            **kwargs,
        )

    @classmethod
    def with_layer3_static(cls, ips: list = None, **kwargs):
        """Create an Ethernet Interface with layer3 static IP configuration.

        Args:
            ips: List of static IP addresses
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with layer3 static IP
        """
        if ips is None:
            ips = ["10.0.0.1/24"]

        return cls(
            tap=None,
            layer2=None,
            layer3=Layer3(ip=ips),
            **kwargs,
        )

    @classmethod
    def with_layer3_dhcp(cls, **kwargs):
        """Create an Ethernet Interface with layer3 DHCP configuration.

        Args:
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with layer3 DHCP
        """
        dhcp_client = DhcpClient(
            enable=True,
            create_default_route=True,
            send_hostname=SendHostname(
                enable=True,
                hostname="test-host",
            ),
            default_route_metric=10,
        )

        return cls(
            tap=None,
            layer2=None,
            layer3=Layer3(dhcp_client=dhcp_client),
            **kwargs,
        )

    @classmethod
    def with_layer3_pppoe(
        cls,
        username: str = "testuser",
        password: str = "testpass",
        **kwargs,
    ):
        """Create an Ethernet Interface with layer3 PPPoE configuration.

        Args:
            username: PPPoE username
            password: PPPoE password
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with layer3 PPPoE
        """
        pppoe = Pppoe(
            enable=True,
            username=username,
            password=password,
            authentication="auto",
            default_route_metric=10,
        )

        return cls(
            tap=None,
            layer2=None,
            layer3=Layer3(pppoe=pppoe),
            **kwargs,
        )

    @classmethod
    def with_poe(cls, enabled: bool = True, reserved_power: int = 30, **kwargs):
        """Add PoE configuration to an interface.

        Args:
            enabled: Enable PoE
            reserved_power: Reserved power in watts (0-90)
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with PoE configuration
        """
        poe_config = PoE(
            poe_enabled=enabled,
            poe_rsvd_pwr=reserved_power,
        )

        # Default to layer3 static if no mode specified
        if "tap" not in kwargs and "layer2" not in kwargs and "layer3" not in kwargs:
            kwargs["layer3"] = Layer3(ip=["10.0.0.1/24"])
            kwargs["tap"] = None
            kwargs["layer2"] = None

        return cls(
            poe=poe_config,
            **kwargs,
        )

    @classmethod
    def with_ddns(
        cls,
        hostname: str = "test.example.com",
        cert_profile: str = "cert-profile-1",
        **kwargs,
    ):
        """Add DDNS configuration to a layer3 interface.

        Args:
            hostname: DDNS hostname
            cert_profile: Certificate profile name
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with DDNS configuration
        """
        ddns_config = DdnsConfig(
            ddns_enabled=True,
            ddns_vendor="dyndns",
            ddns_update_interval=1,
            ddns_cert_profile=cert_profile,
            ddns_hostname=hostname,
            ddns_vendor_config="vendor-config",
        )

        # DDNS is only valid for layer3
        if "layer3" not in kwargs:
            kwargs["layer3"] = Layer3(
                ip=["10.0.0.1/24"],
                ddns_config=ddns_config,
            )
        else:
            # Add ddns_config to existing layer3
            if isinstance(kwargs["layer3"], Layer3):
                kwargs["layer3"].ddns_config = ddns_config

        kwargs["tap"] = None
        kwargs["layer2"] = None

        return cls(**kwargs)

    @classmethod
    def with_arp(cls, entries: list = None, **kwargs):
        """Add ARP entries to a layer3 interface.

        Args:
            entries: List of dicts with 'name' (IP) and 'hw_address' (MAC)
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface with ARP entries
        """
        if entries is None:
            entries = [
                {"name": "10.0.0.10", "hw_address": "00:11:22:33:44:55"},
            ]

        arp_entries = [ArpEntry(**entry) for entry in entries]

        # ARP is only valid for layer3
        if "layer3" not in kwargs:
            kwargs["layer3"] = Layer3(
                ip=["10.0.0.1/24"],
                arp=arp_entries,
            )
        else:
            # Add arp to existing layer3
            if isinstance(kwargs["layer3"], Layer3):
                kwargs["layer3"].arp = arp_entries

        kwargs["tap"] = None
        kwargs["layer2"] = None

        return cls(**kwargs)

    @classmethod
    def with_snippet(cls, snippet: str = "TestSnippet", **kwargs):
        """Create an interface in a snippet container.

        Args:
            snippet: Snippet name
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface in snippet container
        """
        # Default to tap mode if no mode specified
        if "tap" not in kwargs and "layer2" not in kwargs and "layer3" not in kwargs:
            kwargs["tap"] = Tap()
            kwargs["layer2"] = None
            kwargs["layer3"] = None

        return cls(
            folder=None,
            snippet=snippet,
            device=None,
            **kwargs,
        )

    @classmethod
    def with_device(cls, device: str = "TestDevice", **kwargs):
        """Create an interface in a device container.

        Args:
            device: Device name
            **kwargs: Additional fields to override

        Returns:
            EthernetInterfaceCreateModel: Interface in device container
        """
        # Default to tap mode if no mode specified
        if "tap" not in kwargs and "layer2" not in kwargs and "layer3" not in kwargs:
            kwargs["tap"] = Tap()
            kwargs["layer2"] = None
            kwargs["layer3"] = None

        return cls(
            folder=None,
            snippet=None,
            device=device,
            **kwargs,
        )
