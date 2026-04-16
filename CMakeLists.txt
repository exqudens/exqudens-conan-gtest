cmake_minimum_required(VERSION "3.25" FATAL_ERROR)

set(CMAKE_UTIL_FILE "" CACHE STRING "...")
set(USE_CONAN "1" CACHE BOOL "...")

message(STATUS "USE_CONAN: '${USE_CONAN}'")

string(REPLACE "." ";" PRESET_NAME_ELEMENTS "${PRESET_NAME}")

if("${USE_CONAN}")
    if("windows" IN_LIST "PRESET_NAME_ELEMENTS")
        find_program(CONAN_COMMAND NAMES "conan.exe" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    else()
        find_program(CONAN_COMMAND NAMES "conan" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    endif()
    message(STATUS "CONAN_COMMAND: '${CONAN_COMMAND}'")
endif()

if("${CMAKE_UTIL_FILE}" STREQUAL "")
    if("$ENV{CMAKE_UTIL_FILE}" STREQUAL "")
        if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake")
            if("${USE_CONAN}")
                #[[execute_process(
                    COMMAND "${CONAN_COMMAND}" "user" "$ENV{CONAN_LOGIN_USERNAME}" "-r" "artifactory" "-p"
                    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                    COMMAND_ECHO "STDOUT"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )]]
                execute_process(
                    COMMAND "${CONAN_COMMAND}" "install" "--tool-requires=exqudens-cmake/0.0.1" "--deployer" "direct_deploy" "--deployer-folder" "${CMAKE_SOURCE_DIR}/build/dependencies"
                    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                    COMMAND_ECHO "STDOUT"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )
                set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
            else()
                message(FATAL_ERROR "Unable to resolve CMAKE_UTIL_FILE: '${CMAKE_UTIL_FILE}'")
            endif()
        else()
            set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
        endif()
    else()
        set(CMAKE_UTIL_FILE "$ENV{CMAKE_UTIL_FILE}" CACHE STRING "..." FORCE)
    endif()
endif()

include("${CMAKE_UTIL_FILE}")

if("msvc-x64-x64" IN_LIST "PRESET_NAME_ELEMENTS")
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/msvc-x64-x64-toolchain.cmake")
        set_msvc_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            VERSION "17"
            HOST "x64"
            TARGET "x64"
            SET_CMAKE_SYSTEM_NAME "0"
            OUTPUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/msvc-x64-x64-toolchain.cmake"
        )
    endif()
elseif("gcc" IN_LIST PRESET_NAME_ELEMENTS)
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/gcc-toolchain.cmake")
        find_file(compilerFile NAMES "gcc" PATHS ENV GCC_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
        set_gnu_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            PATH "${compilerFile}"
            SET_CMAKE_SYSTEM_NAME "0"
            OUTPUT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/gcc-toolchain.cmake"
        )
    endif()
endif()

message(STATUS "CMAKE_TOOLCHAIN_FILE: '${CMAKE_TOOLCHAIN_FILE}'")

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.txt" INFO)
string(REPLACE ":" ";" INFO_LIST "${INFO}")
list(GET INFO_LIST 0 RAW_NAME)
list(GET INFO_LIST 1 RAW_VERSION)
string(STRIP "${RAW_NAME}" NAME)
string(STRIP "${RAW_VERSION}" VERSION)
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message(STATUS "project: '${PROJECT_NAME}-${PROJECT_VERSION}'")

enable_language("C")
enable_language("CXX")
include("GenerateExportHeader")
include("CMakePackageConfigHelpers")
enable_testing()
include("GoogleTest")

if("${CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT}")
    set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/cmake-install" CACHE PATH "..." FORCE)
endif()
set(CMAKE_VERBOSE_MAKEFILE "1" CACHE BOOL "..." FORCE)
set(CMAKE_EXPORT_COMPILE_COMMANDS "1" CACHE BOOL "..." FORCE)

cmake_path(RELATIVE_PATH "PROJECT_BINARY_DIR" BASE_DIRECTORY "${PROJECT_SOURCE_DIR}" OUTPUT_VARIABLE "PROJECT_BINARY_DIR_REL")
cmake_path(CONVERT "$ENV{PATH}" TO_CMAKE_PATH_LIST "ENV_PATH" NORMALIZE)
set(CMAKE_OBJECT_PATH_MAX "1000")
set(CMAKE_SHARED_LIBRARY_PREFIX "")
set(CMAKE_SHARED_MODULE_PREFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_IMPORT_LIBRARY_PREFIX "")
set(CMAKE_STAGING_PREFIX "")
set(CMAKE_FIND_LIBRARY_PREFIXES "" "lib")
set(CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH "0")
set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH "0")
set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH "1")
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY "0")
set(CMAKE_FIND_USE_PACKAGE_REGISTRY "0")
set(CMAKE_FIND_USE_PACKAGE_ROOT_PATH "0")
set(CMAKE_FIND_USE_CMAKE_PATH "1")
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG "0")
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS "1")
set(CMAKE_BUILD_RPATH "\$ORIGIN")
set(CMAKE_INSTALL_RPATH "\$ORIGIN")
set(CMAKE_SKIP_BUILD_RPATH "1")
set(CMAKE_BUILD_RPATH_USE_ORIGIN "1")
set(CMAKE_BUILD_WITH_INSTALL_RPATH "1")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH "0")
set(CMAKE_CXX_VISIBILITY_PRESET "default") # "default" or "hidden"
set(CMAKE_VISIBILITY_INLINES_HIDDEN "0")
set(CMAKE_C_STANDARD "11")
set(CMAKE_C_STANDARD_REQUIRED "1")
set(CMAKE_C_EXTENSIONS "0")
set(CMAKE_CXX_STANDARD "20")
set(CMAKE_CXX_STANDARD_REQUIRED "1")
set(CMAKE_CXX_EXTENSIONS "0")

if("msvc-x64-x64" IN_LIST "PRESET_NAME_ELEMENTS")
    #set(CMAKE_CXX_STANDARD_LIBRARIES "${CMAKE_CXX_STANDARD_LIBRARIES} setupapi.lib")
    separate_arguments(CMAKE_CXX_FLAGS NATIVE_COMMAND "${CMAKE_CXX_FLAGS}")
    if(NOT "/EHa" IN_LIST CMAKE_CXX_FLAGS AND "/EHsc" IN_LIST CMAKE_CXX_FLAGS)
        list(REMOVE_ITEM CMAKE_CXX_FLAGS "/EHsc")
        list(APPEND CMAKE_CXX_FLAGS "/EHa")
    endif()
    string(JOIN " " CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
    set(CMAKE_RC_FLAGS "${CMAKE_RC_FLAGS} -D_WINDOWS")
    foreach(v IN LISTS "CMAKE_C_STANDARD_INCLUDE_DIRECTORIES")
        cmake_path(NATIVE_PATH "v" NORMALIZE "vn")
        set(CMAKE_RC_FLAGS "${CMAKE_RC_FLAGS} -I \"${vn}\"")
    endforeach()
endif()

set(SKIP_TEST "0" CACHE BOOL "" FORCE)
set(TARGET_CMAKE_INSTALL_DEPENDS_ON "gmock" "gmock_main" "${PROJECT_NAME}" "${PROJECT_NAME}_main")
if(NOT "${SKIP_TEST}")
    set(TARGET_CMAKE_INSTALL_DEPENDS_ON "cmake-test")
endif()

string(TOLOWER "${PROJECT_NAME}" PROJECT_NAME_LOWER)
set(PROJECT_VERSION_NOTWEAK "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")
set(BASE_DIR "${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}")
cmake_path(RELATIVE_PATH "BASE_DIR" BASE_DIRECTORY "${PROJECT_SOURCE_DIR}" OUTPUT_VARIABLE "BASE_DIR_REL")

if("${USE_CONAN}")
    set_conan_architecture(CONAN_ARCH "${CMAKE_SYSTEM_PROCESSOR}")
    set_conan_os(CONAN_OS "${CMAKE_SYSTEM_NAME}")
    set_conan_compiler(CONAN_COMPILER "${CMAKE_CXX_COMPILER_ID}")
    set_conan_compiler_version(CONAN_COMPILER_VERSION "${CMAKE_CXX_COMPILER_ID}" "${CMAKE_CXX_COMPILER_VERSION}" MAX_ELEMENTS "1")
    set_conan_compiler_runtime(CONAN_COMPILER_RUNTIME "${CMAKE_MSVC_RUNTIME_LIBRARY}")
    set_conan_compiler_runtime_type(CONAN_COMPILER_RUNTIME_TYPE "${CMAKE_MSVC_RUNTIME_LIBRARY}")

    set_python_boolean(CONAN_INTERFACE_ONLY "${INTERFACE_ONLY}")
    set_python_boolean(CONAN_BUILD_SHARED_LIBS "${BUILD_SHARED_LIBS}")

    set_conan_settings(CONAN_SETTINGS
        "arch=${CONAN_ARCH}"
        "os=${CONAN_OS}"
        "compiler=${CONAN_COMPILER}"
        "compiler.version=${CONAN_COMPILER_VERSION}"
        "compiler.cstd=${CMAKE_C_STANDARD}"
        "compiler.cppstd=${CMAKE_CXX_STANDARD}"
        "compiler.runtime=${CONAN_COMPILER_RUNTIME}"
        "compiler.runtime_type=${CONAN_COMPILER_RUNTIME_TYPE}"
        "compiler.libcxx=${CONAN_COMPILER_LIBCXX}"
        "build_type=${CMAKE_BUILD_TYPE}"
    )
    set_conan_options(CONAN_OPTIONS
        "&:shared=${CONAN_BUILD_SHARED_LIBS}"
        "*:shared=${CONAN_BUILD_SHARED_LIBS}"
    )
    set(CONAN_INSTALL_PREFIX "${PROJECT_BINARY_DIR}/conan-install")

    if(NOT EXISTS "${BASE_DIR}")
        #[[execute_process(
            COMMAND "${CONAN_COMMAND}" "user" "$ENV{CONAN_LOGIN_USERNAME}" "-r" "artifactory" "-p"
            WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
            COMMAND_ECHO "STDOUT"
            ENCODING "UTF-8"
            COMMAND_ERROR_IS_FATAL "ANY"
        )]]
        execute_process(
            COMMAND "${CONAN_COMMAND}" "install"
                    "--output-folder" "${BASE_DIR}"
                    "${PROJECT_SOURCE_DIR}/build-conanfile.py"
            WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
            COMMAND_ECHO "STDOUT"
            ENCODING "UTF-8"
            COMMAND_ERROR_IS_FATAL "ANY"
        )
    endif()
else()
    message(FATAL_ERROR "unable to get BASE_DIR_REL: '${BASE_DIR_REL}'")
endif()

# apply custom cmake package version
file(READ "${BASE_DIR}/CMakeLists.txt" "${PROJECT_NAME}_CMAKE_LISTS_CONTENT")
set("${PROJECT_NAME}_CMAKE_LISTS_VERSION_ANCHOR" "set(GOOGLETEST_VERSION 1.11.0)")
string(FIND "${${PROJECT_NAME}_CMAKE_LISTS_CONTENT}" "${${PROJECT_NAME}_CMAKE_LISTS_VERSION_ANCHOR}" "${PROJECT_NAME}_CMAKE_LISTS_VERSION_INDEX")
if(NOT "${${PROJECT_NAME}_CMAKE_LISTS_VERSION_INDEX}" STREQUAL "-1")
    string(REPLACE "${${PROJECT_NAME}_CMAKE_LISTS_VERSION_ANCHOR}" "set(GOOGLETEST_VERSION ${PROJECT_VERSION})" "${PROJECT_NAME}_CMAKE_LISTS_CONTENT" "${${PROJECT_NAME}_CMAKE_LISTS_CONTENT}")
    file(WRITE "${BASE_DIR}/CMakeLists.txt" "${${PROJECT_NAME}_CMAKE_LISTS_CONTENT}")
endif()

if("${BUILD_SHARED_LIBS}")
    set(gtest_force_shared_crt ON)
endif()

add_subdirectory("${BASE_DIR_REL}")

if(NOT "${SKIP_TEST}")
    add_library("test-lib"
        "src/test/cpp/TestUtils.hpp"
        "src/test/cpp/TestUtils.cpp"
        "src/test/cpp/TestApplication.hpp"
        "src/test/cpp/TestApplication.cpp"

        "src/test/cpp/unit/FunctionalUnitTests.hpp"
    )
    generate_export_header("test-lib"
        BASE_NAME "TEST_LIB"
        EXPORT_FILE_NAME "generated/src/test/cpp/test_lib_export.hpp"
    )
    if(NOT "${BUILD_SHARED_LIBS}")
        target_compile_definitions("test-lib" PUBLIC
            "TEST_LIB_STATIC_DEFINE"
        )
    endif()
    target_include_directories("test-lib" PUBLIC
        "$<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/generated/src/test/cpp>"
        "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src/test/cpp>"
        "$<INSTALL_INTERFACE:include>"
    )
    target_link_libraries("test-lib" PUBLIC
        "GTest::gmock"
        "GTest::gtest"
        "GTest::gmock_main"
        "GTest::gtest_main"
    )
    set_target_properties("test-lib" PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/bin"

        ARCHIVE_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/lib"

        LIBRARY_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/lib"
    )

    add_executable("test-app"
        "src/test/cpp/main.cpp"
    )
    target_link_libraries("test-app"
        "test-lib"
    )
    set_target_properties("test-app" PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/bin"
        RUNTIME_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/bin"

        ARCHIVE_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/lib"
        ARCHIVE_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/lib"

        LIBRARY_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/test/lib"
        LIBRARY_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/test/lib"
    )
    if("${BUILD_SHARED_LIBS}")
        if("${CMAKE_SYSTEM_NAME}" STREQUAL "Windows")
            add_custom_command(TARGET "test-app"
                PRE_BUILD
                #COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "${CONAN_INSTALL_PREFIX}/test/bin" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                #COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "${CONAN_INSTALL_PREFIX}/bin" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "$<TARGET_PROPERTY:${PROJECT_NAME},RUNTIME_OUTPUT_DIRECTORY>" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                USES_TERMINAL
                VERBATIM
            )
        else()
            add_custom_command(TARGET "test-app"
                PRE_BUILD
                #COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "${CONAN_INSTALL_PREFIX}/test/lib" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "$<TARGET_PROPERTY:test-lib,LIBRARY_OUTPUT_DIRECTORY>" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                #COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "${CONAN_INSTALL_PREFIX}/lib" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                COMMAND "${CMAKE_COMMAND}" "-E" "copy_directory" "$<TARGET_PROPERTY:${PROJECT_NAME},LIBRARY_OUTPUT_DIRECTORY>" "$<TARGET_PROPERTY:test-app,RUNTIME_OUTPUT_DIRECTORY>"
                WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                USES_TERMINAL
                VERBATIM
            )
        endif()
    endif()
    add_custom_command(TARGET "test-app"
        POST_BUILD
        COMMAND "$<TARGET_FILE:test-app>" "--gtest_list_tests" "--gtest_output=json:tests.json" "--project-binary-dir=${PROJECT_BINARY_DIR}"
        WORKING_DIRECTORY "$<TARGET_FILE_DIR:test-app>"
        USES_TERMINAL
        VERBATIM
    )

    gtest_discover_tests("test-app"
        DISCOVERY_EXTRA_ARGS "--project-binary-dir=${PROJECT_BINARY_DIR}"
        EXTRA_ARGS "--project-binary-dir=${PROJECT_BINARY_DIR}"
        WORKING_DIRECTORY "$<TARGET_FILE_DIR:test-app>"
        PROPERTIES ENVIRONMENT "PATH=$<TARGET_FILE_DIR:test-app>;${ENV_PATH}"
    )

    set(TEST_GROUP ".*UnitTests" CACHE STRING "...")
    set(TEST_METHOD "all" CACHE STRING "...")

    if("${TEST_GROUP}" STREQUAL "all" AND "${TEST_METHOD}" STREQUAL "all")
        set(TEST_PATTERN "^.+\\..+$")
    elseif("${TEST_GROUP}" STREQUAL "all")
        set(TEST_PATTERN "^.+\\.${TEST_METHOD}$")
    elseif("${TEST_METHOD}" STREQUAL "all")
        set(TEST_PATTERN "^${TEST_GROUP}\\..+$")
    endif()

    message(STATUS "TEST_PATTERN: '${TEST_PATTERN}'")

    add_custom_command(
        OUTPUT "${PROJECT_BINARY_DIR}/junit.xml"
        COMMAND "${CMAKE_CTEST_COMMAND}"
                "--build-nocmake"
                "--output-junit" "${PROJECT_BINARY_DIR}/junit.xml"
                "--test-dir" "${PROJECT_BINARY_DIR}"
                #"-R" "^.+\\..+$"
                #"-R" "^FunctionalSystemTests\\..+$"
                #"-R" "^FunctionalUnitTests\\..+$"
                "-R" "${TEST_PATTERN}"
        DEPENDS "test-app"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("cmake-test"
        DEPENDS "${PROJECT_BINARY_DIR}/junit.xml"
    )
endif()

add_custom_command(
    OUTPUT "${CMAKE_INSTALL_PREFIX}/lib/cmake/GTest/GTestConfig.cmake"
    COMMAND "${CMAKE_COMMAND}" "--install" "${PROJECT_BINARY_DIR}" "--prefix" "${CMAKE_INSTALL_PREFIX}"
    DEPENDS ${TARGET_CMAKE_INSTALL_DEPENDS_ON}
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("cmake-install" ALL
    DEPENDS "${CMAKE_INSTALL_PREFIX}/lib/cmake/GTest/GTestConfig.cmake"
)

if("${USE_CONAN}")
    add_custom_target("conan-export"
        COMMAND "${CONAN_COMMAND}" "export-pkg"
                "--output-folder" "${CMAKE_INSTALL_PREFIX}"
                ${CONAN_SETTINGS}
                ${CONAN_OPTIONS}
                #"--user" "gitlab-group+gitlab-sub-group+${PROJECT_NAME}"
                #"--channel" "stable"
                "${PROJECT_SOURCE_DIR}/conanfile.py"
        DEPENDS "cmake-install"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-remove"
        COMMAND "${CONAN_COMMAND}" "remove" "-c" "${PROJECT_NAME}/${PROJECT_VERSION}"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-list"
        COMMAND "${CONAN_COMMAND}" "list" "${PROJECT_NAME}/${PROJECT_VERSION}:*"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )
endif()

add_custom_target("vscode"
    COMMAND "${CMAKE_COMMAND}" "-E" "make_directory" "${PROJECT_SOURCE_DIR}/.vscode"
    COMMAND "${CMAKE_COMMAND}" "-E" "copy" "${PROJECT_SOURCE_DIR}/src/test/resources/vscode/tasks.json" "${PROJECT_SOURCE_DIR}/.vscode"
    COMMAND "${CMAKE_COMMAND}" "-P" "cmake/util.cmake" "--" "vscode"
            SOURCE_DIR "${PROJECT_SOURCE_DIR}"
            BINARY_DIR "${PROJECT_BINARY_DIR}"

            LAUNCH_GENERATE "1"
            LAUNCH_FILE_OVERWRITE "1"
            LAUNCH_TEMPLATE_FILE "${PROJECT_SOURCE_DIR}/src/test/resources/vscode/command-variable-launch.json"
            LAUNCH_FILE "${PROJECT_SOURCE_DIR}/.vscode/launch.json"
            LAUNCH_TESTS_FILE "${PROJECT_BINARY_DIR}/test/bin/tests.json"
            LAUNCH_TESTS "*.*" "*UnitTests.*"
            LAUNCH_TESTS_INDENT "20"
    DEPENDS "${PROJECT_NAME}" "test-app"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("clion"
    COMMAND "${CMAKE_COMMAND}" "-P" "cmake/util.cmake" "--" "clion"
            SOURCE_DIR "${PROJECT_SOURCE_DIR}"
            BINARY_DIR "${PROJECT_BINARY_DIR}"

            GTEST_GENERATE "1"
            GTEST_FILES_OVERWRITE "1"
            GTEST_TESTS_FILE "${PROJECT_BINARY_DIR}/test/bin/tests.json"
            GTEST_TEMPLATE_FILE "${PROJECT_SOURCE_DIR}/src/test/resources/clion/gtest/filter-run.xml"
            GTEST_CONFIG_NAME "${PRESET_NAME}"
            GTEST_PROJECT_NAME "${PROJECT_NAME}"
            GTEST_TARGET_NAME "test-app"
            GTEST_OUTPUT_DIR "${PROJECT_SOURCE_DIR}/.clion/gtest"
            GTEST_TESTS "*.*" "*UnitTests.*" "*IntegrationTests.*"
            GTEST_PROGRAM_PARAMS "--project-binary-dir=${PROJECT_BINARY_DIR}"
    DEPENDS "${PROJECT_NAME}" "test-app"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

set_target_names(ALL_TARGETS "${CMAKE_CURRENT_SOURCE_DIR}")
message(STATUS "all-targets:")
foreach(t IN LISTS ALL_TARGETS)
    message(STATUS "${t}")
endforeach()

set("${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES"
    "${CMAKE_INSTALL_PREFIX}"
)
set_directory_properties(PROPERTIES
    ADDITIONAL_CLEAN_FILES "${${PROJECT_NAME}_ADDITIONAL_CLEAN_FILES}"
)
