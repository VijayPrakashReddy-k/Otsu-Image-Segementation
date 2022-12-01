# Otsu-Image-Segementation
OTSU method is a global adaptive binarization threshold image segmentation algorithm.

### Image thresholding with Otsu method

◉ Image thresholding is a process for separating the foreground and background of the image. There are lots of methods for image thresholding, Otsu method is one of the methods proposed by **Nobuyuki Otsu**. The Otsu algorithm is a variance-based way to automatically find a threshold value by which the weighted variance between foreground and background is the least.

◉ With different threshold value, the pixel values of foreground and background are various. Hence, both pixels have different variance for different thresholding. The key of Otsu algorithm is to calculate the total variance from the two variances of both distributions. The process needs to iterate through all the possible threshold vlaues and find a threshold that makes the total variance is smallest.

### Image Binarization

**Definition** : `Image binarization applies often just one global threshold T for mapping a scalar image I into a binary image.`

◉ The global threshold can be identified by an optimization strategy aiming at creating "large" connected regions and at reducing the number of small-sized regions, called **"Artifacts"**.

```math
J(x,y) = \begin{cases} 0 &\text{if } I(x,y) < T \\ 1 &\text Otherwise \end{cases}

```

### Otsu Thresholding

**Definition** : `The method uses grey-value histogram of the given image I as input and aims at providing the best threshold.`

◉ Otsu’s algorithm selects a threshold that maximizes the between-class variance.

◉ In the case of two classes,

```math
\sigma_{b}^2 = P_{1}(\mu_{1}-\mu)^2 + P_{2}(\mu_{2}-\mu)^2 = P_{1}P_{2}(\mu_{1}-\mu_{2})^2
``` 
where P1 and P2 denote class probabilities, and μi the means of object and background classes.
