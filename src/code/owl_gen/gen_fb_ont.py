#!/usr/bin/env jython

import sys
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools


