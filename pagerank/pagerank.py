import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transitions = {}

    num_pages = len(corpus)
    num_links = len(corpus[page])

    if len(corpus[page]) < 1:
        for url in corpus:
            transitions[url] = 1 / num_pages
    else:
        factor_1 = damping_factor / num_links
        factor_2 = (1 - damping_factor) / num_pages
        for url in corpus:
            if url not in corpus[page]:
                transitions[url] = factor_2
            else:
                transitions[url] = factor_1 + factor_2
    return transitions    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = dict()

    for url in corpus:
        rank[url] = 0

    sample = random.choices(list(corpus))[0]
    rank[sample] += (1 / n)
    for _ in range(1, n):
        model = transition_model(corpus, sample, damping_factor)
        links = []
        probabilities = []
        for key, value in model.items():
            links.append(key)
            probabilities.append(value)
        
        sample = random.choices(links, weights=probabilities)[0]
        rank[sample] += (1 / n)
    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = dict()
    threshold = 0.0001

    N = len(corpus)
    for url in corpus:
        ranks[url] = 1 / N

    while True:
        count = 0
        for url in corpus:
            new_s = (1 - damping_factor) / N
            s = 0
            for linking_page in corpus:
                if url in corpus[linking_page]:
                    s = s + ranks[linking_page] / len(corpus[linking_page])
            s = damping_factor * s
            new_s += s
            if abs(ranks[url] - new_s) < threshold:
                count += 1           
            ranks[url] = new_s
        
        if count == N:
            break
    return ranks

if __name__ == "__main__":
    main()
