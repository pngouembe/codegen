/* This is a Dummy Header to demonstrate */

#ifndef BIG_TEST_HPP
#define BIG_TEST_HPP

#include <string>

class RefCountInterface {
public:
    virtual void AddRef() = 0;
    virtual RefCountReleaseStatus Release() = 0;
};

class NotifierInterface {
public:
    virtual void RegisterObserver(ObserverInterface* observer) = 0;
    virtual void UnregisterObserver(ObserverInterface* observer) = 0;
};

class ObserverInterface {
public:
    virtual void OnChanged() = 0;
};

class MediaStreamTrackInterface {
public:
    virtual std::string kind() = 0;
    virtual bool set_enabled(bool enable) = 0;
    virtual bool enabled() = 0;
    virtual TrackState state() = 0;
};

class VideoSourceInterface {
public:
    virtual void AddOrUpdateSink(VideoSinkInterface<VideoFrameT>* sink, const VideoSinkWants& wants) = 0;
    virtual void RemoveSink(VideoSinkInterface<VideoFrameT>* sink) = 0;
};

class VideoTrackInterface {
public:
    VideoTrackSourceInterface* GetSource();
    void set_content_hint(ContentHint hint);
    ContentHint content_hint();
};

class Notifier {
public:
    std::list<ObserverInterface*>;
public:
    void RegisterObserver(ObserverInterface* observer);
    void UnregisterObserver(ObserverInterface* observer);
    void FireOnChanged();
};

class MediaStreamTrack {
public:
    bool;
    std::string;
    MediaStreamTrackInterface::TrackState;
public:
    MediaStreamTrackInterface::TrackState state();
    bool enabled();
    bool set_enabled(bool enable);
protected:
    bool set_state(MediaStreamTrackInterface::TrackState new_state);
};

class VideoSourceBase {
public:
    std::vector<SinkPair>;
protected:
    SinkPair* FindSinkPair(const VideoSinkInterface<webrtc::VideoFrame>* sink);
};

class VideoTrack {
public:
    void;
public:
    rtc::scoped_refptr<VideoTrack> Create(...);
    void RemoveSink(rtc::VideoSinkInterface<VideoFrame>* sink);
    VideoTrackSourceInterface* GetSource();
    ContentHint content_hint();
    void set_content_hint(ContentHint hint);
    bool set_enabled(bool enable);
    std::string kind();
private:
    OnChanged();
};

#endif //BIG_TEST_HPP