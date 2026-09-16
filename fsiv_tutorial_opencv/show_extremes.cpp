#include <iostream>
#include <exception>
#include <iomanip>
#include <sstream>

// OpenCV includes
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
// #include <opencv2/calib3d.hpp> //Uncomment when it was appropiated.
// #include <opencv2/ml.hpp> //Uncomment when it was appropiated.

#include "common_code.hpp"

const char *keys =
    "{help h usage ? |      | print this message}"
    "{m method       | 1    | Method to get the extremes: 1, 2. Default is 1.}"
    "{w              |20    | Wait time (miliseconds) between frames.}"
    "{v              |      | the input is a video file.}"
    "{c              |      | the input is a camera index.}"
    "{@input         |<none>| input <fname|int>}";

void do_the_work(const cv::Mat &img, const cv::String &winname, int method, int frame_idx = 0)
{
    std::vector<double> min_v, max_v;
    std::vector<cv::Point> min_loc, max_loc;
    if (method == 1)
        fsiv_find_min_max_loc_1(img, min_v, max_v, min_loc, max_loc);
    else
        fsiv_find_min_max_loc_2(img, min_v, max_v, min_loc, max_loc);

    std::ostringstream min_text, max_text, frame_text;
    frame_text << "Frame idx: " << frame_idx;
    min_text << "Min:";
    max_text << "Max:";
    for (size_t c = 0; c < min_v.size(); ++c)
    {
        min_text << " c" << c << "=" << std::setprecision(6) << min_v[c]
                 << " (" << min_loc[c].x << "," << min_loc[c].y << ")";
        max_text << " c" << c << "=" << std::setprecision(6) << max_v[c]
                 << " (" << max_loc[c].x << "," << max_loc[c].y << ")";
    }

    cv::Mat display = img.clone();
    const int margin = 8;
    const int baseline = 4;
    const int line_height = 18;
    const int text_y = std::max(0, display.rows - margin - baseline - 2 * line_height);
    cv::rectangle(display,
                  cv::Point(0, text_y - line_height),
                  cv::Point(display.cols, display.rows),
                  cv::Scalar::all(0), cv::FILLED);
    cv::putText(display, frame_text.str(), cv::Point(margin, text_y),
                cv::FONT_HERSHEY_SIMPLEX, 0.45, cv::Scalar::all(255), 1,
                cv::LINE_AA);
    cv::putText(display, min_text.str(), cv::Point(margin, text_y + line_height),
                cv::FONT_HERSHEY_SIMPLEX, 0.45, cv::Scalar::all(255), 1,
                cv::LINE_AA);
    cv::putText(display, max_text.str(), cv::Point(margin, text_y + 2 * line_height),
                cv::FONT_HERSHEY_SIMPLEX, 0.45, cv::Scalar::all(255), 1,
                cv::LINE_AA);
    cv::imshow(winname, display);
}

int main(int argc, char *const *argv)
{
    int retCode = EXIT_SUCCESS;

    try
    {

        cv::CommandLineParser parser(argc, argv, keys);
        parser.about("Show the extremes values and their locations.");
        if (parser.has("help"))
        {
            parser.printMessage();
            return 0;
        }
        int method = parser.get<int>("m");
        bool is_video = parser.has("v");
        bool is_camera = parser.has("c");
        int wait = parser.get<int>("w");
        cv::String input = parser.get<cv::String>("@input");
        if (!parser.check())
        {
            parser.printErrors();
            return 0;
        }

        cv::Mat img;
        if (is_video || is_camera)
        {
            cv::VideoCapture v;
            cv::String winname;
            if (is_video)
            {
                v.open(input);
                winname = "VIDEO";
            }
            else
            {
                v.open(std::stoi(input));
                winname = "CAMERA";
            }
            if (!v.isOpened())
                throw std::runtime_error("Could not open the video source.");
            v >> img;
            if (img.empty())
                throw std::runtime_error("Could not load any frame from the video source.");
            int count = 0;
            int key = 0;
            while (!img.empty() && key != 27)
            {
                do_the_work(img, winname, method, count);
                key = cv::waitKey(wait) & 0xff;
                if (key == 32) // Space bar pressed
                    key = cv::waitKey(0) & 0xff;
                v >> img;
                ++count;
            }
        }
        else
        {
            img = cv::imread(input, cv::IMREAD_ANYCOLOR);
            if (img.empty())
                throw std::runtime_error("Could not load the input image.");
            do_the_work(img, "IMG", method);
            std::cout << "Press any key to exit." << std::endl;
            cv::waitKey(0);
        }
    }
    catch (std::exception &e)
    {
        std::cerr << "Caught exception: " << e.what() << std::endl;
        retCode = EXIT_FAILURE;
    }
    catch (...)
    {
        std::cerr << "Caught unknown exception!" << std::endl;
        retCode = EXIT_FAILURE;
    }
    return retCode;
}
