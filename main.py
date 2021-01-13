import os, sys, zipfile, json

def walk():
    path = './'
    filesList = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            print(os.path.join(root, name))
            filesList.append(os.path.join(root, name))
        for name in directories:
            print(os.path.join(root, name))
            filesList.append(os.path.join(root, name))
    return(filesList)

def main():
    loadedjsondata = {}
    # checks if dat.json exists, if so open it
    if os.path.isfile('dat.json'):
        print('dat.json in place')
        with open('dat.json','r') as jsondata:
            loadedjsondata = json.loads(jsondata.read())
            jsondata.close()
    # if dat.json is not found exits
    else: exit()
    
    name = loadedjsondata['zipData']['name'] + '.zip'            

    # if zip file already exists check files
    if os.path.isfile(name):
        zipFile = zipfile.ZipFile(name, 'r')
        for a in loadedjsondata['files']:
            zipFileContents = zipFile.read(a.strip('./'))
            # if file doesn't exist create it
            if (not os.path.isfile(a) and not os.path.isdir(a)) and not a in loadedjsondata['exclude']:
                print('adding removed file')
                with open(a, 'wb') as newFile:
                    print(zipFileContents)
                    newFile.write(zipFileContents)
                    newFile.close()
            # if file changed revert it
            elif os.path.isfile(a) or os.path.isdir(a):
                with open(a, 'rb') as checkFile:
                    checkFileContents = checkFile.read()
                    checkFile.close()
                if checkFileContents != zipFileContents:
                    print('Reverting file contents')
                    with open(a, 'wb') as newVersion:
                        newVersion.write(zipFileContents)
    # if zip file doesn't exist create it
    else: 
        loadedjsondata['files'] = []
        newZip = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
        for a in walk():
            if not(any(b in a for b in loadedjsondata['exclude'])):
                if (not a in loadedjsondata['exclude']) and (a != name):
                    print(a)
                    newZip.write(a)
                    loadedjsondata['files'].append(a)
                    print('saved ' + a)
                else: pass
        with open('dat.json', 'w') as jsondata:
            json.dump(loadedjsondata, jsondata, indent=4)
            jsondata.close()
        newZip.close()
        #main()


    print('completed')
    for a in loadedjsondata['run']:
        exec(a)
    #shell.ShellExecuteEx(lpVerb='runas', lpFile=loadedjsondata['run'])

if __name__ == "__main__":
    main()