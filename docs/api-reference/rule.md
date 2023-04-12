<a id="src.chess.base.rule"></a>

# src.chess.base.rule

<a id="src.chess.base.rule.Rule"></a>

## Rule

```python
class Rule(Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\rule.py#L10)

<a id="src.chess.base.rule.Rule.on_join_board"></a>

#### on\_join\_board

```python
@abstractmethod
def on_join_board(board: "Board")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\rule.py#L12)

<a id="src.chess.base.rule.Rule.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\rule.py#L16)

<a id="src.chess.base.rule.as_rule"></a>

#### as\_rule

```python
def as_rule(rule_func: Callable[["Board"], None]) -> Type[Rule]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/fa904e10464b6e4f95136eb8c6d988f269e3f1a5/src\chess\base\rule.py#L20)

