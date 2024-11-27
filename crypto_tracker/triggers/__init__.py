from .update_trades import update_trades
from .calculate_pnl import calculate_pnl
from .update_current_prices import update_current_prices
from .add_wallet import add_wallet
from .mac_numbers_price_sync import mac_numbers_price_sync
from .start_server import start_server

TRIGGERS = {
    "update_trades": {
        "function": update_trades,
        "help": "Update trades for trading pairs",
    },
    "calculate_pnl": {
        "function": calculate_pnl,
        "help": "Calculate Profit and Loss (PnL)",
    },
    "update_current_prices": {
        "function": update_current_prices,
        "help": "Update current prices for supported pairs",
    },
    "mac_numbers_price_sync": {
        "function": mac_numbers_price_sync,
        "help": "Updates altcoins and memecoins sheet in Numbers"
    },
    "add_wallet": {
        "function": add_wallet,
        "help": "Add a new wallet",
        "args": {
            "--address": {"required": True, "help": "Wallet address"},
            "--chain_id": {"required": True, "help": "Blockchain chain ID"},
            "--name": {"required": True, "help": "The name of the address"},
        },
    },
    "start_server": {
        "function": start_server,
        "help": "Start the FastAPI server",
        "args": {
            "--host": {"default": "127.0.0.1", "help": "Server host"},
            "--port": {"default": 8000, "type": int, "help": "Server port"},
            "--reload": {"action": "store_true", "help": "Enable hot-reload for development"},
        },
    },
}
