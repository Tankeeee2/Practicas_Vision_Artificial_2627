/**
 * @file usm_enhance.cpp
 * @author Francisco José Madrid Cuevas (fjmadrid@uco.es)
 * @brief Main program to do an Unsharp Mask image enhance.
 * @version 0.1
 * @date 2024-09-19
 *
 * @copyright Copyright (c) 2024-
 *
 */
#include <iostream>
#include <exception>

#include <opencv2/core/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "common_code.hpp"

const cv::String keys =
    "{help h usage ? |      | print this message.}"
    "{i interactive  |      | Interactive mode.}"
    "{r radius       |1     | Window's radius. Default 1.}"
    "{g gain         |1.0   | Enhance's gain. Default 1.0}"
    "{c circular     |      | Use circular convolution. Default: fill borders.}"
    "{f filter       |0     | Filter type: 0->Box, 1->Gaussian. Default Box.}"
    "{@input         |<none>| input image.}"
    "{@output        |<none>| output image.}";

/**
 * @brief Application State.
 * Use this structure to maintain the state of the application
 * that will be passed to the callbacks.
 */
struct UserData
{
    cv::Mat in;                    // input image.
    std::vector<cv::Mat> channels; // HSV channels.
    cv::Mat luma;                  // luma/V to be enhanced.
    cv::Mat out;                   // output image.
    cv::Mat unsharp_mask;          // unsharp mask used to do the enhance.
    int r;                         // Windows' radius.
    double g;                      // Enhance's gain.
    int f;                         // filter type.
    int circular;                  // use circular expansion.
    bool interactive;              // interactive mode is activated.
    float contrast = 1.0f;         // contrast for details visualization.
};

// img_f: CV_32F o CV_64F en [-1, 1]
static cv::Mat
to_diverging_heatmap_neg_blue_pos_red(const cv::Mat &img_f)
{
    CV_Assert(img_f.type() == CV_32F || img_f.type() == CV_64F);
    cv::Mat f32;
    img_f.convertTo(f32, CV_32F);

    // Magnitud en [0,1]
    cv::Mat mag = cv::abs(f32);
    cv::min(mag, 1.0f, mag);

    // Hue (H): 0=rojo (positivos), 120=azul (negativos) en escala [0..179]
    cv::Mat H(f32.size(), CV_8U), S(f32.size(), CV_8U, cv::Scalar(255)), V(f32.size(), CV_8U);
    cv::Mat posMask = (f32 > 0), negMask = (f32 < 0);

    H.setTo(0);            // rojo por defecto
    H.setTo(120, negMask); // azul para negativos

    // Brillo según magnitud
    cv::Mat Vf;
    mag.convertTo(Vf, CV_32F, 255.0);
    Vf.convertTo(V, CV_8U);

    // Mezclar HSV y convertir a BGR
    std::vector<cv::Mat> hsv = {H, S, V};
    cv::Mat hsvImg, bgr;
    cv::merge(hsv, hsvImg);
    cv::cvtColor(hsvImg, bgr, cv::COLOR_HSV2BGR);
    return bgr;
}

/**@brief Do the gui work**/
void do_the_work(UserData *user_data)
{
    user_data->out = fsiv_usm_enhance(user_data->luma, user_data->g,
                                      user_data->r, user_data->f,
                                      user_data->circular,
                                      &user_data->unsharp_mask);
    if (user_data->channels.size() == 3)
    {
        // Revert to BGR.
        cv::Mat hsv;
        user_data->channels[2] = user_data->out;
        cv::merge(user_data->channels, hsv);
        cv::cvtColor(hsv, user_data->out, cv::COLOR_HSV2BGR);
    }
    if (user_data->interactive && !user_data->luma.empty() && !user_data->unsharp_mask.empty())
    {
        cv::imshow("OUTPUT", user_data->out);
        cv::imshow("UNSHARP MASK", user_data->unsharp_mask);
        cv::Mat h_freqs = cv::Mat_<float>(user_data->luma) - cv::Mat_<float>(user_data->unsharp_mask);
        cv::Mat heat_map = to_diverging_heatmap_neg_blue_pos_red(h_freqs);
        heat_map = heat_map.mul(cv::Scalar::all(user_data->contrast));
        cv::imshow("DETAILS", heat_map);
    }
}

/** @brief Standard trackbar callback
 * Use this function an argument for cv::createTrackbar to control
 * the trackbar changes.
 *
 * @arg v give the trackbar position.
 * @arg user_data allow to pass user data to the callback.
 */
void on_change_r(int v, void *user_data_)
{
    UserData *user_data = static_cast<UserData *>(user_data_);
    user_data->r = v + 1; // to avoid 0 value.
    std::cout << "Setting radius to " << user_data->r << std::endl;
    do_the_work(user_data);
}

/**
 * @brief Standard trackbar callback
 * Use this function an argument for cv::createTrackbar to control
 * the trackbar changes.
 *
 * @arg v give the trackbar position.
 * @arg user_data allow to pass user data to the callback.
 */
void on_change_g(int v, void *user_data_)
{
    UserData *user_data = static_cast<UserData *>(user_data_);
    user_data->g = v / 10.0; // we assume that max value is 100
    std::cout << "Setting gain to " << user_data->g << std::endl;
    do_the_work(user_data);
}

/**
 * @brief Standard trackbar callback
 * Use this function an argument for cv::createTrackbar to control
 * the trackbar changes.
 *
 * @arg v give the trackbar position.
 * @arg user_data allow to pass user data to the callback.
 */
void on_change_f(int v, void *user_data_)
{
    UserData *user_data = static_cast<UserData *>(user_data_);
    user_data->f = v;
    std::cout << "Setting filter type to " << (v == 0 ? "box" : "gaussian")
              << std::endl;
    do_the_work(user_data);
}

/**
 * @brief Standard button callback
 * Use this function an argument for cv::createTrackbar to control
 * the trackbar changes.
 *
 * @arg state give the button's state.
 * @arg user_data allow to pass user data to the callback.
 */
void on_change_c(int state, void *user_data_)
{
    UserData *user_data = static_cast<UserData *>(user_data_);
    user_data->circular = state;
    std::cout << "Setting image expansion type to " << (state == 0 ? "filling" : "circular")
              << std::endl;
    do_the_work(user_data);
}

void on_change_contrast(int v, void *user_data_)
{
    UserData *user_data = static_cast<UserData *>(user_data_);
    user_data->contrast = 1.0 + v / 10.0f; // we assume that max value is 100
    std::cout << "Setting details contrast to " << user_data->contrast << std::endl;
    do_the_work(user_data);
}

int main(int argc, char *const *argv)
{
    int retCode = EXIT_SUCCESS;

    try
    {
        UserData user_data;
        cv::CommandLineParser parser(argc, argv, keys);
        parser.about("Apply an unsharp mask enhance to an image.");
        if (parser.has("help"))
        {
            parser.printMessage();
            return EXIT_SUCCESS;
        }
        user_data.r = parser.get<int>("r");
        if (user_data.r < 0)
        {
            std::cerr << "Error: r must be >0" << std::endl;
            return EXIT_FAILURE;
        }
        user_data.g = parser.get<double>("g");
        if (user_data.g < 0.0 || user_data.g > 10.0)
        {
            std::cerr << "Error: g must be in [0.0, 10.0]." << std::endl;
            return EXIT_FAILURE;
        }
        user_data.f = parser.get<int>("f");
        user_data.circular = parser.has("c");
        user_data.interactive = parser.has("i");

        cv::String input_n = parser.get<cv::String>("@input");
        cv::String output_n = parser.get<cv::String>("@output");
        if (!parser.check())
        {
            parser.printErrors();
            return EXIT_FAILURE;
        }

        cv::Mat in = cv::imread(input_n, cv::IMREAD_UNCHANGED);
        if (in.empty())
        {
            std::cerr << "Error: could not open input image '" << input_n
                      << "'." << std::endl;
            return EXIT_FAILURE;
        }

        in.convertTo(user_data.in, CV_32F, 1.0 / 255.0);

        if (user_data.in.channels() == 3)
        {
            cv::Mat hsv;
            cv::cvtColor(user_data.in, hsv, cv::COLOR_BGR2HSV);
            cv::split(hsv, user_data.channels);
            user_data.luma = user_data.channels[2];
        }
        else
            user_data.luma = user_data.in;

        int k = 0;

        if (user_data.interactive)
        {
            cv::namedWindow("INPUT", cv::WINDOW_GUI_EXPANDED + cv::WINDOW_NORMAL);
            cv::imshow("INPUT", user_data.in);
            cv::resizeWindow("INPUT", cv::Size(800, 600));
            cv::namedWindow("OUTPUT", cv::WINDOW_GUI_EXPANDED + cv::WINDOW_NORMAL);
            cv::resizeWindow("OUTPUT", cv::Size(800, 600));
            cv::namedWindow("UNSHARP MASK", cv::WINDOW_GUI_EXPANDED + cv::WINDOW_NORMAL);
            cv::resizeWindow("UNSHARP MASK", cv::Size(800, 600));
            cv::namedWindow("DETAILS", cv::WINDOW_GUI_EXPANDED + cv::WINDOW_NORMAL);
            cv::resizeWindow("DETAILS", cv::Size(800, 600));
            cv::createTrackbar("Contrast", "DETAILS", nullptr, 100, on_change_contrast, &user_data);
            cv::setTrackbarPos("Contrast", "DETAILS", 0);
            cv::namedWindow("PARAMETERS", cv::WINDOW_GUI_EXPANDED + cv::WINDOW_NORMAL);
            cv::createTrackbar("R", "PARAMETERS", nullptr, std::min(in.rows, in.cols) / 2 - 1, on_change_r, &user_data);
            cv::setTrackbarPos("R", "PARAMETERS", user_data.r - 1);
            int g_int = static_cast<int>(std::min(10.0, user_data.g * 10.0));
            cv::createTrackbar("G", "PARAMETERS", nullptr, 100, on_change_g, &user_data);
            cv::setTrackbarPos("G", "PARAMETERS", g_int);
            cv::createTrackbar("Filter", "PARAMETERS", nullptr, 1, on_change_f, &user_data);
            cv::setTrackbarPos("Filter", "PARAMETERS", user_data.f);
            cv::createTrackbar("Circular", "PARAMETERS", nullptr, 1, on_change_c, &user_data);
            cv::setTrackbarPos("Circular", "PARAMETERS", user_data.circular);
            do_the_work(&user_data);
            do
            {
                k = cv::waitKey(0) & 0xff;
            } while (k != 27 && k != 13);
        }
        else
            do_the_work(&user_data);

        if (k != 27)
        {
            cv::Mat out;
            user_data.out.convertTo(out, CV_8U, 255.0);
            cv::imwrite(output_n, out);
        }
    }
    catch (std::exception &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        retCode = EXIT_FAILURE;
    }
    return retCode;
}
