from dataclasses import dataclass

import numpy as np


@dataclass
class SquareDetection:
    text: str | None
    contour: list[int]
    bounding_box: list[int]
    center: list[int]


@dataclass
class CrossWordDetection:
    image: np.ndarray
    x_size: int
    y_size: int
    contour: list[int]
    bounding_box: list[int]
    squares: list[list[SquareDetection]]


@dataclass
class SquareSchema:
    text: str | None


@dataclass
class CrossWordSchema:
    squares: list[list[SquareSchema]]


@dataclass
class CrossWordsSchema:
    crossword: list[CrossWordSchema]
