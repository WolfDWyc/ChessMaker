<a id="chessmaker.chess.base.rule"></a>

# chessmaker.chess.base.rule

<a id="chessmaker.chess.base.rule.Rule"></a>

## Rule

```python
class Rule(Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\rule.py#L10)

<a id="chessmaker.chess.base.rule.Rule.on_join_board"></a>

#### on\_join\_board

```python
@abstractmethod
def on_join_board(board: "Board")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\rule.py#L12)

<a id="chessmaker.chess.base.rule.Rule.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\rule.py#L16)

<a id="chessmaker.chess.base.rule.as_rule"></a>

#### as\_rule

```python
def as_rule(rule_func: Callable[["Board"], None]) -> Type[Rule]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/dc56d4841f94820eba4c40c003f75d8396c128d9/chessmaker\chess\base\rule.py#L20)

