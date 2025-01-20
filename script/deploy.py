from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network
from src import buy_me_a_coffee
from script.deploy_mocks import deploy_feed


def deploy_coffee(price_feed:VyperContract)->VyperContract:
    coffee_contract:VyperContract=buy_me_a_coffee.deploy(price_feed)


    active_network = get_active_network()
    if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
        result = active_network.moccasin_verify(coffee_contract)
        result.wait_for_verification()
    return coffee_contract

def moccasin_main() ->VyperContract:
    active_network = get_active_network()
    price_feed:VyperContract = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name}, using  rice feed at {price_feed.address}")
    return deploy_coffee(price_feed)
  
