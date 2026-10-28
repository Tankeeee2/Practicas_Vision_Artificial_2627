#!/usr/bin/env python3
"""
Enhance an image using a sharpening filter.
Versión Python 3 equivalente a sharpen.cpp
"""

import sys
import argparse
import cv2
import numpy as np

from common_code import (
    fsiv_create_gaussian_filter,
    fsiv_create_lap4_filter,
    fsiv_create_lap8_filter,
    fsiv_fill_expansion,
    fsiv_circular_expansion,
    fsiv_create_dog_filter,
    fsiv_create_sharpening_filter,
    fsiv_image_sharpening,
)


class UserData:
    """
    Application State.
    """

    def __init__(self):
        self.input: np.ndarray | None = None
        self.input_channels: list[np.ndarray] = []
        self.output_channels: list[np.ndarray] = []
        self.output: np.ndarray | None = None
        self.filter_type: int = 0
        self.r1: int = 1
        self.r2: int = 2
        self.only_luma: int = 0
        self.circular: bool = False
        self.interactive: bool = False
        self.contrast: float = 1.0


def to_diverging_heatmap_neg_blue_pos_red(img_f: np.ndarray) -> np.ndarray:
    """
    Convert float map in [-1, 1] to diverging heatmap (blue for negative, red for positive).
    """
    assert img_f.dtype in (np.float32, np.float64), "img_f must be float32 or float64"
    f32 = img_f.astype(np.float32)

    # Magnitude in [0, 1]
    mag = np.abs(f32)
    mag = np.minimum(mag, 1.0)

    # Hue (H): 0=red (positives), 120=blue (negatives) in scale [0..179]
    h = np.zeros(f32.shape, dtype=np.uint8)
    s = np.full(f32.shape, 255, dtype=np.uint8)

    pos_mask = (f32 > 0)
    neg_mask = (f32 < 0)

    h[pos_mask] = 0
    h[neg_mask] = 120

    # Brightness according to magnitude
    v = (mag * 255.0).astype(np.uint8)

    hsv = cv2.merge([h, s, v])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def do_the_work(user_data: UserData) -> None:
    """
    Execute sharpening and display intermediate windows if interactive.
    """
    input_img = user_data.input
    if len(user_data.input_channels) == 3:
        input_img = user_data.input_channels[2]

    user_data.output = fsiv_image_sharpening(
        input_img,
        user_data.filter_type,
        user_data.r1,
        user_data.r2,
        user_data.circular
    )

    if len(user_data.input_channels) == 3:
        # Revert to BGR
        user_data.output_channels[2] = user_data.output
        hsv = cv2.merge(user_data.output_channels)
        user_data.output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    if user_data.interactive:
        cv2.imshow("OUTPUT", user_data.output)
        if len(user_data.input_channels) == 3:
            luma = cv2.cvtColor(user_data.input, cv2.COLOR_BGR2GRAY)
        else:
            luma = user_data.input.copy()
        luma = (luma * (1.0 / 255.0)).astype(np.float32)

        if user_data.filter_type == 0:
            filt = fsiv_create_lap4_filter()
        elif user_data.filter_type == 1:
            filt = fsiv_create_lap8_filter()
        elif user_data.filter_type == 2:
            filt = fsiv_create_dog_filter(user_data.r1, user_data.r2)
        else:
            raise ValueError(f"Invalid filter type: {user_data.filter_type}")

        k_r = filt.shape[0] // 2
        if user_data.circular:
            luma = fsiv_circular_expansion(luma, k_r)
        else:
            luma = fsiv_fill_expansion(luma, k_r)

        lap = cv2.filter2D(luma, cv2.CV_32F, filt, anchor=(-1, -1), delta=0.0, borderType=cv2.BORDER_ISOLATED)
        lap = lap[k_r: k_r + user_data.output.shape[0], k_r: k_r + user_data.output.shape[1]].copy()

        min_v = float(np.min(lap))
        max_v = float(np.max(lap))
        lap_neg = lap / (abs(min_v) + 1e-6)
        lap_pos = lap / (max_v + 1e-6)
        lap = np.where(lap < 0, lap_neg, lap_pos).astype(np.float32)

        heatmap = to_diverging_heatmap_neg_blue_pos_red(lap)
        heatmap = cv2.multiply(heatmap, (user_data.contrast, user_data.contrast, user_data.contrast, 0.0))
        cv2.imshow("LAPLACIAN", heatmap)


def filter_trackbar(pos: int, user_data: UserData) -> None:
    pos = max(0, min(pos, 2))
    user_data.filter_type = pos
    print(f"Set filter type to {user_data.filter_type}", flush=True)
    do_the_work(user_data)


def r1_trackbar(pos: int, user_data: UserData) -> None:
    if pos > 0 and pos < user_data.r2:
        user_data.r1 = pos
        print(f"Set r1={user_data.r1} r2={user_data.r2}", flush=True)
        do_the_work(user_data)
    else:
        cv2.setTrackbarPos("R1", "PARAMETERS", user_data.r1)


def r2_trackbar(pos: int, user_data: UserData) -> None:
    if pos > user_data.r1:
        user_data.r2 = pos
        print(f"Set r1={user_data.r1} r2={user_data.r2}", flush=True)
        do_the_work(user_data)
    else:
        cv2.setTrackbarPos("R2", "PARAMETERS", user_data.r2)


def circular_trackbar(pos: int, user_data: UserData) -> None:
    user_data.circular = (pos == 1)
    state = 1 if user_data.circular else 0
    print(f"Set circular convolution mode to state {state}", flush=True)
    do_the_work(user_data)


def contrast_trackbar(pos: int, user_data: UserData) -> None:
    user_data.contrast = 1.0 + pos / 10.0  # [1.0, 10.0]
    print(f"Set contrast to {user_data.contrast}", flush=True)
    do_the_work(user_data)


def main() -> int:
    ret_code = 0

    try:
        parser = argparse.ArgumentParser(
            description="Enhance an image using a sharpening filter. (ver 1.11.0)",
            add_help=False
        )
        parser.add_argument("-h", "--help", "-?", "--usage", action="help", default=argparse.SUPPRESS,
                            help="print this message.")
        parser.add_argument("-i", "--interactive", action="store_true",
                            help="Activate interactive mode.")
        parser.add_argument("-f", "--filter", type=int, default=0,
                            help="Laplacian filter to be used to build the sharpening filter: 0->LAP_4, 1->LAP_8, 2->DOG")
        parser.add_argument("-r1", type=int, default=1,
                            help="r1 for DoG filter.")
        parser.add_argument("-r2", type=int, default=2,
                            help="r2 for DoG filter. (0<r1<r2)")
        parser.add_argument("-c", "--circular", action="store_true",
                            help="use circular convolution.")
        parser.add_argument("input", help="input image.")
        parser.add_argument("output", help="output image.")

        args = parser.parse_args()

        data = UserData()
        data.filter_type = args.filter
        data.r1 = args.r1
        data.r2 = args.r2
        data.interactive = args.interactive
        data.circular = args.circular

        input_name = args.input
        output_name = args.output

        data.input = cv2.imread(input_name, cv2.IMREAD_ANYCOLOR)
        if data.input is None:
            sys.stderr.write(f"Error: could not open the input image '{input_name}'.\n")
            return 1

        data.input = (data.input.astype(np.float32) / 255.0)

        channels = 1 if data.input.ndim == 2 else data.input.shape[2]
        if channels == 3:
            hsv_img = cv2.cvtColor(data.input, cv2.COLOR_BGR2HSV)
            data.input_channels = list(cv2.split(hsv_img))
            data.output_channels = list(data.input_channels)

        if data.filter_type < 0 or data.filter_type > 2:
            sys.stderr.write("Error: filter type parameter has values in {0, 1, 2}.\n")
            return 1

        rows, cols = data.input.shape[:2]
        if data.r1 < 0 or data.r1 >= data.r2 or data.r2 >= min(rows, cols) // 2:
            sys.stderr.write("Error: Condition 0 <= r1 < r2 < min(rows, cols) / 2 is not meet.\n")
            return 1

        key = 0

        if data.interactive:
            data.contrast = 1.0
            cv2.namedWindow("INPUT", cv2.WINDOW_GUI_EXPANDED + cv2.WINDOW_NORMAL)
            cv2.resizeWindow("INPUT", 800, 600)
            cv2.namedWindow("OUTPUT", cv2.WINDOW_GUI_EXPANDED + cv2.WINDOW_NORMAL)
            cv2.resizeWindow("OUTPUT", 800, 600)
            cv2.namedWindow("LAPLACIAN", cv2.WINDOW_GUI_EXPANDED + cv2.WINDOW_NORMAL)
            cv2.resizeWindow("LAPLACIAN", 800, 600)
            cv2.namedWindow("PARAMETERS", cv2.WINDOW_GUI_EXPANDED + cv2.WINDOW_NORMAL)

            max_r = min(rows, cols) // 2
            initializing = True

            cv2.createTrackbar("FILTER", "PARAMETERS", 0, 2, lambda v: not initializing and filter_trackbar(v, data))
            cv2.setTrackbarPos("FILTER", "PARAMETERS", data.filter_type)

            cv2.createTrackbar("R1", "PARAMETERS", 0, max_r, lambda v: not initializing and r1_trackbar(v, data))
            cv2.setTrackbarPos("R1", "PARAMETERS", data.r1)

            cv2.createTrackbar("R2", "PARAMETERS", 0, max_r, lambda v: not initializing and r2_trackbar(v, data))
            cv2.setTrackbarPos("R2", "PARAMETERS", data.r2)

            cv2.createTrackbar("CIRC", "PARAMETERS", 0, 1, lambda v: not initializing and circular_trackbar(v, data))
            cv2.setTrackbarPos("CIRC", "PARAMETERS", 1 if data.circular else 0)

            cv2.createTrackbar("CONTRAST", "LAPLACIAN", 0, 90, lambda v: not initializing and contrast_trackbar(v, data))
            cv2.setTrackbarPos("CONTRAST", "LAPLACIAN", 0)

            initializing = False

            cv2.imshow("INPUT", data.input)
            print("Interative mode. Press <ENTER> to finish with saving or <ESC> to abort.", flush=True)
            do_the_work(data)

            while True:
                key = cv2.waitKey(0) & 0xFF
                if key in (27, 13):
                    break
        else:
            do_the_work(data)

        if key != 27:
            output_save = (data.output * 256.0).astype(np.float32)
            if not cv2.imwrite(output_name, output_save):
                sys.stderr.write(f"Error: could not save the result in file '{output_name}'.\n")
                return 1

    except Exception as e:
        sys.stderr.write(f"Caught exception: {e}\n")
        ret_code = 1

    return ret_code


if __name__ == "__main__":
    sys.exit(main())
