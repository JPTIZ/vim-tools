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
    sections = re.findall(r'^([\w ]+)\n=+\n*(([\w\W \n](?![\w ]+\n=+))*)',
                          text, re.MULTILINE)
    return Section(title=sections[0][0],
                   contents='',
                   subsections=split_subsections(sections[0][1]))


def split_subsections(text):
    subsections = re.findall(r'^([\w ]+)\n-+\n*(([\w\W \n](?![\w ]+\n-+))*)',
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
    def sections_index(document):
        return '\n'.join(f'{i+1}. {as_link(section.title)}'
                         for i, section in enumerate(document.subsections))

    document = without_index(document)
    index = Section(title='Índice',
                    contents=sections_index(document),
                    subsections=[])
    document = Section(title=document.title,
                       contents=document.contents,
                       subsections=[index] + document.subsections)
    print(index.contents)


if __name__ == '__main__':
    make_index(stdin.read())
