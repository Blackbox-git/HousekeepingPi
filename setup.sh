#!/bin/bash

# Create supporting variables
PS3="
Option: "
root=`pwd`
cd ~
user=`pwd`
installed='n'
selection='0'

echo -e "\e[0m"
echo -e "\e[0m"
echo -e "\e[0m#############################################################"
echo -e "\e[0m######                                                 ######"
echo -e "\e[0m######                   Installation                  ######"
echo -e "\e[0m######                  HousekeepingPI                 ######"
echo -e "\e[0m######                                                 ######"
echo -e "\e[0m#############################################################"
echo -e "\e[0m"
echo -e "\e[0m"


# Check if program is already installed
if [ -f /opt/haushalt/haushalt.py ] && [ -f /opt/haushalt/datenbank.py ] ;
	then
	installed='y'
fi

# Message about installation
if [ $installed == 'n' ];
	then
	echo -e "\e[96mThe program is not installed. Please choose from the following options:\e[0m"
	echo -e "\e[96m"
elif [ $installed == 'y' ];
	then
	echo -e "\e[96mThe program is already installed. Please choose from the following options:\e[0m"
	echo -e "\e[96m"
else
	exit
fi

# Display of a selection menu
if [ $installed == 'n' ];
	then 
	select selection in "Install program" "End setup"
	do
	   case "$selection" in
		  "End setup") 	echo -e "\e[0m"; echo -e "\e[91mSetup aborted. No changes made.\e[0m"; echo -e "\e[96m"; exit ;;
			"")  echo -e "\e[96mWrong selection. Select any number from 1 - 2\e[0m" ; echo -e "\e[96m" ;;
			 *)  break ;;
	   esac
	done
elif [ $installed == 'y' ];
	then
	select selection in "Deinstall programm" "End setup"
	do
	   case "$selection" in
		  "End setup") echo -e "\e[0m"; echo -e "\e[91mSetup aborted. No changes made.\e[0m"; echo -e "\e[96m"; exit ;;
			"")  echo -e "\e[96mWrong selection. Select any number from 1 - 2\e[0m" ; echo -e "\e[96m" ;;
			 *)  break ;;
	   esac
	done
else
	exit
fi

# Convert varialbe selection
if [ "$selection" == 'Install program' ];
	then
	selection='1'
elif [ "$selection" == 'Deinstall programm' ];
	then
	selection='2'
else
	exit
fi

# Running setup
if [ $selection == '1' ];
	then
	
	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                Number of Sockets                ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Query Hoch much sockets do you have
	echo -e "\e[96mHow much Sockets do you have (1 - 3 are supportet):"
	echo -e "\e[96m"
	select sockets in "I have 1 Socket" "I have 2 Sockets" "I have 3 Sockets"
	do
	   case "$sockets" in
			"")  echo -e "\e[96mWrong selection. Select any number from 1 - 3\e[0m" ; echo -e "\e[96m" ;;
			 *)  break ;;
	   esac
	done

	# Convert varialbe sockets
	if [ "$sockets" == 'I have 1 Socket' ];
		then
		sockets='1'
	elif [ "$sockets" == 'I have 2 Sockets' ];
		then
		sockets='2'
	elif [ "$sockets" == 'I have 3 Sockets' ];
		then
		sockets='3'
	fi

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                     Socket 1                    ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Insert the name of the device of the first socket
	read -p "Insert the name of the device of the first socket (example: Waschmaschine): " Name1
	echo -e "\e[96m"
	echo -e "\e[96m"
	
	# Insert the AIN of the first socket
	read -p "Insert the AIN of the first socket: " AIN1
	echo -e "\e[96m"
	echo -e "\e[96m"
	
	# Insert the Token-ID of the First socket
	read -p "Insert the Token-ID of the first telegram-bot of the first socket: " Bot1
	echo -e "\e[96m"
	echo -e "\e[96m"

	if [ "$sockets" == '2' ] || [ "$sockets" == '3' ]
		then
	
		echo -e "\e[0m#############################################################"
		echo -e "\e[0m######                     Socket 2                    ######"
		echo -e "\e[0m#############################################################"
		echo -e "\e[96m"
		echo -e "\e[96m"

		# Insert the name of the device of the second socket
		read -p "Insert the name of the device fo the second socket (example: Waschmaschine): " Name2
		echo -e "\e[96m"
		echo -e "\e[96m"
		
		# Insert the AIN of the second socket
		read -p "Insert the AIN of the second socket: " AIN2
		echo -e "\e[96m"
		echo -e "\e[96m"
		
		# Insert the Token-ID of the second socket
		read -p "Insert the Token-ID of the second telegram-bot of the second socket: " Bot2
		echo -e "\e[96m"
		echo -e "\e[96m"
	
		if [ "$sockets" == '3' ]
			then
					
			echo -e "\e[0m#############################################################"
			echo -e "\e[0m######                     Socket 3                    ######"
			echo -e "\e[0m#############################################################"
			echo -e "\e[96m"
			echo -e "\e[96m"
			
			# Insert the name of the device of the third socket
			read -p "Insert the name of the device fo the third socket (example: Waschmaschine): " Name3
			echo -e "\e[96m"
			echo -e "\e[96m"
			
			# Insert the AIN of the third socket
			read -p "Insert the AIN of the third socket: " AIN3
			echo -e "\e[96m"
			echo -e "\e[96m"
			
			# Insert the Token-ID of the third socket
			read -p "Insert the Token-ID of the third telegram-bot of the third socket: " Bot3
			echo -e "\e[96m"
			echo -e "\e[96m"
			fi
	fi

	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                     Group-ID                    ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"
	
	# Insert the ID of the telegram-group
	read -p "Insert the ID of the telegram-group (example: -3257961): " groupid
	echo ""
	echo ""

	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                     Fritzbox                    ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Insert the Fritz!Box  user
	read -p "Insert the Fritz!Box user: " fritzboxuser
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Insert the Fritz!Box  password
	read -s -p "Insert the Fritz!Box password: " fritzboxpassword
	echo -e "\e[96m"
	echo -e "\e[96m"
	echo -e "\e[96m"
	
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                  User password                  ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Insert your user password
	read -s -p "Insert your user password: " userpassword
	echo -e "\e[96m"
	echo -e "\e[96m"
	echo -e "\e[96m"

	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                Create directories               ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"

	# Create directories
	echo -e "\e[0m"
	echo -e "\e[96mCreate directories\e[0m"
	if [ ! -d $user/.credentials ];
		then
		mkdir $user/.credentials
	fi
	if [ ! -d /opt/haushalt ];
		then
		sudo mkdir /opt/haushalt
	fi

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######       Update system and install  programs       ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"

	# Update Raspberry
	echo -e "\e[0m"
	echo -e "\e[96mUpdate Raspberry\e[0m"
	echo -e "\e[0m"
	sudo apt-get -y update 
	sudo apt-get -y dist-upgrade

	# Install necessary programs
	echo -e "\e[0m"
	echo -e "\e[96mInstall necessary programs\e[0m"
	echo -e "\e[0m"
	sudo apt-get -y install python-pip python3-pip mariadb-server-10.3 python-mysqldb python3-mysqldb

	# PyDect200 instalieren
	echo -e "\e[0m"
	echo -e "\e[96mInstall Library PyDect200\e[0m"
	echo -e "\e[0m"
	sudo pip install PyDect200
	sudo pip3 install PyDect200

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######              Setting up the system              ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"

	# Creating datenbank.json files
	echo -e "\e[0m"
	echo -e "\e[96mCreating datenbank.json\e[0m"
	if [ -f $user/.credentials/datenbank.json ];
		then
		sudo rm $user/.credentials/datenbank.json
	fi	
	touch $user/.credentials/datenbank.json
	echo "{" >> $user/.credentials/datenbank.json
	echo '"datenbankserver":"localhost",' >> $user/.credentials/datenbank.json
	echo '"datenbankbenutzername":"root",' >> $user/.credentials/datenbank.json
	echo '"datenbankpasswort":"",' >> $user/.credentials/datenbank.json
	sed $user/.credentials/datenbank.json -i -e 's/^"datenbankpasswort":"",/"datenbankpasswort":"'$userpassword'",/'
	echo '"datenbankname":"haushalt"' >> $user/.credentials/datenbank.json
	echo "}" >> $user/.credentials/datenbank.json
	
	# Creating schwellenwerte.json files
	echo -e "\e[0m"
	echo -e "\e[96mCreating schwellenwerte.json\e[0m"
	if [ -f $user/.credentials/schwellenwerte.json ];
		then
		sudo rm $user/.credentials/schwellenwerte.json
	fi	
	touch $user/.credentials/schwellenwerte.json
	echo "{" >> $user/.credentials/schwellenwerte.json
	echo '"AIN1start": "",' >> $user/.credentials/schwellenwerte.json
	echo '"AIN1stop": "",' >> $user/.credentials/schwellenwerte.json
	echo '"AIN2start": "",' >> $user/.credentials/schwellenwerte.json
	echo '"AIN2stop": "",' >> $user/.credentials/schwellenwerte.json
	echo '"AIN3start": "",' >> $user/.credentials/schwellenwerte.json
	echo '"AIN3stop": ""' >> $user/.credentials/schwellenwerte.json
	echo "}" >> $user/.credentials/schwellenwerte.json
	
	# Creating avm.json files
	echo -e "\e[0m"
	echo -e "\e[96mCreating avm.json\e[0m"
	if [ -f $user/.credentials/avm.json ];
		then
		sudo rm $user/.credentials/avm.json
	fi	
	touch $user/.credentials/avm.json
	echo "{" >> $user/.credentials/avm.json
	echo '"fritzboxbenutzername":"",' >> $user/.credentials/avm.json
	sed $user/.credentials/avm.json -i -e 's/^"fritzboxbenutzername":"",/"fritzboxbenutzername":"'$fritzboxuser'",/'
	echo '"fritzboxpasswort":"",' >> $user/.credentials/avm.json
	sed $user/.credentials/avm.json -i -e 's/^"fritzboxpasswort":"",/"fritzboxpasswort":"'$fritzboxpassword'",/'
	if [ "$sockets" == '2' ] || [ "$sockets" == '3' ]
		then
		echo '"Name1":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"Name1":"",/"Name1":"'$Name1'",/'
		echo '"AIN1":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"AIN1":"",/"AIN1":"'$AIN1'",/'	
	else
		echo '"Name1":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"Name1":"",/"Name1":"'$Name1'",/'
		echo '"AIN1":""' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"AIN1":""/"AIN1":"'$AIN1'"/'
	fi
	if [ "$sockets" == '3' ]
		then
		echo '"Name2":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"Name2":"",/"Name2":"'$Name2'",/'
		echo '"AIN2":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"AIN2":"",/"AIN2":"'$AIN2'",/'
		echo '"Name3":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"Name3":"",/"Name3":"'$Name3'",/'
		echo '"AIN3":""' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"AIN3":""/"AIN3":"'$AIN3'"/'	
	elif [ "$sockets" == '2' ]
		then
		echo '"Name2":"",' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"Name2":"",/"Name2":"'$Name2'",/'		
		echo '"AIN2":""' >> $user/.credentials/avm.json
		sed $user/.credentials/avm.json -i -e 's/^"AIN2":""/"AIN2":"'$AIN2'"/'
	fi
	echo "}" >> $user/.credentials/avm.json

	# Creating telegram.json files
	echo -e "\e[0m"
	echo -e "\e[96mCreating telegram.json\e[0m"
	if [ -f $user/.credentials/telegram.json ];
		then
		sudo rm $user/.credentials/telegram.json
	fi	
	touch $user/.credentials/telegram.json
	echo "{" >> $user/.credentials/telegram.json
	echo '"Name1":"",' >> $user/.credentials/telegram.json
	sed $user/.credentials/telegram.json -i -e 's/^"Name1":"",/"Name1":"'$Name1'",/'
	echo '"Bot1":"",' >> $user/.credentials/telegram.json
	sed $user/.credentials/telegram.json -i -e 's/^"Bot1":"",/"Bot1":"'$Bot1'",/'	
	if [ "$sockets" == '3' ]
		then
		echo '"Name2":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Name2":"",/"Name2":"'$Name2'",/'
		echo '"Bot2":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Bot2":"",/"Bot2":"'$Bot2'",/'	
		echo '"Name3":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Name3":"",/"Name3":"'$Name3'",/'
		echo '"Bot3":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Bot3":"",/"Bot3":"'$Bot3'",/'	
	elif [ "$sockets" == '2' ]
		then
		echo '"Name2":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Name2":"",/"Name2":"'$Name2'",/'
		echo '"Bot2":"",' >> $user/.credentials/telegram.json
		sed $user/.credentials/telegram.json -i -e 's/^"Bot2":"",/"Bot2":"'$Bot2'",/'	
	fi
	echo '"groupid":""' >> $user/.credentials/telegram.json
	sed $user/.credentials/telegram.json -i -e 's/^"groupid":""/"groupid":"'$groupid'"/'
	echo "}" >> $user/.credentials/telegram.json

	# Adapt MarriaDB-Config
	echo -e "\e[0m"
	echo -e "\e[96mAdapt MarriaDB-Config\e[0m"
	sudo sed /etc/mysql/mariadb.conf.d/50-server.cnf -i -e "s/^bind-address=*.*/bind-address            = 0.0.0.0/g"	

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                Create database                  ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"	

	if [ "$sockets" == '1' ]
		then

		# Create database
		echo -e "\e[0m"
		echo -e "\e[96mCreate database\e[0m"
		sudo mysql -u root --password=$userpassword <<EOF
		DROP DATABASE IF EXISTS haushalt;
		CREATE DATABASE haushalt;
		USE haushalt;
		CREATE TABLE device1 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE failure (id INT AUTO_INCREMENT PRIMARY KEY, device1 TINYINT, device2 TINYINT, device3 TINYINT);
		INSERT INTO device1 (running) VALUES (0);
		INSERT INTO failure (device1,device2,device3) VALUES (0,0,0);
		GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '$userpassword';
		FLUSH PRIVILEGES;
EOF

	elif [ "$sockets" == '2' ]
		then

		# Create database
		echo -e "\e[0m"
		echo -e "\e[96mCreate database\e[0m"
		sudo mysql -u root --password=$userpassword <<EOF
		DROP DATABASE IF EXISTS haushalt;
		CREATE DATABASE haushalt;
		USE haushalt;
		CREATE TABLE device1 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE device2 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE failure (id INT AUTO_INCREMENT PRIMARY KEY, device1 TINYINT, device2 TINYINT, device3 TINYINT);
		INSERT INTO device1 (running) VALUES (0);
		INSERT INTO device2 (running) VALUES (0);
		INSERT INTO failure (device1,device2,device3) VALUES (0,0,0);
		GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '$userpassword';
		FLUSH PRIVILEGES;
EOF

	elif [ "$sockets" == '3' ]
		then

		# Create database
		echo -e "\e[0m"
		echo -e "\e[96mCreate database\e[0m"
		sudo mysql -u root --password=$userpassword <<EOF
		DROP DATABASE IF EXISTS haushalt;
		CREATE DATABASE haushalt;
		USE haushalt;
		CREATE TABLE device1 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE device2 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE device3 (id INT AUTO_INCREMENT PRIMARY KEY, running TINYINT, starttimestamp TIMESTAMP NULL, endtimestamp TIMESTAMP NULL);
		CREATE TABLE failure (id INT AUTO_INCREMENT PRIMARY KEY, device1 TINYINT, device2 TINYINT, device3 TINYINT);
		INSERT INTO device1 (running) VALUES (0);
		INSERT INTO device2 (running) VALUES (0);
		INSERT INTO device3 (running) VALUES (0);
		INSERT INTO failure (device1,device2,device3) VALUES (0,0,0);
		GRANT ALL ON *.* TO 'root'@'localhost' IDENTIFIED BY '$userpassword';
		FLUSH PRIVILEGES;
EOF
	fi
	
	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                   Copy files                    ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"
	
	# Copy program files
	echo -e "\e[0m"
	echo -e "\e[96mCopy program files\e[0m"
	find $root/haushalt/* -type f -exec chmod a+x {} +
	sudo cp -r $root/haushalt/* /opt/haushalt/
	
	# Copy haushalt deamon
	echo -e "\e[0m"
	echo -e "\e[96mCopy haushalt deamon\e[0m"
	sudo cp $root/system/haushalt.service /lib/systemd/system/haushalt.service
	sudo chown root:root /lib/systemd/system/haushalt.service
	sudo chmod 0644 /lib/systemd/system/haushalt.service
	
	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                Starting deamon                  ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"	

	# Starting deamon
	echo -e "\e[0m"
	echo -e "\e[96mStarting deamon\e[0m"
	sudo systemctl enable haushalt.service

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m######                 Installation Done               ######"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m######                   Reboot with:                  ######"
	echo -e "\e[0m######                   sudo reboot                   ######"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"
	echo -e "\e[0m"

elif [ $selection == '2' ];
	then

	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                  User password                  ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[96m"
	echo -e "\e[96m"

	# Insert your user password
	read -s -p "Insert your user password: " userpassword
	echo -e "\e[96m"
	echo -e "\e[96m"
	echo -e "\e[96m"

	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######          Delete files and directories           ######"	
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"

	# Stopping deamon
	echo -e "\e[0m"
	echo -e "\e[96mStopping deamon\e[0m"
	sudo systemctl disable haushalt.service

	# Delete program files
	echo -e "\e[0m"
	echo -e "\e[96mDelete program files\e[0m"
	sudo rm -rf /opt/haushalt

	# Delete database
	echo -e "\e[0m"
	echo -e "\e[96mDelete database\e[0m"
	sudo mysql -u root --password=$userpassword <<EOF
	DROP DATABASE IF EXISTS haushalt;
EOF

	# Delete credentials
	echo -e "\e[0m"
	echo -e "\e[96mDelete credentials\e[0m"
	sudo rm -rf /home/pi/.credentials
	
	echo -e "\e[0m"
	echo -e "\e[0m"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m######                Uninstallation Done              ######"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m######                   Reboot with:                  ######"
	echo -e "\e[0m######                   sudo reboot                   ######"
	echo -e "\e[0m######                                                 ######"
	echo -e "\e[0m#############################################################"
	echo -e "\e[0m"
	echo -e "\e[0m"

fi
