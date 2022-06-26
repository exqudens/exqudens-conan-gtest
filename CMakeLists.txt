cmake_minimum_required(VERSION 3.21 FATAL_ERROR)
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.txt" INFO)
string(REPLACE ":" ";" INFO_LIST "${INFO}")
list(GET INFO_LIST 0 RAW_NAME)
list(GET INFO_LIST 1 RAW_VERSION)
string(STRIP "${RAW_NAME}" NAME)
string(STRIP "${RAW_VERSION}" VERSION)
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message("project: '${PROJECT_NAME}-${PROJECT_VERSION}'")

include("util.cmake")
include("config.cmake")

if(NOT EXISTS "${PROJECT_BINARY_DIR}/googletest-release-1.11.0.zip")
    file(DOWNLOAD
        "file:///C:/install/googletest-release-1.11.0.zip" #"https://github.com/google/googletest/archive/refs/tags/release-1.11.0.zip"
        "${PROJECT_BINARY_DIR}/googletest-release-1.11.0.zip"
        EXPECTED_MD5 "52943a59cefce0ae0491d4d2412c120b"
        )
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/googletest-release-1.11.0")
    file(ARCHIVE_EXTRACT INPUT "${PROJECT_BINARY_DIR}/googletest-release-1.11.0.zip")
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/gtest")
    file(MAKE_DIRECTORY "${PROJECT_BINARY_DIR}/gtest")
    file(COPY "${PROJECT_BINARY_DIR}/googletest-release-1.11.0/" DESTINATION "${PROJECT_BINARY_DIR}/gtest")
endif()
get_filename_component("PROJECT_BINARY_DIR_NAME" "${PROJECT_BINARY_DIR}" NAME)
get_filename_component("PROJECT_BINARY_DIR_PARENT" "${PROJECT_BINARY_DIR}" DIRECTORY)
get_filename_component("PROJECT_BINARY_DIR_PARENT_NAME" "${PROJECT_BINARY_DIR_PARENT}" NAME)

add_subdirectory("${PROJECT_BINARY_DIR_PARENT_NAME}/${PROJECT_BINARY_DIR_NAME}/gtest")

add_custom_target("cmake-install"
    COMMAND "${CMAKE_COMMAND}" --install "${PROJECT_BINARY_DIR}" --prefix "${CMAKE_INSTALL_PREFIX}/gtest"
    DEPENDS "gmock" "gmock_main" "gtest" "gtest_main"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
)

set_conan_settings(CONAN_SETTINGS
    "${CMAKE_SYSTEM_NAME}"
    "${CMAKE_SYSTEM_PROCESSOR}"
    "${CMAKE_CXX_COMPILER_ID}"
    "${CMAKE_CXX_COMPILER_VERSION}"
    "${CMAKE_MSVC_RUNTIME_LIBRARY}"
    "${CMAKE_CXX_STANDARD}"
    "${CMAKE_BUILD_TYPE}"
)

set_conan_options(CONAN_OPTIONS
    "shared=${CONAN_BUILD_SHARED_LIBS}"
)

add_custom_target("conan-export" ALL
    COMMAND "${CONAN_COMMAND}"
            export-pkg
            --force
            "${PROJECT_SOURCE_DIR}/conanfile.py"
            #"gitlab-group+gitlab-sub-group+${PROJECT_NAME}/stable"
            --package-folder
            "${CMAKE_INSTALL_PREFIX}/gtest"
            ${CONAN_SETTINGS}
            ${CONAN_OPTIONS}
    DEPENDS "cmake-install"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
)
