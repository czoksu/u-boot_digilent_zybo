#!/bin/python

import os
import subprocess as sub
import sys

vivado = {'found':False,'filename':'', 'dir':''}
arm_xilinx = {'found':False,'filename':''}


if __name__ == "__main__":
	print "Checking for installation files...\n"
	files = os.listdir('.')
	
	for element in files:
		if (element.find('Xilinx_Vivado_SDK') != -1):
			vivado['found'] = True
			vivado['filename'] = element
			vivado['dir'] = \
				vivado['filename'].replace('.tar.gz', '')
			print "\t" + element + " found!"
		elif (element.find('arm-xilinx-linux') != -1):
			arm_xilinx['found'] = True
			arm_xilinx['filename'] = element
			print "\t" + element + " found!"

	print "\tDownloading 32-bit libraries...\n"
	sub.check_call(["sudo", "apt-get", "install", "-y", "lib32z1", "git",
			"lib32ncurses5", "lib32bz2-1.0", "libc6-i386", "lib32tinfo5"])

	if not (vivado['found'] | arm_xilinx['found']):
		sys.exit("\n\tDownload the needed software first!\n")
	else:
		print "\tManually complete the installation!\n"
		#if not (vivado['dir'] in files):
			#print "\tExtracting " + vivado['filename']
			#sub.check_call(["tar", "zxvf", vivado['filename']])
		
		#sub.check_call(["chmod", "+x", vivado['dir'] + '/xsetup'])	
		#sub.check_call(["sudo", vivado['dir'] + '/xsetup'])
		
		sub.check_call(["chmod", "+x", arm_xilinx['filename']])
		sub.check_call([os.getcwd() + "/" + arm_xilinx['filename']])
		
		print "\n\tInstallation finished.\n"
		
		print "\tDownloading git repository...\n"
		sub.check_call(["git", "clone", "-b", "master-next", 
				"https://github.com/DigilentInc/" +
				"u-boot-Digilent-Dev.git"])
		
		print "\n\tGit repo downloaded!\n"
		
		print "\tLooking for compiler path..."
		
		compiler_path = \
			sub.check_output(["find", "/home/" , "-name",
					  "arm-xilinx-linux-gnueabi-gcc"]).replace("arm-xilinx-linux-gnueabi-gcc", "")
		
		print "\tCompiler path found!"
		print compiler_path
		
		print "\tAdding compiler path to the PATH variable..."
		os.environ["PATH"] += os.pathsep + compiler_path.replace("\n", "")
		
		print "\tDone!"
		print "\t" + os.environ.get("PATH")
		
		#print "\tLooking for Vivado settings path..."
		#vivado_path = sub.check_output(["find", 
		#				"/opt/Xilinx/Vivado", 
		#		  		"-name", "settings64.sh"])
		
		#print "\tSetting path found!"
		
		#print "\t" + vivado_path
		
		print "\tEntering the u-boot repository..."
		os.chdir(os.getcwd() + "/u-boot-Digilent-Dev")
		
		#print "\tSourcing Vivado settings..."
		#sub.check_call(["source", vivado_path.replace("\n", "")], shell=True)
		
		print "\tPreparing config..."
		sub.check_call(["make",
				"CROSS_COMPILE=arm-xilinx-linux-gnueabi-",
				"zynq_zybo_config"])
				
		print "\tConfig prepared!"
		
		print "\t Compiling u-boot..."
		
		sub.check_call(["make",
				"CROSS_COMPILE=arm-xilinx-linux-gnueabi-",
				"zynq_zybo"])
				
		print "\tU-boot image compiled!"
