# Upload v3.pmtiles from source coop to a bucket I own

make use of `get_pmtiles.ipynb` to run the upload

In short update the `source_coop_credentials` python dictionary with new credentials from https://beta.source.coop/repositories/protomaps/openstreetmap/description/ 

run the notebook which:
 - gets the latest file size
 - initialises a multipart upload
 - uses the lambda function in lambda/index.py to copy each part
 - then completes the multipart download
 - be sure to abort the download if it fails using the uncommented code

I have now also added a tile server to here:
 - some settings are done manually following instructions from https://docs.protomaps.com/deploy/aws
  
  
to do:
 - formalise the notebook to a script
 - run the script from another lambda function with a central trigger point
 - set on aws cronjob equivalant to run monthly