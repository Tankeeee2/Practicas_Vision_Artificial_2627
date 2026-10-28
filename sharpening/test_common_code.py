#!/usr/bin/env python3
"""
Test FSIV common code functions in Python.
Equivalente a test_common_code.cpp
"""

import sys
import time
import argparse
import cv2
import numpy as np

import common_code


from solutions_ref import (
    my_fsiv_create_gaussian_filter,
    my_fsiv_create_lap4_filter,
    my_fsiv_create_lap8_filter,
    my_fsiv_fill_expansion,
    my_fsiv_circular_expansion,
    my_fsiv_create_dog_filter,
    my_fsiv_create_sharpening_filter,
    my_fsiv_image_sharpening,
)

available_tests = (
    "fsiv_create_gaussian_filter\n"
    "fsiv_create_lap4_filter\n"
    "fsiv_create_lap8_filter\n"
    "fsiv_fill_expansion\n"
    "fsiv_circular_expansion\n"
    "fsiv_create_dog_filter\n"
    "fsiv_create_sharpening_filter\n"
    "fsiv_image_sharpening\n"
    "ALL\n"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test FSIV common code functions.", add_help=False)
    parser.add_argument("-h", "--help", "-?", "--usage", action="help", default=argparse.SUPPRESS,
                        help="print this message")
    parser.add_argument("-r", "--rseed", type=int, default=None,
                        help="Set the random seed.")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List of available tests.")
    parser.add_argument("test", nargs="?", default="ALL",
                        help="test to execute.")

    args = parser.parse_args()

    if args.list:
        print("Available tests: ")
        print(available_tests, end="")
        return 0

    if args.rseed is not None:
        seed = args.rseed
    else:
        seed = int(time.time() * 1000) & 0xFFFFFFFF
    sys.stderr.write(f"Random seed: {seed}\n")
    np.random.seed(seed)

    test_to_execute = args.test
    tests = 0
    tests_passed = 0

    try:
        # Test 1: fsiv_create_gaussian_filter
        if test_to_execute in ("ALL", "fsiv_create_gaussian_filter"):
            try:
                r = int(np.random.randint(1, 50))
                sys.stderr.write(
                    f"Testing fsiv_create_gaussian_filter (r={r}) ... ")
                tests += 1

                my_filter = my_fsiv_create_gaussian_filter(r)
                your_filter = common_code.fsiv_create_gaussian_filter(r)
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

        # Test 2: fsiv_create_lap4_filter
        if test_to_execute in ("ALL", "fsiv_create_lap4_filter"):
            try:
                sys.stderr.write("Testing fsiv_create_lap4_filter ... ")
                tests += 1

                my_filter = my_fsiv_create_lap4_filter()
                your_filter = common_code.fsiv_create_lap4_filter()
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

        # Test 3: fsiv_create_lap8_filter
        if test_to_execute in ("ALL", "fsiv_create_lap8_filter"):
            try:
                sys.stderr.write("Testing fsiv_create_lap8_filter ... ")
                tests += 1

                my_filter = my_fsiv_create_lap8_filter()
                your_filter = common_code.fsiv_create_lap8_filter()
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

        # Test 4: fsiv_fill_expansion
        if test_to_execute in ("ALL", "fsiv_fill_expansion"):
            tests += 1
            sys.stderr.write("Testing fsiv_fill_expansion ...\n")
            sub_tests = 0
            sub_tests_passed = 0

            try:
                sub_tests += 1
                r = int(np.random.randint(1, 10))
                sys.stderr.write(
                    f"\tTesting fsiv_fill_expansion (CV_8UC1 r={r}) ... ")
                test_img = np.random.randint(
                    0, 256, (128, 256), dtype=np.uint8)
                my_img = my_fsiv_fill_expansion(test_img, r)
                your_img = common_code.fsiv_fill_expansion(test_img, r)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            try:
                sub_tests += 1
                r = int(np.random.randint(1, 10))
                sys.stderr.write(
                    f"\tTesting fsiv_fill_expansion (CV_32FC1 r={r}) ... ")
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_fill_expansion(test_img, r)
                your_img = common_code.fsiv_fill_expansion(test_img, r)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            if sub_tests == sub_tests_passed:
                tests_passed += 1

        # Test 5: fsiv_circular_expansion
        if test_to_execute in ("ALL", "fsiv_circular_expansion"):
            tests += 1
            sys.stderr.write("Testing fsiv_circular_expansion ...\n")
            sub_tests = 0
            sub_tests_passed = 0

            try:
                sub_tests += 1
                r = int(np.random.randint(1, 10))
                sys.stderr.write(
                    f"\tTesting fsiv_circular_expansion (CV_8UC1 r={r}) ... ")
                test_img = np.random.randint(
                    0, 256, (128, 256), dtype=np.uint8)
                my_img = my_fsiv_circular_expansion(test_img, r)
                your_img = common_code.fsiv_circular_expansion(test_img, r)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            try:
                sub_tests += 1
                r = int(np.random.randint(1, 10))
                sys.stderr.write(
                    f"\tTesting fsiv_circular_expansion (CV_32FC1 r={r}) ... ")
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_circular_expansion(test_img, r)
                your_img = common_code.fsiv_circular_expansion(test_img, r)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            if sub_tests == sub_tests_passed:
                tests_passed += 1

        # Test 6: fsiv_create_dog_filter
        if test_to_execute in ("ALL", "fsiv_create_dog_filter"):
            try:
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                sys.stderr.write(
                    f"Testing fsiv_create_dog_filter(r1={r1}, r2={r2}) ... ")
                tests += 1

                my_filter = my_fsiv_create_dog_filter(r1, r2)
                your_filter = common_code.fsiv_create_dog_filter(r1, r2)
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

        # Test 7: fsiv_create_sharpening_filter
        if test_to_execute in ("ALL", "fsiv_create_sharpening_filter"):
            tests += 1
            sys.stderr.write("Testing fsiv_create_sharpening_filter ...\n")
            sub_tests = 0
            sub_tests_passed = 0

            try:
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                sys.stderr.write(
                    "\tTesting fsiv_create_sharpening_filter LAP4 ... ")
                sub_tests += 1

                my_filter = my_fsiv_create_sharpening_filter(0, r1, r2)
                your_filter = common_code.fsiv_create_sharpening_filter(
                    0, r1, r2)
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            try:
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                sys.stderr.write(
                    "\tTesting fsiv_create_sharpening_filter LAP8 ... ")
                sub_tests += 1

                my_filter = my_fsiv_create_sharpening_filter(1, r1, r2)
                your_filter = common_code.fsiv_create_sharpening_filter(
                    1, r1, r2)
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            try:
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                sys.stderr.write(
                    f"\tTesting fsiv_create_sharpening_filter DOG (r1={r1}, r2={r2}) ... ")
                sub_tests += 1

                my_filter = my_fsiv_create_sharpening_filter(2, r1, r2)
                your_filter = common_code.fsiv_create_sharpening_filter(
                    2, r1, r2)
                norm_v = cv2.norm(my_filter, your_filter)
                if norm_v < 1.0e-6:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_filter, your_filter)={norm_v}<1.e-6.!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            if sub_tests == sub_tests_passed:
                tests_passed += 1

        # Test 8: fsiv_image_sharpening
        if test_to_execute in ("ALL", "fsiv_image_sharpening"):
            tests += 1
            sys.stderr.write("Testing fsiv_image_sharpening ...\n")
            sub_tests = 0
            sub_tests_passed = 0

            # Subtest 1: filter_type=0, circular=False
            try:
                filter_type = 0
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                circular = False
                sys.stderr.write(
                    f"\tTesting fsiv_image_sharpening (filter_type={filter_type}, circular={circular}) ... ")
                sub_tests += 1
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                your_img = common_code.fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            # Subtest 2: filter_type=1, circular=False
            try:
                filter_type = 1
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                circular = False
                sys.stderr.write(
                    f"\tTesting fsiv_image_sharpening (filter_type={filter_type}, circular={circular}) ... ")
                sub_tests += 1
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                your_img = common_code.fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            # Subtest 3: filter_type=2, circular=False
            try:
                filter_type = 2
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                circular = False
                sys.stderr.write(
                    f"\tTesting fsiv_image_sharpening (filter_type={filter_type}, r1={r1}, r2={r2}, circular={circular}) ... ")
                sub_tests += 1
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                your_img = common_code.fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            # Subtest 4: filter_type=0, circular=True
            try:
                filter_type = 0
                r1 = int(np.random.randint(1, 5))
                r2 = r1 + int(np.random.randint(1, 5))
                circular = True
                sys.stderr.write(
                    f"\tTesting fsiv_image_sharpening (filter_type={filter_type}, circular={circular}) ... ")
                sub_tests += 1
                test_img = np.random.uniform(
                    0.0, 1.0, (128, 256)).astype(np.float32)
                my_img = my_fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                your_img = common_code.fsiv_image_sharpening(
                    test_img, filter_type, r1, r2, circular)
                norm_v = cv2.norm(my_img, your_img)
                if norm_v < 0.1:
                    sub_tests_passed += 1
                    sys.stderr.write(" Ok!\n")
                else:
                    sys.stderr.write(
                        f"Test fail: cv::norm(my_img, your_img)={norm_v} < 0.1!\n")
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

            if sub_tests == sub_tests_passed:
                tests_passed += 1

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")

    if tests == 0:
        sys.stderr.write(f"Error: unknown test '{test_to_execute}'.\n")
        parser.print_help()
        return 1

    if test_to_execute == "ALL" and tests > 0:
        pct = int((100.0 * tests_passed) / tests)
        print(f"Tests passed ({pct}%): {tests_passed} / {tests}")

    return 0 if tests == tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())
