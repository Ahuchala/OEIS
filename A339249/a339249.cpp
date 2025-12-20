// Code written by Andy Huchala
// Computes the list of dimensions for which there exist several non-isomorphic irreducible representations of F4.

#include <iostream>
#include <queue>
#include <math.h>
#include <fstream>
#include <unordered_set>

// Requires this file in the same directory to print, available at https://github.com/sercantutar/infint/blob/master/InfInt.h
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

	const long UPPER_BOUND_FACTOR = 90000;
	const long shift_const = (1LL << 16L) - 1L;
	long double* cachedLogs = (long double*) malloc(sizeof (long double) * UPPER_BOUND_FACTOR);
	// long double cachedLogs [UPPER_BOUND_FACTOR];
	int cums[4] = {0, 16, 32, 48};
	const long long denom = 24141680640000;

	for (long i = 1; i < UPPER_BOUND_FACTOR; i++) {
		cachedLogs[i] = std::log ( i);
    }
    long long x = 0LL;
    std::priority_queue<Pair> fringe;
	std::unordered_set<long long> seen;
	
	// const long long numToCompute = 10;
	const long long numToCompute = 20000;
	long numComputed = 0;
	int numSeen = 1;

	long double irrep = 30.814960949;

	fringe.push(Pair(x, irrep));

	long double lastLog = 0.0;
	long long lastCoord = -1LL;
	long x0; long x1; long x2; long x3;
	long long newCoord;
	long double newIrrep;
	std::cout<< "Initialization complete\n";

	std::ofstream myfile ("f4_rep.txt");
	if (myfile.is_open()) {

		while (numSeen < numToCompute + 1) {
			numComputed++;
			Pair cur = fringe.top();
			fringe.pop();
			seen.erase(cur.coordinates);

			if (std::abs(lastLog-cur.log) < 1e-12) {
				x0 = (long) (cur.coordinates & shift_const) + 1L;
				x1 = (long) ((cur.coordinates >> 16LL) & shift_const) + 1L;
				x2 = (long) ((cur.coordinates >> 32LL) & shift_const) + 1L;
				x3 = (long) ((cur.coordinates >> 48LL) & shift_const) + 1L;
				InfInt dim1 = "1";
				dim1 *= (x0);
				dim1 *= (x1);
				dim1 *= (x2);
				dim1 *= (x3);
				dim1 *= (x0+x1);
				dim1 *= (x1+x2);
				dim1 *= (x2+x3);
				dim1 *= (x0+x1+x2);
				dim1 *= (x1+x2+x3);
				dim1 *= (x0+x1+x2+x3);
				dim1 *= (2*x1+x2);
				dim1 *= (2*x1+x2+x3);
				dim1 *= (x0+2*x1+x2);
				dim1 *= (2*x1+2*x2+x3);
				dim1 *= (x0+2*x1+x2+x3);
				dim1 *= (2*x0+2*x1+x2);
				dim1 *= (x0+2*x1+2*x2+x3);
				dim1 *= (2*x0+2*x1+x2+x3);
				dim1 *= (x0+3*x1+2*x2+x3);
				dim1 *= (2*x0+2*x1+2*x2+x3);
				dim1 *= (2*x0+3*x1+2*x2+x3);
				dim1 *= (2*x0+4*x1+2*x2+x3);
				dim1 *= (2*x0+4*x1+3*x2+x3);
				dim1 *= (2*x0+4*x1+3*x2+2*x3);
				dim1 /= denom;

				x0 = (long) (lastCoord & shift_const) + 1L;
				x1 = (long) ((lastCoord >> 16LL) & shift_const) + 1L;
				x2 = (long) ((lastCoord >> 32LL) & shift_const) + 1L;
				x3 = (long) ((lastCoord >> 48LL) & shift_const) + 1L;
				InfInt dim2 = "1";
				dim2 *= (x0);
				dim2 *= (x1);
				dim2 *= (x2);
				dim2 *= (x3);
				dim2 *= (x0+x1);
				dim2 *= (x1+x2);
				dim2 *= (x2+x3);
				dim2 *= (x0+x1+x2);
				dim2 *= (x1+x2+x3);
				dim2 *= (x0+x1+x2+x3);
				dim2 *= (2*x1+x2);
				dim2 *= (2*x1+x2+x3);
				dim2 *= (x0+2*x1+x2);
				dim2 *= (2*x1+2*x2+x3);
				dim2 *= (x0+2*x1+x2+x3);
				dim2 *= (2*x0+2*x1+x2);
				dim2 *= (x0+2*x1+2*x2+x3);
				dim2 *= (2*x0+2*x1+x2+x3);
				dim2 *= (x0+3*x1+2*x2+x3);
				dim2 *= (2*x0+2*x1+2*x2+x3);
				dim2 *= (2*x0+3*x1+2*x2+x3);
				dim2 *= (2*x0+4*x1+2*x2+x3);
				dim2 *= (2*x0+4*x1+3*x2+x3);
				dim2 *= (2*x0+4*x1+3*x2+2*x3);
				dim2 /= denom;

				if (dim1 == dim2) {
					// std::cout<< std::to_string((long) (cur.coordinates & shift_const) + 1L) + " " + std::to_string((long) ((cur.coordinates >> 16LL) & shift_const) + 1L) + " " + std::to_string((long) ((cur.coordinates >> 32LL) & shift_const) + 1L) + " " + std::to_string((long) ((cur.coordinates >> 48LL) & shift_const) + 1L) + "\n";
					// std::cout<< std::to_string(x0)+ " " +std::to_string(x1)+" " + std::to_string(x2)+ " "+std::to_string(x3)+ " ""\n";
					myfile <<std::to_string(numSeen) + " " +(dim1.toString())+ "\n";
					std::cout<< std::to_string(numSeen) + " " +(dim1.toString())+ "\n";
					numSeen++;
				}
			}
			lastLog = cur.log;
			lastCoord = cur.coordinates;
			for (int i = 0; i < 4; i++) {
				newCoord = cur.coordinates + (1LL << cums[i]);
				if (seen.count(newCoord)) {
					continue;
				}
				x0 = (long) (newCoord & shift_const) + 1L;
				x1 = (long) ((newCoord >> 16LL) & shift_const) + 1L;
				x2 = (long) ((newCoord >> 32LL) & shift_const) + 1L;
				x3 = (long) ((newCoord >> 48LL) & shift_const) + 1L;

				newIrrep = 0;
				newIrrep += cachedLogs[x0];
				newIrrep += cachedLogs[x1];
				newIrrep += cachedLogs[x2];
				newIrrep += cachedLogs[x3];
				newIrrep += cachedLogs[x0+x1];
				newIrrep += cachedLogs[x1+x2];
				newIrrep += cachedLogs[x2+x3];
				newIrrep += cachedLogs[x0+x1+x2];
				newIrrep += cachedLogs[x1+x2+x3];
				newIrrep += cachedLogs[x0+x1+x2+x3];
				newIrrep += cachedLogs[2*x1+x2];
				newIrrep += cachedLogs[2*x1+x2+x3];
				newIrrep += cachedLogs[x0+2*x1+x2];
				newIrrep += cachedLogs[2*x1+2*x2+x3];
				newIrrep += cachedLogs[x0+2*x1+x2+x3];
				newIrrep += cachedLogs[2*x0+2*x1+x2];
				newIrrep += cachedLogs[x0+2*x1+2*x2+x3];
				newIrrep += cachedLogs[2*x0+2*x1+x2+x3];
				newIrrep += cachedLogs[x0+3*x1+2*x2+x3];
				newIrrep += cachedLogs[2*x0+2*x1+2*x2+x3];
				newIrrep += cachedLogs[2*x0+3*x1+2*x2+x3];
				newIrrep += cachedLogs[2*x0+4*x1+2*x2+x3];
				newIrrep += cachedLogs[2*x0+4*x1+3*x2+x3];
				newIrrep += cachedLogs[2*x0+4*x1+3*x2+2*x3];

				fringe.push(Pair(newCoord, newIrrep));
				seen.insert(newCoord);
			}

		}
	}
	myfile.close();
	free(cachedLogs);

    return 0;
}