#include "stdio.h"  
#include "stdafx.h"
#include <cstdlib>
#include <iostream>

static unsigned long randx = 123456789, randy = 362436069, randz = 521288629;

unsigned long xorshf96(void) {          //period 2^96-1
	unsigned long t = 0;
	randx ^= randx << 16;
	randx ^= randx >> 5;
	randx ^= randx << 1;

	t = randx;
	randx = randy;
	randy = randz;
	randz = t ^ randx ^ randy;

	return randz;
}




class Player {
public:
	int p_depth = 0, p_height = 0, p_input = 0, p_output = 0, p_id = 0, p_parentOne = 0, p_parentTwo = 0;
	float* p_weights = 0;
	// constructor
	Player(int depth, int height, int input, int output, int id, float weights[], int parentOne, int parentTwo);
	// copy constructor
	Player(const Player &obj);
	// destrutor
	~Player();
	float* generateResult(int inputs[]) {
		// Need to change hard coded nature of this
		int nodesPerLayer[] = { p_input, p_height, p_height, p_height };
		int* nodesPerLayerCum = new int[p_depth + 1];
		for (int i = 0; i < p_depth + 1; i++) {
			if (i == 0) {
				nodesPerLayerCum[i] = 0;
			}
			else {
				nodesPerLayerCum[i] = nodesPerLayerCum[i - 1] + nodesPerLayer[i - 1];
			}
		}
		int weightPerNode[] = { p_height, p_height, p_height, p_output };
		int size = nodesPerLayer[0] + nodesPerLayer[1] + nodesPerLayer[2] + nodesPerLayer[3];
		float* nodeOutput = new float[size]();

		float* returnArray = new float[p_output]();

		for (int a = 0; a < p_input; a++) {
			nodeOutput[a] = inputs[a];
		}

		for (int x = 0; x < p_depth; x++) {
			for (int y = 0; y < nodesPerLayer[x]; y++) {
				float output = 0;
				for (int z = 0; z < weightPerNode[x]; z++) {
					output += p_weights[(nodesPerLayerCum[x] + y)*weightPerNode[x] + z] * nodeOutput[nodesPerLayerCum[x] + y];
				}
				nodeOutput[nodesPerLayerCum[x + 1] + y] = output;
			}
		}

		for (int j = 0; j < p_output; j++) {
			returnArray[j] = nodeOutput[size - 1 - p_output + j];
		}

		return returnArray;
	}


};
// Constructor
Player::Player(int depth = 3, int height = 363, int input = 363, int output = 362, int id = 999, float weights[] = {}, int parentOne = 999, int parentTwo = 999) {
	p_depth = depth;
	p_height = height;
	p_input = input;
	p_output = output;
	p_id = id;
	p_parentOne = parentOne;
	p_parentTwo = parentTwo;
	float* weights2 = new float[height*(input + (depth - 1)*height + output)];
	if (weights == 0) {
		for (int x = 0; x < height*(input + (depth - 1)*height + output); x++) {
			//float a = rand() % 100;
			float a = xorshf96() % 100;
			weights2[x] = a / 100;
		}
		p_weights = weights2;
	}
	else {
		float p_weights = *weights;
	}
	//cout << "Created " << this << endl;

}
// Copy constructor
Player::Player(const Player& obj) {
	p_depth = obj.p_depth;
	p_height = obj.p_height;
	p_input = obj.p_input;
	p_output = obj.p_output;
	p_id = obj.p_id;
	p_parentOne = obj.p_parentOne;
	p_parentTwo = obj.p_parentTwo;
	float* weights2 = new float[p_height*(p_input + (p_depth - 1)*p_height + p_output)];
	for (int x = 0; x < p_height*(p_input + (p_depth - 1)*p_height + p_output); x++) {
		weights2[x] = obj.p_weights[x];
	}
	p_weights = weights2;
	//cout << "copied " << &obj << " to " << this << endl;
}
//Destructor
Player::~Player() {
	//cout << "Deleted " << this << endl;
	delete[] p_weights;
}
