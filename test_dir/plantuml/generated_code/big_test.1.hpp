/* This is a Dummy Header to demonstrate */

#ifndef BIG_TEST.1_HPP
#define BIG_TEST.1_HPP

#include <cstdint>
#include <string>

class TransactionEntity {
public:
    uint32_t ID;
    time CreatedAt;
    time UpdatedAt;
    time DeletedAt;
    uint32_t Customer_id;
    CustomerEntity Customer;
    uint32_t Agent_id;
    AgentEntity Agent;
    std::string Address;
    std::string Province;
    std::string City;
    std::string District;
    decimal Latitude;
    decimal Longitude;
    std::string Services;
    std::string Type;
    uint32_t Amount;
    uint32_t Status;
    uint32_t Rating;
};

class TransactionContractInterface {
public:
    TransactionContractInterface FromEntity(ent TransactionEntity);
    TransactionEntity ToEntity();
};

class TransactionContract {
public:
    uint32_t ID;
    int Status;
    time CreatedAt;
    std::string Services;
    std::string Type;
    uint32_t Amount;
    uint32_t Rating;
    AgentContract Agent;
    CustomerContract Customer;
};

class TransactionRepositoryInterface {
public:
    TransactionEntity* GetAll();
    TransactionEntity* GetAllByID(usertype std.string, id uint32_t);
    TransactionEntity* GetByID(id uint32_t);
    TransactionEntity* Create(ent TransactionEntity*);
    TransactionEntity* Update(ent TransactionEntity*);
    error Delete(ent TransactionEntity*);
};

class Transaction {
public:
    int id;
    Customer customerId;
    Agent agentId;
    Location locationId;
    char type;
    int amount;
    int status;
    int ratting;
};

class UserInterface {
public:
    GetAll(UserInterface, error);
    GetByID(UserInterface, error);
};

class User {
public:
    int id;
    Login loginId;
    std::string name;
    std::string phone_number;
};

class Customer {
};

class Agent {
public:
    std::string outletName;
    int locationId;
public:
    error GetByLocation(city, *Agent);
};

class LoginInterface {
public:
    error Login(username, password, &User);
    error Logout(token);
};

class SessionInterface {
public:
    error Create(User, token);
    error Validate(token, &User);
    error Remove(token);
};

class Login {
public:
    int id;
    std::string username;
    std::string password;
    int loginAs;
    time::Time lastLogin;
};

class Session {
public:
    int id;
    Login loginId;
    std::string token;
    time::Time expiredAt;
};

class LocationInterface {
public:
    error GetLocationByLogin(Login, LocationInterface*);
};

class Location {
public:
    int id;
    Login createById;
    std::string address;
    std::string province;
    std::string city;
    std::string district;
    float32_t latitude;
    float32_t longitude;
};

#endif //BIG_TEST.1_HPP