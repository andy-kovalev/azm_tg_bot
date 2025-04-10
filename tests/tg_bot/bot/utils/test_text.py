import pytest

from bot.utils.text import mdv2_escape, mdv2_bold, _E, _B

# MARKDOWN_V2 escape symbol
ES = '\\'
# MARKDOWN_V2 bold symbol
BS = '*'


def test_markdown_v2_symbols():
    assert ES == _E
    assert BS == _B


@pytest.mark.parametrize(['text', 'escaped_text'],
                         (('t_e*s[t)', f't{ES}_e{ES}*s{ES}[t{ES})'),
                          ('test', 'test')))
def test_mdv2_escape(text, escaped_text):
    result_escaped_text = mdv2_escape(text)
    assert result_escaped_text == escaped_text


@pytest.mark.parametrize(['text', 'bold_text'],
                         (('test', f'{BS}test{BS}'),))
def test_mdv2_bold(text, bold_text):
    result_bold_text = mdv2_bold(text)
    assert result_bold_text == bold_text
