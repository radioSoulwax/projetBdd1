#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from bdd import *

con = lite.connect('test.db')
with con:
    cur = con.cursor()
    line = []
    cur = con.cursor()

    for raw in cur.execute("select name from sqlite_master where type = 'table'"):
        line.append(raw)
        if raw[0]=='Cars':
            print 'vrai'
        print raw[0]
    print line
    for raw in cur.execute("PRAGMA table_info(Cars)"):
         print raw[1],
    print #retour a la ligne

#Test de la methode pour checker les consequences logiques
def get_logical_consequence(triplet_list):
        triplets = []
        sigma = triplet_list
        for i in range(len(sigma)):
            functional_dependence = sigma[i][1]
            implication = [sigma[i][2]]
            last_call = ''
            owned = split_str(sigma[i][1])+[sigma[i][2]]
            to_recheck = sigma
            added = True
            found = False
            while added:
                added = False
                checklist = []
                for j in range(len(to_recheck)):
                    if to_recheck[j][0] == sigma[i][0]:
                        list = split_str(to_recheck[j][1])
                        if not included_in(list,owned):
                            print list,
                            print "is not included in",
                            print owned
                            checklist.append(to_recheck[j])
                        else:
                            print list,
                            print "is included in",
                            print owned,
                            if to_recheck[j][2] not in owned:
                                if to_recheck[j][1] == last_call:
                                    print to_recheck[j][1],
                                    print 'is already known'
                                    implication.append(to_recheck[j][2])
                                else:
                                    implication = [to_recheck[j][2]]
                                owned.append(to_recheck[j][2])
                                found = True
                                last_call = to_recheck[j][1]
                            for k in list:
                                if k not in owned:
                                    owned.append(k)
                                    print k + "is added to owned",
                            print '\n'
                            print functional_dependence + "->",
                            print owned
                            added = True
                            if j+1 < len(to_recheck):
                                checklist += to_recheck[j+1:]
                            to_recheck=checklist
                            print "to recheck :",
                            print checklist
                            print
                            break
            for attribute in implication :
                if found and not is_useless(sigma,(sigma[i][0], functional_dependence, attribute)):
                    triplets.append((sigma[i][0], functional_dependence, attribute))
                if is_useless(sigma,(sigma[i][0], functional_dependence, attribute)):
                    print (sigma[i][0], functional_dependence, i),
                    print "is useless"
            print
        return triplets

def is_useless(functional_dependencies,triplet):
        for df in functional_dependencies:
            if triplet[0] == df[0] and triplet[2] == df[2] and included_in(split_str(df[1]),split_str(triplet[1])):
                return True
        return False

print(split_str("michel ma belle sont des mots qui vont tres bien ensembles"))
print(included_in(['a','b','c'], ['x','b','v','d','a','g','c','s']))
print "\n \n"
print get_logical_consequence([("table1","A B","C"),("table2","michel","mabelle"),("table1","C D", "E"), ("table1", "B","D")])
print '\n \n'
print get_logical_consequence([("t", "A B","C"), ("t","A B","D"), ("t", "G", "E"), ("t", "E F", "G"), ("t", "E F", "H"), ("t", "B C D", "A"), ("t", "B", "F"), ("t", "F", "A")])