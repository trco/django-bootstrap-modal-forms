def is_ajax(meta):
    if 'HTTP_X_REQUESTED_WITH' not in meta:
        return False

    if meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        return True

    return False