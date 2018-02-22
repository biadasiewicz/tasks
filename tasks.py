import sys
from tasks.cli import CLI


if __name__ == "__main__":
    cli = CLI()
    cli.execute(sys.argv)
