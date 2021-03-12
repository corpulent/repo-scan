import sys
import argparse

from reposcan.core import run


if __name__ == '__main__':
    argv = sys.argv[1:]
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-l', '--limit', help='Number of top trending repos', required=True, dest='limit')
    arg_parser.add_argument('-d', '--date-created', help='Date created, like 2021-01-01', required=True, dest='date_created')
    arg_parser.add_argument('-s', '--sast-scan', help='Include a SAST scan report.', required=False, dest='sast_scan')
    args = arg_parser.parse_args()
    limit = args.limit
    date_created = args.date_created
    sast_scan = bool(vars(args).get('sast_scan', False))
    ret = run(date_created, limit, sast_scan)

    for k, v in ret.items():
        print("\n")
        print(f"Scanned {v['name']} by {v['owner']} at {v['html_url']}")

        if v['scan']['req']['extras']:
            print(f"Found unused modules: {[r for r in v['scan']['req']['extras']]}")

        if v['scan']['req']['message']:
            print(v['scan']['req']['message'])

        print(f"Score {v['score']}")
