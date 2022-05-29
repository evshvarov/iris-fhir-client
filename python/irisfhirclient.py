import sys,json
from fhirpy import SyncFHIRClient
from json import dump
from tabulate import tabulate
import requests

resources = ["Patient", "Observation", "Appointment","Procedure","Practitioner"]
contentType = "application/fhir+json"

# 1-Count Number of Resources
def CountResource(resource,url,api_key):
    #Init headers
    headers={"Content-Type":contentType,"x-api-key":api_key}
    #Add / at the end of endpoint if not added
    if url[-1]!="/":
        url=url+"/"
    try:
        #Get Request 
        req = requests.get(url+resource+'/',headers=headers)  
    except:
        #in case of exception return 0
        return 0
        
    data=req.json()
    #count number of element entry
    count = len(data['entry'])
    return count


#Get Table header based on resource
def GetTableHeader(resource):
    if resource == "Patient":
        header = ["ID","Family Name","Given Name","DOB","Gender"]
    elif resource == "Observation":
        header = ["ID","Category","Code","Value","UOM","Date","Patient"]
    elif resource == "Procedure":
        header = ["ID","Code","Details","StartDate","EndDate","Status"]    
    elif resource == "Immunization":
        header = ["ID","VaccineCode","Details","Date","Encounter","Status"]    
    elif resource == "Encounter":
        header = ["ID","Class","StartDate","EndDate","Provider","Status"]    
    elif resource == "Organization":
        header = ["ID","Code","Details","Name"]   
    elif resource == "Condition":
        header = ["ID","Code","Details","ClinicalStatus","VerificationStatus"]    
    elif resource == "Practitioner":
        header = ["ID","Name","Gender"]     

        #AllergyIntolerance,DiagnosticReport,Claim

    return header

def GetTableData(resource,data,opt):
    rows = []
    if opt == 1: #Get Rows Data
        if resource == "Patient":
            for rowval in data:
                row = [rowval.get('id'),rowval.get_by_path('name.0.family'),rowval.get_by_path('name.0.given.0'),rowval.get_by_path('birthDate'),rowval.get_by_path('gender')]
                rows.append(row)
        elif resource == "Observation":
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('category.0.coding.0.code'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('valueQuantity.value'),
                rowval.get_by_path('valueQuantity.code'),
                rowval.get('effectiveDateTime'),
                rowval.get_by_path('subject.reference')
                ,]
                rows.append(row)    
        elif resource == 'Procedure':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('code.coding.0.display'),
                rowval.get_by_path('performedPeriod.start'),
                rowval.get_by_path('performedPeriod.end'),
                rowval.get_by_path('status')           
                ]
                rows.append(row)    
        elif resource == 'Immunization':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('vaccineCode.coding.0.code'),
                rowval.get_by_path('vaccineCode.coding.0.display'),
                rowval.get('occurrenceDateTime'),
                rowval.get_by_path('encounter.reference'),
                rowval.get_by_path('status')           
                ]
                rows.append(row) 
        elif resource == 'Encounter':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('class.code'),
                rowval.get_by_path('period.start'),
                rowval.get_by_path('period.end'),
                rowval.get_by_path('serviceProvider.reference'),
                rowval.get_by_path('status')           
                ]
                rows.append(row)  
        elif resource == 'Organization':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('type.0.coding.0.code'),
                rowval.get_by_path('type.0.coding.0.display'),
                rowval.get('name')           
                ]
                rows.append(row)     
        elif resource == 'Condition':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('code.coding.0.display'),
                rowval.get_by_path('clinicalStatus.coding.0.code'),           
                rowval.get_by_path('verificationStatus.coding.0.code')           
                ]
                rows.append(row)     
        elif resource == 'Practitioner':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('name.0.prefix.0')+' '+rowval.get_by_path('name.0.family')+' '+rowval.get_by_path('name.0.given.0'),
                rowval.get('gender')           
                ]
                rows.append(row)             
    if opt == 2: #Get data for HTML
        rows = ""
        patid = ""
        if resource == "Patient":
            for rowval in data:
                rows = rows + "<tr>"
                #including <a> tag to pass to patient.csp page
                patid = "fhirclient\patient.csp?pid="+str(rowval.get('id'))+"&pname="+str(rowval.get_by_path('name.0.family'))+" "+str(rowval.get_by_path('name.0.given.0'))
                patid = "\csp\\"+ patid     
                patid = '<A HREF="'+patid+'"'+'>'+str(rowval.get('id'))+'</A>'
                rows = rows + "<td>"+patid+"</td><td>"+str(rowval.get_by_path('name.0.family'))+"</td><td>"+str(rowval.get_by_path('name.0.given.0'))+"</td><td>"+str(rowval.get_by_path('birthDate'))+"</td><td>"+str(rowval.get_by_path('gender'))+"</td></tr>"
                
        elif resource == "Observation":
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('category.0.coding.0.code'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('valueQuantity.value'),
                rowval.get_by_path('valueQuantity.code'),
                rowval.get('effectiveDateTime'),
                rowval.get_by_path('subject.reference')
                ,]
                rows.append(row)    
        elif resource == 'Procedure':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('code.coding.0.display'),
                rowval.get_by_path('performedPeriod.start'),
                rowval.get_by_path('performedPeriod.end'),
                rowval.get_by_path('status')           
                ]
                rows.append(row)    
        elif resource == 'Immunization':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('vaccineCode.coding.0.code'),
                rowval.get_by_path('vaccineCode.coding.0.display'),
                rowval.get('occurrenceDateTime'),
                rowval.get_by_path('encounter.reference'),
                rowval.get_by_path('status')           
                ]
                rows.append(row) 
        elif resource == 'Encounter':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('class.code'),
                rowval.get_by_path('period.start'),
                rowval.get_by_path('period.end'),
                rowval.get_by_path('serviceProvider.reference'),
                rowval.get_by_path('status')           
                ]
                rows.append(row)  
        elif resource == 'Organization':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('type.0.coding.0.code'),
                rowval.get_by_path('type.0.coding.0.display'),
                rowval.get('name')           
                ]
                rows.append(row)     
        elif resource == 'Condition':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('code.coding.0.code'),
                rowval.get_by_path('code.coding.0.display'),
                rowval.get_by_path('clinicalStatus.coding.0.code'),           
                rowval.get_by_path('verificationStatus.coding.0.code')           
                ]
                rows.append(row)     
        elif resource == 'Practitioner':        
            for rowval in data:
                row = [rowval.get('id'),
                rowval.get_by_path('name.0.prefix.0')+' '+rowval.get_by_path('name.0.family')+' '+rowval.get_by_path('name.0.given.0'),
                rowval.get('gender')           
                ]
                rows.append(row)                                                                                       
    
    return rows


#2-Print patient resource from terminal
def GetResource(resource,url,api_key):
    #Get Connection
    cclient = SyncFHIRClient(url = url, extra_headers={"Content-Type":contentType,"x-api-key":api_key})
    try:
        data = cclient.resources(resource).fetch()
    except:
        print("Connection Error")    
          
    header = GetTableHeader(resource)
    rows = GetTableData(resource,data,1)
    #Print Resources
    print(tabulate(rows,headers = header))
    
#3-Print resource agaisnt Patient
def GetPatientResources(resource,patientId,url,api_key):
     #Get Connection
    cclient = SyncFHIRClient(url = url, extra_headers={"Content-Type":contentType,"x-api-key":api_key})
    try:
        data = cclient.resources(resource).search(patient=patientId).fetch()
    except:
        print("Connection Error")    
    header = GetTableHeader(resource)
    rows = GetTableData(resource,data,1)
    #Print Resources
    print(tabulate(rows,headers = header))

#Get Resource HTML Rows data
def GetResourceHTML(resource,url,api_key):
    #Get Connection
 
    data = ""
    if url[-1]!="/":
        url=url+"/"
    cclient = SyncFHIRClient(url = url, extra_headers={"Content-Type":contentType,"x-api-key":api_key})
    try:
        data = cclient.resources(resource).fetch()
    except:
        print("Connection Error")    
    
    rows = GetTableData(resource,data,2)
    return rows
def ListResources(url,api_key,opt):
# #--Counting all the resources ----------------------------------------------------
    headers = {"Content-Type":contentType,"x-api-key":api_key}
    if url[-1]!="/":
        url=url+"/"
    x = requests.get(url+'metadata',headers=headers)
    data = x.json()
    # # # print (len(data['rest'][0]['resource']))
    if opt == 0: 
        for item in data['rest'][0]['resource']: 
            print(item['type'])
    
    if opt == 1: 
        for item in data['rest'][0]['resource']: 
            # #--Counting all the resources -    
            x = requests.get(url+item['type']+'/',headers=headers)  
            # #      #print(x)
            data2 = x.json()
            # #      #print(data2)
            s = json.dumps(data2)
            if s.find('entry') != -1:
                print (item['type'] +":"+str(len(data2['entry'])))
            #       else:   
            #           print (item['type'] +": 0")
            # #########################################################################################

# id = GetResourceHTML("Patient","https://r4.smarthealthit.org","0")
# print(id)