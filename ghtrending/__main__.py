import argparse
from ghtrending.ghtrending import GHClient

def main():
    args = ARGS.parse_args()
    GHClient(args.qtype, args.since, args.lang, args.json).request()

ARGS = argparse.ArgumentParser(description='Github Trending')
ARGS.add_argument('-q', '--qtype', dest='qtype', default=0, action='store', type=int,
                  help='Setting the query type, options: 0 for repository, 1 for developers. Default is repository.')
ARGS.add_argument('-s', '--since', dest='since', default='today', action='store', type=str,
                  help='Setting the since type, options: today/weekly/monthly. Default is today.')
ARGS.add_argument('-l', '--lang', dest='lang', action='store', type=str,
                  help='Specify the programming language. javascript, python, swift, etc. Default is wildcards.')
ARGS.add_argument('-j', '--json', dest='json',
                  action='store_true', help='Setting output to JSON format.')
ARGS.set_defaults(json=False)
if __name__ == '__main__':
    main()
