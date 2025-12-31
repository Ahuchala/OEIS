// Code written by Andy Huchala, lightly modified for memory efficiency

#include <iostream>
#include <queue>
#include <cmath>
#include <unordered_set>

// Requires this file in the same directory, available at
// https://github.com/sercantutar/infint/blob/master/InfInt.h
#include "InfInt.h"

struct Pair {
    long double log;
    long long coordinates;

    Pair(long long coordinates_, long double log_)
        : log(log_), coordinates(coordinates_) {}
};

bool operator<(const Pair& p1, const Pair& p2) {
    // priority_queue is max-heap by default; we want smallest log on top
    return p1.log > p2.log;
}

int main() {

    const int UPPER_BOUND_FACTOR = 900;
    long double cachedLogs[UPPER_BOUND_FACTOR];

    const int cums[8] = {0, 7, 16, 23, 34, 40, 48, 57};

    const InfInt denom(
        "12389761771281087987161913865011039548629176646031786340025309566313679656889905840128000000000000000000000"
    );

    for (int i = 1; i < UPPER_BOUND_FACTOR; ++i) {
        cachedLogs[i] = std::log(static_cast<long double>(i));
    }

    long long x = 0LL;

    std::priority_queue<Pair> fringe;
    std::unordered_set<long long> seen;

    const long long numToCompute = 1000000000LL;
    long long numComputed = 0;
    long numSeen = 1;

    long double irrep = 244.2883052323315L;

    fringe.push(Pair(x, irrep));
    seen.insert(x);

    long double lastLog = 0.0L;
    long long lastCoord = -1LL;

    int x0, x1, x2, x3, x4, x5, x6, x7;

    // Reuse these big integers each time instead of constructing them afresh
    InfInt dim1(1);
    InfInt dim2(1);

    std::cout << "Initialization complete\n";

    while (numComputed++ < numToCompute && !fringe.empty()) {
        Pair cur = fringe.top();
        fringe.pop();
        seen.erase(cur.coordinates);

        if (std::abs(lastLog - cur.log) < 1e-12L) {

            // ------------ decode cur.coordinates ------------
            x0 = static_cast<int>( (cur.coordinates      & ((1LL << 7LL)  - 1LL)) ) + 1;
            x1 = static_cast<int>( (cur.coordinates >> 7LL)  & ((1LL << 9LL)  - 1LL) ) + 1;
            x2 = static_cast<int>( (cur.coordinates >> 16LL) & ((1LL << 7LL)  - 1LL) ) + 1;
            x3 = static_cast<int>( (cur.coordinates >> 23LL) & ((1LL << 11LL) - 1LL) ) + 1;
            x4 = static_cast<int>( (cur.coordinates >> 34LL) & ((1LL << 6LL)  - 1LL) ) + 1;
            x5 = static_cast<int>( (cur.coordinates >> 40LL) & ((1LL << 8LL)  - 1LL) ) + 1;
            x6 = static_cast<int>( (cur.coordinates >> 48LL) & ((1LL << 9LL)  - 1LL) ) + 1;
            x7 = static_cast<int>( (cur.coordinates >> 57LL) & ((1LL << 7LL)  - 1LL) ) + 1;

            // ------------ dim1: reuse InfInt object ------------
            dim1 = 1;
            dim1 *= (x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + x3 + x4 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x1 + x2 + x4 + x5 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + x4 + x5 + x7);
            dim1 *= (x0 + x1 + x2 + x4 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + x4 + x7);
            dim1 *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
            dim1 *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x1 + x2 + 2*x4 + x5 + x7);
            dim1 *= (x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
            dim1 *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim1 *= (x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x1 + x4 + x5 + x7);
            dim1 *= (x0 + x1 + x4 + x5);
            dim1 *= (x0 + x1 + x4 + x7);
            dim1 *= (x0 + x1 + x4);
            dim1 *= (x0 + x1 + 2*x4 + x5 + x7);
            dim1 *= (x0 + x1);
            dim1 *= (x0 + x2 + x3 + x4 + x5 + x6 + x7);
            dim1 *= (x0 + x2 + x3 + x4 + x6 + x7);
            dim1 *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim1 *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x2 + x4 + x5 + x6 + x7);
            dim1 *= (x0 + x2 + x4 + x5 + x7);
            dim1 *= (x0 + x2 + x4 + x6 + x7);
            dim1 *= (x0 + x2 + x4 + x7);
            dim1 *= (x0 + x2 + 2*x4 + x5 + x6 + x7);
            dim1 *= (x0 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x2 + 2*x4 + x5 + x7);
            dim1 *= (x0 + x2 + 2*x4 + x5 + 2*x7);
            dim1 *= (x0 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim1 *= (x0 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (x0 + x4 + x5 + x7);
            dim1 *= (x0 + x4 + x5);
            dim1 *= (x0 + x4 + x7);
            dim1 *= (x0 + x4);
            dim1 *= (x0 + 2*x4 + x5 + x7);
            dim1 *= (x0);
            dim1 *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim1 *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
            dim1 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x7);
            dim1 *= (2*x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 3*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 3*x4 + x5 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (2*x0 + x1 + 2*x4 + x5 + x7);
            dim1 *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (3*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim1 *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (3*x0 + 2*x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim1 *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim1 *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim1 *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim1 *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim1 *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 4*x7);
            dim1 *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
            dim1 *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
            dim1 *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
            dim1 *= (4*x0 + 2*x1 + 4*x2 + 2*x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
            dim1 *= (x1);
            dim1 *= (x2 + x3 + x4 + x6 + x7);
            dim1 *= (x2 + x3 + x6 + x7);
            dim1 *= (x2 + x3 + x6);
            dim1 *= (x2 + x4 + x6 + x7);
            dim1 *= (x2 + x4 + x7);
            dim1 *= (x2 + x6 + x7);
            dim1 *= (x2 + x6);
            dim1 *= (x2 + x7);
            dim1 *= (x2);
            dim1 *= (x2 + x3 + x4 + x5 + x6 + x7);
            dim1 *= (x2 + x4 + x5 + x6 + x7);
            dim1 *= (x2 + x4 + x5 + x7);
            dim1 *= (x3 + x6);
            dim1 *= (x3);
            dim1 *= (x4 + x7);
            dim1 *= (x4);
            dim1 *= (x4 + x5 + x7);
            dim1 *= (x4 + x5);
            dim1 *= (x5);
            dim1 *= (x6);
            dim1 *= (x7);
            dim1 /= denom;

            // ------------ decode lastCoord ------------
            x0 = static_cast<int>( (lastCoord      & ((1LL << 7LL)  - 1LL)) ) + 1;
            x1 = static_cast<int>( (lastCoord >> 7LL)  & ((1LL << 9LL)  - 1LL) ) + 1;
            x2 = static_cast<int>( (lastCoord >> 16LL) & ((1LL << 7LL)  - 1LL) ) + 1;
            x3 = static_cast<int>( (lastCoord >> 23LL) & ((1LL << 11LL) - 1LL) ) + 1;
            x4 = static_cast<int>( (lastCoord >> 34LL) & ((1LL << 6LL)  - 1LL) ) + 1;
            x5 = static_cast<int>( (lastCoord >> 40LL) & ((1LL << 8LL)  - 1LL) ) + 1;
            x6 = static_cast<int>( (lastCoord >> 48LL) & ((1LL << 9LL)  - 1LL) ) + 1;
            x7 = static_cast<int>( (lastCoord >> 57LL) & ((1LL << 7LL)  - 1LL) ) + 1;

            // ------------ dim2: reuse InfInt object ------------
            dim2 = 1;
            dim2 *= (x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + x3 + x4 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x1 + x2 + x4 + x5 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + x4 + x5 + x7);
            dim2 *= (x0 + x1 + x2 + x4 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + x4 + x7);
            dim2 *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
            dim2 *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x1 + x2 + 2*x4 + x5 + x7);
            dim2 *= (x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
            dim2 *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim2 *= (x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x1 + x4 + x5 + x7);
            dim2 *= (x0 + x1 + x4 + x5);
            dim2 *= (x0 + x1 + x4 + x7);
            dim2 *= (x0 + x1 + x4);
            dim2 *= (x0 + x1 + 2*x4 + x5 + x7);
            dim2 *= (x0 + x1);
            dim2 *= (x0 + x2 + x3 + x4 + x5 + x6 + x7);
            dim2 *= (x0 + x2 + x3 + x4 + x6 + x7);
            dim2 *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim2 *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x2 + x4 + x5 + x6 + x7);
            dim2 *= (x0 + x2 + x4 + x5 + x7);
            dim2 *= (x0 + x2 + x4 + x6 + x7);
            dim2 *= (x0 + x2 + x4 + x7);
            dim2 *= (x0 + x2 + 2*x4 + x5 + x6 + x7);
            dim2 *= (x0 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x2 + 2*x4 + x5 + x7);
            dim2 *= (x0 + x2 + 2*x4 + x5 + 2*x7);
            dim2 *= (x0 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim2 *= (x0 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (x0 + x4 + x5 + x7);
            dim2 *= (x0 + x4 + x5);
            dim2 *= (x0 + x4 + x7);
            dim2 *= (x0 + x4);
            dim2 *= (x0 + 2*x4 + x5 + x7);
            dim2 *= (x0);
            dim2 *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
            dim2 *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
            dim2 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 2*x4 + x5 + x7);
            dim2 *= (2*x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 3*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 3*x4 + x5 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 2*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (2*x0 + x1 + 2*x4 + x5 + x7);
            dim2 *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (3*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim2 *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (3*x0 + 2*x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
            dim2 *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
            dim2 *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim2 *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
            dim2 *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
            dim2 *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 4*x7);
            dim2 *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
            dim2 *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
            dim2 *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
            dim2 *= (4*x0 + 2*x1 + 4*x2 + 2*x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
            dim2 *= (x1);
            dim2 *= (x2 + x3 + x4 + x6 + x7);
            dim2 *= (x2 + x3 + x6 + x7);
            dim2 *= (x2 + x3 + x6);
            dim2 *= (x2 + x4 + x6 + x7);
            dim2 *= (x2 + x4 + x7);
            dim2 *= (x2 + x6 + x7);
            dim2 *= (x2 + x6);
            dim2 *= (x2 + x7);
            dim2 *= (x2);
            dim2 *= (x2 + x3 + x4 + x5 + x6 + x7);
            dim2 *= (x2 + x4 + x5 + x6 + x7);
            dim2 *= (x2 + x4 + x5 + x7);
            dim2 *= (x3 + x6);
            dim2 *= (x3);
            dim2 *= (x4 + x7);
            dim2 *= (x4);
            dim2 *= (x4 + x5 + x7);
            dim2 *= (x4 + x5);
            dim2 *= (x5);
            dim2 *= (x6);
            dim2 *= (x7);
            dim2 /= denom;

            if (dim1 == dim2) {
                std::cout << numSeen << " " << dim1.toString() << "\n";
                ++numSeen;
            }
        }

        lastLog = cur.log;
        lastCoord = cur.coordinates;

        for (int i = 0; i < 8; ++i) {
            long long newCoord = cur.coordinates + (1LL << cums[i]);
            if (seen.count(newCoord)) {
                continue;
            }

            // decode newCoord
            x0 = static_cast<int>( (newCoord      & ((1LL << 7LL)  - 1LL)) ) + 1;
            x1 = static_cast<int>( (newCoord >> 7LL)  & ((1LL << 9LL)  - 1LL) ) + 1;
            x2 = static_cast<int>( (newCoord >> 16LL) & ((1LL << 7LL)  - 1LL) ) + 1;
            x3 = static_cast<int>( (newCoord >> 23LL) & ((1LL << 11LL) - 1LL) ) + 1;
            x4 = static_cast<int>( (newCoord >> 34LL) & ((1LL << 6LL)  - 1LL) ) + 1;
            x5 = static_cast<int>( (newCoord >> 40LL) & ((1LL << 8LL)  - 1LL) ) + 1;
            x6 = static_cast<int>( (newCoord >> 48LL) & ((1LL << 9LL)  - 1LL) ) + 1;
            x7 = static_cast<int>( (newCoord >> 57LL) & ((1LL << 7LL)  - 1LL) ) + 1;

            long double newIrrep = 0.0L;

            // all your cachedLogs[...] sum as before:
            newIrrep += cachedLogs[x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x3 + x4 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x1 + x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x1 + x4 + x5];
            newIrrep += cachedLogs[x0 + x1 + x4 + x7];
            newIrrep += cachedLogs[x0 + x1 + x4];
            newIrrep += cachedLogs[x0 + x1 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x1];
            newIrrep += cachedLogs[x0 + x2 + x3 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + x3 + x4 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + x3 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x2 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x2 + x4 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + x4 + x7];
            newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + 2*x7];
            newIrrep += cachedLogs[x0 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7];
            newIrrep += cachedLogs[x0 + 2*x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[x0 + x4 + x5 + x7];
            newIrrep += cachedLogs[x0 + x4 + x5];
            newIrrep += cachedLogs[x0 + x4 + x7];
            newIrrep += cachedLogs[x0 + x4];
            newIrrep += cachedLogs[x0 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[x0];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 3*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + x5 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + 2*x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + 2*x5 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 2*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[2*x0 + x1 + 2*x4 + x5 + x7];
            newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 4*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7];
            newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + 2*x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7];
            newIrrep += cachedLogs[x1];
            newIrrep += cachedLogs[x2 + x3 + x4 + x6 + x7];
            newIrrep += cachedLogs[x2 + x3 + x6 + x7];
            newIrrep += cachedLogs[x2 + x3 + x6];
            newIrrep += cachedLogs[x2 + x4 + x6 + x7];
            newIrrep += cachedLogs[x2 + x4 + x7];
            newIrrep += cachedLogs[x2 + x6 + x7];
            newIrrep += cachedLogs[x2 + x6];
            newIrrep += cachedLogs[x2 + x7];
            newIrrep += cachedLogs[x2];
            newIrrep += cachedLogs[x2 + x3 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x2 + x4 + x5 + x6 + x7];
            newIrrep += cachedLogs[x2 + x4 + x5 + x7];
            newIrrep += cachedLogs[x3 + x6];
            newIrrep += cachedLogs[x3];
            newIrrep += cachedLogs[x4 + x7];
            newIrrep += cachedLogs[x4];
            newIrrep += cachedLogs[x4 + x5 + x7];
            newIrrep += cachedLogs[x4 + x5];
            newIrrep += cachedLogs[x5];
            newIrrep += cachedLogs[x6];
            newIrrep += cachedLogs[x7];

            fringe.push(Pair(newCoord, newIrrep));
            seen.insert(newCoord);
        }
    }

    return 0;
}
