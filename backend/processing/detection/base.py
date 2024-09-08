class Preprocessor:
    def __init__(self):
        pass

    def process(self, image):
        raise NotImplementedError


class SquaresDetector:
    def __init__(self):
        pass

    def detect(self, image):
        raise NotImplementedError


class GridDetector:
    def __init__(self):
        pass

    def detect(self, image, squares):
        raise NotImplementedError


class ArrowDetector:
    def __init__(self):
        pass

    def detect(self, image, grid):
        raise NotImplementedError
