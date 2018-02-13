
def fetchRows (cur, rv):
    cols = getCols(cur)
    rows = []
    row = {}
    for i in range(len(rv)):
        for key, value in zip(cols, rv[i]):
            row[key] = value
        rows.append(row)
        row = {}
    return rows


def getCols(cur):
    return [info[0] for info in cur.description]


class NoQueryResultError (Exception):
    def __init__(self):
        super().__init__()
        self.msg = "<h6>We couldn\'t find a match in the database!</h6>"