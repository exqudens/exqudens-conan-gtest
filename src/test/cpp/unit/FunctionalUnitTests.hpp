#pragma once

#include <string>
#include <exception>
#include <iostream>

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include "TestUtils.hpp"

class FunctionalUnitTests: public testing::Test {

    public:

        inline static const char* LOGGER_ID = "FunctionalUnitTests";

};

TEST_F(FunctionalUnitTests, test_1) {
    try {
        std::string testGroup = testing::UnitTest::GetInstance()->current_test_info()->test_suite_name();
        std::string testCase = testing::UnitTest::GetInstance()->current_test_info()->name();
        std::cout << LOGGER_ID << ": bgn" << std::endl;

        int expected = 123;
        std::cout << LOGGER_ID << ": expected: " << expected << std::endl;
        int actual = 123;
        std::cout << LOGGER_ID << ": actual: " << actual << std::endl;

        ASSERT_EQ(expected, actual);

        std::cout << LOGGER_ID << ": end" << std::endl;
    } catch (const std::exception& e) {
        std::string errorMessage = TestUtils::toString(e);
        std::cout << LOGGER_ID << " ERROR: " << errorMessage << std::endl;
        FAIL() << errorMessage;
    }
}
