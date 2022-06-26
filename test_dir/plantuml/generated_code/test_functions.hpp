/* This is a Dummy Header to demonstrate */

#ifndef TEST_FUNCTIONS_HPP
#define TEST_FUNCTIONS_HPP


namespace test.coucou {

class TestClass1 {
public:
    virtual void public_function(int arg) = 0;
private:
    virtual ns::int private_function(char arg1, int arg2) = 0;
};

class TestClass2 {
public:
    wallah();
private:
    package_private_function();
protected:
    virtual ns1::ns2::char protected_function(ns::int arg1 = 0, char arg2 = NULL) = 0;
};

} //test.coucou
#endif //TEST_FUNCTIONS_HPP