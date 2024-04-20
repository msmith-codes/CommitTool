from dataclasses import dataclass
from datetime import date
from sys import platform
import subprocess
import cutie
import sys
import os

@dataclass
class VersionT:
    vType: str
    major: int
    minor: int
    patch: int

vNumStr: str
newType: str

def main():
    # Get the version:
    vStr: str = getVersion()
    global vNumStr
    global newType
    version: VersionT = parseVersion(vStr)
    
    newType = version.vType
    
    if not(cutie.prompt_yes_or_no("Is this commit of type " + version.vType + "?")):
        types = [
            "Development:",
                "predev", 
                "indev",
            "Pre-Release:",
                "alpha",
                "beta",
            "Release:",
                "snapshot",
                "release"
        ]
        
        captions = [0, 3, 6]
        defaultIndex = 0
        if version.vType == "predev":
            defaultIndex = 1
        elif version.vType == "indev":
            defaultIndex = 2
        
        elif version.vType == "alpha":
            defaultIndex = 4
        elif version.vType == "beta":
            defaultIndex = 5
        
        elif version.vType == "snapshot":
            defaultIndex = 7
        elif version.vType == "release":
            defaultIndex = 8
        
        newType = types[cutie.select(types, caption_indices=captions, selected_index=defaultIndex)]
    
    
    print("What kind of update is this?")
    numTypes = [ "Major", "Minor", "Patch" ]
    numType = numTypes[cutie.select(numTypes, selected_index=0)]
    
    if numType == "Major": 
        version.major += 1
    elif numType == "Minor": 
        version.minor += 1
    elif numType == "Patch": 
        version.patch += 1
    
    vNumStr = str(version.major) + "." + str(version.minor) + "." + str(version.patch)
    
    if not (cutie.prompt_yes_or_no("Is the version '" + vNumStr + "' correct?")):
        version.major = cutie.get_number("What is the correct Major number?", min_value=0, allow_float=False)
        version.minor = cutie.get_number("What is the correct Minor number?", min_value=0, allow_float=False)
        version.patch = cutie.get_number("What is the correct Patch number?", min_value=0, allow_float=False)
        
        vNumStr = str(version.major) + "." + str(version.minor) + "." + str(version.patch)
    global vstr
    print("Set version number to: " + vNumStr)
    
    versionFile = open("version.txt", 'w')
    versionFile.write(newType + " " + vNumStr)
    versionFile.close()
    
    tags = [
        "GAMEPLAY",
        "MAPS",
        "FIXED",
        "MISC",
    ]
    print("Added tags: ")
    for tag in tags:
        print("\t" + tag)
    
    customTags = ""
    if (cutie.prompt_yes_or_no("Would you like to add custom tag?")):
        customTagsInput: str = input("Enter tags seperated by spaces: ")
        customTags = customTagsInput.split(' ')
        tags += customTags
    
    print("Select tags would you like to add.")
    tagsIndexes = cutie.select_multiple(tags)
    
    tagsAdded = [
        _tag
        for tagsIndex, _tag in enumerate(tags)
        if tagsIndex in tagsIndexes
    ]
    
    
    date: str = getDate()
    title: str = "Commit '" + vNumStr + "' - " + date + "\n"
    
    messages = [
        title,
        "\n",
        
    ]
    
    exitInfo = "':q' to quit."
    for tag in tagsAdded:
        print("Enter changes for tag " + tag + " [" + exitInfo + "]:")
        changes = []
        while True:
            change = input("- ")
            if change == ":q":
                break
            changes.append("- " + change + "\n")
        messages.append("[ " + tag + " ]\n")
        messages += changes
        messages.append("\n")
    
    messageStr = ""
    for msg in messages:
        messageStr += msg
    
    subprocess.run(["git", "add", "."]) 
    subprocess.run(["git", "commit", "-m", "" + messageStr + ""]) 
    
    if (cutie.prompt_yes_or_no("Push to remote repository?")):
        subprocess.run(["git", "push"]) 

def getVersion() -> str:
    versionFile = open("version.txt", 'r')
    lines = versionFile.readlines()
    
    version: str = ""
    for line in lines:
        if line.startswith('#'):
            continue
        version = line.strip()
    return version

def parseVersion(version: str) -> VersionT:
    # Split the version string.
    vSplit = version.split(' ', 1)
    vNumSplit = vSplit[1].split('.')
    
    # Assign variables.
    vType: str = vSplit[0]
    vMajor: int = int(vNumSplit[0])
    vMinor: int = int(vNumSplit[1])
    vPatch: int = int(vNumSplit[2])
    
    return VersionT(vType, vMajor, vMinor, vPatch)

def getDate() -> str:
    today = date.today()
    return today.strftime("%m/%d/%Y")
    
if __name__ == "__main__":
    main()
