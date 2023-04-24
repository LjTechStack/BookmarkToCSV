"""Module convert CSV files to alfred snippets."""

import json
import os
import plistlib
import sys

import bookmarks_parser

BOOKMARK_HEADER = "type\tparent\ttitle\turl\n"
BOOKMARK_LIST = []


def create_bookmark_data(bookmark, root_folder):
    """create the bookmark csv data from chrome bookmark."""
    bookmark_type = "folder" if bookmark.get('type') is None else bookmark.get('type')
    bookmark_line_list = [bookmark_type,
                          str(root_folder),
                          bookmark['title']]
    if bookmark_type == 'bookmark':
        bookmark_line_list.append(bookmark['url'])
    return "\t".join(bookmark_line_list)


def parse_bookmark_folders(bookmarks, root_folder):
    """parse data in bookmark."""
    for bookmark in bookmarks:
        if bookmark.get('children') is not None:
            BOOKMARK_LIST.append(create_bookmark_data(bookmark, root_folder))
            parse_bookmark_folders(bookmark['children'], bookmark['title'])
        else:
            BOOKMARK_LIST.append(create_bookmark_data(bookmark, root_folder))


def process_html_files(root, file):
    """process html data using bookmark."""
    bookmarks = bookmarks_parser.parse(os.path.join(root, file))
    parse_bookmark_folders(bookmarks, None)


def walk_through_folder(folders):
    """walk through all file under the 'input' folder."""
    for (root, _, files) in os.walk(folders):
        for file in files:
            if str(file).endswith(".html"):
                process_html_files(root, file)


def write(bookmark_data, header, file_name):
    """write to corresponding files."""
    root = "output"
    if not os.path.isdir(root):
        os.mkdir(root)
    with open(file_name, "w", encoding="utf8") as output:
        output.write(header)
        output.writelines([f"{line}\n" for line in bookmark_data])


if __name__ == '__main__':
    args = sys.argv
    walk_through_folder(args[1])
    write(BOOKMARK_LIST, BOOKMARK_HEADER, "output/bookmark.csv")
