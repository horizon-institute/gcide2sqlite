#!/usr/bin/env python3
import argparse
import codecs
import os
import re
import sqlite3
import string
import sys

from pathlib import Path

DESCRIPTION = 'Convert the GNU Collaborative International' \
        + 'Dictionary of English to an SQLite database'

def main(gcide_dir, out_file, ignore_file=None):
    line_pattern = re.compile(r'<p><ent>(.*)</ent><br/')
    word_pattern = re.compile(r'^[a-z]+$')

    words = {}

    for c in string.ascii_uppercase:
        path = os.path.join(gcide_dir, 'CIDE.' + c)
        with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_match = line_pattern.match(line)
                if line_match != None:
                    word = line_match.group(1).lower()
                    word_match = word_pattern.match(word)
                    if word_match != None and len(word) > 4:
                        words[word] = ''

    if os.path.isfile(out_file):
        os.remove(out_file)
    conn = sqlite3.connect(out_file)
    c = conn.cursor()
    c.execute('CREATE TABLE words (word text)')
    c.executemany('INSERT INTO words VALUES (?)',
            map(lambda k : (k,), words.keys()))
    conn.commit()

    if ignore_file:
        with codecs.open(ignore_file, 'r',
                encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                c.execute('DELETE FROM words WHERE word like ?',
                        ('%' + word + '%',))

    conn.commit()

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        'dir',
        type=str,
        help='path to the GCIDE directory')
    parser.add_argument(
        'outfile',
        type=str,
        help='output file path')
    parser.add_argument(
        '--ignore',
        type=str,
        default=None,
        help='optional file containing words to ignore')
    args = parser.parse_args()
    main(args.dir, args.outfile, ignore_file=args.ignore)
