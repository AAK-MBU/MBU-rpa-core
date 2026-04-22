# MBU-rpa-core

Core library for RPA processes.

`mbu_rpa_core` provides shared building blocks that RPA processes in the MBU department can rely on: a managed database connection, helpers for constants and encrypted credentials, heartbeat and event logging, symmetric encryption, custom exception types, and standardized process completion states.

## Features

- **Managed database connection** – `RPAConnection` is a context manager wrapping a pyodbc connection with automatic commit/rollback on exit.
- **Constants and credentials store** – helpers to add, fetch, and update application constants and encrypted credentials in the RPA database.
- **Event and heartbeat logging** – write log entries and service heartbeats to the RPA database, and read them back.
- **Stored procedure execution** – call stored procedures with typed parameters and get a structured result back.
- **Fernet encryption** – `Encryptor` for symmetric encryption/decryption of sensitive values such as passwords.
- **Custom RPA exceptions** – `BusinessError` and `ProcessError` (both inheriting from `BaseRPAError`) with Pydantic validation.
- **Process completion states** – `CompletedState` model with `completed` / `completed_with_exception` factory methods.

## Project structure

```
mbu_rpa_core/
├── database/
│   ├── connection.py     # RPAConnection context manager
│   ├── constants.py      # Constants and credentials helpers
│   ├── logging.py        # Event logging and heartbeats
│   └── utility.py        # execute_query / execute_stored_procedure
├── utils/
│   └── fernet_encryptor.py
├── tests/
├── exceptions.py         # BaseRPAError, BusinessError, ProcessError
└── process_states.py     # CompletedState, StateType
```

## Installation

```bash
pip install mbu_rpa_core
```

Requires Python 3.8 or newer. Runtime dependencies: `pydantic>=2.0.0`, `pyodbc`, `python-dateutil`, `python-dotenv`, `cryptography`.

## Usage

### Opening a connection

`RPAConnection` must be used as a context manager. Work committed only if `commit=True` is passed; otherwise the transaction is rolled back on exit.

```python
from mbu_rpa_core.database import RPAConnection

with RPAConnection(db_env="PROD", commit=True) as rpa_conn:
    rpa_conn.add_constant("MyConstant", "some value")
```

### Constants

```python
with RPAConnection(db_env="TEST", commit=True) as rpa_conn:
    rpa_conn.add_constant("RetryLimit", "3")
    value = rpa_conn.get_constant("RetryLimit")
    rpa_conn.update_constant("RetryLimit", "5")
```

### Credentials (encrypted passwords)

```python
with RPAConnection(db_env="PROD", commit=True) as rpa_conn:
    rpa_conn.add_credential("ServiceAccount", username="svc_user", password="s3cret")
    creds = rpa_conn.get_credential("ServiceAccount")
    # creds = {"username": ..., "decrypted_password": ..., "encrypted_password": ...}
```

### Executing queries and stored procedures

```python
with RPAConnection(db_env="PROD", commit=False) as rpa_conn:
    rows = rpa_conn.execute_query(
        "SELECT id, name FROM [test] WHERE active = ?",
        params=[1],
        return_dict=True,
    )

    result = rpa_conn.execute_stored_procedure(
        stored_procedure="rpa.sp_DoWork",
        params={
            "ItemId": (int, 42),
            "Payload": ("json", {"key": "value"}),
        },
    )
    # result = {"success": True, "error_message": None, "rows_updated": ...}
```

Stored-procedure parameters are passed as a dict where each value is a `(type, value)` tuple. Supported type keys are `"str"`, `"int"`, `"float"`, `"datetime"` (parsed with `dateutil`), and `"json"` (serialized via `json.dumps`).

### Event logging and heartbeats

```python
with RPAConnection(db_env="PROD", commit=True) as rpa_conn:
    rpa_conn.log_event(
        log_db="Logs",
        level="INFO",
        message="Process started",
        context="MyProcess",
    )
    latest = rpa_conn.get_latest_log(log_db="rpa.Logs")

    # Send a heartbeat loop (runs until `stop` becomes True)
    rpa_conn.log_heartbeat(
        stop=False,
        servicename="MyProcess",
        heartbeat_interval=30,
        details="main loop",
    )
```

### Encryption

```python
from mbu_rpa_core.utils.fernet_encryptor import Encryptor

encryptor = Encryptor()
token = encryptor.encrypt("my secret")
plaintext = encryptor.decrypt(token)
```

### Exceptions and process states

```python
from mbu_rpa_core.exceptions import BusinessError, ProcessError
from mbu_rpa_core.process_states import CompletedState

# Raise domain-specific errors
raise BusinessError("Invoice number is missing")
raise ProcessError("Upstream service did not respond")

# Report process outcome
state = CompletedState.completed("All 120 records processed")
state_with_issues = CompletedState.completed_with_exception("3 records skipped")
```

## Development

Install the package with its development extras and run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

The repository ships with GitHub Actions workflows for linting (`pylint`), unit tests, version-number validation on PRs, release branch creation, and publishing to PyPI.

## License

Released under the [MIT License](./LICENSE).

## Repository

<https://github.com/AAK-MBU/MBU-rpa-core>