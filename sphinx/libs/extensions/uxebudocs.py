# -*- coding: utf-8 -*-
from docutils.nodes import literal_block, TextElement, Element, General, raw
from docutils.parsers.rst import directives, Directive
import docutils

from sphinx.writers.html import SmartyPantsHTMLTranslator

class UxebuHTMLTranslator(SmartyPantsHTMLTranslator):
    """
    Uxebu-specific reST for the codeviewer stuff.
    """

    def visit_codeviewer(self, node):
        self.body.append('<div label="%s" lang="%s"><pre>' % (node['label'], node['lang']))
        self.no_smarty += 1
        #SmartyPantsHTMLTranslator.visit_literal_block(self, node)

    def depart_codeviewer(self, node):
        #SmartyPantsHTMLTranslator.depart_literal_block(self, node)
        self.no_smarty -= 1
        self.body.append('</pre></div>')

    def visit_codeviewer_compound(self, node):
        self.body.append('<div dojoType="CodeGlass" type="%s" chrome="uxebu" djConfig="%s" width="%s" height="%s" version="%s" toolbar="%s">' % (
            node['type'].lower(),
            node['djconfig'],
            node['width'],
            node['height'],
            node['version'],
            node['toolbar'])
        )

    def depart_codeviewer_compound(self, node):
        self.body.append('</div>')

    # Don't apply smartypants to literal blocks
    def visit_literal_block(self, node):
        self.no_smarty += 1
        SmartyPantsHTMLTranslator.visit_literal_block(self, node)

    def depart_literal_block(self, node):
        SmartyPantsHTMLTranslator.depart_literal_block(self, node)
        self.no_smarty -= 1

class codeviewer(TextElement): pass
class codeviewer_js(TextElement): pass
class codeviewer_css(TextElement): pass
class codeviewer_html(TextElement): pass
class codeviewer_compound(General, Element): pass

# Additional directive to output an example/source viewer
def _codeviewer(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    code = u'\n'.join(content)
    language = "html"
    if len(arguments) > 0:
        language = arguments[0]
        if language == "js":
            language = "javascript"
    label = ""
    if 'label' in options:
        label = options['label']
    mycode = codeviewer(code, code)
    mycode['lang'] = language
    mycode['label'] = label
    return [mycode]

def _codeviewer_js(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    return _codeviewer(name, ['js'], options, content, lineno,
               content_offset, block_text, state, state_machine)

def _codeviewer_css(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    return _codeviewer(name, ['css'], options, content, lineno,
               content_offset, block_text, state, state_machine)

def _codeviewer_html(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    return _codeviewer(name, ['html'], options, content, lineno,
               content_offset, block_text, state, state_machine)

# a more complex compounded component (so we can separate our code-blocks)
def _codeviewer_compound(name, arguments, options, content, lineno,
             content_offset, block_text, state, state_machine):
    text = '\n'.join(content)
    if not text:
        error = state_machine.reporter.error(
            'The "%s" directive is empty; content required.' % name,
            literal_block(block_text, block_text), line=lineno)
        return [error]
    node = codeviewer_compound(text)
    djconfig = "parseOnLoad: true"
    if 'djconfig' in options:
        djconfig = options['djconfig']
    node['djconfig'] = djconfig
    width = "700"
    if 'width' in options:
        width = options['width']
    node['width'] = width
    height = "400"
    if 'height' in options:
        height = options['height']
    node['height'] = height
    type = "dialog"
    if 'type' in options and (options['type'].lower() == 'inline'):
        type = "inline"
    node['type'] = type
    version = ""
    if 'version' in options:
        version = options['version']
    node['version'] = version
    toolbar = ""
    if 'toolbar' in options:
        toolbar = options['toolbar']
    node['toolbar'] = toolbar
    state.nested_parse(content, content_offset, node)
    return [node]

class Oembed(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'maxwidth': directives.nonnegative_int,
                   'maxheight': directives.nonnegative_int}

    def run(self):
        reference = directives.uri(self.arguments[0])
        self.options['url'] = reference

        width = self.options.pop('maxwidth', None)
        height = self.options.pop('maxheight', None)

        # call oembed to construct the html code
        if width or height:
            if not height:
                height = width
            elif not width:
                width = height
            html = '<a href="%s" data-maxwidth="%s" data-maxheight="%s" rel="oembed">%s</a>' % (self.options['url'], width, height, self.options['url'],)
        else:
            html = '<a href="%s" rel="oembed">%s</a>' % (self.options['url'], self.options['url'])
        return [raw('', html, format='html')]

def setup(app):
    app.add_node(codeviewer)
    app.add_node(codeviewer_compound)
    app.add_directive('oembed', Oembed)
    app.add_directive('js', _codeviewer_js,
                      1, (0, 1, 0), label=lambda x: x)
    app.add_directive('javascript', _codeviewer_js,
                      1, (0, 1, 0), label=lambda x: x)
    app.add_directive('css', _codeviewer_css,
                      1, (0, 1, 0), label=lambda x: x)
    app.add_directive('html', _codeviewer_html,
                      1, (0, 1, 0), label=lambda x: x)
    app.add_directive('cv', _codeviewer,
                      1, (0, 1, 0), label=lambda x: x) #deprecated
    app.add_directive('codeviewer', _codeviewer,
                      1, (0, 1, 0), label=lambda x: x) #deprecated  #deprecated
    app.add_directive('code-example', _codeviewer_compound, 1, (0, 0, 0))
    app.add_directive('codeviewer-compound', _codeviewer_compound, 1, (0, 0, 0)) # deprecated
    app.add_directive('cv-compound', _codeviewer_compound, 1, (0, 0, 0)) # deprecated
