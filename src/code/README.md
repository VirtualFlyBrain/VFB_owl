# To run these scripts

Install [Jython 2.5](http://www.jython.org/downloads.html)

Download [the latest Brain jar](https://github.com/loopasam), and a [JBDC mysql connection jar](http://dev.mysql.com/downloads/connector/j/) and make sure both of these are in $CLASSPATH

Alternatively, one can run jython directly from a standalone JAR:
java -cp '.:\<Path to jar lib directory>/*' org.python.util.jython

The jar lib dir must contain the standalone jython JAR + any JARs required for the scripts being run.  This method is necessary because JARs in $CLASSPATH are not read when running Jython from JAR.



Generation of fb_features.owl additionally requires a postgres connection for which you will need a JBDC postgres jar in your classpath.


To connect to the LMB DB you will need to request access from GJ, providing a public key.  
You should then connect via an shh tunnel
