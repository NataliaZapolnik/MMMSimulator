from typing import List

class Parameters:
    a1: float
    a0: float
    b2: float
    b1: float
    b0: float
    kp: float
    ki: float
    amplitude: float
    frequency: float
    duration: float
    dt: float

class Simulation:
    def __init__(self, signal_type: InputSignalType, signal_parameters: Parameters): ...
    def get_input(self) -> List[float]: ...
    def get_output(self) -> List[float]: ...
    def get_error(self) -> List[float]: ...
    def get_control(self) -> List[float]: ...

class InputSignalType:
    SINUS: InputSignalType
    SQUARE: InputSignalType
    TRIANGLE: InputSignalType

def export_to_csv(signal: List[float], filename: str, dt: float = ...) -> None: ...
