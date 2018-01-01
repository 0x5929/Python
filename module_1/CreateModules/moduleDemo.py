#!/usr/bin/python

## in order to import the modules, 
## use the import key word, and then the file name you want to include
## without the .py suffix


import classDemoModuleTobeExport

## you can also import specific objects/classes from a file by syntax below
## from classDemoModuleTobeExport import Scientific

## then using the above method, you can directly use Scientific, or w.e you import

## note we can now use the global function in the imported module,
## python does not require an export keyword for scripts to be exported
## all you need to do is to import and use it as an object, cool!
print 'Quick Add a + b= %d' %classDemoModuleTobeExport.quickAdd(10, 20)


integer = classDemoModuleTobeExport.Scientific(5,6)

print 'the overridden method of mult is used here: %d' %integer.mult()
print 'power is: %d' %integer.power()

