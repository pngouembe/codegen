/* This is a Dummy Header to demonstrate */

#ifndef TEST_FUNCTIONS_HPP
#define TEST_FUNCTIONS_HPP


namespace test.coucou {

class TestClass1 {
public:
    /**
     * coucou
     * on
     * multi
     * line
     */
    virtual void public_function(int arg) = 0;
private:
    /**
     * coucou 4
     */
    virtual ns::int private_function(char arg1, int arg2) = 0;
};

class TestClass2 {
public:
    /**
     * coucou 5
     */
    wallah();
    test();
private:
    /**
     * coucou 4
     */
    private_function();
protected:
    /**
     * coucou 3
     */
    virtual ns1::ns2::char protected_function(ns::int arg1 = 0, char arg2 = NULL) = 0;
};

} //test.coucou
#endif //TEST_FUNCTIONS_HPP