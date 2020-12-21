import pickle

from highlight import highlight


def search(course_name, keyword):
    with open('data/manaba.pickle', 'rb') as f:
        tree = pickle.load(f)
        results = []
        for pre, fill, node in tree:
            if hasattr(node, 'content') and node.parent.name == course_name:
                res = highlight(node.content, keyword)
                if len(res):
                    results.append({
                        'highlights': res,
                        'url': node.url,
                        'title': node.name
                    })
        return results
