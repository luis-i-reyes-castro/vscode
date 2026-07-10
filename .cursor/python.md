# General Guidelines

* Max line length: **92 characters**
* My editor is in **portrait mode**, so vertical readability is preferred over horizontal density.
* Preserve whitespace that supports vertical readability, including indented blank lines.
* Do not run broad trailing-whitespace cleanup commands unless I explicitly ask for that. If `git diff --check` flags whitespace, report it or fix only the exact lines being semantically edited.

# Python Code Style Guidelines

## Variable Naming

* Variables, functions, and method names: `snake_case`
* Class names: `CamelCase`

## PEP 8 Exceptions

I generally follow [PEP 8](https://peps.python.org/pep-0008/) guidelines for writing Python code. However, I prefer to **add extra spaces in specific places** for better readability, especially in the context of my vertical screen setup. These exceptions are listed below.

### Assignments

* Leave a space before and after the equal sign.
* ✅ Example: `value = 10`

### Lists, Tuples, Dictionaries, and Sets (with 2+ elements)

* Leave a space between the opening bracket/brace/parenthesis and the first item.
* Leave a space after each comma.
* For dictionaries, leave a space before and after each colon between key and value.
* ✅ Examples:
  * `my_list = [ item1, item2, item3 ]`
  * `my_dict = { key1 : value1, key2 : value2 }`

### Comprehensions

* Leave a space after the opening bracket/brace/parenthesis.
* Leave a space before the closing bracket/brace/parenthesis.
* For dictionary comprehensions, leave a space before and after each colon.
* ✅ Examples:
  * `[ item for item in items ]`
  * `{ key : value for key, value in items }`

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

### Conditionals and Loops

* Leave a space before the ending colon.
  ✅ Examples:
  `if condition :`
  `for item in list_of_items :`

### Type Annotations

* Prefer [PEP 604](https://peps.python.org/pep-0604/) pipe-style unions over `typing.Optional` / `typing.Union`.
  * ✅ Example: `value : list[str] | None`
  * ❌ Counterexample: `value : Optional[list[str]]`

### Assignment Blocks

* When writing a cluster of related assignments, align the equal signs so the values form a clean vertical column.
  * ✅
    ```python
    check_components_flag  = …
    check_connections_flag = …
    check_others_flag      = …
    ```
  * Do something similar when declaring dictionaries and function arguments. For arguments also align the type hints. E.g.:
    ```python
    new_dict = { components  : …,
                 connections : …,
                 debug       : … }
    …
    new_method( self,
                comp       : str,
                comp_probs : list[str] = [],
                debug      : bool      = False ) -> list | None :
    ```
* Leave a blank line before the assignment block and after it so each cluster reads like its own paragraph.

### Functions that Return Something or None

```python
def function(...) -> return_type | None :
    """
    Function or method to do some things \\
    Args:
        ...
    Returns:
        If (some condition) then (some object); else None.
    """
```

### Functions With Dependent Return Type

```python
def function( ...,
              arg_k : type_k,
              ...
            ) -> return_type_1 | return_type_2 | ... :
    """
    Function or method to do some things \\
    Args:
        ...
    Returns:
        Result depends on the value of `arg_k`:
        `value_1`: Result is (some type of object)
        `value_2`: Result is (some other type of object)
        ...
    """
```

## Imports

* Declare the imports in sections according to the following order:
  1. Standard library modules imported at the module-name level, e.g., `import os`, `import re`.
  2. Functions and/or classes imported from the standard library and/or external packages (installed via `pip` or `uv`), e.g., `from pydantic import BaseModel`, `from json import dumps`.
  3. Functions and/or classes imported from `sofia_utils` or `wa_agents`.
  4. Functions and/or classes imported from local modules.
* Within each of the previous sections, sort the declarations alphabetically.
* Leave a blank line between sections.
* When importing multiple functions and/or classes from a single module, use parenthesis to declare each function/class in a separate line. E.g.:
```python
from basemodels import ( ProductData,
                         TaxData,
                         UserData )
```

## Docstring Style Guidelines

* Space and `\\` after the function/method description
* Align the argument descriptions
* No need to re-state argument types or return types, since the IDE already shows them. What I want instead is relevant information.

Example:
```python
def function( argument1 : type_1, arg2 : type_2, ...) -> return_type :
    """
    Function or method to do some things \\
    Args:
        argument1 : Relevant info about this argument...
        arg2      : Relevant info about this argument...
    Returns:
        Relevant info about the returned object
    """
```
