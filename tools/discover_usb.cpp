#include "libusb_transport.hpp"
#include "../logging.hpp"
#include <iostream>
#include <chrono>
#include <thread>

using namespace fibre;

DEFINE_LOG_TOPIC(EXAMPLE);
USE_LOG_TOPIC(EXAMPLE);

int main() {
    EventLoop event_loop;
    LibusbDiscoverer discoverer;

    // Initialize the discoverer
    if (discoverer.init(&event_loop) != 0) {
        FIBRE_LOG(E) << "Failed to initialize LibusbDiscoverer";
        return 1;
    }

    // Define the USB device search path
    const char* search_path = "usb:idVendor=0x1209,idProduct=0x0D32,bInterfaceClass=0,bInterfaceSubClass=1,bInterfaceProtocol=0";
    size_t search_path_len = strlen(search_path);

    // Define a callback for when a channel is found
    class MyCompleter : public Completer<ChannelDiscoveryResult> {
    public:
        void complete(ChannelDiscoveryResult result) override {
            if (result.status == kFibreOk) {
                FIBRE_LOG(I) << "Found a matching USB device!";
                if (result.ep_in) {
                    FIBRE_LOG(I) << "  Bulk IN Endpoint: " << result.ep_in->endpoint_id();
                }
                if (result.ep_out) {
                    FIBRE_LOG(I) << "  Bulk OUT Endpoint: " << result.ep_out->endpoint_id();
                }
                // You can now use result.ep_in and result.ep_out to communicate with the device
                // For example, you can start a transfer:
                // result.ep_out->start_transfer(...);
            } else if (result.status == kFibreInvalidArgument) {
                FIBRE_LOG(E) << "Invalid search path.";
            } else {
                FIBRE_LOG(E) << "Failed to find a matching USB device.";
            }
        }
    };

    MyCompleter completer;
    ChannelDiscoveryContext* handle = nullptr;

    // Start the channel discovery
    discoverer.start_channel_discovery(search_path, search_path_len, &handle, completer);

    // Let the discovery run for a while
    std::this_thread::sleep_for(std::chrono::seconds(5));

    // Stop the channel discovery
    if (handle) {
        discoverer.stop_channel_discovery(handle);
    }

    // Deinitialize the discoverer
    discoverer.deinit(0);

    FIBRE_LOG(I) << "Finished.";
    return 0;
}