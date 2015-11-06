#!/usr/bin/env python
# -*- coding: utf8 -*-
import codecs
from os.path import join

import yaml
import CommonMark
from jinja2 import Environment, FileSystemLoader


def md(raw):
    ast = parser.parse(raw)
    return renderer.render(ast)


if __name__ == '__main__':

    # templates
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('base.html')
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()

    # Load pages
    with codecs.open('meta.yaml', 'r', encoding='utf8') as fd:
        raw = yaml.load(fd)

    pages = raw['pages']
    context = raw['context']
    meta = raw['meta']

    for data in pages:
        name = data['name']
        title = data['title']
        target = data['target']

        with codecs.open("{}.md".format(name), 'r', encoding='utf8') as fd:
            content = fd.read()

        body = md(content)

        context.update({
            "body": body,
            "title": title,
            "footer": md(context['footer']),
        })

        output = template.render(**context)
        target_path = join(meta['build_path'], '{}.html'.format(target))
        with codecs.open(target_path, 'w', encoding='utf8') as fd:
            fd.write(output)
