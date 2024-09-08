from backend.processing.detection.grid import BasicGridDetector
from backend.processing.detection.preprocessors import CannyPreprocessor


class CrossWordPipeline:
    def __init__(self):
        pass

    def warp_perspective(self):
        pass

    def resize_image(self):
        pass

    def process(self, image):
        # Apply the pipeline to the image
        pass


class ImagePipeline:
    def __init__(self):
        self.default_preprocessor = CannyPreprocessor()
        self.squares_detector = BasicGridDetector()
        self.grid_detector = BasicGridDetector()
        self.crossword_pipeline = CrossWordPipeline()

    def check_if_crossword(self, grid, image):
        pass

    def crop_crossword(self, grid, image):
        pass

    def process(self, image):
        # Apply the pipeline to the image
        processed_img = self.default_preprocessor.preprocess(image)

        squares = self.squares_detector.detect(processed_img)

        grids = self.grid_detector.detect(processed_img, squares)

        for grid in grids:
            if not self.check_if_crossword(grid, image):
                continue

            crossword_image = self.crop_crossword(grid, image)

            self.crossword_pipeline.process(crossword_image)
