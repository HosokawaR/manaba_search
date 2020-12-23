import pickle
from glob import glob

from highlight import highlight
import re


def search(course_name, keyword):
    files = glob('./data/*')
    filename = sorted(files)[-1]
    crawling_time = re.search(r'[0-9]{10}', filename).group()
    with open(filename, 'rb') as f:
        tree = pickle.load(f)
        data = {}
        data['results'] = []
        data['crawling_time'] = crawling_time
        for pre, fill, node in tree:
            if hasattr(node, 'content') and node.parent.name == course_name:
                res = highlight(node.content, keyword)
                if len(res):
                    data['results'].append({
                        'highlights': res,
                        'url': node.url,
                        'title': node.name
                    })
        return data
