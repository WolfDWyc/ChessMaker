<a id="chessmaker.chess.base.rule"></a>

# chessmaker.chess.base.rule

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/c9884fe15fb48873a51b855d661dad2103a0857d/chessmaker\chess\base\rule.py#L1)

<a id="chessmaker.chess.base.rule.Rule"></a>

## Rule

```python
class Rule(Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/c9884fe15fb48873a51b855d661dad2103a0857d/chessmaker\chess\base\rule.py#L10)

<a id="chessmaker.chess.base.rule.Rule.on_join_board"></a>

#### on\_join\_board

```python
@abstractmethod
def on_join_board(board: "Board")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/c9884fe15fb48873a51b855d661dad2103a0857d/chessmaker\chess\base\rule.py#L12)

<a id="chessmaker.chess.base.rule.Rule.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/c9884fe15fb48873a51b855d661dad2103a0857d/chessmaker\chess\base\rule.py#L16)

<a id="chessmaker.chess.base.rule.as_rule"></a>

#### as\_rule

```python
def as_rule(rule_func: Callable[["Board"], None]) -> Type[Rule]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/c9884fe15fb48873a51b855d661dad2103a0857d/chessmaker\chess\base\rule.py#L20)

