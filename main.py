from web3 import Web3
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import requests


def generate_address(mnemonics=[]) -> list:
    accounts = []
    for mnemonic in mnemonics:
        seed = Bip39SeedGenerator(mnemonic).Generate()
        bip44_mst = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0)
        bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)
        address = bip44_change.AddressIndex(0).PublicKey().ToAddress()
        privateKey = bip44_change.AddressIndex(0).PrivateKey().ToExtended()
        accounts.append({
            "address": address,
            "privateKey": privateKey,
            "mnemonic": mnemonic
        })

    return accounts


def connect_rpc(address):
    w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com/"))
    if w3.is_connected:
        balance = w3.eth.get_balance(address)
        print(f"我的余额:{balance}")
        return w3
    else:
        return None


def send_balance(w3: Web3, receiver_address: str, privateKey: str):
    tx = {
        # 'nonce': 1,
        'to': receiver_address,
        'value': w3.to_wei(0.01, 'ether'),  # 转账金额，单位为以太币
        'gas': 2000000,  # Gas 限制
        'gasPrice': w3.to_wei(50, 'gwei'),  # Gas 价格
    }
    signed_tx = w3.eth.account.sign_transaction(tx, privateKey)

    # 发送交易
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash)


def get_coin_price(symbol):
    symbol += "USDT"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    url = f"https://api1.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("请求失败")







if __name__ == "__main__":
    pass
