"""
@CTB: still need to find something that only BS (and not the intolerant
parser) can parse.
"""

import twilltestlib
from twill import commands

def setup_module():
    global url
    url = twilltestlib.get_url()

def test_links_parsing():
    commands.config('use_tidy', '0')
    commands.go('/broken_linktext')
    commands.config('use_tidy', '1')

def test_raw():
    """
    test parsing of raw, unfixed HTML.
    """
    b = commands.get_browser()

    commands.config('use_tidy', '0')
    commands.config('use_BeautifulSoup', '0')
    commands.config('allow_parse_errors', '0')

    commands.go(url)

    ###
    
    commands.go('/tidy_fixable_html')

    forms = b.get_all_forms()
    assert len(forms) == 1, "lxml should find one form on this page"

    ###

    commands.go('/BS_fixable_html')
    forms = b.get_all_forms()
    assert len(forms) == 1, "there should be one mangled form on this page"

    ###

#    commands.go('/unfixable_html')
#    try:
#        b._browser.forms()
#        assert 0, "this page has a parse error."
#    except ClientForm.ParseError:
#        pass

def test_tidy():
    """
    test parsing of tidy-processed HTML.
    """
    b = commands.get_browser()

    commands.config('use_tidy', '1')
    commands.config('use_BeautifulSoup', '0')
    commands.config('allow_parse_errors', '0')

    commands.go(url)

    ###
    
    commands.go('/tidy_fixable_html')

    forms = b.get_all_forms()
    assert len(forms) == 1, \
	"you must have 'tidy' installed for this test to pass"

    ###

    commands.go('/BS_fixable_html')
    forms = b.get_all_forms()
    assert len(forms) == 1, \
            "there should be one mangled form on this page"

    ###

#    commands.go('/unfixable_html')
#    try:
#        b._browser.forms()
#        assert 0, "this page has a parse error."
#    except ClientForm.ParseError:
#        pass

def test_BeautifulSoup():
    """
    test parsing of BS-processed HTML.
    """
    b = commands.get_browser()

    commands.config('use_tidy', '0')
    commands.config('use_BeautifulSoup', '1')
    commands.config('allow_parse_errors', '0')

    commands.go(url)

    ###
    
    commands.go('/tidy_fixable_html')

    forms = b.get_all_forms()
    assert len(forms) == 1, "lxml should find one form on this page"


    ###

    commands.go('/BS_fixable_html')
    forms = b.get_all_forms()
    assert len(forms) == 1, \
           "there should be one mangled form on this page"

    ###

#   this no longer breaks... @CTB
#    commands.go('/unfixable_html')
#    try:
#        b._browser.forms()
#        assert 0, "this page has a parse error."
#    except ClientForm.ParseError:
#        pass

def test_allow_parse_errors():
    """
    test nice parsing.
    """
    b = commands.get_browser()

    commands.config('use_tidy', '0')
    commands.config('use_BeautifulSoup', '1')
    commands.config('allow_parse_errors', '1')

    commands.go(url)

    commands.go('/unfixable_html')
    b.get_all_forms()

def test_global_form():
    """
    test the handling of global form elements
    """
    b = commands.get_browser()
    commands.config('use_tidy', '0')

    commands.go(url)
    commands.go('/effed_up_forms')
    forms = b.get_all_forms()
    assert len(forms) == 2

def test_effed_up_forms2():
    """
    should always succeed; didn't back ~0.7.
    """
    commands.config('use_tidy', '1')
    commands.config('use_BeautifulSoup', '1')
    commands.config('allow_parse_errors', '0')

    commands.go(url)
    commands.go('/effed_up_forms2')

    b = commands.get_browser()
    forms = b.get_all_forms()
    form = forms[0]
    inputs = [i for i in form.inputs]
    assert len(inputs) == 3, \
    "you must have 'tidy' installed for this test to pass"

    # with a more correct form parser this would work like the above.
    commands.config('use_tidy', '0')
    commands.reload()
    forms = b.get_all_forms()
    form = forms[0]
    inputs = [i for i in form.inputs]
    assert len(inputs) == 3, "lxml should find 3 form inputs"
