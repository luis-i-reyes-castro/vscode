# Markdown Typesetting Preferences

## Text

* No line length limit; IDE takes care of line wrapping.
* One sentence per line so that we can keep version control at the sentence-level.

### Example

```text
The submodule is a Python package under `backend/case_handlers/ieced`.
Its autocomplete handler and endpoint functions are in `casehandler_for_autocomplete.py`, its async booking handler and presentation data are in `casehandler_for_booking.py`, and its async MariaDB code remains in the package-local `database_io` module.
The app constructor (`backend/app.py`) registers handler key `ieced` and the legacy `/webhook` and `/data_retrieval_test` paths directly.

Route `GET /diagnostics` dispatches by preserved host header.
IECED domains receive the MariaDB/OpenRouter result;
Sofia domains and localhost receive Sofia diagnostics.
All businesses continue to use the shared `/whatsapp` callback and `wa_agents.case_handler_routes` selects their handler.

The backend image includes Connector/Python, `pdftotext`, and Poppler development libraries.
Configured `backend/.dockerignore` prevents nested `.env`/`.git data`, caches, local queues, `tmp/`, patient exports, and result sets from entering the build context.
```

## Tables

* If you can keep the entire table in ≤ 92 chars wide then do align the columns.
* Else, align only the left side columns that fit in ≤ 92 chars and use regular spacing between columns after the limit, i.e., " | ".

## Code Blocks

* Use the corresponding typesetting rules found in this same directory.
  * [Python](typesetting/python.md)
  * [SQL](typesetting/sql.md)
  * [Typescript](typesetting/typescript.md) (only for `sofia-server`'s frontend)
* If the code block is preceded by text referring to the code, e.g., "Run the code below:", do not leave a space between the text and the code block.
