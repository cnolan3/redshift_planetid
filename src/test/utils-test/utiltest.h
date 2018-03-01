#include "gtest/gtest.h"

/**
 * utils unit test class
**/
class utiltest : public ::testing::Test
{
protected:
    /**
     * utiltest constructor
    **/
    utiltest();

    /**
     * utiltest setup
    **/
    virtual void SetUp();

    /**
     * utiltest teardown
    **/
    virtual void TearDown();
};
