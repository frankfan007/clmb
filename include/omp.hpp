#pragma once

#ifndef STRINGIFY
#define STRINGIFY(a) #a
#endif

#ifdef NOPAR
    #define PARFOR
    #define PARSECS
    #define PARSEC
    #define CRITICAL(NAME)
    #define OMP(ARG)
#else
    #define PARFOR _Pragma("omp parallel for")
    #define PARSECS _Pragma("omp parallel sections")
    #define PARSEC _Pragma("omp section")
    #define CRITICAL(NAME) _Pragma(STRINGIFY(omp critical(NAME)))
    #define OMP(ARG) _Pragma(STRINGIFY(omp ARG))
#endif

