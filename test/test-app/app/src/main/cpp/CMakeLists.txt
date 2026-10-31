# https://developer.android.com/studio/projects/configure-cmake

# Sets the minimum version of CMake required to build your native library.
# This ensures that a certain set of CMake features is available to
# your build.

cmake_minimum_required(VERSION 3.4.1)

set(OMVLL "-fpass-plugin=/home/gemesa/projects/omvll/omvll-ndk.so")
if(NOT CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_C_FLAGS   "${CMAKE_C_FLAGS} ${OMVLL}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OMVLL}")
endif()

project(test)

# Specifies a library name, specifies whether the library is STATIC or
# SHARED, and provides relative paths to the source code. You can
# define multiple libraries by adding multiple add_library() commands,
# and CMake builds them for you. When you build your app, Gradle
# automatically packages shared libraries with your APK.

add_library( # Specifies the name of the library.
        native-lib

        # Sets the library as a shared library.
        SHARED

        # Provides a relative path to your source file(s).
        native-lib.cpp )