cmake_minimum_required(VERSION 2.8)
project(sinc)

set(SINC_VERSION "0.0.1")

################################
# Export library
################################

export_project(
    NAME sinc
    PYTHON_INCLUDES ${CMAKE_CURRENT_LIST_DIR}/sinc
    VERSION ${SINC_VERSION}
)
