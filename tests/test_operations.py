import numpy as np
import pytest
from center_of_mass_spiral import (
    VertexList, reverse, append, prepend, close, join, repeat
)


class TestReverse:
    """Test the reverse operation."""

    def test_reverse_open_shape(self):
        """Test reversing an open vertex list."""
        vertices = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        result = reverse(vl)

        assert result.name == "test/reversed"
        assert len(result.vertices) == 3
        assert np.allclose(result.vertices[0], [1.0, 1.0])
        assert np.allclose(result.vertices[1], [1.0, 0.0])
        assert np.allclose(result.vertices[2], [0.0, 0.0])
        assert result.is_closed == False
        assert result.is_discrete == False

    def test_reverse_closed_shape(self):
        """Test reversing a closed vertex list."""
        vertices = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 0.0]  # Closing vertex
        ])
        vl = VertexList(name="square", vertices=vertices,
                        is_closed=True, is_discrete=False)

        result = reverse(vl)

        assert result.name == "square/reversed"
        assert len(result.vertices) == 4
        assert result.is_closed == True
        # First and last should still match after reversal
        assert np.allclose(result.vertices[0], result.vertices[-1])

    def test_reverse_preserves_flags(self):
        """Test that reverse preserves all flags."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=True, num_repeat=3)

        result = reverse(vl)

        assert result.is_discrete == True
        assert result.num_repeat == 3


class TestAppend:
    """Test the append operation."""

    def test_append_basic(self):
        """Test appending a vertex without refinement."""
        vertices = np.array([
            [0.0, 0.0],
            [1.0, 0.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        new_vertex = np.array([1.0, 1.0])
        result = append(vl, new_vertex, refine=False)

        assert result.name == "test/append"
        assert len(result.vertices) == 3
        assert np.allclose(result.vertices[-1], new_vertex)
        assert result.is_closed == False

    def test_append_with_refine(self):
        """Test that refine inserts intermediate vertices for large distances."""
        vertices = np.array([
            [0.0, 0.0],
            [1.0, 0.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        # Append a vertex far away - should trigger refinement
        new_vertex = np.array([10.0, 0.0])
        result = append(vl, new_vertex, refine=True)

        # Should have more than 3 vertices due to refinement
        assert len(result.vertices) > 3
        # First vertex unchanged
        assert np.allclose(result.vertices[0], vertices[0])
        # Last vertex is the new one
        assert np.allclose(result.vertices[-1], new_vertex)

    def test_append_to_closed_warns(self):
        """Test that appending to closed shape returns original."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 0.0, 0.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=True, is_discrete=False)

        new_vertex = np.array([2.0, 2.0, 2.0])
        result = append(vl, new_vertex)

        # Should return original
        assert result is vl

    def test_append_invalid_vertex_shape(self):
        """Test that invalid vertex shape raises error."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        with pytest.raises(ValueError, match="must have 3 coordinates"):
            append(vl, np.array([1.0, 2.0]))  # Only 2 coordinates


class TestPrepend:
    """Test the prepend operation."""

    def test_prepend_basic(self):
        """Test prepending a vertex without refinement."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        new_vertex = np.array([-1.0, 0.0, -1.0])
        result = prepend(vl, new_vertex, refine=False)

        assert result.name == "test/prepend"
        assert len(result.vertices) == 3
        assert np.allclose(result.vertices[0], new_vertex)
        assert result.is_closed == False

    def test_prepend_with_refine(self):
        """Test that refine inserts intermediate vertices for large distances."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        # Prepend a vertex far away - should trigger refinement
        new_vertex = np.array([-10.0, 0.0, -10.0])
        result = prepend(vl, new_vertex, refine=True)

        # Should have more than 3 vertices due to refinement
        assert len(result.vertices) > 3
        # First vertex is the new one
        assert np.allclose(result.vertices[0], new_vertex)
        # Last vertex unchanged
        assert np.allclose(result.vertices[-1], vertices[-1])

    def test_prepend_to_closed_warns(self):
        """Test that prepending to closed shape returns original."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 0.0, 0.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=True, is_discrete=False)

        new_vertex = np.array([-1.0, -1.0, -1.0])
        result = prepend(vl, new_vertex)

        # Should return original
        assert result is vl


class TestClose:
    """Test the close operation."""

    def test_close_open_shape(self):
        """Test closing an open shape."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 2.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        result = close(vl, refine=False)

        assert result.name == "test/closed"
        assert result.is_closed == True
        assert len(result.vertices) == 4
        # First and last should match
        assert np.allclose(result.vertices[0], result.vertices[-1])

    def test_close_already_closed_geometrically(self):
        """Test closing a shape that's already closed geometrically."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 2.0],
            [0.0, 0.0, 0.0]  # Already closed
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        result = close(vl, refine=False)

        assert result.is_closed == True
        # Should not add extra vertex
        assert len(result.vertices) == 4

    def test_close_with_refine(self):
        """Test closing with refinement for large gaps."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [10.0, 0.0, 10.0]  # Far from origin
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=False, is_discrete=False)

        result = close(vl, refine=True)

        assert result.is_closed == True
        # Should have intermediate vertices
        assert len(result.vertices) > 4
        # First and last should match
        assert np.allclose(result.vertices[0], result.vertices[-1])

    def test_close_already_closed_warns(self):
        """Test that closing already closed shape returns original."""
        vertices = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 0.0, 0.0]
        ])
        vl = VertexList(name="test", vertices=vertices,
                        is_closed=True, is_discrete=False)

        result = close(vl)

        # Should return original
        assert result is vl


class TestJoin:
    """Test the join operation."""

    def test_join_basic(self):
        """Test joining two vertex lists."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vertices2 = np.array([
            [2.0, 0.0, 2.0],
            [3.0, 0.0, 3.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=False, is_discrete=False)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=False)

        result = join(vl1, vl2, refine=False)

        assert result.name == "first+second"
        assert len(result.vertices) == 4
        assert result.is_closed == False
        assert np.allclose(result.vertices[0], vertices1[0])
        assert np.allclose(result.vertices[-1], vertices2[-1])

    def test_join_with_duplicate_endpoint(self):
        """Test joining when last vertex of first equals first vertex of second."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vertices2 = np.array([
            [1.0, 0.0, 1.0],  # Duplicate
            [2.0, 0.0, 2.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=False, is_discrete=False)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=False)

        result = join(vl1, vl2, refine=False)

        # Should remove duplicate
        assert len(result.vertices) == 3
        assert np.allclose(result.vertices[0], [0.0, 0.0, 0.0])
        assert np.allclose(result.vertices[1], [1.0, 0.0, 1.0])
        assert np.allclose(result.vertices[2], [2.0, 0.0, 2.0])

    def test_join_with_refine(self):
        """Test joining with refinement for large gap."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vertices2 = np.array([
            [10.0, 0.0, 10.0],
            [11.0, 0.0, 11.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=False, is_discrete=False)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=False)

        result = join(vl1, vl2, refine=True)

        # Should have intermediate vertices
        assert len(result.vertices) > 4

    def test_join_closed_raises_error(self):
        """Test that joining closed shapes raises error."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 0.0, 0.0]
        ])
        vertices2 = np.array([
            [2.0, 0.0, 2.0],
            [3.0, 0.0, 3.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=True, is_discrete=False)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=False)

        with pytest.raises(ValueError, match="Both vertex lists must be open"):
            join(vl1, vl2)

    def test_join_mismatched_discrete_raises_error(self):
        """Test that joining with mismatched is_discrete flags raises error."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vertices2 = np.array([
            [2.0, 0.0, 2.0],
            [3.0, 0.0, 3.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=False, is_discrete=False)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=True)

        with pytest.raises(ValueError, match="different is_discrete flags"):
            join(vl1, vl2)

    def test_join_preserves_discrete_flag(self):
        """Test that join preserves is_discrete flag when both match."""
        vertices1 = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0]
        ])
        vertices2 = np.array([
            [2.0, 0.0, 2.0],
            [3.0, 0.0, 3.0]
        ])
        vl1 = VertexList(name="first", vertices=vertices1,
                         is_closed=False, is_discrete=True)
        vl2 = VertexList(name="second", vertices=vertices2,
                         is_closed=False, is_discrete=True)

        result = join(vl1, vl2)

        assert result.is_discrete == True
