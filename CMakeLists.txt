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

cmake_path(CONVERT "$ENV{HOME}" TO_CMAKE_PATH_LIST HOME NORMALIZE)
if(NOT EXISTS "${HOME}" OR NOT IS_DIRECTORY "${HOME}")
    message(FATAL_ERROR "HOME: '${HOME}' not exists or not directory.")
endif()
set(CMAKE_HOME "${HOME}/.cmake")
if(NOT EXISTS "${CMAKE_HOME}")
    file(MAKE_DIRECTORY "${CMAKE_HOME}")
endif()
if(NOT EXISTS "${CMAKE_HOME}" OR NOT IS_DIRECTORY "${CMAKE_HOME}")
    message(FATAL_ERROR "CMAKE_HOME: '${CMAKE_HOME}' not exists or not directory.")
endif()
set(CMAKE_DOWNLOADS "${CMAKE_HOME}/downloads")
if(NOT EXISTS "${CMAKE_DOWNLOADS}")
    file(MAKE_DIRECTORY "${CMAKE_DOWNLOADS}")
endif()
if(NOT EXISTS "${CMAKE_DOWNLOADS}" OR NOT IS_DIRECTORY "${CMAKE_DOWNLOADS}")
    message(FATAL_ERROR "CMAKE_DOWNLOADS: '${CMAKE_DOWNLOADS}' is not directory.")
endif()
if(NOT EXISTS "${CMAKE_DOWNLOADS}/${PROJECT_NAME}-${PROJECT_VERSION}.zip")
    message("download ...")
    file(DOWNLOAD
            "https://github.com/google/googletest/archive/refs/tags/release-${PROJECT_VERSION}.zip"
            "${CMAKE_DOWNLOADS}/${PROJECT_NAME}-${PROJECT_VERSION}.zip"
            EXPECTED_MD5 "52943a59cefce0ae0491d4d2412c120b"
    )
    message("... done")
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-${PROJECT_VERSION}.zip")
    message("copy from downloads ...")
    file(COPY "${CMAKE_DOWNLOADS}/${PROJECT_NAME}-${PROJECT_VERSION}.zip" DESTINATION "${PROJECT_BINARY_DIR}")
    message("... done")
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/googletest-release-${PROJECT_VERSION}")
    file(ARCHIVE_EXTRACT INPUT "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-${PROJECT_VERSION}.zip")
endif()
if(NOT EXISTS "${PROJECT_BINARY_DIR}/${PROJECT_NAME}")
    file(MAKE_DIRECTORY "${PROJECT_BINARY_DIR}/${PROJECT_NAME}")
    file(COPY "${PROJECT_BINARY_DIR}/googletest-release-${PROJECT_VERSION}/" DESTINATION "${PROJECT_BINARY_DIR}/${PROJECT_NAME}")
endif()
get_filename_component("PROJECT_BINARY_DIR_NAME" "${PROJECT_BINARY_DIR}" NAME)
get_filename_component("PROJECT_BINARY_DIR_PARENT" "${PROJECT_BINARY_DIR}" DIRECTORY)
get_filename_component("PROJECT_BINARY_DIR_PARENT_NAME" "${PROJECT_BINARY_DIR_PARENT}" NAME)

add_subdirectory("${PROJECT_BINARY_DIR_PARENT_NAME}/${PROJECT_BINARY_DIR_NAME}/${PROJECT_NAME}")

add_custom_target("cmake-install"
    COMMAND "${CMAKE_COMMAND}" --install "${PROJECT_BINARY_DIR}" --prefix "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME}"
    DEPENDS "gmock" "gmock_main" "${PROJECT_NAME}" "${PROJECT_NAME}_main"
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
            "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME}"
            ${CONAN_SETTINGS}
            ${CONAN_OPTIONS}
    DEPENDS "cmake-install"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    VERBATIM
)
