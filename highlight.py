import re

PADDING = 20


def highlight(text, word):
    results = []
    if matches := re.finditer(word, text):
        for match in matches:
            word_start = match.span(0)[0]
            word_end = match.span(0)[1]
            start = max(0, word_start - PADDING)
            end = min(word_end + PADDING, len(text))
            results.append(
                text[start:word_start]
                + '<<<'
                + text[word_start:word_end]
                + '>>>'
                + text[word_end:end]
            )
    return results
