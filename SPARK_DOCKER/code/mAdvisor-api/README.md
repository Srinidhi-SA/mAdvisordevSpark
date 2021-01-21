# To build docker image using latest tag:

	command : docker build -t api .
	
 	otherwise command : docker build -t <image_name>:<tag> .


# To run:

	NOTE :Edit /etc/hosts file with <HOST_MACHINE_IP> <Hostname> of Host machine containing any other linked containers.
	
	command : docker run -p 8000:8000 -it <Image_ID> bash
