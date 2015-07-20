/*
 * main.cpp
 *
 *  Created on: Oct 24, 2014
 *      Author: parallels
 */

#include <iostream>
#include <cstdlib>
#include <libgen.h>
#include <signal.h>
#include <getopt.h>
#include <BeagleRT.h>

using namespace std;

int gSensorInputFrequency = 0;
int gSensorInputAmplitude = 1;


// Handle Ctrl-C by requesting that the audio rendering stop
void interrupt_handler(int var)
{
	gShouldStop = true;
}

// Print usage information
void usage(const char * processName)
{
	cerr << "Usage: " << processName << " [options]" << endl;

	BeagleRT_usage();

	cerr << "   --frequency [-f] input:  Choose the analog input controlling frequency (0-7; default 0)\n";
	cerr << "   --amplitude [-a] input:  Choose the analog input controlling amplitude (0-7; default 1)\n";
	cerr << "   --help [-h]:             Print this menu\n";
}

int main(int argc, char *argv[])
{
	BeagleRTInitSettings settings;	// Standard audio settings

	struct option customOptions[] =
	{
		{"help", 0, NULL, 'h'},
		{"frequency", 1, NULL, 'f'},
		{"amplitude", 1, NULL, 'a'},
		{NULL, 0, NULL, 0}
	};

	// Set default settings
	BeagleRT_defaultSettings(&settings);

	// Parse command-line arguments
	while (1) {
		int c;
		if ((c = BeagleRT_getopt_long(argc, argv, "hf:a:", customOptions, &settings)) < 0)
				break;
		switch (c) {
		case 'h':
				usage(basename(argv[0]));
				exit(0);
		case 'f':
				gSensorInputFrequency = atoi(optarg);
				if(gSensorInputFrequency < 0 || gSensorInputFrequency > 7) {
					usage(basename(argv[0]));
					exit(0);
				}
				break;
		case 'a':
				gSensorInputAmplitude = atoi(optarg);
				if(gSensorInputAmplitude < 0 || gSensorInputAmplitude > 7) {
					usage(basename(argv[0]));
					exit(0);
				}
				break;
		case '?':
		default:
				usage(basename(argv[0]));
				exit(1);
		}
	}

	// Initialise the PRU audio device
	if(BeagleRT_initAudio(&settings, 0) != 0) {
		cout << "Error: unable to initialise audio" << endl;
		return -1;
	}

	if(settings.verbose) {
		cout << "--> Frequency on input " << gSensorInputFrequency << endl;
		cout << "--> Amplitude on input " << gSensorInputAmplitude << endl;
	}

	// Start the audio device running
	if(BeagleRT_startAudio()) {
		cout << "Error: unable to start real-time audio" << endl;
		return -1;
	}

	// Set up interrupt handler to catch Control-C and SIGTERM
	signal(SIGINT, interrupt_handler);
	signal(SIGTERM, interrupt_handler);

	// Run until told to stop
	while(!gShouldStop) {
		usleep(100000);
	}

	// Stop the audio device
	BeagleRT_stopAudio();

	// Clean up any resources allocated for audio
	BeagleRT_cleanupAudio();

	// All done!
	return 0;
}
