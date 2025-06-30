from rapidfuzz import fuzz

async def fuzzy_match_words(sentence: str, word_list: list[dict], lang_field="kr", threshold=75, max_terms=10):
    matches = []
    for word in word_list:
        term = word.get(lang_field)
        if term:
            score = fuzz.partial_ratio(term, sentence)
            if score >= threshold:
                matches.append((score, word))
    matches.sort(key=lambda x: -x[0])
    return [w for _, w in matches[:max_terms]]
