import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import flask
from werkzeug import secure_filename
from SwiftConnect import SwiftConnect
import json

#containernames = 'empty';

# Initialize the Flask application
app = Flask(__name__)

#Instantiating SwiftClient
swift = SwiftConnect()
#print(swift.containerList())
#swift.connectToSwift()

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#####################################################################################################################################################################################

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#####################################################################################################################################################################################

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    #return app.send_static_file('index.html')
    return render_template('index.html')

#####################################################################################################################################################################################

@app.route('/containers', methods=['GET'])  # /containers/foldername/file.txt
def getContainers():
    
    folderlist = ''
    cts = swift.containerList(folderlist)
    j = json.dumps(cts,sort_keys=True)
    return Response(j, mimetype='application/json')
    #return Response(j, mimetype='application/octet-stream')
    #return Response(str(cts), mimetype='text/plain')

##########################################################################################
@app.route('/cotainername', methods=['GET'])
def getContainerName():
    
    print("got the value")
    containernames =  request.args.get('suggest')
    print(containernames)
    cts = swift.fileList(containernames)
    f = json.dumps(cts,sort_keys=True)
    return Response(f, mimetype='application/json')
    #return Response(str(cts), mimetype='text/plain')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    inputFile = request.files['infile']
    # Check if the file is one of the allowed types/extensions
    if inputFile: #and allowed_file(inputFile.filename):
        print("accepted file upload")
        # Make the filename safe, remove unsupported chars
        inputFileName = secure_filename(inputFile.filename)
        inputFileContent = inputFile.read()
        folderName = request.form['infolder']
        # Move the file form the temporal folder to
        # the upload folder we setup
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #swift = SwiftConnect()
        #swift.connectToSwift()
        swift.createContainer(folderName)
        swift.createObject(inputFileName,inputFileContent,folderName)
        
        
        
        encodedoutputFileContent = swift.retrieveObject(folderName,inputFileName)
        #print(inputFileName)
        #print(encodedoutputFileContent.decode("utf-8"))
        #with open(inputFileName, 'w') as my_file:
        #    my_file.write(encodedoutputFileContent.decode("utf-8"))
        #    print ("Successfully written")
        #    my_file.close()
            
        #swift.containerList()    
        #swift.closeConnection()
        
    return Response(encodedoutputFileContent, mimetype='application/octet-stream')
    #return Response(encodedoutputFileContent, mimetype='text/plain')
        
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return redirect(url_for('Upload Success'))
#########################################################################################################################
# Route that will process the file downloadfile
@app.route('/downloadfile/<containername>/<path:filename>', methods=['GET'])
def downloadfile(containername, filename):
        #containernames =  request.args.get('suggest')
        #filename = request.args.get('files')
#         containernames = "myContainerNew"
#         filename = "Archana.txt"
        print("inside download section")
        print(filename)
        print(containername)
        encodedoutputFile = swift.getObject(containername,filename)
        return Response(encodedoutputFile, mimetype='application/octet-stream')
        
#####################################################################################################################################
# Route that will process the file downloadfile
@app.route('/deletefile', methods=['DELETE'])
def deletefile():
        containernames =  request.args.get('suggest')
        filename = request.args.get('files')
        print("inside delete section")
        print(filename)
        print(containernames)
        successsfuloutput = swift.delObject(containernames,filename)
#         return Response(encodedoutputFile, mimetype='application/octet-stream')
        return Response(successsfuloutput)   
#####################################################################################################################################################################################

# Route that will process the file download
#@app.route('/download', methods=['GET'])
#def download():
    # Get the name of the file and name of the folder from which file has to be downloaded 
    #outputFileName = request.form['outfileName']
    #folderName = request.form['outfolder']
    # Check if the file is one of the allowed types/extensions
    #if outputFileName and allowed_file(outputFileName):
        # Make the filename safe, remove unsupported chars
        #outputFileName = secure_filename(outputFileName)
        #swift = SwiftConnect()
        #swift.connectToSwift()
        #outputFileContent = swift.retrieveObject(folderName,outputFileName)
        #print(outputFileName)
        #print(outputFileContent)
        #swift.closeConnection()
        #Writing the contents into the file
        #out_file = open(outputFileName,'a')
        #out_file.write(outputFileContent + "\n")
        #out_file.close()
        #request.files['outfile'] = out_file 
        #return Response(out_file, mimetype='text')
        
                
#####################################################################################################################################################################################

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                             filename)


#####################################################################################################################################################################################

#Main Function    
if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
            
    )

