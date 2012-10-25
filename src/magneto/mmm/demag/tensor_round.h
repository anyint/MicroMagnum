#ifndef TENSOR_ROUND_H
#define TENSOR_ROUND_H

#include "config.h"

enum {
	PADDING_DISABLE = 0,
	PADDING_ROUND_2 = 1,
	PADDING_ROUND_4 = 2,
	PADDING_ROUND_8 = 3,
	PADDING_ROUND_POT = 4,
	PADDING_SMALL_PRIME_FACTORS = 5,
};

int round2(int x);
int round4(int x);
int round8(int x);
int round_pot(int x);
int round_small_prime_factors(int x);

int round_tensor_dimension(int dim, bool periodic, int padding);

int my_mod(int x, int y);

#endif