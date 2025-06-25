cmake_minimum_required(VERSION 3.10)
project(cpp_backend)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)
pybind11_add_module(cpp_backend cpp_backend.cpp)

add_custom_command(TARGET cpp_backend POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    $<TARGET_FILE:cpp_backend>
    ${CMAKE_SOURCE_DIR}/..
)