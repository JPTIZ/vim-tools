#!/usr/bin/env python3
'''Module for generating index.'''
import re

from sys import stdin
from typing import NamedTuple, Sequence


class Section(NamedTuple):
    title: str
    contents: str
    subsections: Sequence['Section']


def split_sections(text):
    sections = re.findall(r'^([\w ]+)\n=+\n*(([\w\W \n](?!^[\w ]+\n=+))*)',
                          text, re.MULTILINE)
    return Section(title=sections[0][0],
                   contents='',
                   subsections=split_subsections(sections[0][1]))


def split_subsections(text):
    # TODO: Recursivelly extract and separate contents from subsections.
    subsections = re.findall(r'^([\w ]+)\n-+\n*(([\w\W \n](?!^[\w ]+\n-+))*)',
                             text, re.MULTILINE)
    return [Section(title=sub[0],
                    contents=sub[1],
                    subsections=[]) for sub in subsections]


def without_index(document):
    if isinstance(document, Section):
        return Section(title=document.title,
                       contents=document.contents,
                       subsections=list(filter(
                           lambda section: section.title != 'Índice',
                           document.subsections)))
    return without_index(split_sections(document))


def as_link(title):
    link = '-'.join(title.lower().split())
    return f'[{title}](#{link})'


def make_index(document):
    def sections_index(document, level=0):
        if not isinstance(document, Section):
            return ''
        return '\n'.join(' '*level +
                         f'{i+1}. {as_link(section.title)}' +
                         sections_index(document.subsections, level+1)
                         for i, section in enumerate(document.subsections))

    document = without_index(document)
    index = Section(title='Índice',
                    contents=sections_index(document),
                    subsections=[])
    return Section(title=document.title,
                   contents=document.contents,
                   subsections=[index] + document.subsections)


def to_markdown(document):
    TITLES = ['=', '-', '*']

    def make_title(title, level: int=0):
        if level < 2:
            return (f'\n{title}\n'
                    f'{TITLES[level]*len(title)}\n\n')
        return f'\n{TITLES[2]*len(title)} {title}\n\n'

    if isinstance(document, Section):
        return (make_title(document.title) +
                '\n'.join((make_title(section.title, 1) +
                           section.contents
                           ) for section in document.subsections)).strip()
    return to_markdown(split_sections(document))


if __name__ == '__main__':
    print(to_markdown(make_index(stdin.read())))
