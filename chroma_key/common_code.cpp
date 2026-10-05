#include <iostream>
#include "common_code.hpp"
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

cv::Mat
fsiv_convert_bgr_to_hsv(const cv::Mat &img)
{
    CV_Assert(img.channels() == 3);
    cv::Mat out;
    //! TODO
    // Hint: use cvtColor.
    // Remember: the input color scheme is assumed to be BGR.
    cv::cvtColor(img, out, cv::COLOR_BGR2HSV);
    //
    CV_Assert(out.channels() == 3);
    return out;
}

cv::Mat
fsiv_combine_images(const cv::Mat &img1, const cv::Mat &img2,
                    const cv::Mat &mask)
{
    CV_Assert(img2.size() == img1.size());
    CV_Assert(img2.type() == img1.type());
    CV_Assert(mask.size() == img1.size());
    cv::Mat output;
    //! TODO
    //  HINT: you can use cv::Mat::copyTo().
    img2.copyTo(output);
    img1.copyTo(output, mask);
    //
    CV_Assert(output.size() == img1.size());
    CV_Assert(output.type() == img1.type());
    return output;
}

cv::Mat
fsiv_compute_chroma_key_mask(const cv::Mat &bgr_img,
                             int chroma_key,
                             int sensitivity)
{
    CV_Assert(bgr_img.type() == CV_32FC3);
    cv::Mat mask;
    // TODO
    // Hint: use fsiv_xxx defined functions.
    // Hint: use cv::inRange to get the mask.
    // Remember: the input are floats, so the H range is [0,360] and S,V is [0,1]
    // Remember: Hue is a circular measure, so be careful when H is less than 0 or greater than 360.
    // Remember: Use full range for S and V.
    cv::Mat hsv_img = fsiv_convert_bgr_to_hsv(bgr_img);

    int h_min = (chroma_key - sensitivity + 360) % 360;
    int h_max = (chroma_key + sensitivity) % 360;

    if (h_min <= h_max) {
        cv::inRange(hsv_img, cv::Scalar(h_min, 0.0, 0.0), cv::Scalar(h_max, 1.0, 1.0), mask);
    } else {
        cv::Mat m1, m2;
        cv::inRange(hsv_img, cv::Scalar(h_min, 0.0, 0.0), cv::Scalar(360.0, 1.0, 1.0), m1);
        cv::inRange(hsv_img, cv::Scalar(0.0, 0.0, 0.0), cv::Scalar(h_max, 1.0, 1.0), m2);
        mask = m1 | m2;
    }
    //
    CV_Assert(mask.size() == bgr_img.size());
    return mask;
}

cv::Mat
fsiv_apply_chroma_key(const cv::Mat &foreg, const cv::Mat &backg, int hue,
                      int sensitivity, cv::Mat *mask_out)
{
    cv::Mat out;
    cv::Scalar lower_b, upper_b; // HSV range.

    // TODO
    // Hint: use fsiv_xxx defined functions.
    // Hint: use cv::resize if backg img has different size than foreg.
    // Remember: if mask_out is not null, the computed mask must be assigned to *mask_out.
    cv::Mat mask = fsiv_compute_chroma_key_mask(foreg, hue, sensitivity);

    if (mask_out != nullptr) {
        mask.copyTo(*mask_out);
    }

    cv::Mat resized_backg;
    if (backg.size() != foreg.size()) {
        cv::resize(backg, resized_backg, foreg.size());
    } else {
        backg.copyTo(resized_backg);
    }

    cv::Mat inv_mask;
    cv::bitwise_not(mask, inv_mask);
    out = fsiv_combine_images(foreg, resized_backg, inv_mask);
    //
    CV_Assert(out.size() == foreg.size());
    CV_Assert(out.type() == foreg.type());
    return out;
}
