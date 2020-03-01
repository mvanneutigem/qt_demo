"""Utility methods for qt demo."""

def pixel_to_point(pixel, dpi):
    """Convert pixel to point size.

    Args:
        pixel (float): pixel size.
        dpi (float): dots per inch.
    """
    return pixel*72/dpi