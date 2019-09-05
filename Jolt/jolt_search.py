from gsearch.googlesearch import search
from jolt_spider import get_h1_text


def google_search(query, site='straitstimes.com'):
    """Google search.

    Args:
        query (str): search query.
        site (str): url of website to search from. Defaults to ST.com.

    Returns:
        The search results if successful. Limited to 5 results.
    """
    init_results = list()
    retry = 0
    while len(init_results) == 0:
        searching = search(f'{query} site:{site}', num_results=10)
        init_results += searching
        retry += 1
        if retry == 3:
            return

    results = list()

    # return only articles that have the h1 heading tag,
    # else skip over the article
    for (headline, url) in init_results:
        try:
            headline = get_h1_text(url)
            results.append((headline, url))
        except AttributeError:
            pass

    return results[:5]
