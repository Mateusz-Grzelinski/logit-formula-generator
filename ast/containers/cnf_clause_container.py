from .literal_container import LiteralContainer


class CNFClauseContainer(LiteralContainer):
    @staticmethod
    def _item_type_check(obj):
        from ast.cnf_clause import CNFClause
        return isinstance(obj, CNFClause)

    def clauses(self):
        from ast.cnf_clause import CNFClause
        return (c for c in self._items if isinstance(c, CNFClause))
