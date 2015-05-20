## JSON files for easy export of VFB individuals data

JSON structure: 

~~~.javascript

{ shortFormID : 
      { 'label': string,
        'def': string,
        'types': [ 
         { 'isAnonymous': boolean, 
           'relId': shortFormID_string,
           'objectId': shortFormID_string
          },
          { ... },
          ]
      }
  }

~~~~~
