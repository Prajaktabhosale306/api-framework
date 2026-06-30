_current_item = None

def set_current_test(item):
    global _current_item
    _current_item=item

def get_current_test():
    return _current_item