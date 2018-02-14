class NoQueryResultException (Exception):
    def __init__ (self):
        msg = "Oops! Seems like we cannot find any result for your query"


def fetchRows(cur, rv):
    col_names = []
    rows = [] # [{"restaurant_name": "name"}, {}, {}]
    for desc in cur.description:
        col_names.append(desc[0])

    for row in rv:
        row_dict = {}
        for col_name, col_value in zip (col_names, row):
            row_dict[col_name] = col_value
        # print (row_dict)
        rows.append(row_dict)

    return rows
