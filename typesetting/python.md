# Portrait Python

A Python typesetting specification for visual grouping and vertical scanning.

## Principles and Scope

* Group related statements into logical paragraphs.
* Align related data when it helps readers compare it.
* Keep code narrow enough to scan on a portrait monitor.
* Apply this spec to handwritten Python.
  Leave generated and third-party code in its own style.
* Follow PEP 8 where this spec does not state an exception.
* When rules conflict, prioritize correctness, clarity, small reviewable diffs, then typography.
* Apply formatting to new or semantically edited code.
  Do not reformat unrelated code merely to enforce this spec.

## General Guidelines

* Max line length for code: **92 characters**
  * Reason is I use a **portrait mode** monitor (right side) for editing code.
* No max line length for non-code text (inline comments, docstrings, markdown).
  * Reason is I use a **landscape mode** monitor (left side) for editing non-code text, and so in that monitor I prefer that my IDE's editor wrap the text.
* Preserve whitespace that supports vertical readability, including indented blank lines.
* Do not run broad trailing-whitespace cleanup commands unless I explicitly ask for that. If `git diff --check` flags whitespace, report it or fix only the exact lines being semantically edited.

# Python Code Style Guidelines

## Variable Naming

* Variables, functions, and method names: `snake_case`
* Class names:
  * Short names:`CamelCase`
  * Long names: For class names with 4 or more segments use underscores to separate logical segments, e.g., `WhatsApp_Local_FlowContext`.

## PEP 8 Exceptions

I generally follow [PEP 8](https://peps.python.org/pep-0008/) guidelines for writing Python code.
However, I prefer to **add extra spaces in specific places** for better readability, especially in the context of my vertical screen setup. These exceptions are listed below.

### Assignments

* In general:
  * Leave at least one space before the equal sign.
  * Leave one space after the equal sign.
  * ✅ Example: `value = 10`
  * ❌ Counterexample: `horrible_style=True`
* Assignment Blocks:
  * Align `=` or annotation/dictionary colons within small, contiguous groups describing the same thing.
  * Align type annotations and defaults in related parameter declarations when this fits within 92 characters.
  * Do not align unrelated statements or extend alignment across logical paragraphs.
  * Prefer wrapping over excessive padding. When alignment causes a large unrelated diff, keep the edited group smaller or use single spaces.
  * Separate assignment groups from other logical stages with blank lines; do not insert extra blank lines at module or block boundaries solely for alignment.
  * ✅ Example:
    ```python
    check_components_flag  = True
    check_connections_flag = False
    check_others_flag      = True
    …
    new_dict = {
        "components"  : components,
        "connections" : connections,
        "debug"       : debug,
    }
    …
    def new_method(
        self,
        comp       : str,
        comp_probs : list[str] | None = None,
        debug      : bool             = False,
    ) -> list[str] :
        
        if comp_probs is None :
            comp_probs = []
        
        # Continue with the operation here.
        return comp_probs
    ```

### Line Wrapping

* When a definition, call, or collection exceeds 92 characters, prefer one parameter, argument, or item per line.
* Use four spaces per indentation level.
* Align the closing delimiter with the start of the statement.
* Use a trailing comma in multiline definitions, calls, imports, and collection displays.
* Prefer implicit continuation inside parentheses over backslash continuation.
* Keep indivisible URLs and strings intact when splitting them would obscure meaning or change their value.
* In annotations:
  * Keep simple generic types compact: `dict[ str, Any]`.
  * Apply collection-literal spacing to values, not to type parameters.
  * ✅ Example:
    ```python
    def build_report(
        customer_id : int,
        *,
        include_tax : bool = True,
    ) -> Report :
        
        return render_report(
            customer_id,
            include_tax = include_tax,
        )
    ```

### Conditionals and Loops

* In compound statements, including `if`, `for`, `while`, `try`, `except`, `with`, `match`, and `case`, do leave a space before the ending colon:
* ✅ Examples:
  * `if condition :`
  * `for item in list_of_items :`

### Lists, Tuples, Dictionaries, and Sets

* For single-line nonempty collection literals, leave a space after the opening delimiter and before the closing delimiter.
* Multiline literals follow the line-wrapping rules.
* Leave a space after each comma.
* For dictionaries, leave a space before and after each colon between key and value.
* Keep empty literals compact: `[]`, `{}`, `()`.
  Use `set()` for an empty set.
* ✅ Examples:
  * `one_item = [ item ]`
  * `one_tuple = ( item, )`
  * `single_line_list = [ item1, item2, item3 ]`
  * `single_line_dict = { key1 : value1, key2 : value2 }`

### Comprehensions

* Leave a space after the opening bracket/brace/parenthesis.
* Leave a space before the closing bracket/brace/parenthesis.
* For dictionary comprehensions, leave a space before and after each colon.
* ✅ Examples:
  * `[ item for item in items ]`
  * `{ key : value for key, value in items }`

## Iterable/Dict Unpacking

* When unpacking values in calls or displays do wrap expressions after `*` or `**` in parentheses, EXCEPT for parameter declarations such as `*args` or `**kwargs`.
* Example:
  * Suppose object `some_object` has a list/tuple member `some_list`
  * ❌ Bad: `*some_object.some_list`
  * ✅ Good: `*(some_object.some_list)`

### Function and Method Definitions

* Leave a space between the opening parenthesis and the first argument.
* Leave a space before and after colons used in type annotations.
* Do **not** leave a space before the closing parenthesis.
* Leave a space before and after the `->` return type arrow.
* Leave a space between the return type and the final colon.
* ✅ Example:
  * `def function( arg : list) -> None :`
  * `def class_method( arg1 : int, arg2 : str) -> bool :`
* Exception: Methods that take only `cls` or `self`. In this case leave no spaces.
  * E.g., `def my_instance_method(self) -> None :`

### Function and Method Calls

* No argument: `function()`
* Single argument:
  * Leave no spaces.
  * ✅ Example: `function(arg)`
  * ❌ Counterexamples:
    * `function( arg)`
    * `function( arg )`
* Multiple arguments:
  * Leave a space between the opening parenthesis and the first argument.
  * Leave a space after each comma.
  * Do **not** leave a space before the closing parenthesis.
    ✅ Examples:
    * `isinstance( var, type)`
    * `class_method( arg1, arg2, arg3)`

### Type Annotations

* Prefer [PEP 604](https://peps.python.org/pep-0604/) pipe-style unions over `typing.Optional` / `typing.Union`.
  * ✅ Example: `value : list[str] | None`
  * ❌ Counterexample: `value : Optional[list[str]]`

### Functions that Return Something or None

Document the condition that produces `None`, rather than merely restating the union type.

```python
def find_customer( customer_id : int) -> Customer | None :
    """
    Find a customer by internal ID \\
    Args:
        ...
    Returns:
        The matching customer, or None if the ID is not in the database.
    """
```

### Functions With Dependent Return Type

Describe which condition selects each return value.
Use `Literal` and `@overload` when callers benefit from a more precise static return type;
do not add overloads solely to restate documentation.

```python
def read_payload(
  payload : bytes,
  *,
  decode  : bool = True,
) -> str | bytes :
    """
    Read a payload as text or raw bytes \\
    Args:
        ...
    Returns:
        UTF-8 text when decode is True; otherwise the original bytes.
    Raises:
        UnicodeDecodeError: The requested text is not valid UTF-8.
    """
    ...
    return payload.decode("utf-8") if decode else payload
```

### Vertical Whitespace Within Functions

* Treat a function body like prose divided into logical paragraphs.
* Leave an indented blank line:
  * after a function or method header, or after its docstring;
  * between setup, validation, I/O, transformation, mutation, and return stages;
  * around non-trivial control-flow blocks when they form a distinct logical stage;
  * before a final return when it follows other work.
* Within nested control flow, use indented blank lines to separate logical stages at that indentation level.
* Keep connected branches (`if`/`elif`/`else`, `try`/`except`/`finally`) together unless a blank line marks a useful logical boundary.
  Do not add blank lines mechanically around every nested block.
* Keep directly related statements together. Do not add a blank line between a condition and its immediate single-line action.
* Do not collapse logical paragraphs merely because PEP 8 does not require blank lines there.
* Preserve indentation on blank lines inside indented blocks.

## Imports

* Put `from __future__` imports first, right after the module docstring (if present).
* Declare the imports in sections according to the following order:
  1. Standard library and popular publicly-available modules imported at the module-name level, e.g.:
  ```python
  import numpy as np
  import os
  import re
  ```
  2. Functions and/or classes imported from the standard library and/or any popular publicly-available packages installable via `pip` or `uv`, e.g.:
  ```python
  from datetime import timedelta
  from fastapi import (
    FastAPI,
    status,
  )
  from json import (
    dumps,
    loads,
  )
  from pydantic import BaseModel
  from typing import (
    Any,
    Self,
  )
  ```
  3. Functions and/or classes imported from `sofia_utils` or `wa_agents`.
  4. Functions and/or classes imported from local modules.
* Within each of the previous sections, sort the declarations alphabetically.
* Leave a blank line between sections.
* When importing multiple functions and/or classes from a single module, use parenthesis to declare each function/class in a separate line. E.g.:
```python
from .basemodels import (
  ProductData,
  TaxData,
  UserData,
)
```

## Docstring Style Guidelines

### Text

Use the guidelines in [`markdown.md`](markdown.md).

### Functions

* Triple double quotes on their own lines.
* NEVER put the entire docstring in single line.
* Space and `\\` after the function/method description.
* Separate the summary from `Args:`, `Returns:`, or `Raises:` with a blank line.
  No trailing backslash marker is required.
* Align argument descriptions within each docstring.
* Explain argument meaning, units, constraints, side effects, and failure behavior rather than repeating annotations.
* Omit `Args:` and `Returns:` when they would only restate obvious information.
* Document when `None` is returned and what it means.
  For dependent return values, describe which input or condition selects each result.
* Add `Raises:` for exceptions callers are expected to handle;
  do not list every possible implementation exception.

**EXAMPLES:**

✅ Good for simple functions:
```python
def function( argument1 : type_1, arg2 : type_2) -> return_type :
    """
    Explanation of function's main goal
    """
```
✅ Good for complex functions:
```python
def function( argument1 : type_1, arg2 : type_2) -> return_type :
    """
    Function or method to do some things \\
    Args:
        argument1 : Relevant info about this argument...
        arg2      : Relevant info about this argument...
    Returns:
        Relevant info about the returned object
    """
```
❌ Bad:
```python
def function( argument1 : type_1, arg2 : type_2) -> return_type :
    """Awful explanation of function's main goal"""
```

### Constants (Including Class Variables)

* If it fits, write the entire docstring in a single line, with spaces separating the first and last characters from the triple double quotes.
* If it does not fit in a single line, do the same as with functions.

**EXAMPLES:**

✅ Good:
  ```python
  SOME_CONSTANT = 42
  """ Explanation of constant's meaning or goal """
  ```
✅ Good:
  ```python
  SOME_OTHER_CONSTANT = 0
  """
  Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor.
  """
  ```
❌ Bad:
  ```python
  YET_ANOTHER_CONSTANT = None
  """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor."""
  ```
