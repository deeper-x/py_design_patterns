from typing import Any, Callable,  TypeAlias, Type

MSQL: TypeAlias = "MetaSQL"


class MetaSQL(type):
    query: Callable[[MSQL, str, str], str]

    def __new__(cls: Type[MSQL], name: Any, bases: Any, attrs: Any) -> MSQL:
        new_cls: MSQL = super().__new__(cls, name, bases, attrs)

        def query(self: MSQL, action: str, target: str) -> str:
            haystack: dict[str, Callable[[MSQL], str]] = {k: v for k, v in attrs.items() if k.startswith(action)}

            res: str = f"action '{action}' not found"
            needle: str = f"{action}_{target}"

            if needle in haystack:
                res = haystack[needle](self)

            return res

        # Add the new method to the class
        new_cls.query = query

        return new_cls


class SQL(metaclass=MetaSQL):
    query: Callable[[str, str], str]

    def update_table_1(self) -> str:
        return "UPDATE table_1 ..."

    def update_table_2(self) -> str:
        return "UPDATE table_2 ..."

    def delete_table_3(self) -> str:
        return "DELETE table_3 ..."

    def create_table_4(self) -> str:
        return "CREATE table_4 ..."


sql = SQL()
a: str = sql.query("update", "table_1")
b: str = sql.query("update", "table_2")
c: str = sql.query("delete", "table_3")
d: str = sql.query("create", "table_4")
e: str = sql.query("insert", "table 5")

print(a)
print(b)
print(c)
print(d)
print(e)

# OUTPUT:
# UPDATE table_1 ...
# UPDATE table_2 ...
# DELETE table_3 ...
# CREATE table_4 ...
# action 'insert' not found
