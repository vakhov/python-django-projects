def dict2htmlattrs(d):
    return " ".join(["%s='%s'" % (k, v) for k, v in d.items()])