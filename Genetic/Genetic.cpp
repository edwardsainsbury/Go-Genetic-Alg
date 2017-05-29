// Genetic.cpp : Defines the entry point for the console application.
//
#include "stdio.h"  
#include "stdafx.h"
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <tuple>
#include <array>

using namespace std;

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
	int p_depth = 0, p_height = 0, p_input = 0, p_output = 0, p_id = 0, p_parentOne = 0, p_parentTwo = 0, p_length = 0;
	float* p_weights = 0;
	// constructor
	Player(int depth, int height, int input, int output, int id, float weights[], int parentOne, int parentTwo);
	// copy constructor
	Player(const Player &obj);
	// Assingment operator
	Player& operator= (const Player& obj) {
		delete[] p_weights;
		p_depth = obj.p_depth;
		p_height = obj.p_height;
		p_input = obj.p_input;
		p_output = obj.p_output;
		p_id = obj.p_id;
		p_parentOne = obj.p_parentOne;
		p_parentTwo = obj.p_parentTwo;
		p_length = obj.p_length;
		//cout << "copied " << &obj << " to " << this << endl;
		float* weights2 = new float[p_length];
		for (int x = 0; x < p_length; x++) {
			weights2[x] = obj.p_weights[x];
		}
		p_weights = weights2;
		return *this;
	}
	// destrutor
	~Player();
	float* generateResult(int inputs[]) {
		// Need to change hard coded nature of this
		int nodesPerLayer[] = { p_input, p_height, p_height, p_height };
		int* nodesPerLayerCum = new int[p_depth+1];
		for (int i = 0; i < p_depth + 1; i++) {
			if (i == 0) {
				nodesPerLayerCum[i] = 0;
			}else {
				nodesPerLayerCum[i] = nodesPerLayerCum[i-1] + nodesPerLayer[i-1];
			}
		}
		int weightPerNode[] = {p_height, p_height, p_height, p_output};
		int size = nodesPerLayer[0] + nodesPerLayer[1] + nodesPerLayer[2] + nodesPerLayer[3];
		float* nodeOutput = new float[size]();

		float* returnArray = new float[p_output]();

		for (int a = 0; a < p_input; a++) {
			nodeOutput[a] = inputs[a];
		}

		for (int x = 0; x < p_depth ; x++) {
			for (int y = 0; y < nodesPerLayer[x]; y++) {
				float output = 0;
				for (int z = 0; z < weightPerNode[x];z++) {					
					output += p_weights[(nodesPerLayerCum[x] +y)*weightPerNode[x]+z] * nodeOutput[nodesPerLayerCum[x] + y];
				}
				nodeOutput[nodesPerLayerCum[x+1]+y] = output;
			}
		}

		for (int j = 0; j < p_output; j++) {
			returnArray[j] = nodeOutput[size-1-p_output+j];
		}
		
		return returnArray;
	}


};

Player::Player(int depth = 3, int height = 363, int input = 363, int output = 362, int id = 999, float weights[] = {}, int parentOne = 999, int parentTwo = 999) {
	p_depth = depth;
	p_height = height;
	p_input = input;
	p_output = output;
	p_id = id;
	p_parentOne = parentOne;
	p_parentTwo = parentTwo;
	p_length = height*(input + (depth - 1)*height + output);

	float* weights2 = new float[p_length];
	if (weights == 0){
		for (int x = 0; x < p_length; x++) {
			//float a = rand() % 100;
			float a = xorshf96() % 100;
			weights2[x] = a / 100;
		}
		
	}else {
		//float* p_weights = new float[p_length];
		for (int x = 0; x <p_length; x++) {
			weights2[x] = weights[x];
		}
		
	}
	p_weights = weights2;
	cout << "Created " << this << endl;

}

Player::Player(const Player& obj) {
	p_depth = obj.p_depth;
	p_height = obj.p_height;
	p_input = obj.p_input;
	p_output = obj.p_output;
	p_id = obj.p_id;
	p_parentOne = obj.p_parentOne;
	p_parentTwo = obj.p_parentTwo;
	p_length = obj.p_length;
	//cout << "copied " << &obj << " to " << this << endl;
	float* weights2 = new float[p_length];
	for (int x = 0; x < p_length; x++) {
		weights2[x] = obj.p_weights[x];
	}
	p_weights = weights2;
	
}




Player::~Player() {
	cout << "Deleted " << p_id << endl;
	delete[] p_weights;
}

struct loadStruct {
	Player* arrayOfPlayers;
	int numberOfPlayersCreated;
	int startEra;
	~loadStruct() {
		delete[] arrayOfPlayers;
	};
};


loadStruct load() {
	Player* arrayOfPlayers = new Player[1];
	return { arrayOfPlayers,0,0 };
}

loadStruct *startNew(int numberOfPlayersPerRound) {
	//cout << "in start new" << endl;
	Player* arrayOfPlayers = new Player[numberOfPlayersPerRound];
	loadStruct* toReturn = new loadStruct;
	toReturn->arrayOfPlayers = arrayOfPlayers;
	toReturn->numberOfPlayersCreated = numberOfPlayersPerRound;
	toReturn->startEra = 0;
	return toReturn;
}

int playGo(Player playerOne, Player playerTwo) {
	if (playerOne.p_weights[0] > playerTwo.p_weights[0]) {
		return 0;
	}
	else {
		return 2;
	}
	return 1;
}

Player reproduce(Player player1, Player player2, int numberOfPlayersCreated) {
	float* allNewWeights = new float[player1.p_length]();
	for (unsigned int idx = 0; idx < player1.p_length; idx++) {
		if ((xorshf96() % 100)/100> 0.5) {
			allNewWeights[idx] = player2.p_weights[idx];
		}else{
			allNewWeights[idx] = player1.p_weights[idx];
		}
		if ((xorshf96() % 100) / 100 < 1/ player1.p_length) {
			allNewWeights[idx] = (xorshf96() % 100) / 100;
		}
	}
	Player returnedPlayer = Player(3, 363, 363, 362, numberOfPlayersCreated + 1, allNewWeights, player1.p_id, player2.p_id);
	delete[] allNewWeights;
	return returnedPlayer;
}

void secondary() {
	bool doLoad = false;
	int numberOfEra = 10;
	int numberOfPlayersPerRound = 4;
	bool inUserLoop = true;
	while (inUserLoop) {
		char user = ' ';
		//cout << "(N)ew or (L)oad?" << endl;
		//cin >> user;
		user = 'n';
		if (toupper(user) == 'N') {
			doLoad = false;
			inUserLoop = false;
		}
		else if (toupper(user) == 'L') {
			doLoad = true;
			inUserLoop = false;
		}
		else {
			cout << "Incorrect Input" << endl;
		}
	}




	Player* players = new Player[numberOfPlayersPerRound];

	loadStruct* loaded = new loadStruct;
	if (doLoad) {

		loadStruct loaded = load();
		Player* players = loaded.arrayOfPlayers;
	}
	else {
		loaded = startNew(numberOfPlayersPerRound);
		Player* players = loaded->arrayOfPlayers;
	}
	int startEra = loaded->startEra;
	int numberOfPlayersCreated = loaded->numberOfPlayersCreated;
	delete loaded;


	cout << " Only Players array exists" << endl;
	// Main playing loop
	for (int era = startEra; era < numberOfEra; era++) {
		cout << "Era: " << era + 1 << endl;
		
		int* wins = new int[numberOfPlayersPerRound];
		
		// Could either create each permutation or just use for loop on the fly
		for (int player1 = 0; player1 < numberOfPlayersPerRound; player1++) {
			for (int player2 = 0; player2 < numberOfPlayersPerRound; player2++) {
				//cout << player1 << " vs " << player2 << endl;
				if (player1 == player2) {
					//cout << "skipped" << endl;
					continue;
				}
				//int winner = 1; 
				//for (int idx = 0; idx < 600; idx++) {
				int winner = playGo(players[player1], players[player2]);
				//}

				if (winner == 2) {
					wins[player1] += 3;
				}
				else if (winner == 0) {
					wins[player2] += 3;
				}
				else {
					wins[player1] += 1;
					wins[player2] += 1;
				} 
				//SQL Saving stuff
			}
		}
		// setup and decide winners array
		tuple<int,int>* numbers = new tuple<int,int>[numberOfPlayersPerRound, numberOfPlayersPerRound]();
		for (int idx = 0; idx < numberOfPlayersPerRound; idx++) {
			numbers[idx] = tuple<int, int>(wins[idx],idx);
			//cout << get<0>(numbers[idx]) << " " << get<1>(numbers[idx]) << endl;
		}
		
		sort(numbers,numbers+ numberOfPlayersPerRound);
		//cout << "sorted" << endl;
		int* sortedNumbers = new int[numberOfPlayersPerRound];
		for (int idx = 0; idx < numberOfPlayersPerRound; idx++) {
			sortedNumbers[idx] = get<1>(numbers[numberOfPlayersPerRound-idx-1]);
			//cout << get<0>(numbers[idx]) << " " << sortedNumbers[idx] << endl;
		}

		for (int idx = 0; idx < numberOfPlayersPerRound; idx++) {
			numbers[idx] = tuple<int, int>(wins[idx], idx);
			//cout << get<0>(numbers[idx]) << " " << get<1>(numbers[idx]) << endl;
		}
		//cout << sortedNumbers[0] << endl;
		Player* newPlayers = new Player[numberOfPlayersPerRound];
		for (int idx = 0; idx<int(numberOfPlayersPerRound / 4); idx += 2) {
			newPlayers[idx] = reproduce(players[sortedNumbers[idx]], players[sortedNumbers[idx + 1]],numberOfPlayersCreated);
			newPlayers[idx + 1] = Player(3, 363, 363, 362, numberOfPlayersCreated + 2, {}, 999, 999);
			newPlayers[idx+2] = players[sortedNumbers[idx]];
			newPlayers[idx+3] = players[sortedNumbers[idx+1]];
		}

		for (int x = 0; x < numberOfPlayersPerRound; x++) {
			players[x] = newPlayers[x];

		}
		numberOfPlayersCreated += 2;
		delete[] newPlayers;
		delete[] sortedNumbers;
		delete[] numbers;
		delete[] wins;

	}

	delete[] players;
	/*
	int* input = new int[363];

	for (int x = 0; x < 363; x++) {
		input[x] = 1;
	}

	//float* returned = playerOne.generateResult(input);
	//cout << returned[0] << endl;
	delete[] input;
	*/
}

int	main() {
	for (int idx = 0; idx < 1; idx++) {
		cout << idx << endl;
		secondary();
	}
}



