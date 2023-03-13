import argparse
import logging
from pathlib import Path
from typing import Optional

import exiftool
from colorama import Fore, Style
from prettytable import PrettyTable

import mapping_functions


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='exif_rename',
        description='Rename media files by appending exif metadata to them.')

    parser.add_argument(
        '-t', '--tag', metavar='TAG', type=str,
        help='exif tag to add to filename')

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-p', '--prepend', action='store_true',
        help='prepend tag')

    group.add_argument(
        '-r', '--replace', action='store_true',
        help='replace current name with tag')

    mapping_functions_list = ", ".join(list(mapping_functions._function_dict.keys()))

    parser.add_argument(
        '-m', '--mapping', metavar='MAPPING', nargs='+', action='append', default=[],
        help=f'apply a mapping function to transform the tag string: {mapping_functions_list}')

    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help='do not rename files')

    parser.add_argument(
        dest='files', metavar='FILES', nargs='+', type=Path,
        help='files to rename')

    return parser.parse_args()


def get_tags(file_list: list[Path], exif_tag: str) -> list:
    with exiftool.ExifToolHelper() as et:
        return et.get_tags(file_list, exif_tag)


def get_tag_value(data: dict) -> Optional[str]:
    if len(data.values()) != 2:
        return None
    return data.popitem()[1]


def apply_mappings(string: str, mappings: list[list[str]]) -> str:
    for mapping in mappings:
        function_name = mapping[0]
        function_args = mapping[1:]
        string = mapping_functions.apply_function(
            function_name, string, *function_args)
    return string


def apply_template(stem: str, tag_value: str, args: argparse.Namespace) -> str:
    tmpl = '{tag_value}{stem}' if args.prepend \
        else '{tag_value}' if args.replace \
        else '{stem}{tag_value}'
    return tmpl.format(stem=stem, tag_value=tag_value)


def get_change_row(action: str, path: Path, tag_value: str, args: argparse.Namespace) -> list:
    quote = " '{}' "
    tag_value = Fore.GREEN + tag_value + Style.RESET_ALL
    new_path = apply_template(path.stem, tag_value, args) + path.suffix
    return [action, quote.format(path), '->', quote.format(new_path)]


def print_change_row(change_row: list) -> None:
    print(*[token.strip('  ') for token in change_row])


def main():
    args = get_args()

    tag: str = args.tag
    dry_run: bool = args.dry_run
    files: list[Path] = args.files

    changes_table = PrettyTable(
        header=False,
        border=False,
        preserve_internal_border=False,
        align='l',
        padding_width=0)

    metadata: list[dict] = get_tags(files, tag)

    for (path, data) in zip(files, metadata):
        tag_value = get_tag_value(data)

        if tag_value is None:
            if dry_run:
                changes_table.add_row(get_change_row('Not renamed!', path, '', args))
                logging.warning(f"Tag '{tag}' not found in '{path}'")
            else:
                print(f"Not renamed! Tag '{tag}' not found in '{path}'")

            continue

        tag_value = apply_mappings(tag_value, args.mapping)
        new_stem = apply_template(path.stem, tag_value, args)
        change_row = get_change_row('renamed', path, tag_value, args)

        if dry_run:
            changes_table.add_row(change_row)
            continue

        new_path = path.with_stem(new_stem).with_suffix(path.suffix)
        path.rename(new_path)

        print_change_row(change_row)

    if dry_run:
        [print_change_row(row) for row in changes_table.rows]
        print('---- DRY RUN ----')

    print('Done!')


if __name__ == '__main__':
    main()
