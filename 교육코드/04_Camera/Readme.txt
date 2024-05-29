
"""
-------------------------------------------------------------------
  FILE NAME: Function_Library.py
  Copyright: Sungkyunkwan University, Embedded System Lab.
-------------------------------------------------------------------
  Authors: Jonghun Kim, HyeongKeun Hong

  Generated: 2022-11-10
  Revised: 2022-11-12
-------------------------------------------------------------------
"""


1. Insert all file ("Function_Library.py", "main.py", "Example Image.jpg") in your pycharm project path, such as "D:\Opencvtest".

2. Then, just find the function you need in "Function_Library.py".

3. If you have anything question, plz contact(or join) me.


-------------------------------------------------------------------

[Function Description]

1. object_detection(img, sample=0, mode="circle", print_enable=False)
	a) Color Filtering: Extract Primary Color
	b) GrayScale Conversion
	c) Hough-Transform (Circle Detection)
	d) HSV Format Conversion
	e) Searching Surrounding Pixels (Prediction using center point of circle)
	f) cv2.circle( ): drawing circle in raw image

2. edge_detection(img, width=0, height=0, gap=0, threshold=0, print_enable=False)
	a) GrayScale Conversion
	b) Histogram Equalization
	c) Morphology - Opening Calculation
	d) Gaussian Blurring Filter
	e) Canny Edge Detection
	f) Hough-Transform (Probability-type Hough T/R)
	g) Line Filtering (Pixel Analyze): Calculate Straight Line Equation 
		-> Gradient: Because 2D-Image Matrix is expressed the third quadrant, so you must calculate straight line equation in third quadrant.)
				grad = (xb - xa) / ((-1) * (yb - ya))
	h) Direction Prediction
	i) cv2.line( ): drawing specific edge line in raw image

