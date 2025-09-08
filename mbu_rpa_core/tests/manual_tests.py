"""Manual tests"""

from pydantic import ValidationError
from mbu_rpa_core.exceptions import BusinessError
from mbu_rpa_core.process_states import CompletedState


if __name__ == '__main__':
    try:
        state = CompletedState.completed("")
    except BusinessError as be:
        print(be)
    except Exception as e:
        print("error")
        print(e)
        print(isinstance(e, ValidationError))
