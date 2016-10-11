# -*- coding:utf-8 -*-
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from z3c.form import interfaces
from z3c.form import widget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import zope.interface


class ISkosWidget(interfaces.ISequenceWidget):
    """Sequence widget."""


class SkosWidget(widget.SequenceWidget):
    zope.interface.implementsOnly(ISkosWidget)
    klass = u'token-input-widget'
    display_template = ViewPageTemplateFile('skos_display.pt')
    input_template = ViewPageTemplateFile('skos_input.pt')

    blurrable = False
    minChars = 2
    maxResults = 10
    mustMatch = False
    matchContains = True

    # Não é necessário dar "escape" em "{" e "}" aqui uma vez que essas variáveis
    # são usadas de forma literal como parâmetro do format: só precisamos dar
    # "escape" quando é a string que será aplicada o format (como o js_template)
    formatItem = 'function(row, idx, count, value) { return row[1]; }'
    formatResult = 'function(row, idx, count) { return ''; }'
    #

    # Lembre-se de que para conseguir usar { e }  de forma literal nas aberturas
    # e fechamento de funções do js, você precisa usar {{ e }} respectivamente.
    # https://docs.python.org/3/library/string.html#formatstrings
    js_template = """\
    (function($) {{
        $().ready(function() {{
            $('#formfield-form-widgets-IVCGE-skos #{id}').each(function() {{
                $('#formfield-form-widgets-IVCGE-skos').append('<input name="{name}-input" type="text" id="{id}-input" />');
                $(this).remove();
                $('#formfield-form-widgets-IVCGE-skos #{id}-input').autocomplete('{url}/@@token-search?f={id}', {{
                    autoFill: false,
                    minChars: {minChars},
                    max: {maxResults},
                    mustMatch: {mustMatch},
                    matchContains: {matchContains},
                    formatItem: {formatItem},
                    formatResult: {formatResult}
                }}).result({js_callback});
            }})
        }});
    }})(jQuery);
    """

    # Lembre-se de que para conseguir usar { e }  de forma literal nas aberturas
    # e fechamento de funções do js, você precisa usar {{ e }} respectivamente.
    # https://docs.python.org/3/library/string.html#formatstrings
    js_callback_template = """\
    function(event, data, formatted) {{
        var field = $('#formfield-form-widgets-IVCGE-skos input[type="checkbox"][value="' + data[0] + '"]');
        if(field.length == 0)
            $('#formfield-form-widgets-IVCGE-skos #{id}-input').before("<" + "label class='plain'><" + "input type='checkbox' name='{name}' checked='checked' value='" + data[0] + "' /> " + data[1] + "</label><br />");
        else
            field.each(function() {{ this.checked = true }});
        if(data[0])
            $('#formfield-form-widgets-IVCGE-skos #{id}-input').val('');
    }}
    """

    def js(self):
        context = self.context
        form_url = context.absolute_url()
        js_callback = self.js_callback_template.format(
            **dict(id=self.id, name=self.name)
        )
        return self.js_template.format(
            **dict(
                id=self.id,
                name=self.name,
                url=form_url,
                minChars=self.minChars,
                maxResults=self.maxResults,
                mustMatch=str(self.mustMatch).lower(),
                matchContains=str(self.matchContains).lower(),
                formatItem=self.formatItem,
                formatResult=self.formatResult,
                js_callback=js_callback,
            )
        )

    def vocab(self):
        name = 'brasil.gov.vcge'
        util = queryUtility(IVocabularyFactory, name)
        vcge = util(self.context)
        return vcge

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)

    @property
    def existing(self):
        value = None
        if base_hasattr(self.context, 'skos'):
            value = getattr(self.context, 'skos')
        if not value:
            value = []
        terms = self.vocab()
        data = []
        for token in value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue
            term = terms.getTermByToken(token)
            data.append({'value': token,
                         'title': term.title})
        return data

    @property
    def displayValue(self):
        value = []
        terms = self.vocab()
        for token in self.value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue
            term = terms.getTermByToken(token)
            value.append(term.title)
        return value

    def extract(self, default=interfaces.NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        if (self.name not in self.request):
            return []
        value = self.request.get(self.name, default)
        if value != default:
            if not isinstance(value, (tuple, list)):
                value = (value,)
            # do some kind of validation, at least only use existing values
            terms = self.vocab()
            for token in value:
                if token == self.noValueToken:
                    continue
                try:
                    terms.getTermByToken(token)
                except LookupError:
                    return default
        return value


@zope.interface.implementer(interfaces.IFieldWidget)
def SkosFieldWidget(field, request):
    """IFieldWidget factory for SkosWidget."""
    return widget.FieldWidget(field, SkosWidget(request))


class AutocompleteSearch(BrowserView):

    def vocab(self):
        name = 'brasil.gov.vcge'
        util = queryUtility(IVocabularyFactory, name)
        vcge = util(self.context)
        return vcge

    def __call__(self):
        field = self.request.get('f', None)
        query = safe_unicode(self.request.get('q', ''))
        if not query or not field:
            return ''

        vocab = self.vocab()
        results = [(i.token, i.title) for i in vocab
                   if query in i.title.lower()]

        results = sorted(results, key=lambda pair: len(pair[1]))
        return '\n'.join(['{0}|{1}'.format(value, title)
                          for value, title in results])


class AutocompletePopulate(AutocompleteSearch):

    def __call__(self):
        results = super(AutocompletePopulate, self).__call__()
        results = results.split('\n')
        query = self.request.get('q', '')
        for r in results:
            if r.startswith(u'{0}|'.format(safe_unicode(query))):
                return r
