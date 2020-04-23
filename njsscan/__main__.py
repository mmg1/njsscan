#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""The nodejsscan cli: njsscan."""
import argparse
import json
import sys

from njsscan import __version__
from njsscan.njsscan import NJSScan
from njsscan.logger import init_logger


logger = init_logger(__name__)


def cli_out(rule_id, details):
    """Get CLI friendly format."""
    items = []
    items.append(f'\nRULE ID: {rule_id}')
    for meta, value in details['metadata'].items():
        if meta == 'id':
            continue
        meta_format = meta.upper().replace('_', '')
        items.append(f'{meta_format}: {value}')
    items.append('\n__________________FILES___________________________')
    for match in details['files']:
        items.append('\n')
        file_path = match['file_path']
        items.append(f'File: {file_path}')
        position = match['match_position']
        items.append(f'Match Position: {position[0]} - {position[1]}')
        lines = match.get('match_lines')
        if lines:
            line = (lines[0] if lines[0] == lines[1]
                    else f'{lines[0]}: {lines[1]}')
            items.append(f'Line Number(s): {line}')
        match_string = match['match_string']
        if isinstance(match_string, list):
            match_string = '\n'.join(ln.strip() for ln in match_string)
        items.append(f'Match String: {match_string}')
    items.append('___________________________________________________')
    return '\n'.join(items)


def format_output(output):
    """Format output printing."""
    if not output:
        return
    if output.get('errors'):
        logger.critical(output.get('errors'))
    output.pop('errors', None)
    for out in output:
        for rule_id, details in output[out].items():
            formatted = cli_out(rule_id, details)
            if details['metadata']['severity'].lower() == 'error':
                logger.error(formatted)
            elif details['metadata']['severity'].lower() == 'warning':
                logger.warning(formatted)
            else:
                logger.info(formatted)


def handle_output(out, scan_results):
    """Output."""
    if out:
        with open(out, 'w') as outfile:
            json.dump(scan_results, outfile, sort_keys=True,
                      indent=2, separators=(',', ': '))
    else:
        print((json.dumps(scan_results, sort_keys=True,
                          indent=2, separators=(',', ': '))))


def handle_exit(results):
    """Handle Exit."""
    if results.get('nodejs') or results.get('templates'):
        sys.exit(1)
    sys.exit(0)


def main():
    """Main CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        nargs='*',
                        help=('Path can be file(s) or '
                              'directories with Node.js source code'))
    parser.add_argument('--json',
                        help='Print JSON output',
                        action='store_true')
    parser.add_argument('-o', '--output',
                        help='Output filename to save JSON report.',
                        required=False)
    parser.add_argument('-v', '--version',
                        help='Show njsscan version',
                        required=False,
                        action='store_true')
    args = parser.parse_args()
    if args.path:
        scan_results = NJSScan(args).scan()
        if args.json or args.output:
            handle_output(args.output, scan_results)
        else:
            format_output(scan_results)
        handle_exit(scan_results)
    elif args.version:
        print('njsscan: v' + __version__)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
