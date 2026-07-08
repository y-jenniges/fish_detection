Post Processing 
================
Functions and classes necessary for post processing.

``StereoCorrespondence`` class
********************************
.. autoclass:: maromarker.processing.post_processing.StereoCorrespondence
    :members:
    :undoc-members:
    :show-inheritance:
	
``RectifyMatchWorker`` class
********************************
.. autoclass:: maromarker.processing.post_processing.RectifyMatchWorker
    :members:
    :undoc-members:
    :show-inheritance:
	
Functions
**************
.. autofunction:: maromarker.processing.post_processing.applyNnToImage(model, image) 
.. autofunction:: maromarker.processing.post_processing.applyThresholdToHm(image, threshold=50)
.. autofunction:: maromarker.processing.post_processing.findCoordinates(heatmap, threshold=50, radius=20)
.. autofunction:: maromarker.processing.post_processing.findHeadTailMatches(heads, tails)
.. autofunction:: maromarker.processing.post_processing.loadImage(fname, factor=32, rescale_range=True)
.. autofunction:: maromarker.processing.post_processing.nonMaxSuppression(image, min_distance=20)
.. autofunction:: maromarker.processing.post_processing.resizeHm(img, hm)
.. autofunction:: maromarker.processing.post_processing.scaleMatchCoordinates(matches, input_res, output_res)
.. autofunction:: maromarker.processing.post_processing.weightedEuclidean(x, y)