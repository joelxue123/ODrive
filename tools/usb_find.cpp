#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <libusb-1.0/libusb.h>
#include <ctime>
#include <atomic>
#include <sched.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define ODRIVE_OUT_EP 0x03
#define ODRIVE_IN_EP 0x83

int odrive_command_task(libusb_device_handle *handle, unsigned char* response, int response_size) {
    int ret;
    int actual_length;
    unsigned char data[] = {0xdb, 0x05, 0x32, 0x80, 0x04, 0x00, 0x50, 0x29};
    auto start = std::chrono::high_resolution_clock::now();

    // 转换为微秒
    auto duration_us = std::chrono::duration_cast<std::chrono::microseconds>(start.time_since_epoch());
    long long microseconds = duration_us.count();
    std::cout << "time: " << microseconds << std::endl;
    ret = libusb_bulk_transfer(handle, ODRIVE_OUT_EP, data, sizeof(data), &actual_length, 10);
    if (ret != 0) {
        std::cerr << "libusb_bulk_transfer error (send): " << libusb_error_name(ret) << std::endl;
        return -1; // Indicate send error
    }
    else{
        
    }

    ret = libusb_bulk_transfer(handle,
                                ODRIVE_IN_EP,
                                response,
                                response_size,
                                &actual_length,
                                1000);

    if (ret == 0) {
        return actual_length; // Return the number of bytes received
    } else {
        printf("No response\n"); // Removed print for performance
        return -2; // Indicate receive error
    }
}

void periodic_task(libusb_device_handle *handle, std::atomic<bool>& running) {
    unsigned char response[64];
    auto start_time = std::chrono::high_resolution_clock::now();
    auto next_time = start_time;
    const std::chrono::microseconds period(100); // 0.2ms period

    // Attempt to set real-time scheduling
    struct sched_param params;
    params.sched_priority = sched_get_priority_max(SCHED_FIFO);
    if (pthread_setschedparam(pthread_self(), SCHED_FIFO, &params) != 0) {
        std::cerr << "Failed to set real-time scheduling. Continuing without it." << std::endl;
    }

    while (running) {
        next_time += period;
        while (std::chrono::high_resolution_clock::now() < next_time) {
            std::this_thread::yield();
        }

        int result = odrive_command_task(handle, response, sizeof(response));

        if (result > 0) {
            // Process the response
            //std::cout << "Task completed successfully. Received " << result << " bytes." << std::endl; // Removed print for performance
        } else if (result == -1) {
            std::cerr << "Task failed: Send error." << std::endl;
        } else if (result == -2) {
            std::cerr << "Task failed: Receive error." << std::endl;
        }
    }
}

int main() {
    libusb_device_handle *handle;
    libusb_context *ctx = NULL;
    int ret;
    int actual_length;

    ret = libusb_init(&ctx);
    if (ret < 0) {
        std::cerr << "libusb_init error: " << libusb_error_name(ret) << std::endl;
        return 1;
    }

    handle = libusb_open_device_with_vid_pid(ctx, 0x1209, 0x0d32);
    if (!handle) {
        std::cerr << "Failed to open device" << std::endl;
        libusb_exit(ctx);
        return 1;
    }
    else{
        std::cout << "Device opened successfully" << std::endl;
    }

    std::atomic<bool> running(true);
    std::thread task_thread(periodic_task, handle, std::ref(running));

    std::this_thread::sleep_for(std::chrono::seconds(1)); // Run for 1 second

    running = false;
    task_thread.join();

    libusb_close(handle);
    libusb_exit(ctx);
    return 0;
}