# TypeScript Code Style Guidelines

* Max line length: **92 characters**
  * Apply to code
  * DO NOT apply to comments, Markdown or docs.
* My editor is in **portrait mode**, so vertical readability is preferred over horizontal density.

## Variable Naming

* Variables, functions, and method names: `camelCase`
* React components, classes, interfaces, and type aliases: `PascalCase`
* Constants that are truly constant and global-like may use `UPPER_SNAKE_CASE`
* File names:
  * React components: `PascalCase.tsx`
  * Utility/modules/hooks: `camelCase.ts` or kebab-case if the project already uses that convention
* Boolean variables should read clearly as booleans:
  * ✅ `isOpen`, `hasError`, `canSubmit`, `shouldRefresh`

## General TypeScript / Frontend Conventions

* Prefer **explicit types when they improve readability**
* Avoid adding types that are obvious from immediate assignment unless they clarify intent
* When a matching backend-generated shape already exists in `~/customer-loyalty/frontend/src/basemodels.d.ts`, prefer reusing it instead of redefining an equivalent local type
  * Those declarations are defined in the backend and automatically translated to
    TypeScript, which helps maintain type safety and coordinate work between
    frontend and backend devs
  * For new local frontend-only definitions, prefer `type` over `interface` unless there is a specific reason to use `interface`
* Prefer union types over overly generic abstractions
* Prefer small, readable helper functions over dense inline logic
* In React, prefer:
  * clear prop types
  * small components
  * derived values near where they are used
  * early returns for conditional rendering

## Preferred Formatting Style

I generally follow the normal TypeScript / React ecosystem style. However, I prefer to **add extra spaces in specific places** for better readability, especially in the context of my vertical screen setup. These preferences are listed below.

### Assignments

* Leave a space before and after the equal sign.
* ✅ Example:
  * `const value = 10;`

### Arrays and Objects (with 2+ elements)

* Leave a space between the opening bracket/brace and the first item
* Leave a space after each comma
* For objects, leave a space before and after each colon between key and value
* ✅ Examples:
  * `const items = [ item1, item2, item3 ];`
  * `const obj = { key1 : value1, key2 : value2 };`

### Array Methods and Inline Callbacks

* Prefer vertically expanded callbacks when logic is not trivial
* Keep one-line callbacks only when they remain very readable
* ✅ Examples:
  * `const ids = items.map(item => item.id);`
  * ```ts
    const visibleItems = items.filter(
        item => item.isVisible && item.count > 0
    );
    ```

### Object Literals and Return Objects

* For short objects, inline is fine
* For denser objects, prefer one property per line
* Keep spacing style consistent with the rest of the file
* ✅ Example:
  ```ts
  const payload = {
      userId   : user.id,
      isAdmin  : user.isAdmin,
      metadata : extraData,
  };
  ```

### Function and Method Definitions

* Leave a space between the opening parenthesis and the first argument when there are multiple arguments or when the definition spans multiple lines
* Leave a space before and after colons used in type annotations
* Do **not** leave a space before the closing parenthesis
* Leave a space before and after the `=>` in function type declarations
* ✅ Examples:
  * `function parseValue( value : string) : number {`
  * `const formatLabel = ( value : string, count : number) : string => {`
  * `const handler = ( event : React.MouseEvent<HTMLButtonElement>) : void => {`

### Function and Method Calls

* Single argument:
  * Leave no spaces
  * ✅ Example:
    * `formatValue(value);`

* Multiple arguments:
  * Leave a space between the opening parenthesis and the first argument
  * Leave a space after each comma
  * Do **not** leave a space before the closing parenthesis
  * ✅ Examples:
    * `setValue( key, value);`
    * `updateItem( id, nextState, options);`

### Conditionals and Loops

* Leave a space before the opening brace
* Prefer braces even for short blocks
* ✅ Examples:

  * `if (condition) {`
  * `for (const item of items) {`

### Type Annotations

* Prefer modern union syntax with `|`
  * ✅ `value : string | null`
* Prefer arrays as `Type[]` for simple cases
  * ✅ `items : string[]`
* Use `Array<Type>` when nested generics are clearer
* Prefer precise literal unions when possible
  * ✅ `status : 'idle' | 'loading' | 'error' | 'success'`
* Avoid `any` unless there is a very good reason
* Prefer `unknown` over `any` when the type is genuinely not known yet

### Nullish / Optional Values

* Prefer `value : Type | null` when null is a meaningful state
* Prefer optional properties only when the property may truly be absent
  * ✅ `label? : string`
* Prefer `??` over `||` when you specifically want nullish fallback
  * ✅ `const name = user.name ?? 'Unknown';`

### Assignment Blocks

* When writing a cluster of related assignments, align the equal signs so the
  values form a clean vertical column
  * ✅
    ```ts
    const checkComponentsFlag  = shouldCheckComponents(data);
    const checkConnectionsFlag = shouldCheckConnections(data);
    const checkOthersFlag      = shouldCheckOthers(data);
    ```
* Do something similar when declaring objects and function arguments
  * ✅
    ```ts
    const options = {
        debug      : false,
        retries    : 3,
        timeoutMs  : 5000,
    };
    
    function newMethod(
        comp      : string,
        compProbs : string[] = [],
        debug     : boolean  = false,
    ) : string[] | null {
        ...
    }
    ```
* Leave a blank line before the assignment block and after it so each cluster reads like its own paragraph

## React-Specific Guidelines

### Components

* Prefer function components
* Keep components focused and not overly long
* Extract repeated JSX into small subcomponents when it improves readability
* Prefer early returns over deeply nested conditional rendering
* ✅ Example:
  ```tsx
  if (!user) {
      return null;
  }
  ```

### Props

* Define props with a named `type`
* Keep prop names descriptive
* Destructure props in the parameter list when the component stays readable
* ✅ Example:
  ```tsx
  type UserCardProps = {
      name      : string;
      email     : string;
      isPremium : boolean;
  };
  
  export function UserCard( { name, email, isPremium } : UserCardProps) {
      ...
  }
  ```

### State

* Keep state minimal
* Prefer derived values instead of storing redundant state
* Group related state only when they truly belong together
* Use clear names for setter functions
  * ✅ `isOpen / setIsOpen`
  * ✅ `selectedItem / setSelectedItem`

### Event Handlers

* Use descriptive names:
  * ✅ `handleSubmit`
  * ✅ `handleDeleteClick`
  * ✅ `handleInputChange`
* Keep event handlers short when possible
* Move heavy logic into helpers instead of keeping everything inside JSX

### JSX Formatting

* Prefer multi-line JSX when props or children become dense
* One prop per line when the tag becomes hard to scan
* Keep conditional expressions readable; extract them if needed
* ✅ Example:
  ```tsx
  <Button
      disabled={isLoading}
      onClick={handleSubmit}
      variant="primary"
  >
      Save
  </Button>
  ```

## Imports

* Group imports logically:
  1. External libraries
  2. Internal components/hooks/utils/types
  3. Local relative imports
* Keep import blocks clean and easy to scan
* Prefer named exports unless there is a strong reason to use default exports

## Comments

* Write comments for **intent**, not for obvious mechanics
* Prefer short explanations above the relevant block
* Avoid redundant comments like:
  * ❌ `// increment i`
* Prefer:
  * ✅ `// Keep this separate so the loading skeleton matches final layout`

# TypeScript / JSDoc Style Guidelines

* Use JSDoc sparingly for exported functions, reusable utilities, and components whose behavior is not obvious
* No need to repeat what TypeScript already states clearly through the type system
* What matters most is relevant behavioral information

Example:
```ts
/**
 * Formats a price for display in the current UI \\
 * @param value Currency amount before formatting
 * @param locale Optional locale override for formatting
 * @returns Formatted display string for the UI
 */
function formatPrice( value : number, locale? : string) : string {
    ...
}
```

### Functions that Return Something or Null

```ts
/**
 * Finds the active customer record \\
 * @param customerId Internal customer identifier
 * @returns If a matching active customer exists, returns that object;
 *          otherwise returns null.
 */
function getActiveCustomer( customerId : string) : Customer | null {
    ...
}
```

### Functions With Dependent Return Type

```ts
/**
 * Builds a value for the requested mode \\
 * @param mode Determines which kind of result is returned
 * @returns Result depends on `mode`:
 *          `'text'`: returns a string
 *          `'count'`: returns a number
 *          `'full'`: returns a full metadata object
 */
function buildResult(
    mode : 'text' | 'count' | 'full',
) : string | number | ResultObject {
    ...
}
```

# Practical Note

These rules are intended as **human readability guidelines**. Some of the spacing preferences above intentionally differ from standard Prettier output.

If the frontend project uses Prettier or ESLint auto-formatting, then:
* Let the formatter win for automatic consistency, or
* Use these rules as a writing/style guide for code structure, naming, vertical layout, and readability rather than trying to force every spacing preference mechanically
