# FixExportediPhoneMultimedia (FEiM)

## Environment

 - iPhone 13 15.5
 - Windows 10
 - Python 3.9.7

  
  

## Short description:

This script is intended to rename images to the original creation datetime (and rotate if needed) taken with an iPhone.

  
  

## Explanation


You give the directory where all your exported iPhone data is located (input dir).

You give a directory where to put the renamed images (output dir).

  

The script starts to loop over your input directory.

If the file is an image, it looks to the EXIF tags and gets the 'DateTimeOriginal' and 'Orientation' keys.

  

The DateTimeOriginal value will be used to generate the new filename.

If the new filename would already exist (for example photo taken on the same second) it will add a zero.

  

If the Orientation value is not 8 and the extension is not a '.PNG' (used for screenshots (I think)).

The images taken in portrait mode are rotated 90° degrees counterclockwise (why?: in most cases, after exporting images it was rotated that way).

Images in landscape mode are flipped 180° degrees

Rotating means creating a new image (so most of the) metadata/EXIF data is gone.

(As a dirty solution, it puts DateTimeOriginal value as new c,m, a time. -not yet)

  

## TODO

 - check pictures in landscape if they are upside down or not
 - add EXIF data to pictures that were removed when rotating
 - add support for videos
