import argparse
import os
from os import path
import sqlite3
import shutil
import sys
from typing import List, Dict
from zipfile import ZipFile, ZIP_LZMA


def print_out_genres(index_file: str) -> None:
    con = sqlite3.connect(index_file)

    cursor = con.execute("""
        with counters as (
            select GenreCode,
               count(*) as num_books
            from Genre_List
            group by GenreCode
        )
        select
            g.GenreCode,
            c.num_books,
            g.GenreAlias
        from Genres g
        inner join counters c on g.GenreCode=c.GenreCode
        order by g.GenreCode    
    """)
    res = cursor.fetchall()

    print('%-9s%-12s%-12s' % ('TAG', 'NUM BOOKS', 'TAG DESCRIPTION'))
    for line in res:
        print('%-9s%-12i%-12s' % line)


def get_books_to_drop(index_file: str, tags: List[str], drop_deleted: bool) -> Dict[str, List[List]]:
    con = sqlite3.connect(index_file)

    wrapped_tags = "'" + "','".join(tags) + "'"

    sql = f"""
        select
            b.BookID,
            b.Folder,
            b.FileName
        from Books b
        left join Genre_List g on b.BookID=g.BookID
        where g.GenreCode in ({wrapped_tags})
        """
    if drop_deleted:
        sql += ' or b.IsDeleted=TRUE'

    cursor = con.execute(sql)

    books_to_drop = {}
    for ix, folder, file_name in cursor.fetchall():
        if folder not in books_to_drop:
            books_to_drop[folder] = []
        if [ix, file_name] not in books_to_drop[folder]:
            books_to_drop[folder].append([ix, file_name])

    return books_to_drop


def drop_books_from_db(repacked_index_file: str, book_ids_to_drop: List[int]):
    con = sqlite3.connect(repacked_index_file)

    ids = [(i,) for i in book_ids_to_drop]

    sql = 'update Books set IsDeleted=TRUE where BookID = ?'
    con.executemany(sql, ids)

    con.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')

    parser.add_argument('-f', '--index_file', action='store', required=True)

    parser.add_argument('-a', '--action', action='store', required=True, choices=['list_tags', 'repack'])
    parser.add_argument('-s', '--source_folder', action='store', required=False)
    parser.add_argument('-d', '--destination_folder', action='store', required=False)
    parser.add_argument('-t', '--drop_tags', action='store', required=False)
    parser.add_argument('--drop_deleted', action='store_const', const=True)

    args = parser.parse_args()

    if args.action == 'list_tags':
        print_out_genres(args.index_file)

    if args.action == 'repack':
        if args.destination_folder is None:
            print('You need to specify destination folder for repacking')
            sys.exit(1)

        if args.source_folder is None:
            print('You need to specify source folder for repacking')
            sys.exit(1)

        destination_folder = args.destination_folder
        drop_deleted = args.drop_deleted or False

        if args.drop_tags is None and not drop_deleted:
            print('You need to either specify --drop_deleted or provide tags to drop from repack')
            sys.exit(1)

        if args.drop_tags is not None:
            drop_tags = args.drop_tags.split(',')
        else:
            drop_tags = []

        repacked_index_file = shutil.copy(args.index_file, destination_folder)

        books_to_drop = get_books_to_drop(index_file=repacked_index_file, tags=drop_tags, drop_deleted=drop_deleted)
        for folder, file_data in books_to_drop.items():
            book_ids_to_drop = [d[0] for d in file_data]
            book_names_to_drop = [d[1] for d in file_data]

            print(f'Now processing: {folder}')

            full_path_to_src_zip_archive = path.join(args.source_folder, folder)
            full_path_to_dst_zip_archive = path.join(destination_folder, folder)
            try:
                os.remove(full_path_to_dst_zip_archive)
            except FileNotFoundError as e:
                pass

            with ZipFile(full_path_to_src_zip_archive, 'r') as src_zip:

                has_something_to_delete = False
                for src_file in src_zip.filelist:
                    if src_file.filename.split('.')[0] in book_names_to_drop:
                        has_something_to_delete = True
                        break

                if has_something_to_delete:
                    with ZipFile(full_path_to_dst_zip_archive, 'w', compression=ZIP_LZMA) as dst_zip:
                        for src_file in src_zip.filelist:

                            if src_file.filename.split('.')[0] in book_names_to_drop:
                                continue
                            else:
                                byte_data = src_zip.read(src_file.filename)
                                dst_zip.writestr(src_file.filename, byte_data)

                drop_books_from_db(repacked_index_file, book_ids_to_drop)
