#!/usr/bin/env Jython

import requests
import json
import warnings


'''
Created on 4 Feb 2016

Tools for connecting to the neo4j REST API

@author: davidos
'''

#Could also use py2neo, but this is a bit heavy duty for some uses



def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def results_2_tab(results):
    """Take results table, 
    return as a list of dicts, keyed on headers.
    """
    # This is still a stubb.  Probably better to do inside the class
    out = []
    columns = [x['columns'] for x in results[0]['data']]
    rows  = [x['row'] for x in results[0]['data']]
    return

        
class neo4j_connect():
    """Thin layer over REST API to hold connection details, 
    handle multi-statement POST queries."""
    def __init__(self, base_uri, usr, pwd):
        self.base_uri=base_uri
        self.usr = usr
        self.pwd = pwd
        self.last_results = ''
       
    def commit_list(self, statements):
        """Commit a list of statements to neo4J DB via REST API.
        Prints requests status and warnings if any problems with commit.
        cypher_statments = list of cypher statements as strings
        base_uri = base URL for neo4J DB.
        Errors are returned as warnings.
        Returns results (json, list) or False if any errors are encountered."""
        cstatements = []
    #   results = {}
        for s in statements:
            cstatements.append({'statement': s})
        payload = {'statements': cstatements}
        response = requests.post(url = "%s/db/data/transaction/commit" % self.base_uri, auth = (self.usr, self.pwd) , data = json.dumps(payload))
        if self.rest_return_check(response):
            self.last_results = response.json()['results']
            return response.json()['results']
        else:
            return False
        
    def commit_list_in_chunks(self, statements, verbose=False, chunk_length=100):
        """Commit a list of statements to neo4J DB via REST API, split into chunks.
        cypher_statments = list of cypher statements as strings
        base_uri = base URL for neo4J DB
        Default chunk size = 100 statements. This can be overidden by KWARG chunk_length
        """
        chunked_statements = chunks(l = statements, n=chunk_length)
        chunk_results = []
        for c in chunked_statements:
            if verbose:
                print "Processing chunk starting with: %s" % c[0]
            r = self.commit_list(c)
            chunk_results.append(r)
        return chunk_results
        
    def rest_return_check(self, response):
        """Checks status response to post. Prints warnings to STDERR if not OK.
        If OK, checks for errors in response. Prints any present as warnings to STDERR.
        Returns True STATUS OK and no errors, otherwise returns False.
        """
        if not (response.status_code == 200):
            warnings.warn("Connection error: %s (%s)" % (response.status_code, response.reason))
        else:
            j = response.json()
            if j['errors']:
                for e in j['errors']:
                    warnings.warn(str(e))
                return False
            else:
                return True
            
                
        
    
    