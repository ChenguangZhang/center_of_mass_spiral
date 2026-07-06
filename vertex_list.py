import numpy as np
from dataclasses import dataclass


@dataclass
class VertexList:
    name: str
    vertices: np.ndarray
    is_closed: bool
    is_discrete: bool
