<a id="chessmaker.chess.base.rule"></a>

# chessmaker.chess.base.rule

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/d55fc2f32f12721e1fe31900fd59416040ea3896/chessmaker\chess\base\rule.py#L1)

<a id="chessmaker.chess.base.rule.Rule"></a>

## Rule

```python
class Rule(Cloneable)
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/d55fc2f32f12721e1fe31900fd59416040ea3896/chessmaker\chess\base\rule.py#L10)

<a id="chessmaker.chess.base.rule.Rule.on_join_board"></a>

#### on\_join\_board

```python
@abstractmethod
def on_join_board(board: "Board")
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/d55fc2f32f12721e1fe31900fd59416040ea3896/chessmaker\chess\base\rule.py#L12)

<a id="chessmaker.chess.base.rule.Rule.clone"></a>

#### clone

```python
@abstractmethod
def clone()
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/d55fc2f32f12721e1fe31900fd59416040ea3896/chessmaker\chess\base\rule.py#L16)

<a id="chessmaker.chess.base.rule.as_rule"></a>

#### as\_rule

```python
def as_rule(rule_func: Callable[["Board"], None]) -> Type[Rule]
```

[[view_source]](https://github.com/WolfDWyc/ChessMaker/blob/d55fc2f32f12721e1fe31900fd59416040ea3896/chessmaker\chess\base\rule.py#L20)

