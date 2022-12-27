struct shortDummyObj {
};
struct dummyObj {
    int public_num;

    int protected_num;

    int private_num;

    void (*public_fct)();

    int (*protected_fct)(int);

    char (*private_fct)(int, char);

};