import os, sys, zipfile, json

def main():
    with open('dat.json','r') as jsondata:
        loadedjsondata = json.loads(jsondata.read())
        jsondata.close()
    
    name = loadedjsondata['zipData']['name'] + '.zip'

    if os.path.isfile(name):
        print('zip exists')
        for a in loadedjsondata['files']:
            zipFile = zipfile.ZipFile(name, 'r')
            if (not os.path.isfile(a) and not os.path.isdir(a)) and not a in loadedjsondata['exclude']:
                print('adding removed file')
                with open(a, 'wb') as newFile:
                    print(zipFile.read(a))
                    newFile.write(zipFile.read(a))
                    newFile.close()
            elif os.path.isfile(a) or os.path.isdir(a):
                print('Reverting file contents')
                with open(a, 'rb') as checkFile:
                    checkFileContents = checkFile.read()
                    checkFile.close()
                if checkFileContents != zipFile.read(a):
                    with open(a, 'wb') as newVersion:
                        newVersion.write(zipFile.read(a))
    else: 
        loadedjsondata['files'] = []
        newZip = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
        for a in os.listdir():
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
        main()

if __name__ == "__main__":
    main()