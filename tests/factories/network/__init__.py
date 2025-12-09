"""Network factories for testing."""

from tests.factories.network.ethernet_interface import (
    EthernetInterfaceCreateApiFactory,
)
from tests.factories.network.nat_rules import (
    InterfaceAddressFactory,
    NatRuleCreateApiFactory,
    NatRuleCreateModelFactory,
    NatRuleMoveApiFactory,
    NatRuleMoveModelFactory,
    NatRuleResponseFactory,
    NatRuleUpdateApiFactory,
    NatRuleUpdateModelFactory,
    SourceTranslationFactory,
)

# Explicitly export these factories
__all__ = [
    "EthernetInterfaceCreateApiFactory",
    "InterfaceAddressFactory",
    "NatRuleCreateApiFactory",
    "NatRuleCreateModelFactory",
    "NatRuleMoveApiFactory",
    "NatRuleMoveModelFactory",
    "NatRuleResponseFactory",
    "NatRuleUpdateApiFactory",
    "NatRuleUpdateModelFactory",
    "SourceTranslationFactory",
]
