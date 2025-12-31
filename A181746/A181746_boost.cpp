// Code written by Andy Huchala, adapted to use Boost.Multiprecision
// for faster big integer arithmetic without extra memory usage.

// compile with
// g++ -O3 -std=c++17 ^
//   -IC:\Users\Ahuch\Downloads\boost_1_82_0\boost_1_82_0 ^
//   A181746_boost.cpp -o A181746_boost


#include <iostream>
#include <queue>
#include <cmath>
#include <unordered_set>

#include <boost/multiprecision/cpp_int.hpp>
using boost::multiprecision::cpp_int;
using BigInt = cpp_int;

struct Pair {
    long double log;
    long long coordinates;

    Pair(long long coordinates_, long double log_)
        : log(log_), coordinates(coordinates_) {}
};

// priority_queue is a max-heap; invert comparison so the smallest log is on top.
bool operator<(const Pair &p1, const Pair &p2) {
    return p1.log > p2.log;
}

// Big dimension polynomial, exactly your product but in one function.
// Uses BigInt and divides by denom at the end.
void compute_dim(BigInt &dim,
                 int x0, int x1, int x2, int x3,
                 int x4, int x5, int x6, int x7,
                 const BigInt &denom) {
    dim = 1;

    dim *= (x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7);
    dim *= (x0 + x1 + x2 + x3 + x4 + x6 + x7);
    dim *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
    dim *= (x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x1 + x2 + x4 + x5 + x6 + x7);
    dim *= (x0 + x1 + x2 + x4 + x5 + x7);
    dim *= (x0 + x1 + x2 + x4 + x6 + x7);
    dim *= (x0 + x1 + x2 + x4 + x7);
    dim *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
    dim *= (x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x1 + x2 + 2*x4 + x5 + x7);
    dim *= (x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
    dim *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
    dim *= (x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x1 + x4 + x5 + x7);
    dim *= (x0 + x1 + x4 + x5);
    dim *= (x0 + x1 + x4 + x7);
    dim *= (x0 + x1 + x4);
    dim *= (x0 + x1 + 2*x4 + x5 + x7);
    dim *= (x0 + x1);
    dim *= (x0 + x2 + x3 + x4 + x5 + x6 + x7);
    dim *= (x0 + x2 + x3 + x4 + x6 + x7);
    dim *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + x7);
    dim *= (x0 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x2 + x4 + x5 + x6 + x7);
    dim *= (x0 + x2 + x4 + x5 + x7);
    dim *= (x0 + x2 + x4 + x6 + x7);
    dim *= (x0 + x2 + x4 + x7);
    dim *= (x0 + x2 + 2*x4 + x5 + x6 + x7);
    dim *= (x0 + x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x2 + 2*x4 + x5 + x7);
    dim *= (x0 + x2 + 2*x4 + x5 + 2*x7);
    dim *= (x0 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
    dim *= (x0 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (x0 + x4 + x5 + x7);
    dim *= (x0 + x4 + x5);
    dim *= (x0 + x4 + x7);
    dim *= (x0 + x4);
    dim *= (x0 + 2*x4 + x5 + x7);
    dim *= (x0);
    dim *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7);
    dim *= (2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + x7);
    dim *= (2*x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 2*x4 + x5 + x7);
    dim *= (2*x0 + x1 + x2 + 2*x4 + x5 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 3*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 3*x4 + x5 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + x2 + 3*x4 + 2*x5 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 2*x7);
    dim *= (2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 3*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (2*x0 + x1 + 2*x4 + x5 + x7);
    dim *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (3*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (3*x0 + x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
    dim *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (3*x0 + 2*x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7);
    dim *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7);
    dim *= (3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
    dim *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7);
    dim *= (4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7);
    dim *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 4*x7);
    dim *= (4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
    dim *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7);
    dim *= (4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
    dim *= (4*x0 + 2*x1 + 4*x2 + 2*x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7);
    dim *= (x1);
    dim *= (x2 + x3 + x4 + x6 + x7);
    dim *= (x2 + x3 + x6 + x7);
    dim *= (x2 + x3 + x6);
    dim *= (x2 + x4 + x6 + x7);
    dim *= (x2 + x4 + x7);
    dim *= (x2 + x6 + x7);
    dim *= (x2 + x6);
    dim *= (x2 + x7);
    dim *= (x2);
    dim *= (x2 + x3 + x4 + x5 + x6 + x7);
    dim *= (x2 + x4 + x5 + x6 + x7);
    dim *= (x2 + x4 + x5 + x7);
    dim *= (x3 + x6);
    dim *= (x3);
    dim *= (x4 + x7);
    dim *= (x4);
    dim *= (x4 + x5 + x7);
    dim *= (x4 + x5);
    dim *= (x5);
    dim *= (x6);
    dim *= (x7);

    dim /= denom; // integer division; denom is known to divide exactly
}

int main() {
    const int UPPER_BOUND_FACTOR = 900;
    long double cachedLogs[UPPER_BOUND_FACTOR] = {0.0L};

    const int cums[8] = {0, 7, 16, 23, 34, 40, 48, 57};

    const BigInt denom(
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

    // Tolerance for log equality.
    // 1e-13L is conservative across platforms; if you *know* long double
    // is 80-bit extended, 1e-15L is also reasonable.
    const long double EPS = 1e-13L;

    long double irrep = 244.2883052323315L; // initial log value

    fringe.emplace(x, irrep);
    seen.emplace(x);

    long double lastLog = 0.0L;
    long long lastCoord = -1LL;

    int x0, x1, x2, x3, x4, x5, x6, x7;

    // Reused big integers to avoid repeated heap allocations
    BigInt dim1(1);
    BigInt dim2(1);

    std::cout << "Initialization complete\n";

    while (numComputed++ < numToCompute && !fringe.empty()) {
        Pair cur = fringe.top();
        fringe.pop();
        seen.erase(cur.coordinates);

        if (std::fabs(lastLog - cur.log) < EPS) {
            // ---- decode cur.coordinates for dim1 ----
            x0 = static_cast<int>((cur.coordinates      & ((1LL << 7LL)  - 1LL))) + 1;
            x1 = static_cast<int>((cur.coordinates >> 7LL)  & ((1LL << 9LL)  - 1LL)) + 1;
            x2 = static_cast<int>((cur.coordinates >> 16LL) & ((1LL << 7LL)  - 1LL)) + 1;
            x3 = static_cast<int>((cur.coordinates >> 23LL) & ((1LL << 11LL) - 1LL)) + 1;
            x4 = static_cast<int>((cur.coordinates >> 34LL) & ((1LL << 6LL)  - 1LL)) + 1;
            x5 = static_cast<int>((cur.coordinates >> 40LL) & ((1LL << 8LL)  - 1LL)) + 1;
            x6 = static_cast<int>((cur.coordinates >> 48LL) & ((1LL << 9LL)  - 1LL)) + 1;
            x7 = static_cast<int>((cur.coordinates >> 57LL) & ((1LL << 7LL)  - 1LL)) + 1;

            compute_dim(dim1, x0, x1, x2, x3, x4, x5, x6, x7, denom);

            // ---- decode lastCoord for dim2 ----
            x0 = static_cast<int>((lastCoord      & ((1LL << 7LL)  - 1LL))) + 1;
            x1 = static_cast<int>((lastCoord >> 7LL)  & ((1LL << 9LL)  - 1LL)) + 1;
            x2 = static_cast<int>((lastCoord >> 16LL) & ((1LL << 7LL)  - 1LL)) + 1;
            x3 = static_cast<int>((lastCoord >> 23LL) & ((1LL << 11LL) - 1LL)) + 1;
            x4 = static_cast<int>((lastCoord >> 34LL) & ((1LL << 6LL)  - 1LL)) + 1;
            x5 = static_cast<int>((lastCoord >> 40LL) & ((1LL << 8LL)  - 1LL)) + 1;
            x6 = static_cast<int>((lastCoord >> 48LL) & ((1LL << 9LL)  - 1LL)) + 1;
            x7 = static_cast<int>((lastCoord >> 57LL) & ((1LL << 7LL)  - 1LL)) + 1;

            compute_dim(dim2, x0, x1, x2, x3, x4, x5, x6, x7, denom);

            if (dim1 == dim2) {
                std::cout << numSeen << " " << dim1 << "\n";
                ++numSeen;
            }
        }

        lastLog = cur.log;
        lastCoord = cur.coordinates;

        for (int i = 0; i < 8; ++i) {
            long long newCoord = cur.coordinates + (1LL << cums[i]);
            if (seen.find(newCoord) != seen.end()) {
                continue;
            }

            // decode newCoord -> x0..x7
            x0 = static_cast<int>((newCoord      & ((1LL << 7LL)  - 1LL))) + 1;
            x1 = static_cast<int>((newCoord >> 7LL)  & ((1LL << 9LL)  - 1LL)) + 1;
            x2 = static_cast<int>((newCoord >> 16LL) & ((1LL << 7LL)  - 1LL)) + 1;
            x3 = static_cast<int>((newCoord >> 23LL) & ((1LL << 11LL) - 1LL)) + 1;
            x4 = static_cast<int>((newCoord >> 34LL) & ((1LL << 6LL)  - 1LL)) + 1;
            x5 = static_cast<int>((newCoord >> 40LL) & ((1LL << 8LL)  - 1LL)) + 1;
            x6 = static_cast<int>((newCoord >> 48LL) & ((1LL << 9LL)  - 1LL)) + 1;
            x7 = static_cast<int>((newCoord >> 57LL) & ((1LL << 7LL)  - 1LL)) + 1;

            long double newIrrep = 0.0L;

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

            fringe.emplace(newCoord, newIrrep);
            seen.emplace(newCoord);
        }
    }

    return 0;
}
