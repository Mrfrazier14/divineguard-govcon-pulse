import argparse
import json
import os
from .store import Store, STAGES

def main():
    parser = argparse.ArgumentParser(description='GovCon Pulse local tracker')
    parser.add_argument('--db', default=os.getenv('PULSE_DB', 'data/pulse.db'))
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add')
    add.add_argument('title')
    add.add_argument('source_url')
    commands.add_parser('list')
    stage = commands.add_parser('stage')
    stage.add_argument('id')
    stage.add_argument('stage', choices=STAGES)
    stage.add_argument('--evidence')
    args = parser.parse_args()
    store = Store(args.db)
    try:
        if args.command == 'add':
            print(store.add(args.title, args.source_url))
        elif args.command == 'stage':
            store.update_stage(args.id, args.stage, args.evidence)
        else:
            print(json.dumps(store.list(), indent=2))
    except (ValueError, KeyError) as exc:
        parser.exit(2, f'Invalid operation: {exc}\n')
    finally:
        store.close()

if __name__ == '__main__':
    main()
