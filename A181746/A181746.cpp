// Code written by Andy Huchala


#include <iostream>
#include <queue>
#include <math.h>
#include <unordered_set>

// Requires this file in the same directory, available at https://github.com/sercantutar/infint/blob/master/InfInt.h
#include "InfInt.h" 


class Pair {
public:
	long double log;
	long long coordinates;

	Pair(long long coordinates, long double log) {
		this->coordinates = coordinates;
		this->log = log;
	}
};

bool operator<(const Pair & p1, const Pair & p2) {
    return p1.log > p2.log;
}

int main() {

	const int UPPER_BOUND_FACTOR = 900;
	long double cachedLogs [UPPER_BOUND_FACTOR];
	int cums[8] = {0, 7, 16, 23, 34, 40, 48, 57};
	InfInt denom = "12389761771281087987161913865011039548629176646031786340025309566313679656889905840128000000000000000000000";

	for (long i = 1; i < UPPER_BOUND_FACTOR; i++) {
		cachedLogs[i] = std::log ( i);
    }
    long long x = 0LL;
    // PriorityQueue<Pair> fringe = new PriorityQueue<Pair>();
    std::priority_queue<Pair> fringe;
	// HashSet<Long> seen = new HashSet<Long>();
	std::unordered_set<long long> seen;
	
	// const long long numToCompute = 10;
	const long long numToCompute = 1000000000;
	long numComputed = 0;
	int numSeen = 1;

	long double irrep = 244.2883052323315;
	// next should be 249.80173397849646

	fringe.push(Pair(x, irrep));

	long double lastLog = 0.0;
	long long lastCoord = -1LL;
	long x0;long x1;long x2;long x3;long x4;long x5;long x6;long x7;
	std::cout<< "Initialization complete\n";

	while (numComputed++ < numToCompute) {
		Pair cur = fringe.top();
		fringe.pop();
		seen.erase(cur.coordinates);

		if (std::abs(lastLog-cur.log) < 1e-12) {
			x0 = (long) (cur.coordinates & ((1LL << 7LL) - 1LL)) + 1L;
			x1 = (long) ((cur.coordinates >> 7LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x2 = (long) ((cur.coordinates >> 16LL) & ((1LL << 7LL) - 1LL)) + 1L;
			x3 = (long) ((cur.coordinates >> 23LL) & ((1LL << 11LL) - 1LL)) + 1L;
			x4 = (long) ((cur.coordinates >> 34LL) & ((1LL << 6LL) - 1LL)) + 1L;
			x5 = (long) ((cur.coordinates >> 40LL) & ((1LL << 8LL) - 1LL)) + 1L;
			x6 = (long) ((cur.coordinates >> 48LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x7 = (long) ((cur.coordinates >> 57LL) & ((1LL << 7LL) - 1LL)) + 1L;
			InfInt dim1 = "1";
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

			x0 = (long) (lastCoord & ((1LL << 7LL) - 1LL)) + 1L;
			x1 = (long) ((lastCoord >> 7LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x2 = (long) ((lastCoord >> 16LL) & ((1LL << 7LL) - 1LL)) + 1L;
			x3 = (long) ((lastCoord >> 23LL) & ((1LL << 11LL) - 1LL)) + 1L;
			x4 = (long) ((lastCoord >> 34LL) & ((1LL << 6LL) - 1LL)) + 1L;
			x5 = (long) ((lastCoord >> 40LL) & ((1LL << 8LL) - 1LL)) + 1L;
			x6 = (long) ((lastCoord >> 48LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x7 = (long) ((lastCoord >> 57LL) & ((1LL << 7LL) - 1LL)) + 1L;
			InfInt dim2 = "1";
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
				std::cout<< std::to_string(numSeen) + " " +(dim1.toString())+ "\n";
				numSeen++;
			}
		}
		lastLog = cur.log;
		lastCoord = cur.coordinates;
		for (int i = 0; i < 8; i++) {
			long long newCoord = cur.coordinates + (1LL << cums[i]);
			if (seen.count(newCoord)) {
				continue;
			}
			x0 = (long) (newCoord & ((1LL << 7LL) - 1LL)) + 1L;
			x1 = (long) ((newCoord >> 7LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x2 = (long) ((newCoord >> 16LL) & ((1LL << 7LL) - 1LL)) + 1L;
			x3 = (long) ((newCoord >> 23LL) & ((1LL << 11LL) - 1LL)) + 1L;
			x4 = (long) ((newCoord >> 34LL) & ((1LL << 6LL) - 1LL)) + 1L;
			x5 = (long) ((newCoord >> 40LL) & ((1LL << 8LL) - 1LL)) + 1L;
			x6 = (long) ((newCoord >> 48LL) & ((1LL << 9LL) - 1LL)) + 1L;
			x7 = (long) ((newCoord >> 57LL) & ((1LL << 7LL) - 1LL)) + 1L;

			// std::cout<< std::to_string(x0)+ " " +std::to_string(x1)+ " " +std::to_string(x2)+ " " +std::to_string(x3)+ " " +std::to_string(x4)+ " " +std::to_string(x5)+ " " +std::to_string(x6)+ " " +std::to_string(x7)+ "\n";
			
			long double newIrrep = 0;

			newIrrep += cachedLogs[x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x3 + x4 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + x4 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x1 + x2 + 2*x4 + x5 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x1 + x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x1 + x4 + x5]; newIrrep += cachedLogs[x0 + x1 + x4 + x7]; newIrrep += cachedLogs[x0 + x1 + x4]; newIrrep += cachedLogs[x0 + x1 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x1]; newIrrep += cachedLogs[x0 + x2 + x3 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + x3 + x4 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + x3 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x2 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x2 + x4 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + x4 + x7]; newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x2 + 2*x4 + x5 + 2*x7]; newIrrep += cachedLogs[x0 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7]; newIrrep += cachedLogs[x0 + 2*x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[x0 + x4 + x5 + x7]; newIrrep += cachedLogs[x0 + x4 + x5]; newIrrep += cachedLogs[x0 + x4 + x7]; newIrrep += cachedLogs[x0 + x4]; newIrrep += cachedLogs[x0 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[x0]; newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 3*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x6 + x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 2*x4 + x5 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + x5 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + 2*x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + x2 + 3*x4 + 2*x5 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 2*x4 + x5 + 2*x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 2*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 2*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 3*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 3*x4 + x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 3*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[2*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[2*x0 + x1 + 2*x4 + x5 + x7]; newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[3*x0 + x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 2*x2 + 4*x4 + 2*x5 + x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 3*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[3*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 2*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 5*x4 + 3*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 4*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 3*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 2*x6 + 5*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7]; newIrrep += cachedLogs[4*x0 + 2*x1 + 4*x2 + 2*x3 + 6*x4 + 3*x5 + 3*x6 + 5*x7]; newIrrep += cachedLogs[x1]; newIrrep += cachedLogs[x2 + x3 + x4 + x6 + x7]; newIrrep += cachedLogs[x2 + x3 + x6 + x7]; newIrrep += cachedLogs[x2 + x3 + x6]; newIrrep += cachedLogs[x2 + x4 + x6 + x7]; newIrrep += cachedLogs[x2 + x4 + x7]; newIrrep += cachedLogs[x2 + x6 + x7]; newIrrep += cachedLogs[x2 + x6]; newIrrep += cachedLogs[x2 + x7]; newIrrep += cachedLogs[x2]; newIrrep += cachedLogs[x2 + x3 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x2 + x4 + x5 + x6 + x7]; newIrrep += cachedLogs[x2 + x4 + x5 + x7]; newIrrep += cachedLogs[x3 + x6]; newIrrep += cachedLogs[x3]; newIrrep += cachedLogs[x4 + x7]; newIrrep += cachedLogs[x4]; newIrrep += cachedLogs[x4 + x5 + x7]; newIrrep += cachedLogs[x4 + x5]; newIrrep += cachedLogs[x5]; newIrrep += cachedLogs[x6]; newIrrep += cachedLogs[x7];

			fringe.push(Pair(newCoord, newIrrep));
			seen.insert(newCoord);
		}

	}

    return 0;
}