#include "gtest/gtest.h"

/**
 * photo-fourier unit test class
**/
class pftest : public ::testing::Test
{
protected:
    /**
     * pftest constructor
    **/
    pftest();

    /**
     * pftest setup
    **/
    virtual void SetUp();

    /**
     * pftest teardown
    **/
    virtual void TearDown();
};
