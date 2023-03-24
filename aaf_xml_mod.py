import numpy as np
import xml.etree.ElementTree as ET
import fnmatch

def parse_archive(xml_in):

   tree=ET.parse(xml_in)
   root= tree.getroot()


   print ('start archive')
   #print ()
   #print ()
   #print ()
   for child in root.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset'):
      #print (1)
      #print (child)
      item=child.find('name')
      #print (item)
      for grandchild in child.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset'):
         #print ('grandchild')
         #print (grandchild)
         #print ('grandchild.attrib')
         #print (grandchild.attrib)
         #print ('grandchild.tag')
         #print (grandchild.tag)
         #print ('grandchild.attrib[name]')
         #print (grandchild.attrib['name'])
         if fnmatch.fnmatch(grandchild.attrib['name'], '*det*latest*'):
            #print( grandchild.attrib['name'])
            #print( grandchild.attrib['ID'])
            #print('HHHHHHHHHHHHHHHHH')
            file_f=grandchild.attrib['ID']

            for grandgrandchild in grandchild.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}date'):
               #print ('grandgrandchild.attrib[]')
               #print (grandgrandchild)
               #print (grandgrandchild.attrib)
               #print (grandgrandchild.attrib['type'])
               ##print (grandgrandchild.text.encode('utf8'))
               #print (grandgrandchild.text)
               ##update_time = grandgrandchild.text.encode('utf8')
               update_time = grandgrandchild.text
               #print(update_time)
               #print('end')

               break


   return file_f,update_time




def parsetest(xml_to_test):


   print('PARSETEST')

   test = True

   tree=ET.parse(xml_to_test)
   root= tree.getroot()

   print('my root')
   print(root)
   print( len(root))

   print()
   print()

   print('root tag')
   print(root.tag)

   print('root tags')
   print(root.tag[:])

   print()
   print()

   print('root[0] and [1]')
   print (root[0])
   print (root[1])
   #print (root[2])

   print('child tags')
   # You can iterate over an element's children.
   for child in root:
       print('child.tag')
       print(child.tag)
       print('child.attrib')
       print(child.attrib)

   for child in root:
       print('child.text')
       print(child.text)

   print()
   print()

   print ('root attributes')
   print(root.attrib)

   print ('get attributes')
   if test:

      for child in root.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset'):
          print (1)
          print (child)
          item=child.find('name')
          print (item)
          for grandchild in child.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset'):
             print ('grandchild')
             print (grandchild)
             print ('grandchild.attrib')
             print (grandchild.attrib)
             print ('grandchild.tag')
             print (grandchild.tag)
             print ('grandchild.attrib[name]')
             print (grandchild.attrib['name'])

             item2=grandchild.find('name')
             print (item2)

             for grandgrandchild in grandchild.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}date'):
                print ('grandgrandchild.attrib[]')
                print (grandgrandchild)
                print (grandgrandchild.attrib)
                print (grandgrandchild.attrib['type'])
                print (grandgrandchild.attrib['type'])
                print (grandgrandchild.text.encode('utf8'))
                print('end')


   print('PARESTEST')

