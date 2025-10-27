if(WIN32)
  message(STATUS "Building on Windows")
endif()

if(UNIX)
  message(STATUS "Building on Unix-like system")
  if(APPLE)
    message(STATUS "Configuring for MacOS")
    find_program(CLANG_C_COMPILER clang-mp-20)
    find_program(CLANG_CXX_COMPILER clang++-mp-20)
    if(NOT CLANG_C_COMPILER OR NOT CLANG_CXX_COMPILER)
        message(FATAL_ERROR "clang-mp-20 or clang++-mp-20 not found")
    else()
      set(CMAKE_C_COMPILER clang-mp-20)
      set(CMAKE_CXX_COMPILER clang++-mp-20)
    endif()
  else()
    message(STATUS "Building on Linux or other Unix")
  endif()
endif()

cmake_minimum_required(VERSION 3.10.0)
project(MoDELib VERSION 2.0.0 LANGUAGES C CXX)

option(USE_PYBIND11 "enables pybind11" ON)
option(BUILD_TOOLS "builds tools" ON)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# declare compiled QT library path
list(APPEND CMAKE_PREFIX_PATH "/Users/anon/Programs/Qt/6.9.0/macos/lib/cmake")
# declare compiled VTK library path
set(VTK_DIR "/Users/anon/Programs/VTK/vtk/build")

### Eigen3 (Required) ###
find_package(Eigen3 REQUIRED)
if(Eigen3_FOUND)
  message(STATUS "Eigen3_VERSION:" ${Eigen3_VERSION})
else()
  message(FATAL_ERROR "Eigen3 not found")
endif()

### Boost (Required) ###
find_package(Boost CONFIG REQUIRED)
if(Boost_FOUND)
  message(STATUS "Boost_VERSION:" ${Boost_VERSION})
else()
  message(FATAL_ERROR "Boost not found")
endif()

### SuiteSparse ###
find_package(CHOLMOD)
if(CHOLMOD_FOUND)
  message(STATUS "CHOLMOD_VERSION:" ${CHOLMOD_VERSION})
  add_definitions(-D MODELIB_CHOLMOD)
endif()

find_package(UMFPACK)
if(UMFPACK_FOUND)
  message(STATUS "UMFPACK_VERSION:" ${UMFPACK_VERSION})
  add_definitions(-D MODELIB_UMFPACK)
endif()

### fftw3 ###
find_library(FFTW3_LIBRARIES fftw3)
if(FFTW3_LIBRARIES)
  cmake_path(GET FFTW3_LIBRARIES PARENT_PATH FFTW3_LIBRARY_DIRS)
  set(FFTW3_INCLUDE_DIRS ${FFTW3_LIBRARY_DIRS}/../include)
  message(STATUS "FFTW3_LIBRARIES:" ${FFTW3_LIBRARIES})
  add_definitions(-D _MODEL_GLIDE_PLANE_NOISE_GENERATOR_)
else()
  message(WARNING "FFTW3 not found, noise generator is disabled")
endif()

### pybind11 ###
if(USE_PYBIND11)
  cmake_policy(SET CMP0057 NEW)
  find_package(Python COMPONENTS Interpreter Development)
  if(Python_FOUND)
    message(STATUS "Python_VERSION:" ${Python_VERSION})
    find_package(pybind11 CONFIG REQUIRED)
  else()
    message(WARNING "Python not found, pybind11 is disabled")
  endif()
endif()

# Create target
if(pybind11_FOUND)
  message(STATUS "pybind11_VERSION:" ${pybind11_VERSION})
  set(pybind11_LIBRARIES pybind11::embed pybind11::headers pybind11::module)
  add_definitions(-D_MODEL_PYBIND11_)
  Python_add_library(MoDELib SHARED "")
else()
  message(WARNING "pybind11 is disabled")
  add_library(MoDELib "")
endif()

# Set target properties AFTER target is created
target_include_directories(MoDELib PUBLIC ${EIGEN3_INCLUDE_DIRS})
target_include_directories(MoDELib PUBLIC ${Boost_INCLUDE_DIRS})

if(CHOLMOD_FOUND)
  target_include_directories(MoDELib PUBLIC ${CHOLMOD_INCLUDE_DIR})
endif()

if(UMFPACK_FOUND)
  target_include_directories(MoDELib PUBLIC ${UMFPACK_INCLUDE_DIR})
endif()

if(FFTW3_LIBRARIES)
  target_include_directories(MoDELib PUBLIC ${FFTW3_INCLUDE_DIRS})
endif()

# Project includes
target_include_directories(MoDELib PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Utilities"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/IO"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Math"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Geometry"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Mesh"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Lattices"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/FEM"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/GlidePlanes"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/Quadrature"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/PolycrystallineMaterials"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/DislocationDynamicsIO"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/DislocationMobilities"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/DislocationDynamicsBase"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/MicrostructureGeneration"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/LoopNetwork"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/ParticleInteraction"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/SpaceDecomposition"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/DiscreteCrackMechanics"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/ClusterDynamics"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/ElasticDeformation"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/InclusionMicrostructure"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/DislocationDynamics"
)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src/ src)
target_link_libraries(MoDELib PUBLIC ${FFTW3_LIBRARIES} ${pybind11_LIBRARIES} ${CHOLMOD_LIBRARIES} ${UMFPACK_LIBRARIES})

# compiler flags
target_compile_options(MoDELib  PRIVATE
    -Wall                         # Enable most common warning messages for potential issues
    -Wextra                       # Enable additional warning messages beyond -Wall
    -march=native                 # Optimize for the native CPU architecture of the build machine
    -fopenmp                      # Enable OpenMP support for parallel programming
    -O3                           # Use aggressive optimization level 3 for maximum performance
    -Wno-unused-variable          # Suppress warnings about variables that are declared but never used
    -Wno-unused-but-set-variable  # Suppress warnings about variables that are set but never read
    -Wno-unused-parameter         # Suppress warnings about function parameters that are never used
)

if(BUILD_TOOLS)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tools tools)
endif()
