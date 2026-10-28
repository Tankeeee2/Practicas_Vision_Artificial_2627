import cv2
import numpy as np


def fsiv_create_gaussian_filter(r: int) -> np.ndarray:
    """
    Return a Gaussian filter.

    :param r: is the filter's radius.
    :return: the filter.
    :pre: r > 0
    :post: ret_v.dtype == np.float32
    :post: ret_v.shape == (2*r + 1, 2*r + 1)
    :post: abs(np.sum(ret_v) - 1.0) < 1.0e-6
    """
    assert r > 0, "r must be greater than 0"
    ret_v = None
    # TODO
    # Hint: use cv::getGaussianKernel()
    # Hint: use the @ operator to compute the outer product of the vector
    # with its transpose

    #
    assert ret_v.dtype == np.float32, "Return filter must have float32 dtype"
    assert ret_v.shape == (
        2 * r + 1, 2 * r + 1), "Filter must have shape (2*r+1, 2*r+1)"
    assert abs(float(np.sum(ret_v)) -
               1.0) < 1.0e-6, "Filter elements sum must be 1.0 within tolerance"
    return ret_v


def fsiv_create_lap4_filter() -> np.ndarray:
    """
    Create a four-point Laplacian filter.

    :return: the filter.
    :post: ret_v.dtype == np.float32
    :post: ret_v.shape == (3, 3)
    """
    ret_v = None
    # TODO
    # Hint: Use np.array() with a python array to create a ndarray.

    #
    assert ret_v.size > 0, "Filter must not be empty"
    assert ret_v.shape == (3, 3), "Filter must have shape (3, 3)"
    assert ret_v.dtype == np.float32, "Filter must have float32 dtype"
    return ret_v


def fsiv_create_lap8_filter() -> np.ndarray:
    """
    Create an eight-point Laplacian filter.

    :return: the filter.
    :post: ret_v.dtype == np.float32
    :post: ret_v.shape == (3, 3)
    """
    ret_v = None
    # TODO
    # Hint: Use np.array() with a python array to create a ndarray.

    #
    assert ret_v.size > 0, "Filter must not be empty"
    assert ret_v.shape == (3, 3), "Filter must have shape (3, 3)"
    assert ret_v.dtype == np.float32, "Filter must have float32 dtype"
    return ret_v


def fsiv_fill_expansion(in_img: np.ndarray, r: int) -> np.ndarray:
    """
    Expand an image with zero padding.

    :param in_img: is the input image.
    :param r: is the window's radius to expand.
    :return: the expanded image.
    :pre: in_img is not empty
    :pre: r > 0
    :post: ret_v.dtype == in_img.dtype
    :post: ret_v.shape[0] == in_img.shape[0] + 2 * r
    :post: ret_v.shape[1] == in_img.shape[1] + 2 * r
    """
    assert in_img is not None and in_img.size > 0, "Input image must not be empty"
    assert r > 0, "r must be greater than 0"
    ret_v = None
    # TODO:
    # Hint: use cv::copyMakeBorder() using the constant value 0 to fill the
    #       expanded area.

    #
    assert ret_v.dtype == in_img.dtype, "Output dtype must match input dtype"
    assert ret_v.shape[0] == in_img.shape[0] + \
        2 * r, "Output rows must be in.rows + 2*r"
    assert ret_v.shape[1] == in_img.shape[1] + \
        2 * r, "Output cols must be in.cols + 2*r"
    return ret_v


def fsiv_circular_expansion(in_img: np.ndarray, r: int) -> np.ndarray:
    """
    Circular expansion of an image.

    :param in_img: is the input image.
    :param r: is the window's radius to expand.
    :return: the expanded image.
    :pre: in_img is not empty
    :pre: r > 0
    :post: ret_v.dtype == in_img.dtype
    :post: ret_v.shape[0] == in_img.shape[0] + 2 * r
    :post: ret_v.shape[1] == in_img.shape[1] + 2 * r
    """
    assert in_img is not None and in_img.size > 0, "Input image must not be empty"
    assert r > 0, "r must be greater than 0"
    ret_v = None
    # TODO:
    # Hint: use cv::copyMakeBorder() using the constant value 0 to fill the
    #       expanded area.

    #
    assert ret_v.dtype == in_img.dtype, "Output dtype must match input dtype"
    assert ret_v.shape[0] == in_img.shape[0] + \
        2 * r, "Output rows must be in.rows + 2*r"
    assert ret_v.shape[1] == in_img.shape[1] + \
        2 * r, "Output cols must be in.cols + 2*r"
    return ret_v


def fsiv_create_dog_filter(r1: int, r2: int) -> np.ndarray:
    """
    Create a Difference Of Gaussian (DoG) filter.

    :param r1: radius of the first Gaussian filter.
    :param r2: radius of the second Gaussian filter.
    :return: the filter.
    :pre: r1 > 0 and r1 < r2
    :post: ret_v.dtype == np.float32
    :post: ret_v.shape == (2 * r2 + 1, 2 * r2 + 1)
    """
    assert r1 > 0 and r1 < r2, "Condition r1 > 0 and r1 < r2 must hold"
    ret_v = None
    # TODO
    # Hint: use fsiv_create_gaussian_filter() and fsiv_fill_expansion() to
    #       expand the smaller filter to be the same size as the larger one,
    #       so you can get the difference of both.

    #
    assert ret_v.size > 0, "Filter must not be empty"
    assert ret_v.shape == (2 * r2 + 1, 2 * r2 +
                           1), "Filter shape must be (2*r2+1, 2*r2+1)"
    assert ret_v.dtype == np.float32, "Filter dtype must be float32"
    return ret_v


def fsiv_create_sharpening_filter(filter_type: int, r1: int = 1, r2: int = 2) -> np.ndarray:
    """
    Create a sharpening filter.

    :param filter_type: specify what type of Laplacian filter to use: 0->LAP_4, 1->LAP_8, 2->DoG.
    :param r1: if filter_type is 2 (DoG), r1 is the radius for the first Gaussian filter.
    :param r2: if filter_type is 2 (DoG), r2 is the radius for the second Gaussian filter.
    :return: the filter.
    :pre: filter_type in {0, 1, 2}
    :pre: filter_type != 2 or (0 < r1 < r2)
    :post: ret_v.dtype == np.float32
    :post: (filter_type == 2 and ret_v.shape == (2*r2+1, 2*r2+1)) or (filter_type != 2 and ret_v.shape == (3, 3))
    """
    assert 0 <= filter_type <= 2, "filter_type must be in {0, 1, 2}"
    assert filter_type != 2 or (
        0 < r1 < r2), "For DoG filter, 0 < r1 < r2 must hold"
    filt = None
    # TODO
    #  Remember: sharpening filter = -Laplacian + [1]

    #
    assert filt.dtype == np.float32, "Filter must be non-empty float32"
    assert filter_type == 2 or filt.shape == (
        3, 3), "Laplacian filter must be 3x3"
    assert filter_type != 2 or filt.shape == (
        2 * r2 + 1, 2 * r2 + 1), "DoG filter must have shape (2*r2+1, 2*r2+1)"
    return filt


def fsiv_image_sharpening(in_img: np.ndarray, filter_type: int,
                          r1: int = 1, r2: int = 2, circular: bool = False) -> np.ndarray:
    """
    Do a sharpening enhance to an image.

    :param in_img: is the input single-channel image.
    :param filter_type: is the sharpening filter to use: 0->LAP_4, 1->LAP_8, 2->DOG.
    :param r1: if filter_type is DOG, is the radius of the first Gaussian filter.
    :param r2: if filter_type is DOG, is the radius of the second Gaussian filter.
    :param circular: if True, use circular convolution.
    :return: the enhanced image.
    :pre: in_img.dtype == np.float32 and single-channel
    :pre: 0 < r1 < r2
    :pre: filter_type in {0, 1, 2}
    :post: ret_v.dtype == in_img.dtype
    :post: ret_v.shape == in_img.shape
    """
    assert in_img.dtype == np.float32, "Input image must have float32 depth"
    assert in_img.ndim == 2 or (
        in_img.ndim == 3 and in_img.shape[2] == 1), "Input image must be single-channel"
    assert 0 < r1 < r2, "Condition 0 < r1 < r2 must hold"
    assert 0 <= filter_type <= 2, "filter_type must be in {0, 1, 2}"
    out = None
    # TODO
    # Remember: The effect consists of performing a convolution of the input
    #           image with the appropriate sharpening filter.
    # Hint: use cv::filter2D to convolve. In this case, because the input
    #       image is already extended, you should use 'cv::BORDER_ISOLATED'
    #       to do nothing to the extended area.
    # Remember: the convolved output image has the extended size but we need
    #           to return one with size equal to the input size. You can use
    #           cv::Mat::copyTo on a centered window to extract the result.

    #
    assert out.dtype == in_img.dtype, "Output dtype must match input dtype"
    assert out.shape == in_img.shape, "Output shape must match input shape"
    return out
