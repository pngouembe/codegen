/* This is a Dummy Header to demonstrate */

#ifndef TEST_HPP
#define TEST_HPP

#include <cstdint>

namespace Microsoft {
namespace Console {

enum HostSignals {
    EndTask,
    NotifyApp,
    SetForeground
};

class HostSignalEndTaskData {
public:
    uint32_t ctrlFlags;
    uint32_t eventType;
    uint32_t processId;
    uint32_t sizeInBytes;
};

class HostSignalNotifyAppData {
public:
    uint32_t processId;
    uint32_t sizeInBytes;
};

class HostSignalSetForegroundData {
public:
    bool isForeground;
    uint32_t processId;
    uint32_t sizeInBytes;
};

} //Console
} //Microsoft
namespace Microsoft2 {
namespace Console {

enum HostSignals {
    EndTask,
    NotifyApp,
    SetForeground
};

class HostSignalEndTaskData {
public:
    uint32_t ctrlFlags;
    uint32_t eventType;
    uint32_t processId;
    uint32_t sizeInBytes;
};

class HostSignalNotifyAppData {
public:
    uint32_t processId;
    uint32_t sizeInBytes;
};

class HostSignalSetForegroundData {
public:
    bool isForeground;
    uint32_t processId;
    uint32_t sizeInBytes;
};

} //Console
} //Microsoft2
#endif //TEST_HPP