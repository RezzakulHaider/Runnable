
import base64
import requests
from swiftclient import client, service

#username = '4b544412403bd63cfb9a2073161c287a2eddd0f9'
#password = 'b66cbd58eacb9baea35faee626cb53fb604091abdd6617fd313ee8d530f8'
#authurl='https://swift.ng.bluemix.net/auth/807c4ffd-36a2-4231-ae4d-c4ab5fcd2f65/e1322392-9553-48e1-8f5d-bcaec4b69926'

#Function to connect to swift object store
class SwiftConnect:
        def __init__(self):
            print ("Inside connect To swift")
            encoded = base64.b64encode (bytes('4b544412403bd63cfb9a2073161c287a2eddd0f9:b66cbd58eacb9baea35faee626cb53fb604091abdd6617fd313ee8d530f8',"utf-8"))
            newval = "Basic "+ encoded.decode("utf-8")
            response =  requests.get("https://swift.ng.bluemix.net/auth/807c4ffd-36a2-4231-ae4d-c4ab5fcd2f65/e1322392-9553-48e1-8f5d-bcaec4b69926/4b544412403bd63cfb9a2073161c287a2eddd0f9", 
            headers  =  {"Authorization": newval})
            print (response.headers['x-auth-token'])
            self.conn = client.Connection(
                preauthtoken=response.headers['x-auth-token'],
                preauthurl=response.headers['x-storage-url']
                
        )


#####################################################################################################################################################################################

#Creating a Container
        def createContainer(self,folderName):
            print ("Inside create container")
            self.container_name = folderName
            self.conn.put_container(self.container_name)
            
            
#####################################################################################################################################################################################

#Creating an object
        def createObject(self,fileName,fileContent,folderName):
            print(self.container_name)
            print (fileName)
            #self.serv = service.SwiftService()
            #self.serv.upload(self.container_name,fileName)
            print ("Inside create Object")
            self.conn.put_object(container=self.container_name, obj= fileName, contents= fileContent)
            
#####################################################################################################################################################################################                                        

#Retrieving an object 
        def retrieveObject(self,folderName,fileName):
            print ("Inside retrieve object")
            #obj_tuple = self.conn.get_object(container = self.container_name, obj = fileName)
            obj_tuple = self.conn.get_object(folderName,fileName)
            #with open('C:/Users/Parthasarathy/retrieved.txt', 'w') as my_hello:
            #my_hello.write(obj_tuple[1].decode("utf-8"))
            #print ("Successfully written")
            #my_hello.close()
            print(self.container_name)
            #print (fileName)
            #downloadList = list(self.serv.download(self.container_name,fileName))
            #print (downloadList)
            print (obj_tuple[1])
            #print (obj_tuple[1].decode("utf-8"))
            return obj_tuple[1]
        
#####################################################################################################################################################################################        
#Retrieving an object 
        def getObject(self,containernames,filename):
            print ("Inside get object")
            print (containernames)
            print (filename)
            obj_tuple = self.conn.get_object(containernames,filename)
#             print (filename)
#             print (obj_tuple[1])
            return obj_tuple[1]
################################################################################################       

#deleting an object 
        def delObject(self,containernames,filename):
            print ("Inside del object")
            print (containernames)
            print (filename)
            self.conn.delete_object(containernames, filename)
#             print (filename)
#             print (obj_tuple[1])
#             return obj_tuple[1]


####################################################################################################################################################
#Creating an container list
        def containerList(self,folderlist):
            
            print ("container List")
            #return container list
            #print(self.conn.head_account())
            containers = self.conn.get_account()[1]
            for container  in containers:
                print (container ['name'])
                
            return containers                    
#####################################################################################################################################################################################                                        
#####################################################################################################################################################################################        


#Creating an container list
        def fileList(self,containername):
            
            print ("Files in a container")
            files = self.conn.get_container(containername)[1]
            for file  in files:
                print ('{0}\t{1}\t{2}'.format(file['name'], file['bytes'], file['last_modified']))
               
            return files                    
#####################################################################################################################################################################################                                        


                        
#Closing the connection 
        def closeConnection(self):
            self.conn.close()
        