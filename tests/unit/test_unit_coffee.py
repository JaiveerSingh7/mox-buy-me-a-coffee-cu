from eth_utils import to_wei
import boa
from conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non-owner")
random_user_array = []

for i in range(10):
    random_user_array.append(boa.env.generate_address("non-owner"))

def test_price_feed_is_correct(coffee,eth_usd):
    assert coffee.PRICE_FEED()== eth_usd.address

def test_starting_values(coffee,account):
    coffee.MINIMUM_USD()==to_wei(5,"ether")
    coffee.OWNER()==account.address


def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts():
        coffee.fund()

def test_fund_with_money(coffee,account):
    # arrange
    boa.env.set_balance(account.address,SEND_VALUE*10)
    # act
    coffee.fund(value=SEND_VALUE)
    # assert
    funder=coffee.funders(0)
    assert funder==account.address
    assert coffee.funder_to_amount_funded(funder)==SEND_VALUE


def test_non_owner_cannot_withdraw(coffee_funded,account):

    with boa.env.prank(RANDOM_USER):
        with boa.reverts():
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) ==0



# Workshop(gives a fail when working with zksync)
def test_ten_funders_withdraw_balance(coffee):
    total_funded=0
    # funds the contract with ten different funders
    for i in range(10):
        boa.env.set_balance(random_user_array[i],SEND_VALUE*10)
        with boa.env.prank(random_user_array[i]):
            coffee.fund(value=SEND_VALUE)
            total_funded += coffee.funder_to_amount_funded(coffee.funders(i))
    # withdraws the funds using the owner
    with boa.env.prank(coffee.OWNER()):
        starting_owner_balance=boa.env.get_balance(coffee.OWNER())
        coffee.withdraw()
    # checks ending balance of the owner
    assert boa.env.get_balance(coffee.OWNER()) == total_funded+starting_owner_balance
    
def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE)>0

def test_default(coffee):

    coffee.__default__(value = SEND_VALUE)
    assert boa.env.get_balance(coffee.address)==SEND_VALUE