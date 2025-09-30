# ============================================================
# CmakeLists overview (pymanga_cpp) — What this CMake does
# Author: Guanzhen
# Date:   2025-09-16
# ============================================================
# Goals
# - Build high-performance Python extension modules (pybind11) for pyMANGA.
# - Keep a developer-friendly layout (write .so/.pyd back into the source tree)
#   while also supporting clean install into Python’s site-packages.
#
# Key features
# 1) Python & pybind11 integration
#    - Locates Python (Interpreter + Development.Module) and pybind11.
#    - Falls back to discovering pybind11 via Python if the CMake package is not on CMAKE_PREFIX_PATH.
#
# 2) Cross-platform optimization presets
#    - C++17, -O3, hidden visibility on GCC/Clang; /O2, /utf-8, /permissive- on MSVC.
#    - Optional IPO/LTO (PYMANGA_ENABLE_LTO).
#    - Position-independent code and compile_commands.json enabled by default.
#
# 3) Optional OpenMP
#    - Links OpenMP if available. Threading is controlled solely via environment
#      (e.g., OMP_NUM_THREADS, OMP_PROC_BIND, OMP_PLACES); no hardcoding in code.
#
# 4) Robust runtime linking on Linux
#    - Sets RPATH to Python’s LIBDIR and $ORIGIN so the module can locate
#      libpython and friends when run from site-packages or the source tree.
#
# 5) Developer layout & install behavior
#    - PYMANGA_DEV_LAYOUT=ON: write the built extension (.so/.pyd) directly into
#      the package’s source subfolder (run without installing).
#    - PYMANGA_INSTALL_BACK_TO_SOURCE=ON: optionally copy the built artifact back
#      to the source tree during `cmake --install`.
#    - Default install prefix = Python site-packages (purelib/sitearch).
#
# 6) Selective builds
#    - PYMANGA_BUILD_LIST controls which modules to build (semicolon-separated);
#      empty means “build all”.
#
# 7) Helper for modules
#    - add_hpc_module_in_tree(<name> <dest_subdir_in_package> <sources...>)
#      encapsulates: pybind11 target creation, OpenMP link, macro toggles,
#      dev layout outputs, and site-packages install destinations.
#
# Included module(s)
# - asymzoi  →  ResourceLib/AboveGround/AsymmetricZOI/AsymmetricZOI.cpp
#   (C++ core for Asymmetric Zone-of-Influence, called from Python)
#
# Notes
# - No thread parameter is passed through the Python API; threading is governed
#   by the environment only.
# - On MSVC, PDBs remain in the build directory; only the extension is copied to
#   the source tree (dev layout) / site-packages (install).
#
# Typical usage!!!!!
# Before you start, make sure you use the CmakeLists.txt file to compile C++.
# Just run the following commands in your terminal:
#Remove-Item -Recurse -Force build-msvc -ErrorAction SilentlyContinue
#cmake -S . -B build-msvc -G "Visual Studio 17 2022" -A x64 `
#  -DCMAKE_BUILD_TYPE=Release `
#  -DPYBIND11_FINDPYTHON=ON
#cmake --build build-msvc --config Release -- /m
#
# ============================================================


cmake_minimum_required(VERSION 3.18)
# Normalize DESTINATION (CMake 3.29+)
if(POLICY CMP0177)
  cmake_policy(SET CMP0177 NEW)
endif()

project(pymanga_hpc LANGUAGES CXX)

# Options
option(PYMANGA_DEV_LAYOUT "Write build artifacts back to source tree for development (run without install)" ON)
option(PYMANGA_INSTALL_BACK_TO_SOURCE "Also copy artifacts back to source tree during install (usually not needed)" OFF)
option(PYMANGA_ENABLE_LTO "Enable IPO/LTO (may be unstable with older GCC)" OFF)
option(PYMANGA_MAP_C_MATH_FUNCS "Map expf/logf/powf/sinf -> exp/log/pow/sin (temporary compatibility)" OFF)
option(FON_USE_STD_HYPOT "Define FON_USE_STD_HYPOT=1" OFF)
set(PYMANGA_BUILD_LIST "" CACHE STRING "Modules to build (; separated), empty = all")

# Export compile_commands.json + PIC
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Python / pybind11
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
      "import pybind11, os; print(os.path.join(os.path.dirname(pybind11.__file__),'share','cmake','pybind11'))"
    OUTPUT_VARIABLE _pybind11_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
  if(EXISTS "${_pybind11_dir}/pybind11Config.cmake")
    list(APPEND CMAKE_PREFIX_PATH "${_pybind11_dir}")
  endif()
  if(DEFINED ENV{CONDA_PREFIX})
    list(APPEND CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library/lib/cmake")
  endif()
  find_package(pybind11 CONFIG REQUIRED)
endif()

# Compiler / Optimization
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenMP QUIET)

if(MSVC)
  add_compile_options(/O2 /permissive- /utf-8)
  add_compile_definitions(NOMINMAX)
  if(OpenMP_CXX_FOUND)
    add_compile_options(/openmp)
  endif()
else()
  add_compile_options(-O3 -fvisibility=hidden -fvisibility-inlines-hidden)
  if(OpenMP_CXX_FOUND)
    add_compile_options(-fopenmp)
  endif()
endif()

if(PYMANGA_ENABLE_LTO)
  include(CheckIPOSupported)
  check_ipo_supported(RESULT _ipo_ok OUTPUT _ipo_msg)
  if(_ipo_ok)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
  else()
    message(WARNING "IPO/LTO not supported: ${_ipo_msg}")
  endif()
endif()

# RPATH (Linux: locate Conda/Python shared libs at runtime)
if(UNIX AND NOT APPLE)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c "import sysconfig;print(sysconfig.get_config_var('LIBDIR') or '')"
    OUTPUT_VARIABLE _PY_LIBDIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  file(TO_CMAKE_PATH "${_PY_LIBDIR}" _PY_LIBDIR)
  set(CMAKE_SKIP_RPATH OFF)
  set(CMAKE_BUILD_WITH_INSTALL_RPATH OFF)
  set(CMAKE_BUILD_RPATH "${_PY_LIBDIR}")
  set(CMAKE_INSTALL_RPATH "${_PY_LIBDIR};$ORIGIN")
endif()

# Install prefix: default = site-packages
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
  OUTPUT_VARIABLE PY_SITE
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(CMAKE_INSTALL_PREFIX "${PY_SITE}" CACHE PATH "Install prefix" FORCE)

# Helper: check if module should be built
function(_want name outvar)
  if(PYMANGA_BUILD_LIST STREQUAL "")
    set(${outvar} TRUE PARENT_SCOPE)
  else()
    set(_list "${PYMANGA_BUILD_LIST}")
    string(REPLACE "," ";" _list "${_list}")
    list(FIND _list "${name}" _idx)
    if(_idx EQUAL -1)
      set(${outvar} FALSE PARENT_SCOPE)
    else()
      set(${outvar} TRUE PARENT_SCOPE)
    endif()
  endif()
endfunction()

# Utility: add and install pybind11 module
# Usage: add_hpc_module_in_tree(<name> <dest_subdir_in_package> <sources...>)
function(add_hpc_module_in_tree name dest)
  if(ARGC LESS 3)
    message(FATAL_ERROR "add_hpc_module_in_tree(${name} ${dest} ...) requires at least one source file")
  endif()

  _want(${name} _build_this)
  if(NOT _build_this)
    message(STATUS "Skip module ${name} (not in PYMANGA_BUILD_LIST)")
    return()
  endif()

  pybind11_add_module(${name} ${ARGN})
  target_compile_features(${name} PRIVATE cxx_std_17)

  if(OpenMP_CXX_FOUND)
    target_link_libraries(${name} PRIVATE OpenMP::OpenMP_CXX)
  endif()

  if(PYMANGA_MAP_C_MATH_FUNCS AND (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang"))
    target_compile_definitions(${name} PRIVATE expf=exp logf=log powf=pow sinf=sin)
  endif()
  if(FON_USE_STD_HYPOT)
    target_compile_definitions(${name} PRIVATE FON_USE_STD_HYPOT=1)
  endif()

  # site-packages path (prefer sitearch)
  set(_SITE "${Python_SITEARCH}")
  if(NOT _SITE)
    set(_SITE "${Python_SITELIB}")
  endif()
  file(TO_CMAKE_PATH "${_SITE}" _SITE)

  # Development layout: write .so/.pyd back into source tree(note: .so is for linux, .pyd for Windows)
  if(PYMANGA_DEV_LAYOUT)
    set(_DST "${PROJECT_SOURCE_DIR}/${dest}")
    file(MAKE_DIRECTORY "${_DST}")
    set_target_properties(${name} PROPERTIES
      LIBRARY_OUTPUT_DIRECTORY               "${_DST}"
      RUNTIME_OUTPUT_DIRECTORY               "${_DST}"
      LIBRARY_OUTPUT_DIRECTORY_RELEASE       "${_DST}"
      RUNTIME_OUTPUT_DIRECTORY_RELEASE       "${_DST}"
      LIBRARY_OUTPUT_DIRECTORY_DEBUG         "${_DST}"
      RUNTIME_OUTPUT_DIRECTORY_DEBUG         "${_DST}"
    )
    if(MSVC)
      set_target_properties(${name} PROPERTIES
        PDB_OUTPUT_DIRECTORY                 "${CMAKE_CURRENT_BINARY_DIR}"
        PDB_OUTPUT_DIRECTORY_RELEASE         "${CMAKE_CURRENT_BINARY_DIR}"
        PDB_OUTPUT_DIRECTORY_DEBUG           "${CMAKE_CURRENT_BINARY_DIR}"
      )
    endif()
  endif()

  # Install: copy only dynamic library to site-packages
  install(TARGETS ${name}
    LIBRARY DESTINATION "${_SITE}/${dest}"
    RUNTIME DESTINATION "${_SITE}/${dest}"
  )

  # Optionally also copy back into source tree during install
  if(PYMANGA_INSTALL_BACK_TO_SOURCE)
    install(TARGETS ${name}
      LIBRARY DESTINATION "${PROJECT_SOURCE_DIR}/${dest}"
      RUNTIME DESTINATION "${PROJECT_SOURCE_DIR}/${dest}"
    )
  endif()
endfunction()

# Register modules (we can add more as needed)
add_hpc_module_in_tree(asymzoi ResourceLib/AboveGround/AsymmetricZOI
  ResourceLib/AboveGround/AsymmetricZOI/AsymmetricZOI.cpp
)

# note: add more modules below as needed, just follow the pattern above