# crypto_tracker/__main__.py
import argparse

from .utils import validate_arguments
from .triggers import TRIGGERS
from .logger import Logger


logger = Logger()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crypto Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Add subparsers for each trigger
    for command, trigger in TRIGGERS.items():
        subparser = subparsers.add_parser(command, help=trigger["help"])
        for arg, arg_opts in trigger.get("args", {}).items():
            subparser.add_argument(arg, **arg_opts)

    args = parser.parse_args()

    if args.command in TRIGGERS:
        trigger = TRIGGERS[args.command]
        func = trigger["function"]

        # Validate required arguments
        required_args = [arg.strip("--") for arg in trigger.get("args", {}).keys()]
        validate_arguments(vars(args), required_args)

        # Filter arguments for the function
        func_args = {
            key: value
            for key, value in vars(args).items()
            if key in func.__code__.co_varnames
        }

        try:
            func(**func_args)
        except Exception as e:
            logger.error(f"Error running {args.command}: {e}")
    else:
        logger.error(f"Unknown command: {args.command}")
