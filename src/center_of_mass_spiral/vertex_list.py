import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class VertexList:
    name: str
    vertices: np.ndarray
    is_closed: bool
    is_discrete: bool
    num_repeat: int = 1

    def __post_init__(self):
        vertices_copy = self.vertices.copy()
        vertices_copy.flags.writeable = False
        # Use object.__setattr__ to bypass the frozen=True restriction
        object.__setattr__(self, 'vertices', vertices_copy)
