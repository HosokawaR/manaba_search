import pickle
from glob import glob

from highlight import highlight
import re


def search(course_name, keyword):
    files = glob('./data/*')
    filename = sorted(files)[-1]
    print(filename)
    crawling_time = re.search(r'[0-9]+', filename)
    with open(filename, 'rb') as f:
        tree = pickle.load(f)
        results = []
        for pre, fill, node in tree:
            if hasattr(node, 'content') and node.parent.name == course_name:
                res = highlight(node.content, keyword)
                if len(res):
                    results.append({
                        'highlights': res,
                        'url': node.url,
                        'title': node.name,
                        'crawling_time': crawling_time
                    })
        return results
