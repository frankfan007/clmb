#include <gtest/gtest.h>
#include <Eigen/Core>
#include <hypgen.hpp>

using namespace lmb;

Eigen::MatrixXd MURTY_COST = (Eigen::MatrixXd(10, 10) <<
              7, 51, 52, 87, 38, 60, 74, 66, 0, 20,
              50, 12, 0, 64, 8, 53, 0, 46, 76, 42,
              27, 77, 0, 18, 22, 48, 44, 13, 0, 57,
              62, 0, 3, 8, 5, 6, 14, 0, 26, 39,
              0, 97, 0, 5, 13, 0, 41, 31, 62, 48,
              79, 68, 0, 0, 15, 12, 17, 47, 35, 43,
              76, 99, 48, 27, 34, 0, 0, 0, 28, 0,
              0, 20, 9, 27, 46, 15, 84, 19, 3, 24,
              56, 10, 45, 39, 0, 93, 67, 79, 19, 38,
              27, 0, 39, 53, 46, 24, 69, 46, 23, 1).finished();


class HypgenTests : public ::testing::Test {
    public:
        HypgenTests() {
        }
};


static const unsigned N_TESTS = 1000000;


TEST_F(HypgenTests, SingleLAP) {
    Assignment res(MURTY_COST.rows());
    double cost;
    for (unsigned i = 0; i < N_TESTS; ++i) {
        lap(MURTY_COST, res, cost);
    }
    std::cout << res << std::endl;
}

TEST_F(HypgenTests, SingleLAPJV) {
    Assignment res(MURTY_COST.rows());
    double cost;
    for (unsigned i = 0; i < N_TESTS; ++i) {
        lapjv(MURTY_COST, res, cost);
    }
    std::cout << res << std::endl;
}
