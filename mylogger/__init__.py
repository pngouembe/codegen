import logging

try:
    from rich.logging import RichHandler
    FORMAT = "%(message)s"
    logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

except ImportError:
    FORMAT = "%(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]")

log = logging.getLogger("codgen")