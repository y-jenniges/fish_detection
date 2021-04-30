Post Processing 
================
Functions and classes necessary for post processing.

``StereoCorrespondence`` class
********************************
.. autoclass:: PostProcessing.StereoCorrespondence
    :members:
    :undoc-members:
    :show-inheritance:
	
Functions
**************
.. autofunction:: PostProcessing.applyNnToImage(model, image) 
.. autofunction:: PostProcessing.applyThresholdToHm(image, threshold=50)
.. autofunction:: PostProcessing.findCoordinates(heatmap, threshold=50, radius=20)
.. autofunction:: PostProcessing.findHeadTailMatches(heads, tails)
.. autofunction:: PostProcessing.loadImage(fname, factor=32, rescale_range=True)
.. autofunction:: PostProcessing.measureLength(distance_measurer, camera_config, merged_objects)
.. autofunction:: PostProcessing.nonMaxSuppression(image, min_distance=20)
.. autofunction:: PostProcessing.rectifyAndMatch(matcher, camera_config, left_image_path, right_image_path, objects_left)
.. autofunction:: PostProcessing.resizeHm(img, hm)
.. autofunction:: PostProcessing.scaleMatchCoordinates(matches, input_res, output_res)
.. autofunction:: PostProcessing.weightedEuclidean(x, y)