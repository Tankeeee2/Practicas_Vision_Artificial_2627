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

    //
    CV_Assert(out.size() == foreg.size());
    CV_Assert(out.type() == foreg.type());
    return out;
}
