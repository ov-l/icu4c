
cmake_minimum_required(VERSION 3.10)
project(ICU VERSION 1.0.0 LANGUAGES CXX)

# Find all source files in common and i18n directories
file(GLOB_RECURSE ICU_SOURCES
  "common/*.cpp"
  "i18n/*.cpp"
)

# Create static library
add_library(uc STATIC ${ICU_SOURCES})

# Set include directories
target_include_directories(uc
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/common>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/i18n>
    $<INSTALL_INTERFACE:include/uc>
)

# Set properties for the target
set_target_properties(uc PROPERTIES
  CXX_STANDARD 20
  CXX_STANDARD_REQUIRED ON
  POSITION_INDEPENDENT_CODE ON
)

target_compile_definitions(uc
  PUBLIC
    U_COMMON_IMPLEMENTATION
    U_I18N_IMPLEMENTATION
    U_STATIC_IMPLEMENTATION
    UCONFIG_NO_COLLATION
    UCONFIG_NO_CONVERSION
    UCONFIG_NO_FORMATTING
    UCONFIG_NO_SERVICE
    UCONFIG_NO_IDNA
    UCONFIG_NO_FILE_IO
    UCONFIG_NO_TRANSLITERATION
    "PKGDATA_MODE=static"
    "U_ENABLE_DYLOAD=0"
    "U_HAVE_LIB_SUFFIX=1"
    "U_LIB_SUFFIX_C_NAME=_lxe"
)

# Create an export set for the target
install(TARGETS uc
  EXPORT icu4cTargets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION include/uc
)

# Install headers
install(DIRECTORY common/ i18n/
  DESTINATION include/uc
  FILES_MATCHING PATTERN "*.h"
)

# Export targets
install(EXPORT icu4cTargets
  FILE icu4cTargets.cmake
  NAMESPACE ICU::
  DESTINATION lib/cmake/uc
)

# Create config file template
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfig.cmake.in "
@PACKAGE_INIT@
include(\${CMAKE_CURRENT_LIST_DIR}/icu4cTargets.cmake)
check_required_components(uc)
")

# Create and install config file
include(CMakePackageConfigHelpers)
configure_package_config_file(
  ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfig.cmake
  INSTALL_DESTINATION lib/cmake/uc
)

# Create and install version file
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)

# Install config files
install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/icu4cConfigVersion.cmake
  DESTINATION lib/cmake/uc
)