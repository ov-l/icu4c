
cmake_minimum_required(VERSION 3.10)
project(ICU VERSION 77.1 LANGUAGES CXX)

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
    $<INSTALL_INTERFACE:include>
)

# Set properties for the target
set_target_properties(uc PROPERTIES
  CXX_STANDARD 20
  CXX_STANDARD_REQUIRED ON
  POSITION_INDEPENDENT_CODE ON
  VERSION ${PROJECT_VERSION}
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
    "U_SHOW_CPLUSPLUS_API=1"
    "U_SHOW_CPLUSPLUS_HEADER_API=1"
)

# Create an export set for the target
install(TARGETS uc
  EXPORT ICUTargets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION include/ICU
)

# Install headers
install(DIRECTORY common/ i18n/
  DESTINATION include/ICU
  FILES_MATCHING PATTERN "*.h"
)

# Export targets
install(EXPORT ICUTargets
  FILE ICUTargets.cmake
  NAMESPACE ICU::
  DESTINATION lib/cmake/ICU
)

# Create config file template
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/ICUConfig.cmake.in "
@PACKAGE_INIT@
include(\${CMAKE_CURRENT_LIST_DIR}/ICUTargets.cmake)
check_required_components(uc)
")

# Create and install config file
include(CMakePackageConfigHelpers)
configure_package_config_file(
  ${CMAKE_CURRENT_BINARY_DIR}/ICUConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/ICUConfig.cmake
  INSTALL_DESTINATION lib/cmake/ICU
)

# Create and install version file
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/ICUConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)

# Install config files
install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/ICUConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/ICUConfigVersion.cmake
  DESTINATION lib/cmake/ICU
)