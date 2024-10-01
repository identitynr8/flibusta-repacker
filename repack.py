import argparse
import os
from os import path
import shutil
import sys
from typing import List
from zipfile import ZipFile, ZIP_DEFLATED


def print_out_genres() -> None:

    genres_raw = f"""sf;Научная Фантастика
        sf_action;Боевая фантастика
        sf_heroic;Героическая фантастика
        sf_detective;Детективная фантастика
        sf_epic;Эпическая фантастика
        sf_history;Историческая фантастика
        sf_space;Космическая фантастика
        sf_cyberpunk;Киберпанк
        sf_stimpank;Стимпанк
        sf_technofantasy;Технофэнтези
        sf_postapocalyptic;Постапокалипсис
        sf_social;Социально-психологическая фантастика
        sf_litrpg;ЛитРПГ
        popadancy;Попаданцы
        sf_fantasy;Фэнтези
        sf_fantasy_city;Городское фэнтези
        russian_fantasy;Славянское фэнтези
        fairy_fantasy;Мифологическое фэнтези
        sf_humor;Юмористическая фантастика
        sf_horror;Ужасы
        sf_mystic;Мистика
        hronoopera;Хроноопера
        modern_tale;Современная сказка
        sf_etc;Фантастика: прочее
        detective;Детективы
        det_action;Боевик
        det_classic;Классический детектив
        det_history;Исторический детектив
        det_irony;Иронический детектив
        det_crime;Криминальный детектив
        det_police;Полицейский детектив
        det_hard;Крутой детектив
        det_espionage;Шпионский детектив
        det_political;Политический детектив
        det_su;Советский детектив
        det_maniac;Про маньяков
        thriller;Триллер
        adventure;Приключения
        adv_story;Авантюрный роман
        adv_indian;Приключения про индейцев
        adv_history;Исторические приключения
        adv_maritime;Морские приключения
        child_adv;Детские приключения
        adv_modern;Приключения в современном мире
        adv_animal;Природа и животные
        adv_geo;Путешествия и география
        tale_chivalry;Рыцарский роман
        prose;Проза
        prose_abs;Фантасмагория
        prose_classic;Классическая проза
        prose_contemporary;Современная проза
        prose_counter;Контркультура
        prose_history;Историческая проза
        prose_magic;Магический реализм
        prose_military;Проза о войне
        prose_neformatny;Неформатная проза
        prose_rus_classic;Русская классическая проза
        prose_su_classics;Советская классическая проза
        literature_18;Классическая проза XVII-XVIII веков
        literature_19;Классическая проза ХIX века
        literature_20;Классическая проза ХX века
        foreign_antique;Средневековая классическая проза
        foreign_prose;Зарубежная классическая проза
        gothic_novel;Готический роман
        great_story;Роман, повесть
        story;Новелла
        aphorisms;Афоризмы
        epistolary_fiction;Эпистолярная проза
        children;Детская литература
        child_education;Детская образовательная литература
        child_det;Детская остросюжетная литература
        foreign_children;Зарубежная литература для детей
        prose_game;Игры, упражнения для детей
        child_classical;Классическая детская литература
        child_prose;Проза для детей
        child_tale_rus;Русские сказки
        child_tale;Сказки народов мира
        child_verse;Стихи для детей
        child_sf;Фантастика для детей
        love;Любовные романы
        love_history;Исторические любовные романы
        love_short;Короткие любовные романы
        love_sf;Любовно-фантастические романы
        love_detective;Остросюжетные любовные романы
        love_contemporary;Современные любовные романы
        love_erotica;Эротическая литература
        love_hard;Порно
        science;Научная литература
        sci_theories;Альтернативные научные теории
        sci_cosmos;Астрономия и Космос
        sci_biology;Биология
        sci_botany;Ботаника
        sci_veterinary;Ветеринария
        military_history;Военная история
        sci_oriental;Востоковедение
        sci_geo;Геология и география
        sci_state;Государство и право
        sci_zoo;Зоология
        sci_history;История
        sci_math;Математика
        sci_medicine;Медицина
        sci_medicine_alternative;Альтернативная медицина
        sci_popular;Научпоп
        sci_social_studies;Обществознание
        sci_politics;Политика
        sci_psychology;Психология и психотерапия
        sci_phys;Физика
        sci_philology;Филология
        sci_philosophy;Философия
        sci_chem;Химия
        sci_ecology;Экология
        sci_economy;Экономика
        sci_juris;Юриспруденция
        sci_linguistic;Языкознание
        computers;Околокомпьютерная литература
        comp_db;Базы данных
        comp_www;Интернет
        comp_hard;Компьютерное 'железо'
        tbg_computers;Учебные пособия, самоучители
        reference;Справочная литература
        geo_guides;Путеводители
        ref_guide;Руководства
        ref_dict;Словари
        ref_ref;Справочники
        ref_encyc;Энциклопедии
        sci_textbook;Учебники и пособия
        tbg_school;Школьные учебники и пособия
        tbg_secondary;Для среднего и спец. образования
        tbg_higher;Учебники и пособия ВУЗов
        auto_business;Автодело
        military_weapon;Военная техника и вооружение
        equ_history;История техники
        sci_radio;Радиоэлектроника
        sci_metal;Металлургия
        sci_build;Строительство и сопромат
        sci_tech;Технические науки
        sci_transport;Транспорт и авиация
        economics_ref;Деловая литература
        org_behavior;Кадры, организация
        popular_business;О бизнесе популярно
        banking;Финансы
        economics;Экономика
        home;Домоводство
        home_sport;Боевые искусства, спорт 
        home_pets;Домашние животные
        home_health;Здоровье
        home_collecting;Коллекционирование
        home_cooking;Кулинария
        home_entertain;Развлечения
        home_garden;Сад и огород
        home_diy;Сделай сам
        home_crafts;Хобби и ремесла
        home_sex;Эротика, Секс
        auto_regulations;Автомобили и ПДД
        sci_pedagogy;Педагогика
        family;Семейные отношения
        astrology;Астрология и хиромантия
        religion;Религиозная литература
        religion_budda;Буддизм
        religion_catholicism;Католицизм
        religion_christianity;Христианство
        religion_esoterics;Эзотерика
        religion_hinduism;Индуизм
        religion_islam;Ислам
        religion_judaism;Иудаизм
        religion_orthodoxy;Православие
        religion_paganism;Язычество
        religion_protestantism;Протестантизм
        religion_self;Самосовершенствование
        sci_religion;Религиоведение
        nonfiction;Документальная литература
        nonf_publicism;Публицистика
        nonf_biography;Биографии и Мемуары
        military_special;Военное дело
        nonf_military;Военная документалистика и аналитика ???
        travel_notes;География, путевые заметки
        antique;Старинная литература
        antique_ant;Античная литература
        antique_east;Древневосточная литература
        antique_russian;Древнерусская литература
        antique_european;Европейская старинная литература
        poetry_for_classical;Классическая зарубежная поэзия
        poetry_classical;Классическая поэзия
        poetry_rus_classical;Классическая русская поэзия
        lyrics;Лирика
        palindromes;Палиндромы
        song_poetry;Песенная поэзия
        poetry;Поэзия
        poetry_east;Поэзия Востока
        poem;Поэма, эпическая поэзия
        poetry_for_modern;Современная зарубежная поэзия
        poetry_modern;Современная поэзия
        poetry_rus_modern;Современная русская поэзия
        humor_verse;Юмористические стихи
        drama_antique;Античная драма
        vaudeville;Водевиль
        drama;Драма
        dramaturgy;Драматургия
        screenplays;Сценарии
        comedy;Комедия
        tragedy;Трагедия
        design;Искусство и Дизайн
        art_criticism;Искусствоведение
        painting;Живопись
        nonf_criticism;Критика
        sci_culture;Культурология
        art_world_culture;Мировая художественная культура
        music;Музыка
        notes;Партитуры
        architecture_book;Скульптура и архитектура
        theatre;Театр
        cine;Кино
        epic;Былины, эпопея
        child_folklore;Детский фольклор
        antique_myths;Мифы. Легенды. Эпос
        folk_songs;Народные песни
        folk_tale;Народные сказки
        proverbs;Пословицы, поговорки
        folklore;Фольклор, загадки
        limerick;Частушки, прибаутки, потешки
        humor_anecdote;Анекдоты
        humor;Юмор
        humor_satire;Сатира
        humor_prose;Юмористическая проза
        periodic;Журналы, газеты 
        comics;Комиксы
        fanfiction;Фанфик
        network_literature;Самиздат, сетевая литература
        unfinished;Незавершенное
        other;Разное"""

    print('%-25s%-12s' % ('GENRE', 'GENRE DESCRIPTION'))
    for line in genres_raw.split('\n'):
        tag, descr = line.split(';')

        print('%-25s%-12s' % (tag.strip(), descr.strip()))


def repack_inpx_file(file_path: str, drop_deleted: bool, drop_genres: List[str]):

    drop_genres = set(drop_genres)

    with ZipFile(file_path, 'r') as src_zip:
        with ZipFile(file_path + '.repacked', 'w', compression=src_zip.compression) as dst_zip:
            for src_file in src_zip.filelist:

                if src_file.filename.endswith('.inp'):
                    lines_to_write_back = []
                    lines = src_zip.read(src_file.filename).decode().split('\r\n')
                    for line in lines:
                        if line == '':
                            continue

                        # ['AUTHOR', 'GENRE', 'TITLE', 'SERIES', 'SERNO', 'FILE', 'SIZE', 'LIBID', 'DEL', 'EXT', 'DATE', 'LANG','LIBRATE', 'KEYWORDS']

                        book_data = line.split(chr(0x04))
                        if drop_deleted and book_data[8] == '1':
                            continue

                        genres = book_data[1].split(":")
                        if drop_genres.intersection(set(genres)):
                            continue

                        lines_to_write_back.append(line)

                    dst_zip.writestr(src_file.filename, '\r\n'.join(lines_to_write_back))

                else:
                    byte_data = src_zip.read(src_file.filename)
                    dst_zip.writestr(src_file.filename, byte_data)

    shutil.copy(file_path + '.repacked', file_path)
    os.remove(file_path + '.repacked')


def repack_archives(file_path: str):
    with ZipFile(file_path, 'r') as inpx_zip:
        for src_file in inpx_zip.filelist:
            print(src_file.filename)

            if src_file.filename.endswith('.inp'):

                lines = inpx_zip.read(src_file.filename).decode().split('\r\n')
                book_files_to_keep = []

                for line in lines:
                    if line == '':
                        continue

                    # ['AUTHOR', 'GENRE', 'TITLE', 'SERIES', 'SERNO', 'FILE', 'SIZE', 'LIBID', 'DEL', 'EXT', 'DATE', 'LANG','LIBRATE', 'KEYWORDS']
                    book_data = line.split(chr(0x04))
                    book_files_to_keep.append(book_data[5])

                archive_file = path.join(path.dirname(file_path), src_file.filename.replace('.inp','.zip'))
                with ZipFile(archive_file, 'r') as arch_zip:

                    with ZipFile(archive_file+'.repacked', 'w', compression=ZIP_DEFLATED, compresslevel=9) as dst_zip:
                        for f in book_files_to_keep:
                            byte_data = arch_zip.read(f+'.fb2')
                            dst_zip.writestr(f+'.fb2', byte_data)

                shutil.copy(archive_file + '.repacked', archive_file)
                os.remove(archive_file + '.repacked')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')

    parser.add_argument('-a', '--action', action='store', required=True, choices=['list_genres', 'repack'])
    parser.add_argument('-f', '--inpx_file', action='store', required=False)
    parser.add_argument('-g', '--drop_genres', action='store', required=False)
    parser.add_argument('--drop_deleted', action='store_const', const=True)

    args = parser.parse_args()

    if args.action == 'list_genres':
        print_out_genres()

    elif args.action == 'repack':

        drop_deleted = args.drop_deleted or False

        if args.drop_genres is None and not drop_deleted:
            print('You need to either specify --drop_deleted or provide genres to drop from repack')
            sys.exit(1)

        if args.inpx_file is None:
            print('You need to specify inpx file to continue')
            sys.exit(1)

        if args.drop_genres is not None:
            drop_genres = args.drop_genres.split(',')
        else:
            drop_genres = []

        repack_inpx_file(file_path=args.inpx_file, drop_deleted=drop_deleted, drop_genres=drop_genres)
        repack_archives(file_path=args.inpx_file)
