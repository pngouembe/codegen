/* This is a Dummy Header to demonstrate */

#ifndef TEST_FUNCTIONS_HPP
#define TEST_FUNCTIONS_HPP


class TestClass2 {
public:
    wallah();
protected:
    virtual ns1::ns2::char protected_function(ns::int arg1 = 0, char arg2 = NULL) = 0;
};

namespace test {
namespace coucou {

virtual void public_function(int arg) = 0;

virtual ns::int private_function(char arg1, int arg2) = 0;

} //coucou
} //test
#endif //TEST_FUNCTIONS_HPP