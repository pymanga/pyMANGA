cmake_minimum_required(VERSION 3.18)
# CMake 3.29+ 引入的策略；存在就启用 NEW（规范化 DESTINATION 路径）
if(POLICY CMP0177)
  cmake_policy(SET CMP0177 NEW)
endif()

# --- auto-locate pybind11 installed via pip/conda ---
find_package(Python COMPONENTS Interpreter REQUIRED)

if(NOT DEFINED pybind11_DIR)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
      "import pybind11, os; print(os.path.join(os.path.dirname(pybind11.__file__), 'share', 'cmake', 'pybind11'))"
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
endif()

if(pybind11_DIR AND EXISTS "${pybind11_DIR}/pybind11Config.cmake")
  list(APPEND CMAKE_PREFIX_PATH "${pybind11_DIR}")
endif()

if(DEFINED ENV{CONDA_PREFIX})
  list(APPEND CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library/lib/cmake")
endif()

project(pymanga_hpc LANGUAGES CXX)

# --- cross-platform Python/pybind11 + install prefix (Win/Linux/macOS) ---
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# auto-locate pybind11 (pip/conda)
if(NOT DEFINED pybind11_DIR)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
      "import pybind11, os; print(os.path.join(os.path.dirname(pybind11.__file__),'share','cmake','pybind11'))"
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
endif()
if(pybind11_DIR AND EXISTS "${pybind11_DIR}/pybind11Config.cmake")
  list(APPEND CMAKE_PREFIX_PATH "${pybind11_DIR}")
endif()
# conda-forge fallback
if(DEFINED ENV{CONDA_PREFIX})
  list(APPEND CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library/lib/cmake")
endif()

# auto-set install prefix to current Python's site-packages (so 'cmake --install' puts .so/.pyd into your package tree)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
  OUTPUT_VARIABLE PY_SITE
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
# allow override but default to site-packages
set(CMAKE_INSTALL_PREFIX "${PY_SITE}" CACHE PATH "Install prefix" FORCE)


# ---- toolchains & deps ----
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (MSVC)
  add_compile_options(/O2 /permissive- /openmp)
else()
  add_compile_options(-O3)
  if (OpenMP_CXX_FOUND)
    add_compile_options(-fopenmp)
  endif()
endif()

# ---- helper: install back into package tree ----
# usage:
#   add_hpc_module_in_tree(<name> <dest_dir_in_wheel> <sources...>)
# example:
#   add_hpc_module_in_tree(fon_hpc ResourceLib/BelowGround/Individual/FONCPP
#                          ResourceLib/BelowGround/Individual/FONCPP/fon_hpc.cpp)
function(add_hpc_module_in_tree name dest)
  set(srcs ${ARGN})
  if (NOT srcs)
    message(FATAL_ERROR "add_hpc_module_in_tree(${name} ...) needs at least one source file")
  endif()

  pybind11_add_module(${name} ${srcs})
  target_compile_features(${name} PRIVATE cxx_std_17)

    # MSVC 编码
  if(MSVC)
    target_compile_options(${name} PRIVATE /utf-8)
  endif()

  if (OpenMP_CXX_FOUND)
    target_link_libraries(${name} PRIVATE OpenMP::OpenMP_CXX)
  endif()

  # 传递 hypot 开关到源码
  target_compile_definitions(${name} PRIVATE
    $<$<BOOL:${FON_USE_STD_HYPOT}>:FON_USE_STD_HYPOT=1>
  )

  # 让构建时产物也写入源码目录
  set(_DST "${PROJECT_SOURCE_DIR}/${dest}")
  file(MAKE_DIRECTORY "${_DST}")
  set_target_properties(${name} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY_RELEASE  "${_DST}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE  "${_DST}"
    ARCHIVE_OUTPUT_DIRECTORY_RELEASE  "${_DST}"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG    "${_DST}"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG    "${_DST}"
    ARCHIVE_OUTPUT_DIRECTORY_DEBUG    "${_DST}"
  )

  # 计算 site-packages
  set(_SITE "${Python_SITEARCH}")
  if(NOT _SITE)
    set(_SITE "${Python_SITELIB}")
  endif()
  # 也规范化
  file(TO_CMAKE_PATH "${_SITE}" _SITE)

  # 安装一份到源码目录（绝对路径允许覆盖 CMAKE_INSTALL_PREFIX）
  install(TARGETS ${name}
    LIBRARY DESTINATION "${_DST}"
    RUNTIME DESTINATION "${_DST}"
  )
  # 再安装一份到 site-packages 下的包树
  install(TARGETS ${name}
    LIBRARY DESTINATION "${_SITE}/${dest}"
    RUNTIME DESTINATION "${_SITE}/${dest}"
  )
endfunction()


# ---- register your C++ extensions (add as needed) ----

# 1) 地上竞争 AsymmetricZOI C++ 内核
add_hpc_module_in_tree(asymzoicpp ResourceLib/AboveGround/AsymmetricZOICPP
  ResourceLib/AboveGround/AsymmetricZOICPP/AsymmetricZOICPP.cpp
)

# 2) 地下 FON C++ 内核
add_hpc_module_in_tree(foncpp ResourceLib/BelowGround/Individual/FONCPP
  ResourceLib/BelowGround/Individual/FONCPP/FONCPP.cpp
)

# 3) 地下 FON C++ 内核
add_hpc_module_in_tree(fixedsalcpp ResourceLib/BelowGround/Individual/FixedSalinityCPP
  ResourceLib/BelowGround/Individual/FixedSalinityCPP/FixedSalinityCPP.cpp
)
