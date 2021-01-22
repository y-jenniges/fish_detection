# CNN to Detect and Classify Marine Organisms

**DataGenerator:**
The DataGenerator generates batches of data such that not all images need 
to be kept in memory. 
!! Adapt the OPTION parameter in the DataGenerator depending on the network
you want to run !!

**Heatmap Class:**
It facilititates the creation of heatmaps. Here, a heatmap is defined as 
a grayscale image (range [0, 1]). The value of each pixel denotes the probability
of an object at that pixel position.

**Network Output:**
The highRes networks output heatmaps at half of the input image resolution.
The lowRes networks output heatmaps at 1/32 of the input image resolution.
There is a total of 11 classes (one per output channel): 
  1. background
  2. fish head
  3. fish tail
  4. crustacea head
  5. crustacea tail
  6. chaetognatha head
  7. chaetognatha tail
  8. unidentified head
  9. unidentified tail
  10. jellyfish head
  11. jeyllfish tail

## Neural networks for fish head class 
- lowRes_fishHeads_allLayers
	Uses MobileNetV2 as backbone. All backbone layers are included in the 			
	training process. 
	
- lowRes_fishHeads_allLayersDelayed
	Uses MobileNetV2 as backbone. All backbone layers are unfrozen after
	10 epochs of training.

- lowRes_fishHeads_lastLayers
	Uses MobileNetV2 as backbone. The last 28 layers are unfrozen and hence
	included in training.

- lowRes_fishHeads_noLayers
	Uses MobileNetV2 as backbone. All backbone layers are frozen, i.e. are
	not trained.

- minimalistic_cnn
	A CNN inspired by VGG16 architecture. It does not use the DataGenerator
	and MobileNet for transfer learning.


## Neural networks for all classes 
- highRes_allAnimals
	Outputs 11 channels (one per class), each outputting a heatmap for the
	respective class.

- highRes_allAnimals_weighted
	Similar to highRes_allAnimals. Additionally, it applies weights to the
	classes.


## Different connection encodings 
- highRes_segmentation
	Basic architecture similar to highRes_allAnimals_weighted. Additionally,
	it outputs one more channel that displays the connection between heads
	and tails, i.e. animal bodies (encoded in form of a thick line). 

- lowRes_vectors
	Basic architecture similar to highRes_allAnimals_weighted. Additionally,
	four more output channels are added to output two vector fields (one for 
	head-tail vectors, one for tail-head vectors)

- lowRes_vectors_focused
	Similar to lowRes_vectors, but uses a custom loss for the vector fields.
	It only applies the loss to areas where head and tail heatmaps are white.