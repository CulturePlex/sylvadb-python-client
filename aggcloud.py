import argparse

from gooey import Gooey
from sylvadbpythonclient.apiclient import SylvadbApiClient


@Gooey(dump_build_config=True)
def main():
    parser = argparse.ArgumentParser(
        description='SylvaDB API client for AggCloud.')
    parser.add_argument('host',
                        help='Server for the SylvaDB API')
    parser.add_argument('user',
                        help='User name')
    parser.add_argument('password',
                        help='Password')

    args = parser.parse_args()

    host = args.host
    auth = (args.user, args.password)

    api = SylvadbApiClient()
    api.api_connect(host, auth)

    # Dummy example getting the graphs from the user
    print api.get_graphs()


if __name__ == '__main__':
    main()
