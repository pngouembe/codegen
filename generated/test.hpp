/* This is a Dummy Header to demonstrate */

#ifndef TEST_HPP
#define TEST_HPP


namespace test {
namespace coucou {

class TestClass1 {
public:
    virtual void public_function(int arg) = 0;
private:
    virtual ns::int private_function(char arg1, int arg2) = 0;
}

class TestClass2 {
public:
    wallah();
protected:
    virtual ns1::ns2::char protected_function(ns::int arg1 = 0, char arg2 = NULL) = 0;
}

} //coucou
} //test

#endif //TEST_HPP