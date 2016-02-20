import argparse

from server import app


def parse_args():
    parser = argparse.ArgumentParser(description='Command line arguments.')
    parser.add_argument("-p", type=int, dest="port",
                        help="port", default=9000)
    return parser.parse_args()


def main():
    arg_obj = parse_args()
    app.run("0.0.0.0", port=arg_obj.port, debug=True)


if __name__ == '__main__':
    main()
